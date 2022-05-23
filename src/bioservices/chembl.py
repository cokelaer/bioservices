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
"""This module provides a class :class:`ChEMBL`

.. topic:: What is ChEMBL

    :URL:  https://www.ebi.ac.uk/chembl
    :REST: https://www.ebi.ac.uk/chembl/api/data

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
from bioservices import logger

logger.name == __name__
try:
    from urllib.parse import quote
except:
    from urllib import quote

__all__ = ["ChEMBL"]


class ChEMBL(REST):
    """New ChEMBL API bioservices 1.6.0

    **Resources**

    ChEMBL database is made of a set of resources. We recommend to look at
    https://arxiv.org/pdf/1607.00378.pdf

    Here we first create an instance and retrieve the first 1000 molecules from
    the database using the **limit** parameter.

    .. doctest::

        >>> from bioservices import ChEMBL
        >>> c = ChEMBL()
        >>> res = c.get_molecule(limit=1000)

    The returned objet is a list of 1000 records, each of them being a
    dictionary. The **molecule** resource is actually a very large one
    and one may want to skip some entries. This is possible using the **offset**
    parameter as follows::

        # Retrieve 1000 molecules skipping the first 50
        res = c.get_molecule(limit=1000, offset=50)

    If you want to know all resources available and the number of entries in
    each resources, use::

        status = c.get_status_resources()

    For instance, you should be able to get the total number of entries in the
    *mechanism* resource is about 5,000::

        print(status['mechanism'])

    To retrieve all entries from the mechanism resource, you can either set
    limit to a value large enough::

        res = c.get_mechanism(limit=1000000)

    or simply set it to -1::

        res = c.get_mechanism(limit=-1)

    All resources methods behaves in the same way.

    Those resources methods are: :meth:`get_activity`, :meth:`get_assay`,
    :meth:`get_atc_class`, :meth:`get_binding_site`, :meth:`get_biotherapeutic`,
    :meth:`get_cell_line`, :meth:`get_chembl_id_lookup`,
    :meth:`get_compound_record`, :meth:`get_compound_structural_alert`,
    :meth:`get_document`, :meth:`get_document_similarity`,
    :meth:`get_document_term`, :meth:`get_drug`, :meth:`get_drug_indication`,
    :meth:`get_go_slim`, :meth:`get_mechanism`, :meth:`get_metabolism`,
    :meth:`get_molecule`, :meth:`get_molecule_form`, :meth:`get_protein_class`,
    :meth:`get_source`, :meth:`get_target`, :meth:`get_target_component`,
    :meth:`get_target_prediction`, :meth:`get_target_relation`,
    :meth:`get_tissue`.

    **3 ways of getting items**

    1. Retrieve everything::

        c.get_molecule(limit=-1)

    2. Retrieve a specific entry::

        c.get_molecule("CHEMBL24")

    3. Retrieve a set of entries::

        c.get_molecule(["CHEMBL24","CHEMBL2"])

    **Filtering and Ordering**

    For ordering the results, we provide a simple method :meth:`order_by` that
    allows to sort the dictionary according to values in a specific key.

    Any data returned by a resource method (a list of dictionary) can be process
    through this method::

        c = ChEMBL()
        data = c.get_drug(limit=100)
        ordered_data = c.order_by(data, 'chirality')

    If you want to order using a key within a key, for instance order by
    molecular weight stored in the *molecular_properties* key, use the double
    underscore method as follows::

        c = ChEMBL()
        data = c.get_drug(limit=100)
        ordered_data = c.order_by(data, 'molecular_properties__mw_freebase')

    For filtering, it is possible to apply search filters to any resources.
    For example, it is possible to return all ChEMBL targets that contain
    the term 'kinase' in the pref_name attribute::

        c.get_target(filters='pref_name__contains=kinase")

    The pattern for applying a filter is as follows::

        [field]__[filter_type]=[value]

    where field has to be found by the user. Simply introspect the content of an
    item returned by the resource. For instance::

        c.get_target(limit=1) # to get one entry

    Let us consider the case of the **molecule** resource. You can
    retrieve the first 10 molecules using e.g.::

        res = c.get_molecule(limit=10)

    If you look at the first entry using res[0], you will get about
    38 keys. For instance **molecule_properties** or
    **molecule_chembl_id**.

    You can filter the molecules to keep only the molecule_chembl_id
    that match either CHEMBL25 or CHEMBL1000 using::

        res = c.get_molecule(filters='molecule_chembl_id__in=CHEMBL25,CHEMBL1000')

    For **molecule_properties**, this is actually a dictionary. For instance,
    inside the **molecule_properties** field, you have the molecular weight
    (mw_freebase). So to apply this filter, you need to use the following code
    (to keep molecules with molecular weight greater than 300::

        res = c.get_molecule(filters='molecule_properties__mw_freebase__gte=300')

    Here are the different types of filtering:

    =============== =============================================
    Filter Type     Description
    =============== =============================================
    exact (iexact)  Exact match with query
    contains        wild card search with query
    startswith      starts with query
    endswith        ends with query
    regex           regulqr expression query
    gt (gte)        Greater than (or equal)
    lt (lte)        Less than (or equal)
    range           Within a range of values
    in              Appears within list of query values
    isnull          Field is null
    search          Special type of filter allowing a full text
                    search based on Solr queries.
    =============== =============================================

    Several filters can be applied at the same time using a list::

        filters = ['molecule_properties__mw_freebase__gte=300']
        filters += ['molecule_properties__alogp__gte=3']
        res = c.get_molecule(filters)

    **Use Cases: (inspired from ChEMBL documentation)**

    Search molecules by synonym::

        >>> from bioservices import ChEMBL
        >>> c = ChEMBL()
        >>> res = c.search_molecule('aspirin')

    or SMILE, or InChiKey, or CHEMBLID::

        >>> res = c.get_molecule("CC(=O)Oc1ccccc1C(=O)O")
        >>> res = c.get_molecule("BSYNRYMUTXBXSQ-UHFFFAOYSA-N")
        >>> res = c.get_molecule('CHEMBL25')

    Several molecules at the same time can also be retrieved using lists::

        >>> res = c.get_molecule(['CHEMBL25', 'CHEMBL2'])



    Search target by gene name::

        >>> res = c.search_target("GABRB2")
        >>> len(res['targets'])
        18

    or directly in the target synonym field::

        >>> res = c.get_target(filters='target_synonym__icontains=GABRB2')

    .. note:: Not sure what is the difference between icontains vs contains.
        It looks like icontains is more permissive (you get more entries
        with icontains).

    Having a list of molecules ChEMBL IDs in a list, get uniprot accession
    numbers that map to those compounds::

        # First, get some IDs of approved drugs (about 2000 molecules)
        c = ChEMBL()
        drugs = c.get_approved_drugs()
        IDs = [x['molecule_chembl_id'] for x in drugs]

        # we jump from compounds to targets through activities
        # Here this is a one to many mapping so we initialise a default
        # dictionary.
        compound2target = defaultdict(set)

        filter = "molecule_chembl_id__in={}"
        for i in range(0, len(IDs), 50):
            activities = c.get_activity(filter.format(IDs[i:i+50]))
            # get target ChEMBL IDs from activities
            for act in activities:
                compound2target[act['molecule_chembl_id']].add(act['target_chembl_id'])

        # What we need is to get targets for all targets found in the previous
        # step. For each compound/drug there are hundreds of targets though. And
        # we will call the get_target for each list of hundreds targets. This
        # will take forever. Instead, because there are *only* 12,000 targets,
        # let us download all of them ! This took about 4 minutes on this test but
        # if you use the cache, next time it will be much much quicker. This is
        # not down at the activities level because there are too many entries

        targets = c.get_target(limit=-1)

        # identifies all target chembl id to easily retrieve the entry later on
        target_names = [target['target_chembl_id'] for target in targets]

        # retrieve all uniprot accessions for all targets of each compound
        for compound, targs in compounds2targets.items():
            accessions = set()
            for target in targs:
                index = target_names.index(target)
                accessions = accessions.union([comp['accession']
                    for comp in targets[index]['target_components']])
            compounds2targets[compound] = accessions

    In version 1.6.0 of bioservices, you can simply use::

        res = c.compounds2targets(IDs)


    Get Target type count for all targets::

        import collections
        collections.Counter([x['target_type'] for x in targets]


    Find compounds similar to given SMILES query with similarity threshold of
    85%::

        >>> SMILE = "CN(CCCN)c1cccc2ccccc12"
        >>> c.get_similarity(SMILE, similarity=70)

    Find compounds similar to aspirin (CHEMBL25) with similarity
    threshold of 70%::

        # search for aspirin in all molecules and from first hist
        # get the ChEMBL ID
        >>> molecules = c.search_molecule("aspirin")['molecules']
        >>> chembl_id = molecules[0]['molecule_chembl_id']
        # now use the :meth:`get_similarity` given the ID
        >>> res = c.get_similarity(chembl_id, similarity=70)

    Perform substructure search using SMILES or ChEMBID::

        >>> res = c.get_substructure("CN(CCCN)c1cccc2ccccc12")
        >>> res = c.get_substructure("CHEMBL25")


    Obtain he pChEMBL value for compound::

        res = c.get_activity(filters=['pchembl_value__isnull=False',
                                      'molecule_chembl_id=CHEMBL25'])


    Obtain he pChEMBL value for compound and target::

        res = c.get_activity(filters=['pchembl_value__isnull=False',
                                      'molecule_chembl_id=CHEMBL25',
                                      'target_chembl_id=CHEMBL612545'])

    Get all approved drugs::

        c.get_approved_drugs(max_phase=4)

    Get approved drugs for lung cancer


    The ChEMBL API significantly changed in 2018 and the nez version of
    bioservices (1.6.0) had to change the API as well, which has been
    simplified.

    Here below are some correspondances between the previous and the new API.

    ========================================== ==========================
    bioservices before 1.6.0                   After 1.6.0
    ========================================== ==========================
    get_compounds_substructure                 get_substructure
    get_compounds_similar_to_SMILES            get_similarity(SMILE)
    get_compounds_by_chemblId(ID)              get_similarity(ID)
    get_individual_compounds_by_inChiKey       get_molecule(inchikey)
    get_compounds_by_chemblId_form             get_molecule_form
    get_compounds_by_chemblId_drug_mechanism   get_mechanism(ID)
    get_target_by_chemblId(ID)                 get_target(ID)
    get_image_of_compounds_by_chemblId         get_image
    etc
    ========================================== ==========================

    :references:
        - https://arxiv.org/pdf/1607.00378.pdf
        - https://www.ebi.ac.uk/chembl/api/data/docs
    """

    _url = "https://www.ebi.ac.uk/chembl/api/data"

    def __init__(self, verbose=False, cache=False):
        super(ChEMBL, self).__init__(url=ChEMBL._url, name="ChEMBL", verbose=verbose, cache=cache)
        self.format = "json"

    def _get_data(self, name, params):

        # keep the number of events we want and original offset
        max_data = params["limit"]
        offset = params["offset"]

        # I noticed that
        # if offset + limit > total_count, then limit is set to 1000 - offset
        # Not sure whether it is a bug or intended behaviour but this caused
        # some issues during the debugging.

        # So http_get("mechanism?format=json&limit=10000&offset=10")
        # returns 990 entries and not 1000 as expected.

        # if a resources is small (e.g. tissue has 655 < 1000 entries) there is
        # no such issues.

        # So, the best is to constraint limit to 1000
        params["limit"] = 1000  # for the first call

        # The limit used in all other calls
        limit = 1000

        res = self.http_get("{}".format(name), params=params)
        self._check_request(res)

        # get rid of page_meta key/value
        self.page_meta = res["page_meta"]
        keys = list(res.keys())
        keys.remove("page_meta")
        names = keys[0]  # the parameter name in plural form

        # keep first chunk of data
        data = res[names]

        if max_data == -1:
            max_data = res["page_meta"]["total_count"]
        elif max_data > res["page_meta"]["total_count"]:
            max_data = res["page_meta"]["total_count"]

        N = max_data
        from easydev import Progress

        pb = Progress(N)
        count = 1

        while res["page_meta"]["next"] and len(data) < max_data:
            params["limit"] = limit
            params["offset"] = limit * count + offset
            res = self.http_get("{}".format(name), params=params)
            data += res[names]
            count += 1
            pb.animate(len(data))
            self.page_meta = res["page_meta"]

        if self.page_meta["next"]:
            offset = self.page_meta["offset"]
            total = self.page_meta["total_count"] - len(data) - int(offset)
            self.logging.warning(
                "More data available ({}). rerun with higher"
                "limit and/or offset {}. Check content of page_meta"
                " attribute".format(total, offset)
            )

        if len(data) > max_data:
            return data[0:max_data]
        else:
            return data

    def _check_request(self, res):
        # If there is no output because of wrong query, a 404 is returned.
        if isinstance(res, int):
            raise ValueError("Invalid request for {} {}. Check your query and parameters")

    def _get_this_service(self, name, query, params={"limit": 20, "offset": 0}):
        """


        if query is None, calls the resources

            URL/data/[resource]

        if query is a string, calls

            URL/data/[resource]/ID

        if query is a list of IDS, calls

            URL/data/[resource]/set/[IDS]

        In case 1 and 3, returns a dictionary and populate attribute page_meta.
        In case 2, there is only one requested ID so returns a dictionary (not a
        list of dictionaries).

        """

        # look at any filters provided by the user
        if params["filters"] is None:
            del params["filters"]
        elif isinstance(params["filters"], list):
            for filter in params["filters"]:
                assert filter.count("=") == 1
                key, value = filter.split("=")
                params[key] = value
            del params["filters"]
        else:
            assert params["filters"].count("=") == 1
            k, v = params["filters"].split("=")
            del params["filters"]
            params[k] = v

        params["format"] = self.format
        # Here, we will switch between several ways of using each
        # service.
        if query is None:
            res = self._get_data(name, params)
        # user may use integer, floats or strings.
        elif isinstance(query, (str, int, float)):
            res = self.http_get("{}/{}".format(name, query), params=params)
            self._check_request(res)
        elif isinstance(query, list):
            assert params["limit"] <= 1000, "limit must be less than 1000"
            ids = ";".join([str(x) for x in query])
            res = self.http_get("{}/set/{}".format(name, ids), params=params)
            self._check_request(res)
            # Note that there is no page_meta key in the returned object but a
            # single key that is the plural for of the resource except if some
            # entries are not found. In such case, a
            if "not_found" in res.keys():
                self.logging.warning("Some entries were not found: {}".format(res["not_found"]))
                self.not_found = res["not_found"]
                del res["not_found"]
            names = list(res.keys())[0]
            res = res[names]

        return res

    def _search(self, name, query, params):
        # Check the validity of limits
        assert params["limit"] > 0, "limits must be less than 1000"
        assert params["limit"] <= 1000, "limits must be positive"
        res = self.http_get("{}/search.{}?q={}".format(name, self.format, query), params=params)

        if isinstance(res, int):
            self.logging.warning("Invalid request for {} {}. Check your parameters".format(name, params))
            return {}

        if "page_meta" in res and res["page_meta"]["next"]:
            Next = res["page_meta"]["next"]
            offset = Next.split("&offset=")[1]
            self.logging.warning("More data available with offset {}".format(offset))
        return res

    def search_activity(self, query, limit=20, offset=0):
        """Activity values recorded in an Assay"""
        params = {"limit": limit, "offset": offset}
        return self._search("activity", query, params=params)

    def get_activity(self, query=None, limit=20, offset=0, filters=None):
        """Activity values recorded in an Assay"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("activity", query, params=params)

    def search_assay(self, query, limit=20, offset=0):
        """Assay details as reported in source document"""
        params = {"limit": limit, "offset": offset}
        return self._search("assay", query, params=params)

    def get_assay(self, query=None, limit=20, offset=0, filters=None):
        """Assay details as reported in source Document/Dataset


        >>> c.get_assay("CHEMBL1217643")

        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("assay", query, params=params)

    def get_ATC(self, limit=20, offset=0, filters=None):
        """WHO ATC Classification for drugs

        c.get_atc()
        c['atc']

        .. note:: get_molecule returns 'molecules' and likewise
            all methods return a dictionary whose key is the plural
            of the method name. This is quite consistent through the
            API except for that one because it is an acronym

        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("atc_class", query, params=params)

    def get_binding_site(self, limit=20, offset=0, filters=None):
        """Target binding site definition"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("binding_site", query, params=params)

    def get_biotherapeutic(self, limit=20, offset=0, filters=None):
        """Biotherapeutic molecules, which includes HELM notation and sequence data"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("biotherapeutic", query, params=params)

    def get_cell_line(self, limit=20, offset=0, filters=None):
        """Cell line information"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("cell_line", query, params=params)

    def search_chembl_id_lookup(self, query, limit=20, offset=0):
        """Look up ChEMBL Id entity type"""
        params = {"limit": limit, "offset": offset}
        return self._search("chembl_id_lookup", query, params=params)

    def get_chembl_id_lookup(self, query=None, limit=20, offset=0, filters=None):
        """Look up ChEMBL Id entity type"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("chembl_id_lookup", query, params=params)

    def get_compound_record(self, query=None, limit=20, offset=0, filters=None):
        """Occurence of a given compound in a spcecific document"""
        params = {"limit": limit, "offset": offset, "filters": filters}

        return self._get_this_service("compound_record", query, params=params)

    def get_compound_structural_alert(self, query=None, limit=20, offset=0, filters=None):
        """Indicates certain anomaly in compound structure"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("compound_structural_alert", query, params=params)

    def search_document(self, query, limit=20, offset=0):
        """Document/Dataset from which Assays have been extracted"""
        params = {"limit": limit, "offset": offset}
        return self._search("document", query, params=params)

    def get_document(self, query=None, limit=20, offset=0, filters=None):
        """Document/Dataset from which Assays have been extracted"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("document", query, params=params)

    def get_document_similarity(self, query=None, limit=20, offset=0, filters=None):
        """Provides documents similar to a given one"""

        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("document_similarity", query, params=params)

    def get_document_term(self, query=None, limit=20, offset=0, filters=None):
        """Provides keywords extracted from a document using the TextRank algorithm"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("document_term", query, params=params)

    def get_approved_drugs(self, max_phase=4, maxdrugs=1000000):
        """Return all approved drugs

        :param  max_phase: 4 by default for approved drugs.

        """
        filters = "development_phase__exact={}".format(max_phase)
        data = self.get_drug(filters=filters, limit=maxdrugs)
        return data

    def get_drug(self, query=None, limit=20, offset=0, filters=None):
        """Approved drugs information, icluding (but not limited to) applicants, patent numbers and research codes"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("drug", query, params=params)

    def get_drug_indication(self, query=None, limit=20, offset=0, filters=None):
        """Joins drugs with diseases providing references to relevant sources"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("drug_indication", query, params=params)

    def get_go_slim(self, query=None, limit=20, offset=0, filters=None):
        """GO slim ontology"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("go_slim", query, params=params)

    def get_mechanism(self, query=None, limit=20, offset=0, filters=None):
        """Mechanism of action information for FDA-approved drugs"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("mechanism", query, params=params)

    def get_metabolism(self, query=None, limit=20, offset=0, filters=None):
        """Metabolic pathways with references"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("metabolism", query, params=params)

    def search_molecule(self, query, limit=20, offset=0):
        params = {"limit": limit, "offset": offset}
        return self._search("molecule", query, params=params)

    def get_molecule(self, query=None, limit=20, offset=0, filters=None):
        """Returns some molecules

        :param limit: number of molecules to retrieve
        :param offset: molecules to ignore before retrieving molecules.
        :return: a dictionary with keys *page_meta* and *molecules*.

        There are 1,800,000 molecules (Jan 2019). You can only retrieve
        1,000 molecule at most using the *limit* parameter. With a loop
        you can retrieve molecules in some range.

        ::

            c.get_molecule('QFFGVLORLPOAEC-SNVBAGLBSA-N')
            c.get_molecule("CC(=O)Oc1ccccc1C(=O)O")


        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("molecule", query, params=params)

    def get_molecule_form(self, query=None, limit=20, offset=0, filters=None):
        """Relationships between molecule parents and salts


        >>> s.get_molecule_form("CHEMBL2")['molecule_forms']
        [{'is_parent': 'True',
          'molecule_chembl_id': 'CHEMBL2',
          'parent_chembl_id': 'CHEMBL2'},
         {'is_parent': 'False',
          'molecule_chembl_id': 'CHEMBL1558',
          'parent_chembl_id': 'CHEMBL2'},
         {'is_parent': 'False',
          'molecule_chembl_id': 'CHEMBL1347191',
          'parent_chembl_id': 'CHEMBL2'}]
        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("molecule_form", query, params=params)

    def get_organism(self, query=None, limit=20, offset=0, filters=None):
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("organism", query, params=params)

    def search_protein_class(self, query, limit=20, offset=0):
        params = {"limit": limit, "offset": offset}
        return self._search("protein_class", query, params=params)

    def get_protein_class(self, query=None, limit=20, offset=0, filters=None):
        """Protein family classification of TargetComponents"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("protein_class", query, params=params)

    def get_substructure(self, structure, limit=20, offset=0, filters=None):
        """Molecule substructure search


        :param structure: provide a valid / existing substructure in
            SMILE format to look for in all molecules:
        :return: list of molecules corresponding to the search

        ::

            >>> from bioservices import ChEMBL
            >>> c = ChEMBL()
            >>> res = c.get_substructure("CC(=O)Oc1ccccc1C(=O)O")

        Other examples::

            # Substructure search for against ChEMBL using aspirin
            # SMILES string
            c.get_substructure("CC(=O)Oc1ccccc1C(=O)O")

            # Substructure search for against ChEMBL using aspirin
            # CHEMBL_ID
            c.get_substructure("CHEMBL25")

            # Substructure search for against ChEMBL using aspirin
            # InChIKey
            c.get_substructure("BSYNRYMUTXBXSQ-UHFFFAOYSA-N")


        The 'Substructure' and 'Similarity' web service resources allow
        for the chemical content of ChEMBL to be searched. Similar to the
        other resources, these search based resources except filtering, paging
        and ordering arguments. These methods accept SMILES, InChI Key and
        molecule ChEMBL_ID as arguments and in the case of similarity searches
        an additional identity cut-off is needed. Some example molecule searches
        are provided in the table below.

        Searching with InChI key is only possible for InChI keys found in the
        ChEMBL database. The system does not try and convert InChI key to a
        chemical representation.

        """
        # we use quote to formqt the SMILE/InChiKey for a URL parsing
        structure = quote(structure)
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("substructure/{}".format(structure), query, params=params)

    def get_similarity(self, structure, similarity=80, limit=20, offset=0, filters=None):
        """Molecule similarity search

        :param structure: provide a valid / existing substructure in
            SMILE format to look for in all molecules:
        :param similarity: must be an integer greater than 70 and
            less than 100
        :return: list of **molecules** corresponding to the search

        ::

            >>> from bioservices import ChEMBL
            >>> c = ChEMBL()
            >>> res = c.get_similarity("CC(=O)Oc1ccccc1C(=O)O", 80)
            >>> res['molecules']


        Here are more examples::

            # Similarity (80% cut off) search for against ChEMBL using
            # aspirin SMILES string
            c.get_similarity("CC(=O)Oc1ccccc1C(=O)O") # 80 by default

            # Similarity (80% cut off) search for against ChEMBL using
            # aspirin CHEMBL_ID
            c.get_similarity("CHEMBL25")

            # Similarity (80% cut off) search for against ChEMBL
            # using aspirin InChI Key
            c.get_similarity("BSYNRYMUTXBXSQ-UHFFFAOYSA-N")

        The 'Substructure' and 'Similarity' web service resources allow for the
        chemical content of ChEMBL to be searched. Similar to the other resources, these
        search based resources except filtering, paging and ordering arguments. These
        methods accept SMILES, InChI Key and molecule ChEMBL_ID as arguments and in the
        case of similarity searches an additional identity cut-off is needed. Some
        example molecule searches are provided in the table below.

        Searching with InChI key is only possible for InChI keys found in the
        ChEMBL database. The system does not try and convert InChI key to a chemical
        representation.
        """
        # we use quote to formqt the SMILE/InChiKey for a URL parsing
        structure = quote(structure)

        assert isinstance(similarity, int)
        assert similarity >= 70 and similarity <= 100, "similarity must be in the range [70, 100]"
        params = {"limit": limit, "offset": offset, "filters": filters}
        query = None
        return self._get_this_service("similarity/{}/{}".format(structure, similarity), query, params=params)

    def get_source(self, query=None, limit=20, offset=0, filters=None):
        """Document/Dataset source"""
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("source", query, params=params)

    def search_target(self, query, limit=20, offset=0):
        """Targets (protein and non-protein) defined in Assay"""
        params = {"limit": limit, "offset": offset}
        return self._search("target", query, params=params)

    def get_target(self, query=None, limit=20, offset=0, filters=None):
        """Targets (protein and non-protein) defined in Assay


        >>> from bioservices import *
        >>> s = ChEMBL(verbose=False)
        >>> resjson = s.get_targetd('CHEMBL240')

        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("target", query, params=params)

    def get_target_component(self, query=None, limit=20, offset=0, filters=None):
        """Target sequence information (A Target may have 1 or more sequences)

        ::

            res = c.get_target_component(1)
            res['sequence']

        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("target_component", query, params=params)

    def get_target_prediction(self, query=None, limit=20, offset=0, filters=None):
        """Predictied binding of a molecule to a given biological target


        ::

                >>> res = c.get_target_prediction(1)
                >>> res['molecule_chembl_id']
                'CHEMBL2'
        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("target_prediction", query, params=params)

    def get_target_relation(self, query=None, limit=20, offset=0, filters=None):
        """Describes relations between targets


        ::

            >>> c.get_target_relation('CHEMBL261')
            {'related_target_chembl_id': 'CHEMBL2095180',
             'relationship': 'SUBSET OF',
             'target_chembl_id': 'CHEMBL261'}


        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("target_relation", query, params=params)

    def get_tissue(self, query=None, limit=20, offset=0, filters=None):
        """Tissue classification


        c.get_tissue(filters=['pref_name__contains=cervix'])

        """
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("tissue", query, params=params)

    def get_xref_source(self, query=None, limit=20, offset=0, filters=None):
        params = {"limit": limit, "offset": offset, "filters": filters}
        return self._get_this_service("xref_source", query, params=params)

    def get_image(self, query, dimensions=500, format="png", save=True, view=True, engine="indigo"):
        """Get the image of a given compound in PNG png format.

        :param str query: a valid compound ChEMBLId or a list/tuple
            of valid compound ChEMBLIds.
        :param format: png, svg. json not supported
        :param int dimensions: size of image in pixels.
            An integer z (:math:`1 \leq z \leq 500`)
        :param save:
        :param view:
        :param engine: Defaults to rdkit. can be rdkit or indigo
        :param bool view: show the image if set to True.
        :return: the path (list of paths) used to save the figure (figures) (different from Chembl API)

        .. plot::
            :include-source:
            :width: 50%

            >>> from pylab import imread, imshow
            >>> from bioservices import *
            >>> s = ChEMBL(verbose=False)
            >>> res = s.get_image(31863)
            >>> imshow(imread(res['filenames'][0]))

        .. todo:: ignorecoords option
        """
        # NOTE: not async requests here.
        self.devtools.check_range(dimensions, 1, 500)
        self.devtools.check_param_in_list(engine, ["rdkit", "indigo"])
        self.devtools.check_param_in_list(format, ["png", "svg"])
        queries = self.devtools.to_list(query)

        res = {"filenames": [], "images": [], "chemblids": []}
        for query in queries:
            req = "image/{}".format(query)
            params = {"engine": engine, "format": format, "dimensions": dimensions}
            target_data = self.http_get(req, frmt=None, params=params)

            file_out = os.getcwd()
            if format == "png":
                file_out += "/%s.png" % query
                with open(file_out, "wb") as thisfile:
                    thisfile.write(bytes(target_data))
            elif format == "svg":
                file_out += "/%s.svg" % query
                with open(file_out, "w") as thisfile:
                    thisfile.write(target_data)
            self.logging.info("saved to %s" % file_out)

            fout = file_out
            res["chemblids"].append(query)
            res["filenames"].append(fout)
            res["images"].append(target_data)
        if view:
            webbrowser.open(res["filenames"][0])
        return res

    def get_status(self):
        """Return version of the DB and number of entries

        Returns the number of entries for activities, compound_records,
        distinct_compounds (molecule), publications (document), targets,
        etc...

        .. seealso:: :meth:`get_status_resources`
        """
        return self.http_get("status?format=json")

    def get_status_resources(self):
        """Return number of entries for all resources

        .. note:: not in the ChEMBL API.

        .. versionchanged:: 1.7.3 (removed target_prediction and document_term)
        """

        def _local_get(this):
            params = {"limit": 1, "offset": 0}
            return self.http_get("{}?format=json".format(this), params=params)["page_meta"]["total_count"]

        data = {}
        for this in [
            "activity",
            "assay",
            "atc_class",
            "cell_line",
            "binding_site",
            "biotherapeutic",
            "chembl_id_lookup",
            "compound_record",
            "compound_structural_alert",
            "document",
            "document_similarity",
            "drug",
            "drug_indication",
            "go_slim",
            "mechanism",
            "metabolism",
            "molecule",
            "molecule_form",
            "protein_class",
            "source",
            "target",
            "target_component",
            "target_relation",
            "tissue",
        ]:
            self.logging.info("Looking at {}".format(this))
            try:
                data[this] = _local_get(this)
            except:
                self.logging.warning("{} resources seems down".format(this))
        return data

    def order_by(self, data, name, ascending=True):
        """Ordering data

        we use same API as ChEMBL API using the double underscore
        to indicate a hierarchy in the dictionary. So to access to
        d['a']['b'], we use a__b as the input **name** parameter.
        We only allows 3 levels e.g., a__b__c

        ::


            data = c.get_molecules()
            data1 = c.order_by(data, 'molecule_chembl_id')
            data2 = c.order_by(data, 'molecule_properties__alogp')

        .. note:: the ChEMBL API allows for ordering but we do not use
            that API. Instead, we provide this generic function.
        """

        # FIXME sorry no time for a better solution
        # we allow only 3 levels using 3 if
        if name.count("__") == 0:
            data = sorted(data, key=lambda k: k[name], reverse=not ascending)
        elif name.count("__") == 1:
            n1, n2 = name.split("__")
            data = sorted(data, key=lambda k: k[n1][n2], reverse=not ascending)
        elif name.count("__") == 2:
            n1, n2, n3 = name.split("__")
            data = sorted(data, key=lambda k: k[n1][n2][n3], reverse=not ascending)
        else:
            raise NotImplementedError(
                """Please submit a issue on https://github.com/cokelaer/bioservices to allow this level or ordering together will your code example."""
            )
        return data

    def compounds2accession(self, compounds):
        """For each compound, identifies the target and corresponding UniProt
        accession number

        This is not part of ChEMBL API

        ::

            # we recommend to use cache if you use this method regularly
            c = Chembl(cache=True)
            drugs = c.get_approved_drugs()

            # to speed up example
            drugs = drugs[0:20]
            IDs = [x['molecule_chembl_id] for x in drugs]

            c.compounds2accession(IDs)

        """
        # we jump from compounds to targets through activities
        # Here this is a one to many mapping so we initialise a default
        # dictionary.
        from collections import defaultdict

        compound2target = defaultdict(set)

        filter = "molecule_chembl_id__in={}"
        from easydev import Progress

        if isinstance(compounds, list):
            pass
        else:
            compounds = list(compounds)

        pb = Progress(len(compounds))
        for i in range(0, len(compounds)):
            # FIXME could get activities by bunch using
            # ",".join(compounds[i:i+10) for example
            activities = self.get_activity(filters=filter.format(compounds[i]))
            # get target ChEMBL IDs from activities
            for act in activities:
                compound2target[act["molecule_chembl_id"]].add(act["target_chembl_id"])
            pb.animate(i + 1)

        # What we need is to get targets for all targets found in the previous
        # step. For each compound/drug there are hundreds of targets though. And
        # we will call the get_target for each list of hundreds targets. This
        # will take forever. Instead, because there are *only* 12,000 targets,
        # let us download all of them ! This took about 4 minutes on this test but
        # if you use the cache, next time it will be much much quicker. This is
        # not down at the activities level because there are too many entries
        targets = self.get_target(limit=-1)

        # identifies all target chembl id to easily retrieve the entry later on
        target_names = [target["target_chembl_id"] for target in targets]

        # retrieve all uniprot accessions for all targets of each compound
        for compound, targs in compound2target.items():
            accessions = set()
            for target in targs:
                index = target_names.index(target)
                accessions = accessions.union([comp["accession"] for comp in targets[index]["target_components"]])
            compound2target[compound] = accessions

        return compound2target
