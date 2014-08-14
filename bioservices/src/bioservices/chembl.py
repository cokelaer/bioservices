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
#$Id: chembldb.py 318 2014-02-28 13:30:26Z cokelaer $

"""This module provides a class :class:`ChEMBL`

.. topic:: What is ChEMBL

    :URL:  https://www.ebi.ac.uk/chembldb/index.php/
    :REST: https://www.ebi.ac.uk/chembldb/index.php/ws
    :FAQS: https://www.ebi.ac.uk/chembldb/index.php/faq


    .. highlights::

        "Using the ChEMBL web service API users can retrieve data from the ChEMBL
        database in a programmatic fashion. The following list defines the currently
        supported functionality and defines the expected inputs and outputs of each
        method."

        -- From ChEMBL web page Dec 2012




"""
#import urllib2,  json,
import os
from bioservices.services import RESTService, REST
import webbrowser


class ChEMBL(REST):
    """Interface to `ChEMBL <http://www.ebi.ac.uk/chembldb/index.php>`_


    Here is a quick example to retrieve a target given its ChEMBL Id
    .. doctest::

        >>> from bioservices import ChEMBL
        >>> s = ChEMBL(verbose=False)
        >>> resjson = s.get_target_by_chemblId('CHEMBL240')
        >>> resjson['proteinAccession']
        'Q12809'


    """
    _url = "https://www.ebi.ac.uk/chemblws/"
    _chemblId_example = "CHEMBL1"
    _inChiKey_example = "QFFGVLORLPOAEC-SNVBAGLBSA-N"
    _smiles_example = "COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56"
    _smiles_struct_example = "C\C(=C/C=C/C(=C/C(=O)O)/C)\C=C\C1=C(C)CCCC1(C)C"
    _smiles_similar_example = _smiles_example + "/90"
    _image_chemblId_example = "CHEMBL192"
    _bioactivities_example = "CHEMBL2"
    _target_chemblId_example = "CHEMBL2477"
    _target_uniprotId_example = "Q13936"
    _target_bioactivities_example = "CHEMBL240"
    _target_refseq_example = 'NP_015325'
    _assays_example = "CHEMBL1217643"
    _inspect_example = ('CHEMBL1','compound')

    def __init__(self, verbose=False, cache=False):
        super(ChEMBL, self).__init__(url=ChEMBL._url,
            name="ChEMBL", verbose=verbose, cache=cache)

    def _process(self, query, frmt, request):
        self.devtools.check_param_in_list(frmt, ["json", "xml"])
        request = request + "." + frmt
        if isinstance(query, str):
            res = self.get(request % query, frmt=frmt)
        else:
            res = self.get([request % x for x in query], frmt=frmt)
        return res

    def status(self):
        """ Check API status

        :return: Response is the string 'UP' if services are running
        """
        res = self.get("status", frmt="json")
        return res['status']

    def get_compounds_by_chemblId(self, query, frmt="json"):
        """Get compound by ChEMBLId

        :param query: a compound ChEMBLId or a list of those ones.
            if the identifier is invalid, the number 404 is returned.
        :param str frmt: the output format (json or xml) (defaults to json)
        :return: Compound Record (dictionary from the returned json object). If
            the query is a list of identifiers, a list of compound records is 
            returned.

        If json format is requested, a dictionary is returned with the following 
        keys:

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
            >>> s = ChEMBL(verbose=False)
            >>> print (s._chemblId_example)
            >>> resxml = s.get_compounds_by_chemblId(s._chemblId_example, frmt="xml")
            >>> resjson = s.get_compounds_by_chemblId(s._chemblId_example)

        """
        res = self._process(query, frmt, "compounds/%s")
        return res

    def get_compounds_by_chemblId_form(self, query, frmt="json"):
        """

        See :meth:`get_compounds_by_chemblId` for full doc.

        ::
        
            >>> s.get_compounds_by_chemblId_form("CHEMBL2")
            [{u'chemblId': u'CHEMBL1347191', u'parent': False},
             {u'chemlId': u'CHEMBL1558', u'parent': False},
             {u'chemblId': u'CHEMBL2', u'parent': True}]

        """
        res = self._process(query, frmt, "compounds/%s/form")
        return res


    def get_compounds_by_chemblId_drug_mechanism(self, query, frmt="json"):
        """

        See :meth:`get_compounds_by_chemblId` for full doc.

        CHEMBL3

        [{u'chemblId': u'CHEMBL1347191', u'parent': False},
         {u'chemblId': u'CHEMBL1558', u'parent': False},
         {u'chemblId': u'CHEMBL2', u'parent': True}]

        """
        res = self._process(query, frmt, "compounds/%s/drugMechamism")
        return res

    def get_individual_compounds_by_inChiKey(self, query, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> print(s._inChiKey_example)
            QFFGVLORLPOAEC-SNVBAGLBSA-N
            >>> resxml = s.get_individual_compounds_by_inChiKey(s._inChiKey_example, "xml")
            >>> resjson = s.get_individual_compounds_by_inChiKey(s._inChiKey_example)
        """
        res = self._process(query, frmt, "compounds/stdinchikey/%s")
        return res

    def get_compounds_by_SMILES(self, query, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> print(s._smiles_example)
            >>> resxml = s.get_compounds_by_SMILES(s._smiles_example + ".xml")
            >>> resjson = s.get_compounds_by_SMILES(s._smiles_example)
        """
        res = self._process(query, frmt, "compounds/smiles/%s")
        return res

    def get_compounds_containing_SMILES(self, query, frmt="json"):
        self.logging.error("Deprecated. Use get_compounds_substructure")

    def get_compounds_substructure(self, query, frmt="json"):
        """Get list of compounds containing the substructure represented
        by the given Canonical SMILES

        :param str query: a valid SMILES string or a list of those ones.
            A ".json" or ".xml" extension can be added to bypass default
            :attr:`default_extension`.
        :return: see :meth:`get_compounds_by_SMILES`


        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._smiles_example)
            >>> res = s.get_compounds_substructure(s._smiles_struct_example)
        """
        res = self._process(query, frmt, "compounds/substructure/%s")
        return res

    def get_compounds_similar_to_SMILES(self, query, similarity=90, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> print(s._smiles_similar_example)
            >>> resjson = s.get_compounds_similar_to_SMILES(s._smiles_example + "/100")
            >>> resjson = s.get_compounds_similar_to_SMILES(s._smiles_similar_example)
        """
        res = self._process(query, frmt, "compounds/similarity/%s/"+str(similarity))
        return res

    def get_image_of_compounds_by_chemblId(self, query, dimensions=500,
            save=True, view=True, engine="rdkit"):
        """Get the image of a given compound in PNG png format.

        :param str query: a valid compound ChEMBLId or a list/tuple of valid compound ChEMBLIds.
        :param int dimensions: optional argument. An integer z (:math:`1 \leq z \leq 500`)
            giving the dimensions of the image.
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

        .. plot::
            :include-source:
            :width: 50%

            >>> from pylab import imread, imshow
            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> res = s.get_image_of_compounds_by_chemblId(s._image_chemblId_example)
            >>> imshow(imread(res['filenames'][0]))

        .. todo:: ignorecoords option
        """
        # NOTE: not async requests here. 
        self.devtools.check_range(dimensions, 1,500)
        self.devtools.check_param_in_list(engine, ['rdkit'])
        queries = self.devtools.transform_into_list(query)

        def __f_save(target_data, file_out):
            FILE = open(file_out, 'w')
            FILE.write(target_data)
            FILE.close()
            self.logging.info("saved to %s"%file_out)

        res = {'filenames':[], 'images':[], 'chemblids':[]}
        for query in queries:
            req = "compounds/%s/image" % query
            #url=self.url+'compounds/%s/image' % query
            if dimensions is not None:
                req += '?engine=%s&dimensions=%s'%(engine, dimensions)
            target_data = self.get(req, frmt=None)
            
            file_out = os.getcwd()
            file_out += '/%s.png' % query
            __f_save(target_data,file_out)

            fout = file_out
            res['chemblids'].append(query)
            res['filenames'].append(fout)
            res['images'].append(target_data)
        if view:
            webbrowser.open(res['filenames'][0])
        return res

    def get_compounds_activities(self, query, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> print(s._bioactivities_example)
            >>> resxmls = s.get_compounds_activities(s._bioactivities_example + '.xml')
            >>> resjson = s.get_compounds_activities(s._bioactivities_example)
        """
        res = self._process(query, frmt, "compounds/%s/bioactivities")
        return res

    def get_target_by_chemblId(self, query, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> print(s._target_chemblId_example)
            >>> resxml = s.get_target_by_chemblId(s._target_chemblId_example + '.xml')
            >>> resjson = s.get_target_by_chemblId(s._target_chemblId_example)
        """
        res = self._process(query, frmt, "targets/%s")
        return res

    def get_target_by_uniprotId(self, query, frmt="json"):
        """Get individual target by UniProt Accession Id

        :param str query: a valid uniprot accession Id. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: see :meth:get_target_by_chemblId

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._target_chemblId_example)
            >>> resxmls = s.get_target_by_uniprotId(s._target_uniprotId_example + '.xml')
            >>> resjson = s.get_target_by_uniprotId(s._target_uniprotId_example)
        """
        res = self._process(query, frmt, "targets/uniprot/%s")
        return res


    def get_target_by_refseq(self, query, frmt='json'):
        """Get individual target by RefSeq Accession identifier

        .. warning:: not yet working. Example on the Chembl website is not working.

        :param str query: a valid RefSea accession Id
        :return: Target Record


        .. existing one: NP_015325
        """
        res = self._process(query, frmt, "targets/refseq/%s")
        return res

    def get_target_bioactivities(self, query, frmt="json"):
        """Get individual target bioactivities

        :param str query: a valid target ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: see :meth:`get_compounds_activities`

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._target_bioactivities_example)
            >>> resxml = s.get_target_bioactivities(s._target_bioactivities_example + '.xml')
            >>> resjson = s.get_target_bioactivities(s._target_bioactivities_example)
        """
        res = self._process(query, frmt, "targets/%s/bioactivities")
        return res

    def get_all_targets(self, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> res = s.get_all_targets()
        """
        self.devtools.check_param_in_list(frmt, ["json", "xml"])
        res = self.get("targets", frmt=frmt)
        return res

    def get_assays_by_chemblId(self, query, frmt="json"):
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
            >>> s = ChEMBL(verbose=False)
            >>> print(s._assays_example)
            CHEMBL1217643
            >>> resxml = s.get_assays_by_chemblId(s._assays_example + '.xml')
            >>> resjson = s.get_assays_by_chemblId(s._assays_example)

        """
        res = self._process(query, frmt, "assays/%s")
        return res

    def get_assays_bioactivities(self, query, frmt="json"):
        """Get individual assay bioactivities

        :param str query: a valid assay ChEMBLId. A ".json" or ".xml" extension
            can be added to bypass default :attr:`default_extension`
        :return: Bioactivity records for a given assay in XML or dictionary
            (if json requested). See :meth:`get_compounds_activities`

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._assays_example)
            >>> resxml = s.get_assays_bioactivities(s._assays_example + '.xml')
            >>> resjson = s.get_assays_bioactivities(s._assays_example)
        """
        res = self._process(query, frmt, "assays/%s/bioactivities")
        return res

    def inspect(self, query, item_type):
        """Open the URL of a query in a browser.

        :param str query: a valid ChEMBLId of a compound, target or assay.
        :param str item_type: a valid type. Might be compound, target or assay

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._assays_example)
            >>> s.inspect(*s._inspect_example)
            >>> print(s._assays_example)
            >>> s.inspect(s._assays_example,'assay')

        """
        url = "https://www.ebi.ac.uk/chembldb/%s/inspect/%s"%(item_type, query)
        webbrowser.open(url)

    def version(self):
        """Return version of the API on the server"""
        res = self.get("status", frmt="json")
        return res['version']


class BenchmarkChembl(ChEMBL):

    def __init__(self):
        super(BenchmarkChembl, self).__init__( cache=True)

    def benchmark(self, N=1000):
        #self.name = "compounds"
        import time
        t1 = time.time()
        res = self.get_compounds_by_chemblId(['CHEMBL%s' % i for i in range(1,N)])
        t2 = time.time()
        res1 = t2-t1
        print(t2-t1)

        t1 = time.time()
        res = [self.get_compounds_by_chemblId('CHEMBL%s' % i) for i in range(1,N)]
        t2 = time.time()
        res2   = t2-t1
        print(t2-t1)

        return res, res1, res2

    def benchmark2(self, N):
        print("ORIGINAL chembl")
        from chembl_webresource_client import CompoundResource
        compounds = CompoundResource()
        import time

        t1 = time.time()
        res = compounds.get(['CHEMBL%s' % x for x in range(1,N)])
        t2 = time.time()

        res1 = t2-t1
        print(t2-t1)

        t1 = time.time()
        res = [compounds.get('CHEMBL%s' % x) for x in range(1,N)]
        t2 = time.time()

        res2 = t2-t1
        print(t2-t1)
        return res, res1, res2


    def compare_benchmark(self,n=10, N=1000):

        df = {'bs_sync':[], 'bs_normal':[], 'ch_sync':[], 'ch_normal':[]}
        for i in range(0,n):
            print(i)
            res, res1, res2 = self.benchmark(N)
            df['bs_sync'].append(res1)
            df['bs_normal'].append(res2)
            res, res1, res2 = self.benchmark2(N)
            df['ch_sync'].append(res1)
            df['ch_normal'].append(res2)
            print
        import pandas as pd
        df = pd.DataFrame(df)
        import pylab
        pylab.clf()
        df  = df[['bs_normal','ch_normal','bs_sync','ch_sync']]
        pylab.axvline(2.5)
        df.boxplot()
        return df

