#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#      https://github.com/cokelaer/bioservices
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://bioservices.readthedocs.io
#
##############################################################################
"""Interface to the STRING protein interaction database web service.

.. topic:: What is STRING?

    :URL: https://string-db.org
    :REST: https://string-db.org/api

    .. highlights::

        STRING is a database of known and predicted protein-protein interactions.
        The interactions include direct (physical) and indirect (functional)
        associations; they stem from computational prediction, from knowledge
        transfer between organisms, and from interactions aggregated from other
        (primary) databases. STRING covers proteins from thousands of organisms.

        -- string-db.org home page

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
    """Interface to the `STRING <https://string-db.org>`_ database.

    STRING is a database of known and predicted protein-protein interactions.
    It covers both direct (physical) and indirect (functional) associations
    derived from genomic context, high-throughput experiments, co-expression,
    and the literature.

    ::

        >>> from bioservices import STRING
        >>> s = STRING()
        >>> interactions = s.get_interactions("ZAP70", species=9606)
        >>> partners = s.get_interaction_partners("ZAP70", species=9606)

    """

    _url = "https://string-db.org/api"

    def __init__(self, verbose=True, cache=False):
        """**Constructor**

        :param bool verbose: set to False to prevent informative messages
        :param bool cache: set to True to enable caching of requests
        """
        self.services = REST(
            name="STRING",
            url=STRING._url,
            verbose=verbose,
            cache=cache,
            url_defined_later=True,
        )

    def _identifiers_to_str(self, identifiers):
        """Convert a list or string of identifiers to a ``%0d``-separated string.

        The STRING API accepts ``%0d``-separated (URL-encoded newline) identifiers
        in POST request bodies.
        """
        if isinstance(identifiers, (list, tuple)):
            return "%0d".join(identifiers)
        return str(identifiers)

    def get_version(self):
        """Return the current STRING API version information.

        :return: dict with version details.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> ver = s.get_version()
            >>> "string_version" in ver
            True

        """
        res = self.services.http_get("json/version", frmt="json")
        if isinstance(res, list) and len(res) == 1:
            return res[0]
        return res

    def get_string_ids(self, identifiers, species=None, limit=1, echo_query=True, caller_identity=None):
        """Resolve identifiers to STRING identifiers.

        Maps gene/protein names or other identifiers to their STRING IDs.

        :param identifiers: identifier(s) to resolve. Multiple identifiers
            should be separated by ``%0d`` or provided as a list.
        :param int species: NCBI taxonomy ID. For example, 9606 for *Homo sapiens*.
            If ``None``, STRING will search across all species.
        :param int limit: maximum number of results per input identifier.
            Default is 1 (best match).
        :param bool echo_query: if True, include the query identifier in the response.
        :param str caller_identity: optional application name for tracking.

        :return: list of dicts with STRING identifier mappings.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_string_ids("ZAP70", species=9606)
            >>> res[0]["stringId"]
            '9606.ENSP00000379990'

        """
        params = {"identifiers": self._identifiers_to_str(identifiers), "echo_query": 1 if echo_query else 0, "limit": limit}
        if species is not None:
            params["species"] = species
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/get_string_ids", data=params, frmt="json")
        return res

    def get_interactions(self, identifiers, species=None, required_score=None, network_type="functional",
                         add_nodes=0, show_query_node_labels=0, caller_identity=None):
        """Retrieve protein-protein interactions for the given identifiers.

        Returns the STRING interaction network for a set of proteins. Each
        interaction record includes scores for different evidence channels
        (neighbourhood, co-occurrence, co-expression, experimental, database,
        text-mining) as well as a combined interaction score.

        :param identifiers: gene/protein name(s). Use ``%0d`` as separator for
            multiple identifiers, or provide a list.
        :param int species: NCBI taxonomy ID (e.g. 9606 for human). Required
            when identifiers are gene symbols.
        :param int required_score: minimum combined interaction score (0–1000).
            Interactions below this threshold are excluded.
        :param str network_type: either ``"functional"`` (default) or
            ``"physical"``.
        :param int add_nodes: number of additional white-list nodes to add to
            the network.
        :param int show_query_node_labels: set to 1 to display labels for input
            nodes even when they are not directly connected.
        :param str caller_identity: optional application name for tracking.

        :return: list of dicts, each representing one interaction with scores.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_interactions("ZAP70", species=9606)
            >>> len(res) > 0
            True

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "network_type": network_type,
            "add_nodes": add_nodes,
            "show_query_node_labels": show_query_node_labels,
        }
        if species is not None:
            params["species"] = species
        if required_score is not None:
            params["required_score"] = required_score
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/network", data=params, frmt="json")
        return res

    def get_network(self, identifiers, species=None, required_score=None, network_type="functional",
                    add_nodes=0, show_query_node_labels=0, caller_identity=None):
        """Retrieve protein-protein interactions for the given identifiers.

        This is an alias for :meth:`get_interactions`.

        :param identifiers: gene/protein name(s). Use ``%0d`` as separator for
            multiple identifiers, or provide a list.
        :param int species: NCBI taxonomy ID (e.g. 9606 for human).
        :param int required_score: minimum combined interaction score (0–1000).
        :param str network_type: either ``"functional"`` (default) or
            ``"physical"``.
        :param int add_nodes: number of additional white-list nodes to add to
            the network.
        :param int show_query_node_labels: set to 1 to display labels for input
            nodes.
        :param str caller_identity: optional application name for tracking.

        :return: list of dicts, each representing one interaction with scores.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_network(["TP53", "BRCA1"], species=9606)

        """
        return self.get_interactions(
            identifiers,
            species=species,
            required_score=required_score,
            network_type=network_type,
            add_nodes=add_nodes,
            show_query_node_labels=show_query_node_labels,
            caller_identity=caller_identity,
        )

    def get_interaction_partners(self, identifiers, species=None, required_score=None, limit=None,
                                  network_type="functional", caller_identity=None):
        """Retrieve interaction partners for the given proteins.

        Returns proteins that interact with the query proteins. Compared to
        :meth:`get_interactions`, this method returns partners even if they are
        not in the original query set.

        :param identifiers: gene/protein name(s). Separate multiple identifiers
            with ``%0d`` or provide a list.
        :param int species: NCBI taxonomy ID (e.g. 9606 for human).
        :param int required_score: minimum combined interaction score (0–1000).
        :param int limit: maximum number of interaction partners to return per
            input protein.
        :param str network_type: either ``"functional"`` (default) or
            ``"physical"``.
        :param str caller_identity: optional application name for tracking.

        :return: list of dicts, each representing one interaction.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> partners = s.get_interaction_partners("ZAP70", species=9606, limit=5)
            >>> len(partners) > 0
            True

        """
        params = {"identifiers": self._identifiers_to_str(identifiers), "network_type": network_type}
        if species is not None:
            params["species"] = species
        if required_score is not None:
            params["required_score"] = required_score
        if limit is not None:
            params["limit"] = limit
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/interaction_partners", data=params, frmt="json")
        return res

    def get_homology(self, identifiers, species=None, species_b=None, required_score=None,
                      caller_identity=None):
        """Retrieve homology data for a set of proteins.

        Returns homologous protein pairs between the query species and
        ``species_b`` (or within the query species if ``species_b`` is not
        given).

        :param identifiers: gene/protein name(s). Separate multiple identifiers
            with ``%0d`` or provide a list.
        :param int species: NCBI taxonomy ID of the query species.
        :param int species_b: NCBI taxonomy ID of the second species. If
            ``None``, homologs are retrieved within ``species``.
        :param int required_score: minimum combined interaction score (0–1000).
        :param str caller_identity: optional application name for tracking.

        :return: list of dicts describing homology relationships.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_homology("ZAP70", species=9606, species_b=10090)

        """
        params = {"identifiers": self._identifiers_to_str(identifiers)}
        if species is not None:
            params["species"] = species
        if species_b is not None:
            params["species_b"] = species_b
        if required_score is not None:
            params["required_score"] = required_score
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/homology", data=params, frmt="json")
        return res

    def get_enrichment(self, identifiers, species=None, background_string_identifiers=None,
                        caller_identity=None):
        """Perform functional enrichment analysis on a set of proteins.

        Tests whether the input proteins are significantly enriched for
        Gene Ontology (GO) terms, KEGG pathways, Pfam domains, InterPro
        signatures, and other annotation categories.

        :param identifiers: gene/protein name(s). Separate multiple identifiers
            with ``%0d`` or provide a list.
        :param int species: NCBI taxonomy ID (e.g. 9606 for human). Required
            when identifiers are gene symbols.
        :param background_string_identifiers: optional set of proteins to use
            as the statistical background. Defaults to the entire proteome.
        :param str caller_identity: optional application name for tracking.

        :return: list of dicts, each representing an enriched annotation term
            with fields such as ``category``, ``term``, ``description``,
            ``number_of_genes``, ``p_value``, and ``fdr``.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_enrichment("ZAP70,LCK,CD3E,CD3D", species=9606)
            >>> len(res) > 0
            True

        """
        params = {"identifiers": self._identifiers_to_str(identifiers)}
        if species is not None:
            params["species"] = species
        if background_string_identifiers is not None:
            params["background_string_identifiers"] = self._identifiers_to_str(background_string_identifiers)
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/enrichment", data=params, frmt="json")
        return res

    def get_functional_annotation(self, identifiers, species=None, allow_pubmed=0, caller_identity=None):
        """Get functional annotations for a set of proteins.

        Returns GO terms, KEGG pathway membership, and other annotations
        for the queried proteins.

        :param identifiers: gene/protein name(s). Separate multiple identifiers
            with ``%0d`` or provide a list.
        :param int species: NCBI taxonomy ID (e.g. 9606 for human).
        :param int allow_pubmed: include PubMed references (0 or 1, default: 0).
        :param str caller_identity: optional application name for tracking.

        :return: list of functional annotation records.
        :rtype: list

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_functional_annotation("TP53", species=9606)

        """
        params = {
            "identifiers": self._identifiers_to_str(identifiers),
            "allow_pubmed": allow_pubmed,
        }
        if species is not None:
            params["species"] = species
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/functional_annotation", data=params, frmt="json")
        return res

    def get_ppi_enrichment(self, identifiers, species=None, required_score=None,
                            background_string_identifiers=None, caller_identity=None):
        """Test whether the input proteins are enriched in interactions.

        Returns a single record indicating the observed number of interactions,
        expected number, *p*-value, and the average interaction score for the
        input protein set.

        :param identifiers: gene/protein name(s). Separate multiple identifiers
            with ``%0d`` or provide a list.
        :param int species: NCBI taxonomy ID (e.g. 9606 for human).
        :param int required_score: minimum combined interaction score (0–1000).
            If None, uses STRING default.
        :param background_string_identifiers: optional background gene set for
            enrichment calculation.
        :param str caller_identity: optional application name for tracking.

        :return: dict with keys ``number_of_nodes``, ``number_of_edges``,
            ``average_node_degree``, ``local_clustering_coefficient``,
            ``expected_number_of_edges``, and ``p_value``.

        ::

            >>> from bioservices import STRING
            >>> s = STRING()
            >>> res = s.get_ppi_enrichment("ZAP70,LCK,CD3E", species=9606)
            >>> "p_value" in res
            True

        """
        params = {"identifiers": self._identifiers_to_str(identifiers)}
        if species is not None:
            params["species"] = species
        if required_score is not None:
            params["required_score"] = required_score
        if background_string_identifiers is not None:
            params["background_string_identifiers"] = self._identifiers_to_str(background_string_identifiers)
        if caller_identity:
            params["caller_identity"] = caller_identity

        res = self.services.http_post("json/ppi_enrichment", data=params, frmt="json")
        if isinstance(res, list) and len(res) == 1:
            return res[0]
        return res
