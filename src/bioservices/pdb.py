#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2020 - EBI-EMBL - Institut Pasteur
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
# $Id$
"""Interface to the PDB web Service (New API Jan 2021).

.. topic:: What is PDB ?

    :URL: http://www.rcsb.org/pdb/
    :REST: http://search.rcsb.org/#search-api

    .. highlights::

        An Information Portal to Biological Macromolecular Structures

        -- PDB home page, Jan 2021


"""
from bioservices.services import REST


__all__ = ["PDB"]


class PDB:
    """Interface to `PDB <http://search.rcsb.org/>`_ service (new API Jan 2021)

    With the new API, one method called :meth:`~bioservices.pdb.PDB.search` is
    provided by PDB. To perform a search you need to define a query. Here is an
    example

    .. doctest::

        >>> from bioservices import PDB
        >>> s = PDB()
        >>> query = {"query":
        ...              {"type": "terminal",
        ...               "service": "text",
        ...               "parameters": {
        ...                 "value": "thymidine kinase"
        ...                 }
        ...             },
        ...          "return_type": "entry"}
        >>> res = s.search(query, return_type=return_type)


    .. note:: as of December 2020, a new API has be set up by PDB.
        some prevous functionalities such as return list of Ligand are not
        supported anymore (Jan 2021). However, many more powerful searches as
        available. I encourage everyone to look at the PDB page for complex
        examples: http://search.rcsb.org/#examples

    As mentionnaed above, the PDB service provide one method called search available in
    :meth:`~bioservices.pdb.PDB.search`. We will not cover all the power and
    capability of this search function. User should refer to the official PDB help
    for that. Yet, given examples from PDB should all work with this method.

    When possible, we will add convenient aliases function in this class. For
    now we have for example the :meth:`~bioservices.pdb.PDB.get_current_ids` and
    :meth:`~bioservices.pdb.PDB.get_similarity_sequence` that users may find useful.

    The main idea behind the PDB API is to create queries that can access to
    different type of services. A query will need to at least two keys:

    - **query**
    - **return_type**

    Consider this basic example that searches for the text *thymidine kinase*::

        {
          "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
              "value": "thymidine kinase"
            }
          },
          "return_type": "entry"
        }

    Here the query is defined by a **query** and a **return_type** indeed. The
    return type is a simple value such as **entry**. The query itself is
    composed of 3 pairs of key/value. Here we have the type service and
    parameters as defined below.

    The query can have several fields:

    - **type**: the clause type can be either **terminal** or **group**

        - **terminal**: performs an atomic search operation, e.g. searches
          for a particular value in a particular field.
        - **group**: wraps other terminal or group nodes and is
          used to combine multiple queries in a logical fashion.

    - **service**:

        - **text**: linguistic searches against textual annotations.
        - **sequence**: uses MMSeq2 to perform sequence matching searches (blast-like).
          following targets that are available:

          - pdb_protein_sequence,
          - pdb_dna_sequence,
          - pdb_na_sequence
        - **seqmotif**: performs short motif searches against nucleotide or protein
          sequences using 3 different inputs:

          - simple (e.g., CXCXXL)
          - prosite (e.g., C-X-C-X(2)-[LIVMYFWC])
          - regex (e.g., CXCX{2}[LIVMYFWC])
        - **structure**: searches matching a global 3D shape of assemblies
          or chains of a given entry (identified by PDB ID), in either strict
          (strict_shape_match) or relaxed (relaxed_shape_match) modes
        - strucmotif: Performs structural motif searches on all available PDB structures.
        - chemical: queries of small-molecule constituents of PDB structures,
          based on chemical formula and chemical structure. Queries for matching and similar
          chemical structures can be performed using SMILES and InChI descriptors
          as search targets.

          - graph-strict: atom type, formal charge, bond order, atom and bond chirality,
            aromatic assignment are used as matching criteria for this search type.
          - graph-relaxed: atom type, formal charge and bond order are used as
            matching criteria for this search type.
          - graph-relaxed-stereo: atom type, formal charge, bond order, atom
            and bond chirality are used as matching criteria for this search
            type.
          - fingerprint-similarity: Tanimoto similarity is used as the matching criteria

    Concerning the **return_type** key, it can be one of :

    - entry: a list of PDB IDs.
    - assembly: list of PDB IDs appended with assembly IDs in the format of
      a [pdb_id]-[assembly_id], corresponding to biological assemblies.
    - polymer_entity: list of PDB IDs appended with entity IDs in the format
      of a [pdb_id]_[entity_id], corresponding to polymeric molecular entities.
    - non_polymer_entity: list of PDB IDs appended with entity IDs in the
      format of a [pdb_id]_[entity_id], corresponding to non-polymeric entities (or ligands).
    - polymer_instance: list of PDB IDs appended with asym IDs in the format
      of a [pdb_id].[asym_id], corresponding to instances of certain polymeric
      molecular entities, also known as chains.

    **Optional arguments**

    There are many optional arguments. Let us see a couple of them. Pagination can be
    set (default is 10 entries) using the **request_options** (optional) key.
    Consider this query example::

        {
          "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_polymer_entity.formula_weight",
                "operator": "greater",
                "value": 500
            }
          },
          "request_options": {
            "pager": {
              "start": 0,
              "rows": 100
            }
          },
          "return_type": "polymer_entity"
        }

    Here, the query searches for the polymer_entity that have a formula weight
    above 500. Withe request_options pager set to 100, we will get the first 100
    hits.

    To return all hits, set this field in the request_options::

        "return_all_hits": true

    Coming back at the first basic example, we can reuse it to illustrate how to
    refine the search using attribute and operators::

        {
          "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
              "value": "thymidine kinase",
              "attribute": "exptl.method",
              "operator": "exact_match",
            }
          },
          "return_type": "entry"
        }

    All valid combo of operators and attributes can be found
    here: http://search.rcsb.org/search-attributes.html

    For instance, in the example above only in, exact_match and exists can be
    used with exptl.method attribute. This is not checked in bioservices.

    Sorting is determined by the sort object in the request_options context.
    It allows you to add one or more sorting conditions to control the order of
    the search result hits. The sort operation is defined on a per field level, with
    special field name for score to sort by score (the default)<

    By default sorting is done in descending order ("desc"). The sort can be
    reversed by setting direction property to "asc". This example demonstrates how
    to sort the search results by release date::

        {
          "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
              "attribute": "struct.title",
              "operator": "contains_phrase",
              "value": "\"hiv protease\""
            }
          },
          "request_options": {
            "sort": [
              {
                "sort_by": "rcsb_accession_info.initial_release_date",
                "direction": "desc"
              }
            ]
          },
          "return_type": "entry"
        }

    Again, many more complex examples can be found on PDB page.
    """

    _url = "http://search.rcsb.org/rcsbsearch/v1/"

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages (default is off)

        """
        self.services = REST(name="PDB", verbose=verbose, cache=cache, url_defined_later=True)
        self.services.url = PDB._url

    def search(self, query, request_options=None, request_info=None, return_type=None):
        """search request represented as a JSON object.

        This is the only function in PDB API. You should be able
        to perform any valid PDB searches here (see the
        :class:`bioservices.pdb.PDB` documentation for details.
        Note, however, that we have aliases methods in BioServices that will be
        added on demand for common searches.

        :param str query: the search expression. Can be omitted if, instead of IDs retrieval,
            facets or count operation should be performed. In this case the request must be
            configured via the request_options context.
        :param str request_options: (optional) controls various aspects of the search request
            including pagination, sorting, scoring and faceting.
        :param str request_info: additional information about the query, e.g.
            query_id. (optional)
        :param str return_type: type of results to return.
        :return: json results

        You must define a query as defined in the PDB web page. For example the
        following query search for macromolecular PDB entities that share 90% sequence
        identity with GTPase HRas protein from Gallus gallus (Chicken)::

            query = {
              "query": {
                "type": "terminal",
                "service": "sequence",
                "parameters": {
                  "evalue_cutoff": 1,
                  "identity_cutoff": 0.9,
                  "target": "pdb_protein_sequence",
                  "value": "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHQYREQIKRVKDSDDVPMVLVGNKCDLPARTVETRQAQDLARSYGIPYIETSAKTRQGVEDAFYTLVREIRQHKLRKLNPPDESGPGCMNCKCVIS"
                }
              },
              "request_options": {
                "scoring_strategy": "sequence"
              },
              "return_type": "polymer_entity"
            }

        What is important is that the dictionary called **query** contains 2
        compulsary keys namely **query** and **return_type**. The two other optional
        keys are **request_options** and **return_info**

        You would then call the PDB search as follows::

            from bioservices import PDB
            p = PDB()
            results = p.search(query)

        Now, in BioServices, you can also decompose the query as follows::

            query = {
                "type": "terminal",
                "service": "sequence",
                "parameters": {
                  "evalue_cutoff": 1,
                  "identity_cutoff": 0.9,
                  "target": "pdb_protein_sequence",
                  "value": "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHQYREQIKRVKDSDDVPMVLVGNKCDLPARTVETRQAQDLARSYGIPYIETSAKTRQGVEDAFYTLVREIRQHKLRKLNPPDESGPGCMNCKCVIS"
                }}
            request_options =  { "scoring_strategy": "sequence"}
            return_type= "polymer_entity"

        and then use PDB search again::

            from bioservices import PDB
            p = PDB()
            results = p.search(query, request_options=request_options, return_type=return_type)

        or even simpler for the Pythonic lovers::

            results = p.search(**query)


        """
        if "query" in query:
            pass
        else:
            query = {"query": query}
            if request_options:
                query["request_options"] = request_options
            if request_info:
                query["request_info"] = request_info
            if return_type:
                query["return_type"] = return_type
        if "return_type" not in query:  # pragma: no cover
            raise ValueError("Yourr query must have a return_type key")
        print(query)
        res = self.services.http_post("query", frmt="json", json=query)
        return res

    def get_current_ids(self):
        """Get a list of all current PDB IDs."""

        # first query returns 10 entries by default

        request_options = {"return_all_hits": True}

        # second requests all entries
        res = self.search(
            query={"type": "terminal", "service": "text"},
            request_options=request_options,
            return_type="entry",
        )

        identifiers = [x["identifier"] for x in res["result_set"]]
        return identifiers

    def get_similarity_sequence(self, seq):
        """Search of seauence similarity search with protein sequence

        seq = "VLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTAVAHVDDMPNAL"
        results = p.get_similarity_sequence(seq)

        """
        res = self.search(
            {
                "query": {
                    "type": "terminal",
                    "service": "sequence",
                    "parameters": {"target": "pdb_protein_sequence", "value": seq},
                },
                "return_type": "polymer_entity",
            }
        )
        return res
