#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
# $Id: chembldb.py 318 2014-02-28 13:30:26Z cokelaer $

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
import os
from bioservices.services import REST
import webbrowser

__all__ = ["ChEMBL"]


class ChEMBL(REST):
    """Interface to `ChEMBL <http://www.ebi.ac.uk/chembldb/index.php>`_

    Here is a quick example to retrieve a target given its ChEMBL Id

    .. doctest::

        >>> from bioservices import ChEMBL
        >>> s = ChEMBL(verbose=False)
        >>> resjson = s.get_target_by_chemblId('CHEMBL240')
        >>> resjson['proteinAccession']
        'Q12809'

    By default, most methods return dictionaries (converted from json objects returned
    by the ChEMBL API), however, you can also set the format to be XML.

    """
    _url = "https://www.ebi.ac.uk/chemblws/"

    _chemblId_example = "CHEMBL1"
    _inChiKey_example = "QFFGVLORLPOAEC-SNVBAGLBSA-N"
    _smiles_example = "COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56"
    _smiles_struct_example = "C\C(=C/C=C/C(=C/C(=O)O)/C)\C=C\C1=C(C)CCCC1(C)C"
    _smiles_similar_example = _smiles_example
    _image_chemblId_example = "CHEMBL192"
    _bioactivities_example = "CHEMBL2"
    _target_chemblId_example = "CHEMBL2477"
    _target_uniprotId_example = "Q13936"
    _target_bioactivities_example = "CHEMBL240"
    _alt_compound_form_example = "CHEMBL278020"
    _target_approved_drugs_example = "CHEMBL1824"
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
            res = self.http_get(request % query, frmt=frmt)
        else:
            res = self.http_get([request % x for x in query], frmt=frmt)
        return res

    def _postprocess(self, data, key):
        try:
            return data[key]
        except:
            try:
                return [x[key] for x in data]
            except:
                return data

    def status(self):
        """Return the API status

        :return: Response is the string 'UP' if the service is running
        """
        res = self.http_get("status", frmt="json")
        try:
            #FIXME: wierd behaviour that is different on different systems...
            return res['status']
        except:
            return res

    def get_compounds_by_chemblId(self, query, frmt="json"):
        """Get compound by ChEMBLId

        :param query: a compound ChEMBLId or a list of those ones.
            if the identifier is invalid, the number 404 is returned.
        :param str frmt: json or xml (Default to json)
        :return: Compound Record (dictionary). If
            the query is a list of identifiers, a list of compound records is
            returned.

        If json format is requested, a dictionary is returned. Here are some of the keys:

         * acdLogd
         * chemblId
         * knownDrug
         * molecularFormula
         * molecularWeight
         * passesRuleOfThree
         * smiles
         * stdInChiKey

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print (s._chemblId_example)
            >>> resjson = s.get_compounds_by_chemblId(s._chemblId_example)

        """
        res = self._process(query, frmt, "compounds/%s")
        return res

    def get_compounds_by_chemblId_form(self, query, frmt="json"):
        """

        :param query: valid chembl identifier (or list)
        :param str frmt: json or xml (Default to json)

        See :meth:`get_compounds_by_chemblId` for full doc.

        ::

            >>> s.get_compounds_by_chemblId_form("CHEMBL2")
            [{u'chemblId': u'CHEMBL1347191', u'parent': False},
             {u'chemlId': u'CHEMBL1558', u'parent': False},
             {u'chemblId': u'CHEMBL2', u'parent': True}]

        """
        res = self._process(query, frmt, "compounds/%s/form")
        return self._postprocess(res, 'forms')

    def get_compounds_by_chemblId_drug_mechanism(self, query, frmt="json"):
        """

        :param query: valid chembl identifier (or list)
        :param str frmt: json or xml (Default to json)

        See :meth:`get_compounds_by_chemblId` for full doc.

        ::

            >>> s.get_compounds_by_chemblId_drug_mechanism("CHEMBL3")
            [{u'chemblId': u'CHEMBL1347191', u'parent': False},
            {u'chemblId': u'CHEMBL1558', u'parent': False},
            {u'chemblId': u'CHEMBL2', u'parent': True}]

        """
        res = self._process(query, frmt, "compounds/%s/drugMechanism")
        return res

    def get_individual_compounds_by_inChiKey(self, query, frmt="json"):
        """Get individual compound by standard InChi Key

        :param str query: a valid InChi key or a list.
        :param str frmt: json or xml (Default to json)
        :return: Compound Record as a dictionary (or list of dictionaries)

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
            >>> resjson = s.get_individual_compounds_by_inChiKey(s._inChiKey_example)
        """
        res = self._process(query, frmt, "compounds/stdinchikey/%s")
        return self._postprocess(res, 'compound')

    def get_compounds_by_SMILES(self, query, frmt="json"):
        """Get list of compounds by Canonical SMILES

        :param str query: a valid compound ChEMBLId or a list of those ones.
        :param str frmt: json or xml (Default to json)
        :return: Compound Record in XML or dictionary (if json requested). If
            query os a list/tuple, a  tuple of compound records is returned.

        If json format is requested, a dictionary is returned. The dictionary
        has a unique key 'compounds'. The value of that key is a list of compound
        records. For each compound record dictionary see :meth:`get_compounds_by_chemblId`.

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._smiles_example)
            >>> resjson = s.get_compounds_by_SMILES(s._smiles_example)
        """
        res = self._process(query, frmt, "compounds/smiles/%s")
        return res

    def get_compounds_containing_SMILES(self, query, frmt="json"):
        """Deprecated. Use get_compounds_substructure"""
        self.logging.error("Deprecated. Use get_compounds_substructure")

    def get_compounds_substructure(self, query, frmt="json"):
        """Get list of compounds containing the substructure represented
        by the given Canonical SMILES

        :param str query: a valid SMILES string or a list of those ones.
        :param str frmt: json or xml (Default to json)
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
        :param str frmt: json or xml (Default to json)
        :return: Compound records. See :meth:`get_compounds_by_chemblId`

        Each dictionary has a set of keys amongst which:

         * acdAcidicPka
         * acdBasicPka
         * similarity
         * species

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._smiles_similar_example)
            >>> resjson = s.get_compounds_similar_to_SMILES(s._smiles_example, "100")
            >>> resjson = s.get_compounds_similar_to_SMILES(s._smiles_similar_example)
        """
        self.devtools.check_range(similarity, 70, 100)
        res = self._process(query, frmt, "compounds/similarity/%s/"+str(similarity))
        return self._postprocess(res, 'compounds')

    def get_image_of_compounds_by_chemblId(self, query, dimensions=500,
            save=True, view=True, engine="rdkit"):
        """Get the image of a given compound in PNG png format.

        :param str query: a valid compound ChEMBLId or a list/tuple of valid compound ChEMBLIds.
        :param int dimensions: optional argument. An integer z (:math:`1 \leq z \leq 500`)
            giving the dimensions of the image.
        :param save:
        :param view:
        :param engine: Defaults to rdkit. Implemented for the future but only one value for now.
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
        queries = self.devtools.to_list(query)

        res = {'filenames':[], 'images':[], 'chemblids':[]}
        for query in queries:
            req = "compounds/%s/image" % query
            #url=self.url+'compounds/%s/image' % query
            if dimensions is not None:
                req += '?engine=%s&dimensions=%s'%(engine, dimensions)
            target_data = self.http_get(req, frmt=None)

            file_out = os.getcwd()
            file_out += '/%s.png' % query
            with open(file_out, "wb") as thisfile:
                thisfile.write(bytes(target_data))
                thisfile.close()
                self.logging.info("saved to %s" % file_out)

            fout = file_out
            res['chemblids'].append(query)
            res['filenames'].append(fout)
            res['images'].append(target_data)
        if view:
            webbrowser.open(res['filenames'][0])
        return res

    def get_compounds_activities(self, query, frmt="json"):
        """Get individual compound bioactivities

        :param str query: valid chembl identifier (or list)
        :param str frmt: json or xml (Default to json)
        :return: Bioactivity records in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. Here are some
        of the keys:

         * activity_comment
         * assay_description
         * name_in_reference
         * organism
         * reference
         * target_confidence
         * target_name
         * units
         * value

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._bioactivities_example)
            >>> resjson = s.get_compounds_activities(s._bioactivities_example)
        """
        res = self._process(query, frmt, "compounds/%s/bioactivities")
        return res

    def get_target_by_chemblId(self, query, frmt="json"):
        """Get target by ChEMBLId

        :param str query: target ChEMBLId
        :param str frmt: json or xml (Default to json)
        :return: Target Record in XML or dictionary (if json requested)

        If json format is requested, a dictionary is returned. Here are
        some of dictionary's keys:

         * target
         * geneNames
         * organism
         * proteinAccession
         * targetType

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._target_chemblId_example)
            >>> resjson = s.get_target_by_chemblId(s._target_chemblId_example)
        """
        res = self._process(query, frmt, "targets/%s")
        return res

    def get_target_by_uniprotId(self, query, frmt="json"):
        """Get individual target by UniProt Accession Id

        :param str query: a valid uniprot accession Id.
        :param str frmt: json or xml (Default to json)
        :return: see :meth:`get_target_by_chemblId`

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._target_chemblId_example)
            >>> resjson = s.get_target_by_uniprotId(s._target_uniprotId_example)
        """
        res = self._process(query, frmt, "targets/uniprot/%s")
        if frmt == 'json':
            res = res['target']
        return res

    def get_target_by_refseq(self, query, frmt='json'):
        """Get individual target by RefSeq Accession identifier

        :param str query: a valid RefSeq accession Id
        :param str frmt: json or xml (Default to json)
        :return: Target Record

        .. warning:: this method works but I could not find any example to validate it.
            NP_001128722 provided on chembl blogspot does not work.
            NP_015325 from the ChEMBL API does not work either.

        """
        res = self._process(query, frmt, "targets/refseq/%s")
        return res

    def get_target_bioactivities(self, query, frmt="json"):
        """Get individual target bioactivities

        :param str query: a valid target ChEMBLId.
        :param str frmt: json or xml (Default to json)

        :return: see :meth:`get_compounds_activities`

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._target_bioactivities_example)
            >>> resjson = s.get_target_bioactivities(s._target_bioactivities_example)
        """
        res = self._process(query, frmt, "targets/%s/bioactivities")
        return self._postprocess(res, 'bioactivities')

    def get_all_targets(self, frmt="json"):
        """Get all targets in a dictionary

        :param str frmt: json or xml (Default to json)
        :return: Target Record in a dictionary (default is json)

        The returned list contains a dictionary for each **target**.
        Here are some keys contained in the dictionaries:

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
        res = self.http_get("targets." + frmt, frmt=frmt)
        return self._postprocess(res, 'targets')

    def get_assays_by_chemblId(self, query, frmt="json"):
        """Get assay by ChEMBLId

        :param str query: a valid assay ChEMBLId.
        :param str frmt: json or xml (Default to json)
        :return: Assay record as a dictionary (if json requested)
            (list of dictionaries if input is a list)

        If json format is requested, a dictionary is returned.
        with some of the following keys:

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
            >>> resjson = s.get_assays_by_chemblId(s._assays_example)

        """
        res = self._process(query, frmt, "assays/%s")
        return res

    def get_assays_bioactivities(self, query, frmt="json"):
        """Get individual assay bioactivities

        :param str query: a valid assay ChEMBLId.
        :param str frmt: json or xml (Default to json)
        :return: Bioactivity records for a given assay (dictionary)

        ::

            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> print(s._assays_example)
            >>> resjson = s.get_assays_bioactivities(s._assays_example)
        """
        res = self._process(query, frmt, "assays/%s/bioactivities")
        return res

    def get_alternative_compound_form(self, query, frmt="json"):
        """ Get list of alternative compound forms (e.g. parent and salts) of compound

        :param query: a valid compound ChEMBLId
        :param frmt: json or xml (Default to json)
        :return: List of ChEMBLIDs which correspond to alternative forms of query compound

        >>> from bioservices import *
        >>> s = ChEMBL(verbose=False)
        >>> resjson = s.get_alternative_compound_form(s._alt_compound_form_example)
        """

        res = self._process(query, frmt, "compounds/%s/form")
        return res

    def get_approved_drugs(self, query, frmt="json"):
        """Get list of approved drugs chembl compound details

        :param query: a valid target ChEMBLId
        :param frmt: json or xml (Default to json)
        :return: list of approved drugs ChEMBL compound details (dictionary)

        >>> from bioservices import *
        >>> s = ChEMBL(verbose=False)
        >>> resjson = s.get_approved_drugs(s._target_approved_drugs_example)
        """
        res = self._process(query, frmt, "targets/%s/approvedDrug")
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
        res = self.http_get("status", frmt="json")
        try:
            #FIXME: wierd behaviour that is different on different systems...
            return res['version']
        except:
            return res


class BenchmarkChembl(ChEMBL):

    def __init__(self):
        super(BenchmarkChembl, self).__init__(cache=True)

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
