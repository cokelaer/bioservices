#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s):
#      https://www.assembla.com/spaces/bioservices/team
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id: biomodels.py 141 2013-02-06 10:22:25Z cokelaer $

"""This module provides a class :class:`ChEMBLdb`

.. topic:: What is ChEMBLdb

    :URL:  https://www.ebi.ac.uk/chembldb/index.php/
    :REST: https://www.ebi.ac.uk/chembldb/index.php/ws


    .. highlights::

        "Using the ChEMBLdb web service API users can retrieve data from the ChEMBL
        database in a programmatic fashion. The following list defines the currently
        supported functionality and defines the expected inputs and outputs of each
        method."

        -- From ChEMBLdb web page Dec 2012




"""
import urllib2, urllib, json, re, os
from services import *
import webbrowser


class ChEMBLdb(RESTService):
    """Interface to `ChEMBLdb <http://www.ebi.ac.uk/chembldb/index.php>`_


    Here is a quick example to retrieve a target given its ChEMBL Id
    .. doctest::

        >>> from bioservices import ChEMBLId
        >>> s = ChEMBLdb(verbose=False)
        >>> print(s._target_chemblId_example)
        'CHEMBL2477'
        >>> resjson = s.get_target_by_chemblId(s._target_chemblId_example+".json")

    """
    _url = "http://www.ebi.ac.uk/chemblws/"
    _chemblId_example = "CHEMBL1"
    _inChiKey_example = "QFFGVLORLPOAEC-SNVBAGLBSA-N"
    _smiles_example = "COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56"
    _smiles_similar_example = _smiles_example + "/90"
    _image_chemblId_example = "CHEMBL192"
    _image_dimension_example = 200
    _bioactivities_example = "CHEMBL2"
    _target_chemblId_example = "CHEMBL2477"
    _target_uniprotId_example = "Q13936"
    _target_bioactivities_example = "CHEMBL240"
    _assay_example = "CHEMBL1217643"

    def __init__(self, verbose=True):
        super(ChEMBLdb, self).__init__(url=ChEMBLdb._url,
            name="ChEMBLdb", verbose=verbose)
        self._default_extension = "json"

    # just a get/set to the default extension
    def _set_default_ext(self, ext):
        self.checkParam(ext, ["json","xml"])
        self._default_extension = ext
    def _get_default_ext(self):
        return self._default_extension
    default_extension = property(_get_default_ext, _set_default_ext,
        doc="set extension of the requests (default is json). Can be 'json' or 'xml'")

    # ChEMBL specifies those errors, so let us try to catch thmem. May not be
    # needed. Could to everything within services module.
    def _request(self, query, format="xml", baseUrl=True):
        """calls RESTService.request and check for specific Chembl errors.

        If error are 400, 404 or 500 then a specific Chembl error message is
        returned.
        """
        try:
            res = super(ChEMBLdb, self).request(query, format, baseUrl)
            return res
        except urllib2.HTTPError,e:
            if e.code == 400:
                self.logging.error(""" Bad request. The parameters passed to the
API endpoint were deemed invalid. This response will be returned for invalid
ChEMBLId's i.e. CHEMBLX1, invalid UniProt accessions, invalid SMILES strings
e.t.c. """)
            elif e.code == 404:
                self.logging.error(""" Not found. The resource corresponding to
the supplied parameters does not exist. This response will be returned for
requests for non-existent ChEMBL compound, target, and assay resources. """)
            elif e.code == 500:
                self.logging.error(""" Service unavailable. An internal problem
prevented us from fulfilling your request. """)
            else:
                pass
            raise BioServicesError("Unknown error caught (not 400,404, 500)")
        except Exception,e:
            raise(e)


    def api_status(self):
        """ Check API status

        :return: Response is the string 'UP' if services are running
        """
        res = self.request("status/", format="txt")
        return res

    # a complicated decorator that simplifies the code significantly
    # can accept parameters
    # can be used by methods
    def __process(*args_deco, **kwds_deco):
        service = args_deco[0]
        if len(args_deco)>1:
            service_extra = args_deco[1]
        else:
            service_extra = None

        def decorator(func):
            def newf(self, query):
                if query.endswith(".json"):
                    output = "json"
                elif query.endswith(".xml"):
                    output = "xml"
                elif len(query.split("."))>=2:
                    raise BioServicesError("""The query must be a valid identifier with .json or .xml extensions or no extension at all (default XML)""")
                else: # query has no extension, so we need to figure out the default
                    output = self.default_extension
                    query += "." +  self.default_extension

                if service_extra:
                    # used for example by get_compounds_activities
                    url = self.url + "/" + service + "/" + query.split('.')[0]
                    url += "/" + service_extra
                    if output == "json":
                        url += ".json"
                else:
                    url = self.url + "/" + service + "/" + query
                self.logging.info(url)
                # the request itself
                res = self._request(url, output)

                # converion required if json structure.
                if output == "json":
                    res = json.loads(res)
                return res
                #return func(self, *args, **kwds)
            newf.__name__ = func.__name__
            newf.__doc__ = func.__doc__
            return newf
        return decorator


    @__process("compounds")
    def get_compounds_by_chemblId(self, query):
        """Get compound by ChEMBLId

        :param query: a valid compound ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: Compound Record in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'compound'. The value of that key is another dictionary
        keyed by:

         * acdLogd
         * acdLogp
         * alogp
         * chemblId
         * knownDrug
         * medChemFriendly
         * molecularFormula
         * molecularWeight
         * numRo5Violations
         * passesRuleOfThree
         * rotatableBonds
         * smiles
         * stdInChiKey

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print (s._chemblId_example)
            >>> resxml = s.get_compounds_by_chemblId(s._chemblId_example)
            >>> resjson = s.get_compounds_by_chemblId(s._chemblId_example)
        """
        # the decorator is taking care of the checking and processing
        pass


    @__process("compounds/stdinchikey")
    def get_individual_compounds_by_inChiKey(self, query):
        """Get individual compound by standard InChi Key

        :param str query: a valid InChi key. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: Compound Record in XML or dictionary (if json requested)

        In addition to the keys returned in :meth:`get_compounds_by_chemblId`,
        the following keys are returned:

         * acdAcidicPka
         * acdBasicPka
         * preferredCompoundName
         * species
         * synonyms

        .. doctest::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._inChiKey_example)
            >>> resxml = s.get_individual_compounds_by_inChiKey(s._inChiKey_example + ".xml")
            >>> resjson = s.get_individual_compounds_by_inChiKey(s._inChiKey_example + ".json")
        """
        # the decorator is taking care of the checking and processing
        pass

    @__process("compounds/smiles")
    def get_compounds_by_SMILES(self, query):
        """Get list of compounds by Canonical SMILES

        :param str query: a valid compound ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: Compound Record in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'compounds'. The value of that key is a list of compound
        records. For each compound record dictionary see :meth:`get_compounds_by_chemblId`.

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._smiles_example)
            >>> resxml = s.get_compounds_by_SMILES(s._smiles_example + ".xml")
            >>> resjson = s.get_compounds_by_SMILES(s._smiles_example + ".json")
        """
        pass


    @__process("compounds/substructure")
    def get_compounds_containing_SMILES(self, query):
        """Get list of compounds containing the substructure represented
        by the given Canonical SMILES

        :param str query: a valid SMILES string. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: see :meth:`get_compounds_by_SMILES`


        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._smiles_example)
            >>> resxml = s.get_compounds_containing_SMILES(s._smiles_example + ".xml")
            >>> resjson = s.get_compounds_containing_SMILES(s._smiles_example + ".json")
        """
        pass


    @__process("compounds/similarity")
    def get_compounds_similar_to_SMILES(self, query):
        """Get list of compounds similar to the one represented by the given Canonical SMILES.

        The similarity is at a cutoff percentage score (minimum value=70%, maximum value=100%).


        :param str query: a valid SMILES string. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
            The SMILE string must be followed by a slash character and the
            expected similarity (e.g., "/90")
        :return: Compound records. See :meth:`get_compounds_by_chemblId`

        In addition to the keys returned in :meth:`get_compounds_by_chemblId`,
        the following keys are returned:

         * acdAcidicPka
         * acdBasicPka
         * similarity
         * species

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._smiles_similar_example)
            >>> resjson = s.get_compounds_similar_to_SMILES(s._smiles_example + "/100")
            >>> resjson = s.get_compounds_similar_to_SMILES(s._smiles_similar_example)
        """
        pass


    def get_image_of_compounds_by_chemblId(self, query, dimensions=None,
            file_out=None, view=True):
        """Get the image of a given compound.

        :param str query: a valid compound ChEMBLId or a list/tuple of valid compound ChEMBLIds.
        :param int dimensions: optional argument. An integer z such that :math:`1 \leq z \leq 500`
            giving the dimensions of the image.
        :param str file_out: if None, images are not save
        :param bool view: show the image. If True, images are shown in a browser
        :return: the path (list of paths) used to save the figure (figures) (different from Chembl API)

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print (s._image_chemblId_example, s._image_dimension_example)
            >>> s.get_image_of_compounds_by_chemblId(s._image_chemblId_example)
            >>> s.get_image_of_compounds_by_chemblId(s._image_chemblId_example, s._image_dimension_example)

        """
        def __f_save(target_data,file_out):
            FILE = open(file_out,'w')
            FILE.write(target_data)
            FILE.close()
            print "saved to %s"%file_out

        if isinstance(query, str):
            url='http://www.ebi.ac.uk/chemblws/compounds/%s/image' % query
            if dimensions is not None:
                url += '?dimensions=%s'%dimensions
            target_data = urllib2.urlopen(url).read()
            print url
            if file_out is None:
                file_out = os.getcwd()
                file_out += '/%s.png' % query
            __f_save(target_data,file_out)
            if view:
                webbrowser.open(file_out)
            fout = file_out
        elif isinstance(query, tuple) or isinstance(query,list):
            fout = []
            for item in query:
                url= self.url + '/compounds/%s/image' % item
                if dimensions is not None:
                    url += '?dimensions=%s'%dimensions
                target_data = urllib2.urlopen(url).read()
                if file_out is None:
                    file_out = os.getcwd()
                    file_out += '/%s.png'%item
                fout.append(file_out)
                __f_save(target_data,file_out)
                if view:
                    webbrowser.open(file_out)
        else:
            raise TypeError('Inappropriate argument type.')
        return fout


    @__process("compounds", "bioactivities")
    def get_compounds_activities(self, query):
        """Get individual compound bioactivities

        :param str query: Compound ChEMBLId with optional extension. This is different from
            the API!! API is compounds/%s/bioactivities.json here we need to provide json if
            we want json output. So query must be CHEMBL2.json (or use
            default_extension
        :return: Bioactivity records in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'bioactivities'. The value of that key is a lsit of bioactivity
        records. Each bioactivity record is a dictionary keyed by:

         * activity_comment
         * assay_chemblid
         * assay_description
         * assay_type
         * bioactivity_type
         * ingredient_cmpd_chemblid
         * name_in_reference
         * operator
         * organism
         * parent_cmpd_chemblid
         * reference
         * target_chemblid
         * target_confidence
         * target_name
         * units
         * value

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._bioactivities_example)
            >>> resxmls = get_compounds_activities(s._bioactivities_example + '.xml')
            >>> resjson = s.get_compounds_activities(s._bioactivities_example)
        """
        pass


    @__process("targets")
    def get_target_by_chemblId(self, query):
        """Get target by ChEMBLId

        :param str query: a target ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :param str query: target ChEMBLId
        :return: Target Record in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'target'. The value of that key is another dictionary
        keyed by:

         * target
         * description
         * geneNames
         * organism
         * preferredName
         * proteinAccession
         * synonyms
         * targetType

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._target_chemblId_example)
            >>> resxml = s.get_target_by_chemblId(s._target_chemblId_example + '.xml')
            >>> resjson = s.get_target_by_chemblId(s._target_chemblId_example)
        """
        pass


    @__process("targets/uniprot")
    def get_target_by_uniprotId(self, query):
        """Get individual target by UniProt Accession Id

        :param str query: a valid uniprot accession Id. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: see :meth:get_target_by_chemblId

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._target_chemblId_example)
            >>> resxmls = s.get_target_by_uniprotId(s._target_uniprotId_example + '.xml')
            >>> resjson = s.get_target_by_uniprotId(s._target_uniprotId_example)
        """
        pass


    @__process("targets/refseq")
    def get_target_by_refSeqId(self, query):
        """Get individual target by RefSeq Accession Id

        .. warning:: not yet working. Example on the Chembl website is not working.

        :param query: a valid RefSea accession Id
        :return: Target Record


        .. existing one: NP_015325
        """
        pass

    @__process("targets","bioactivities")
    def get_target_bioactivities(self, query):
        """Get individual target bioactivities

        :param str query: a valid target ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: see :meth:`get_compounds_activities`

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._target_bioactivities_example)
            >>> resxml = s.get_target_bioactivities(s._target_bioactivities_example + '.xml')
            >>> resjson = s.get_target_bioactivities(s._target_bioactivities_example)
        """
        pass


    def get_all_targets(self):
        """Get all targets

        :return: Target Record in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'targets'. The value of that key is a list of dictionaries
        keyed by:


          * chemblId
          * description
          * geneNames
          * organism
          * preferredName
          * proteinAccession
          * synonyms
          * targetType

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> res = s.get_all_targets()
        """
        res = self.request(self.url + "/targets." + self.default_extension)
        if self.default_extension == "json":
            res = json.loads(res)
        return res


    @__process("assays")
    def get_assay_by_chemblId(self, query):
        """Get assay by ChEMBLId

        :param str query: a valid assay ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: Assay record in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'assay'. The value of that key is another dictionary
        keyed by:

         * assayDescription
         * assayOrganism
         * assayStrain
         * assayType
         * chemblId
         * journal
         * numBioactivities

        .. doctest::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._assay_example)
            CHEMBL1217643
            >>> resxml = s.get_assay_by_chemblId(s._assay_example + '.xml')
            >>> resjson = s.get_assay_by_chemblId(s._assay_example)

        """
        pass


    @__process("assays", "bioactivities")
    def get_assay_bioactivities(self, query):
        """Get individual assay bioactivities

        :param str query: a valid assay ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: Bioactivity records for a given assay in XML or dictionary
            (if json requested). See :meth:`get_compounds_activities`

        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._assay_example)
            >>> resxml = s.get_assay_bioactivities(s._assay_example + '.xml')
            >>> resjson = s.get_assay_bioactivities(s._assay_example)
        """
        pass


    def inspect(self, query):
        """Open the URL of a query in a browser

        ::

            s.inspect("CHEMBL1940")

        """
        url = "https://www.ebi.ac.uk/chembldb/target/inspect/" + query
        webbrowser.open(url)
