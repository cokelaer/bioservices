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
    :FAQS: https://www.ebi.ac.uk/chembldb/index.php/faq


    .. highlights::

        "Using the ChEMBLdb web service API users can retrieve data from the ChEMBL
        database in a programmatic fashion. The following list defines the currently
        supported functionality and defines the expected inputs and outputs of each
        method."

        -- From ChEMBLdb web page Dec 2012




"""
import urllib2, urllib, json, re, os
from bioservices.services import *
import webbrowser


class ChEMBLdb(RESTService):
    """Interface to `ChEMBLdb <http://www.ebi.ac.uk/chembldb/index.php>`_ 


    Here is a quick example to retrieve a target given its ChEMBL Id
    .. doctest::

        >>> from bioservices import ChEMBLdb
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
    _inspect_example = ('CHEMBL1','compound')

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
                """
                There are two cases: query is a string or a list/tuple of strings.
                In the first case, query is something close to url query. In the second case,
                is a family of those ones.
                """
                def infunc(query):
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
                if isinstance(query,str):
                    res = infunc(query)
                elif isinstance(query,list) or isinstance(query,tuple):
                    res = tuple(map(infunc, query))
                else:
                    raise TypeError("query must be a string, list or tuple!!")
                return res
                #return func(self, *args, **kwds)
            newf.__name__ = func.__name__
            newf.__doc__ = func.__doc__
            return newf
        return decorator


    @__process("compounds")
    def get_compounds_by_chemblId(self, query):
        """Get compound by ChEMBLId

        :param query: a valid compound ChEMBLId or a list of those ones.
            A ".json" or ".xml" extension can be added to bypass default
            :attr:`default_extension`.
        :return: Compound Record in XML or dictionary (if json requested). If
            query os a list/tuple, a  tuple of compound records is returned.

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

        :param str query: a valid InChi key or a list of those ones.
            A ".json" or ".xml" extension can be added to bypass default
            :attr:`default_extension`.
        :return: Compound Record in XML or dictionary (if json requested). If
            query os a list/tuple, a  tuple of compound records is returned.

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
            QFFGVLORLPOAEC-SNVBAGLBSA-N
            >>> resxml = s.get_individual_compounds_by_inChiKey(s._inChiKey_example + ".xml")
            >>> resjson = s.get_individual_compounds_by_inChiKey(s._inChiKey_example + ".json")
        """
        # the decorator is taking care of the checking and processing
        pass

    @__process("compounds/smiles")
    def get_compounds_by_SMILES(self, query):
        """Get list of compounds by Canonical SMILES

        :param str query: a valid compound ChEMBLId or a list of those ones.
            A ".json" or ".xml" extension can be added to bypass default
            :attr:`default_extension`.
        :return: Compound Record in XML or dictionary (if json requested). If
            query os a list/tuple, a  tuple of compound records is returned.

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

        :param str query: a valid SMILES string or a list of those ones.
            A ".json" or ".xml" extension can be added to bypass default
            :attr:`default_extension`.
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

        :param str query: a valid SMILES string or a list of those ones.
            A ".json" or ".xml" extension can be added to bypass default
            :attr:`default_extension`.
            The SMILE string must be followed by a slash character and the
            expected similarity (e.g., "/90").
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
            file_out=True, view=True):
        """Get the image of a given compound with png fromat.

        :param str query: a valid compound ChEMBLId or a list/tuple of valid compound ChEMBLIds.
        :param int dimensions: optional argument. An integer z such that :math:`1 \leq z \leq 500`
            giving the dimensions of the image.
            If query is a list and dimension is None or an integer, a list of the same size than query
            is created containing the same initial value into all positions.
            If both query and diemnsion are lists, the ith dimension is related to the image of the ith query.
        :param file_out: Can be True | False | a string | list of strings. If
            True, the images are automatically saved to home current work directory with the
            name of compound.
            If False, the images are not saved.
            If string and query is also a string, the image is saved to the path contained into the string.
            If string and query is a list, a list of paths is created using file_out as a seed.
            If list with different length of query, is completed with False's to be the same length
            If both file_out and query are lists with the same length, the image corresponding to ith query
            is saved using ith path into fiel_out.
        :param bool view: show the image. If True the images are opened.
        :return: the path (list of paths) used to save the figure (figures) (different from Chembl API)


        ::

            >>> from bioservices import *
            >>> s = ChEMBLdb(verbose=False)
            >>> print (s._image_chemblId_example, s._image_dimension_example)
            >>> s.get_image_of_compounds_by_chemblId(s._image_chemblId_example)
            >>> s.get_image_of_compounds_by_chemblId(s._image_chemblId_example, s._image_dimension_example)
        """        
        def check_args(master_arg, slave_arg, master_name, slave_name):
            """
            It checks if the slave_arg is agree with master_arg
            """
            if slave_name == 'file_out':
                if isinstance(master_arg,str):
                    if not isinstance(slave_arg,str) and not isinstance(slave_arg,bool):
                        raise TypeError("%s type must be a str or bool type."%slave_name)
                elif isinstance(master_arg,list) or isinstance(master_arg, tuple):
                    if not all([isinstance(v,str) for v in master_arg]):
                        raise TypeError("All %s types must be str type."%master_name)
                    Lm = len(master_arg)
                    if isinstance(slave_arg,bool):
                        slave_arg = [slave_arg]*len(Lm)
                    elif isinstance(slave_arg,str):
                        slave_arg = [slave_arg + '-%d'%i for i in xrange(Lm)]
                    elif isinstance(slave_arg,list) or isinstance(slave_arg,tuple):
                        if len(slave_arg) > len(master_arg):
                            slave_arg = slave_arg[:Lm]
                        if not all([any([isinstance(v,t) for t in [str, bool]]) for v in slave_arg]):
                            raise TypeError("All %s types must be str or bool type."%slave_name)
                        Ls = len(slave_arg)
                        slave_arg = list(slave_arg) + [False for i in xrange(Lm-Ls)]
                    else:
                        raise TypeError("%s type must be a str, bool, list or tuple type"%slave_name)
                else:
                    raise TypeError("%s type must be a str, list or tuple type"%master_name)
                return slave_arg
            elif slave_name == 'dimensions':
                if isinstance(master_arg,str):
                    if not type(slave_arg) == int and not isinstance(slave_arg, type(None)):
                        raise TypeError("%s type must be a int or NoneType type."%slave_name)
                elif isinstance(master_arg,list) or isinstance(master_arg, tuple):
                    if not all([isinstance(v,str) for v in master_arg]):
                        raise TypeError("All %s types must be str type."%master_name)
                    Lm = len(master_arg)
                    if isinstance(slave_arg,type(None)):
                        slave_arg = [slave_arg]*Lm
                    elif type(slave_arg) == int:
                        slave_arg = [slave_arg]*Lm
                    elif isinstance(slave_arg,list) or isinstance(slave_arg,tuple):
                        if len(slave_arg) > len(master_arg):
                            slave_arg = slave_arg[:Lm]
                        if not all([any([type(v) == t for t in [int, type(None)]]) for v in slave_arg]):
                            raise TypeError("All %s types must be int or NoneType type."%slave_name)
                        Ls = len(slave_arg)
                        slave_arg = list(slave_arg) + [None]*(Lm-Ls)
                    else:
                        raise TypeError("%s type must be a str, bool, list or tuple type"%slave_name)
                else:
                    raise TypeError("%s type must be a str, list or tuple type"%master_name)
                return slave_arg

        def __f_save(target_data,file_out):
            FILE = open(file_out,'w')
            FILE.write(target_data)
            FILE.close()
            print "saved to %s"%file_out
        file_out = check_args(query,file_out,'query','file_out')
        dimensions = check_args(query,dimensions,'query','dimensions')
        if isinstance(query, str):
            url='http://www.ebi.ac.uk/chemblws/compounds/%s/image' % query
            if dimensions is not None:
                url += '?dimensions=%s'%dimensions
            target_data = urllib2.urlopen(url).read()
            print url
            if file_out is True:
                file_out = os.getcwd()
                file_out += '/%s.png' % query
            if not file_out is False:
                __f_save(target_data,file_out)
            if view:
                webbrowser.open(file_out)
            fout = file_out
        elif isinstance(query, tuple) or isinstance(query,list):
            L = len(query)
            if not file_out is False:
                fout = []
            for i in xrange(L):
                item = query[i]
                fo = file_out[i]
                dim = dimensions[i]
                url= self.url + '/compounds/%s/image' % item
                if dim is not None:
                    url += '?dimensions=%s'%dim
                target_data = urllib2.urlopen(url).read()
                if fo is False:
                    fo = os.getcwd()
                    fo += '/%s.png'%item
                if not fo is False:
                    fout.append(fo)
                    __f_save(target_data,fo)
                if view:
                    webbrowser.open(fo)                
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
            >>> resxmls = s.get_compounds_activities(s._bioactivities_example + '.xml')
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

        :param str query: a valid RefSea accession Id
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
        """Get all targets in a dictionary

        :return: Target Record in a dictionary (default is json)
          

        The attribute :attr:`default_extension` is set to json so that
        the returned objetc is a json format. You may set the attribute to
        another format such as "XML"
        
        The returned dictionary has a unique key called **targets**.
        The value of that key is a list of dictionaries with the following keys:


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
        if self.default_extension == "json":
            res = self.request(self.url + "/targets." + self.default_extension, format="json")
            res = json.loads(res)
        else:
            res = self.request(self.url + "/targets." + self.default_extension, format="json")
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


    def inspect(self, query, item_type):
        """Open the URL of a query in a browser.

        :param str query: a valid ChEMBLId of a compound, target or assay.
        :param str item_type: a valid type. Might be compound, target or assay

        ::

            >>> from bioservices import *   
            >>> s = ChEMBLdb(verbose=False)
            >>> print(s._assay_example)
            >>> s.inspect(*s._inspect_example)
            >>> print(s._assay_example)
            >>> s.inspect(s._assay_example,'assay')

        """
        url = "https://www.ebi.ac.uk/chembldb/%s/inspect/%s"%(item_type, query)
        webbrowser.open(url)
