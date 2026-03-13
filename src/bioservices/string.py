#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      https://github.com/cokelaer/bioservices
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  source: http://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the STRING protein interaction database web service.

.. topic:: What is STRING?

    :URL: https://string-db.org
    :REST: https://string-db.org/api

    .. highlights::

        STRING is a database of known and predicted protein-protein interactions.
        The interactions include direct (physical) and indirect (functional)
        associations; they are derived from four sources:

        - Genomic Context Predictions
        - High-throughput Lab Experiments
        - (Conserved) Co-Expression
        - Previous Knowledge

        STRING quantitatively integrates interaction data from these sources for a
        large number of organisms, and transfers information between these organisms
        where applicable.

        -- From STRING home page (https://string-db.org/cgi/about)

    The Bioconductor R package ``STRINGdb`` provides a similar interface to the
    STRING database. This module provides an equivalent Python interface.

    :Reference: Szklarczyk D, et al. The STRING database in 2023: protein–protein
        association networks and functional enrichment analyses for any sequenced
        genome of interest. Nucleic Acids Res. 2023;51(D1):D638-D646.
        doi:10.1093/nar/gkac1000

"""

from bioservices import logger
from bioservices.services import REST

logger.name = __name__

__all__ = ["STRING"]


class STRING:
    """Interface to the `STRING <https://string-db.org>`_ protein interaction database.

    STRING is a database of known and predicted protein-protein interactions
    covering over 14,000 organisms. This class provides access to the STRING
    REST API for retrieving protein interaction networks, enrichment analyses,
    and functional annotations.

    The Bioconductor R package ``STRINGdb`` provides an equivalent interface to
    the same database.

    Example usage::

        from bioservices import STRING
        s = STRING()

        # Get interaction network for human TP53
        res = s.get_network("TP53", species=9606)

        # Get functional enrichment for a set of proteins
        res = s.get_enrichment(["TP53", "BRCA1", "BRCA2"], species=9606)

        # Get interaction partners with high confidence score
        res = s.get_interaction_partners("TP53", species=9606, required_score=700)

    """

    _url = "https://string-db.org/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param bool verbose: print informative messages (default False)
        :param bool cache: use caching (default False)
        """
        self.services = REST(name="STRING", url=STRING._url, verbose=verbose, cache=cache)
        self.version = None

    def _identifiers_to_str(self, identifiers):
        """Convert a list or string of identifiers to newline-separated string.

        The STRING API accepts newline-separated identifiers in POST request bodies.
        """
        if isinstance(identifiers, (list, tuple)):
            return "\n".join(identifiers)
        return str(identifiers)

    def get_version(self):
        """Get the current version of the STRING API.

        :return: dict with version information
        :rtype: dict

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> version = s.get_version()

        """
        res = self.services.http_get("json/version", frmt="json")
        if isinstance(res, list) and len(res) > 0:
            self.version = res[0].get("string_version")
        return res

    def get_string_ids(self, identifiers, species=9606, limit=1, echo_query=True, caller_identity=None):
        """Map protein identifiers to STRING database identifiers.

        :param identifiers: protein name(s) to map. Can be a string or list
            of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param int limit: maximum number of STRING identifiers per query protein
            (default: 1)
        :param bool echo_query: include the query identifier in the output
            (default: True)
        :param str caller_identity: optional string to identify the caller
            application (e.g. your website URL or application name)
        :return: list of dicts with STRING identifiers for each input protein
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_string_ids("TP53", species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
            "limit": limit,
            "echo_query": 1 if echo_query else 0,
            "format": "json",
        }
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/get_string_ids", frmt="json", data=params)
        return res

    def get_network(
        self,
        identifiers,
        species=9606,
        required_score=None,
        add_nodes=0,
        network_type="functional",
        show_query_node_labels=0,
        caller_identity=None,
    ):
        """Get protein interaction network data for a set of proteins.

        :param identifiers: protein name(s). Can be a string or list of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param int required_score: minimum required interaction score (0-1000).
            Higher values yield higher-confidence interactions. If None, uses
            STRING default.
        :param int add_nodes: number of additional nodes to add to the network
            (default: 0)
        :param str network_type: type of network to retrieve. Either
            ``"functional"`` (default) or ``"physical"``.
        :param int show_query_node_labels: whether to show labels for query
            nodes (0 or 1, default: 0)
        :param str caller_identity: optional identifier for the caller
        :return: list of interaction records, each containing the interacting
            proteins and their interaction scores
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_network(["TP53", "BRCA1"], species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
            "add_nodes": add_nodes,
            "network_type": network_type,
            "show_query_node_labels": show_query_node_labels,
        }
        if required_score is not None:
            params["required_score"] = required_score
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/network", frmt="json", data=params)
        return res

    def get_interaction_partners(
        self,
        identifiers,
        species=9606,
        required_score=None,
        limit=10,
        network_type="functional",
        caller_identity=None,
    ):
        """Get interaction partners for a set of proteins.

        :param identifiers: protein name(s). Can be a string or list of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param int required_score: minimum required interaction score (0-1000).
            If None, uses STRING default.
        :param int limit: maximum number of interaction partners per query
            protein (default: 10)
        :param str network_type: type of network. Either ``"functional"``
            (default) or ``"physical"``.
        :param str caller_identity: optional identifier for the caller
        :return: list of interaction records with partner proteins and scores
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_interaction_partners("TP53", species=9606, limit=5)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
            "limit": limit,
            "network_type": network_type,
        }
        if required_score is not None:
            params["required_score"] = required_score
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/interaction_partners", frmt="json", data=params)
        return res

    def get_homology(self, identifiers, species=9606, caller_identity=None):
        """Get homology information for a set of proteins.

        :param identifiers: protein name(s). Can be a string or list of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param str caller_identity: optional identifier for the caller
        :return: list of homology records
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_homology("TP53", species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
        }
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/homology", frmt="json", data=params)
        return res

    def get_enrichment(self, identifiers, species=9606, background_identifiers=None, caller_identity=None):
        """Get functional enrichment analysis for a set of proteins.

        Performs over-representation analysis against Gene Ontology (GO),
        KEGG pathways, UniProt keywords, and other annotation databases.

        :param identifiers: protein name(s). Can be a string or list of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param background_identifiers: optional background gene set for
            enrichment calculation. Can be a string or list of strings.
        :param str caller_identity: optional identifier for the caller
        :return: list of enrichment records with category, description, p-value,
            and FDR-corrected p-value
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> proteins = ["TP53", "BRCA1", "BRCA2", "ATM", "CHEK2"]
            >>> res = s.get_enrichment(proteins, species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
        }
        if background_identifiers is not None:
            params["background_string_identifiers"] = self._identifiers_to_str(background_identifiers)
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/enrichment", frmt="json", data=params)
        return res

    def get_functional_annotation(self, identifiers, species=9606, allow_pubmed=0, caller_identity=None):
        """Get functional annotations for a set of proteins.

        Returns GO terms, KEGG pathway membership, and other annotations
        for the queried proteins.

        :param identifiers: protein name(s). Can be a string or list of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param int allow_pubmed: include PubMed references (0 or 1, default: 0)
        :param str caller_identity: optional identifier for the caller
        :return: list of functional annotation records
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_functional_annotation("TP53", species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
            "allow_pubmed": allow_pubmed,
        }
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/functional_annotation", frmt="json", data=params)
        return res

    def get_ppi_enrichment(
        self, identifiers, species=9606, required_score=None, background_identifiers=None, caller_identity=None
    ):
        """Get protein-protein interaction (PPI) enrichment statistics.

        Tests whether the number of interactions among the queried proteins is
        statistically higher than expected for a random set of proteins of the
        same size.

        :param identifiers: protein name(s). Can be a string or list of strings.
        :param int species: NCBI taxon ID (default: 9606 for human)
        :param int required_score: minimum required interaction score (0-1000).
            If None, uses STRING default.
        :param background_identifiers: optional background gene set for
            enrichment calculation. Can be a string or list of strings.
        :param str caller_identity: optional identifier for the caller
        :return: dict with PPI enrichment statistics (observed interactions,
            expected interactions, p-value, etc.)
        :rtype: dict or list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> proteins = ["TP53", "BRCA1", "BRCA2", "ATM", "CHEK2"]
            >>> res = s.get_ppi_enrichment(proteins, species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "species": species,
        }
        if required_score is not None:
            params["required_score"] = required_score
        if background_identifiers is not None:
            params["background_string_identifiers"] = self._identifiers_to_str(background_identifiers)
        if caller_identity:
            params["caller_identity"] = caller_identity
        res = self.services.http_post("json/ppi_enrichment", frmt="json", data=params)
        return res
