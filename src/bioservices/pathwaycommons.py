#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
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
"""This module provides a class :class:`~PathwayCommons`

.. topic:: What is PathwayCommons ?

    :URL: http://www.pathwaycommons.org/about
    :REST:

    .. highlights::

        Pathway Commons is a convenient point of access to biological pathway
        information collected from public pathway databases, which you can
        search, visualize and download. All data is freely available, under the
        license terms of each contributing database.

       -- PathwayCommons home page, Nov 2013


Data is freely available, under the license terms of each contributing database.

"""
from bioservices.services import REST, BioServicesError


__all__ = ["PathwayCommons"]


class PathwayCommons:
    """Interface to the `PathwayCommons <http://www.pathwaycommons.org/about>`_ service


    >>> from bioservices import *
    >>> pc2 = PathwayCommons(verbose=False)
    >>> res = pc2.get("http://identifiers.org/uniprot/Q06609")



    .. todo:: traverse() method not implemented.
    """

    #: valid formats
    _valid_format = ["GSEA", "SBGN", "BIOPAX", "SIF", "TXT", "JSONLD"]
    _valid_directions = ["BOTHSTREAM", "UPSTREAM", "DOWNSTREAM", "UNDIRECTED"]
    _valid_patterns = [
        "CONTROLS_STATE_CHANGE_OF",
        "CONTROLS_PHOSPHORYLATION_OF",
        "CONTROLS_TRANSPORT_OF",
        "CONTROLS_EXPRESSION_OF",
        "IN_COMPLEX_WITH",
        "INTERACTS_WITH",
        "CATALYSIS_PRECEDES",
        "NEIGHBOR_OF",
        "CONSUMPTION_CONTROLLED_BY",
        "CONTROLS_TRANSPORT_OF_CHEMICAL",
        "CONTROLS_PRODUCTION_OF",
        "CHEMICAL_AFFECTS",
        "REACTS_WITH",
        "USED_TO_PRODUCE",
    ]
    _url = "https://www.pathwaycommons.org"

    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages

        """
        self.easyXMLConversion = False
        self._default_extension = "json"

        self.services = REST(name="PathwayCommons", url=PathwayCommons._url, verbose=verbose, cache=cache)

    # just a get/set to the default extension
    def _set_default_ext(self, ext):
        self.services.devtools.check_param_in_list(ext, ["json", "xml"])
        self._default_extension = ext

    def _get_default_ext(self):
        return self._default_extension

    default_extension = property(
        _get_default_ext,
        _set_default_ext,
        doc="set extension of the requests (default is json). Can be 'json' or 'xml'",
    )

    def search(self, q, page=0, datasource=None, organism=None, type=None):
        """Text search in PathwayCommons using Lucene query syntax

        Some of the parameters are BioPAX properties, others are composite
        relationships.

        All index fields are (case-sensitive): comment, ecnumber,
        keyword, name, pathway, term, xrefdb, xrefid, dataSource, and organism.

        The pathway field maps to all participants of pathways that contain
        the keyword(s) in any of its text fields.

        Finally, keyword is a transitive aggregate field that includes all
        searchable keywords of that element and its child elements.

        All searches can also be filtered by data source and organism.

        It is also possible to restrict the domain class using the
        'type' parameter.

        This query can be used standalone or to retrieve starting points
        for graph searches.


        :param str q: requires a keyword , name, external identifier, or a
            Lucene query string.
        :param int page: (N>=0, default is 0), search result page number.
        :param str datasource: filter by data source (use names or URIs of
            pathway data sources or of any existing Provenance object). If
            multiple data source values are specified, a union of hits from
            specified sources is returned. datasource=[reactome,pid] returns
            hits associated with Reactome or PID.
        :param str organism: The organism can be specified either by
            official name, e.g. "homo sapiens" or by NCBI taxonomy id,
            e.g. "9606". Similar to data sources, if multiple organisms
            are declared a union of all hits from specified organisms
            is returned. For example organism=[9606, 10016] returns results
            for both human and mice.
        :param str type: BioPAX class filter. (e.g., 'pathway', 'proteinreference')


        .. doctest::

            >>> from bioservices import PathwayCommons
            >>> pc2 = PathwayCommons(vverbose=False)
            >>> pc2.search("Q06609")
            >>> pc2.search("brca2", type="proteinreference",
                    organism="homo sapiens",  datasource="pid")
            >>> pc2.search("name:'col5a1'", type="proteinreference", organism=9606)
            >>> pc2.search("a*", page=3)

        Find the FGFR2 keyword::

            pc2.search("FGFR2")

        Find pathways by FGFR2 keyword in any index field.::

            pc2.search("FGFR2", type="pathway")

        Finds control interactions that contain the word binding but not
        transcription in their indexed fields::

            pc2.search("binding NOT transcription", type="control")

        Find all interactions that directly or indirectly participate
        in a pathway that has a keyword match for "immune" (Note the star after
        immune):

            pc.search("pathway:immune*", type="conversion")


        Find all Reactome pathways::

            pc.search("*", type="pathway", datasource="reactome")

        """
        if self.default_extension == "xml":
            url = "pc2/search.xml?q=%s" % q
        elif self.default_extension == "json":
            url = "pc2/search.json?q=%s" % q

        params = {}
        if page >= 0:
            params["page"] = page
        else:
            self.services.logging.warning("page should be >=0")

        if datasource:
            params["datasource"] = datasource

        if type:
            params["type"] = type

        if organism:
            params["organism"] = organism

        res = self.services.http_get(url, frmt=self.default_extension, params=params)

        # if self.default_extension == "json":
        #    res = json.loads(res)
        if self.default_extension == "xml":
            res = self.easyXML(res)

        return res

    def get(self, uri, frmt="BIOPAX"):
        """Retrieves full pathway information for a set of elements

        elements can be for example pathway, interaction or physical
        entity given the RDF IDs. Get commands only
        retrieve the BioPAX elements that are directly mapped to the ID.
        Use the :meth:`traverse` query to traverse BioPAX graph and
        obtain child/owner elements.

        :param str uri: valid/existing BioPAX element's URI (RDF ID; for
            utility classes that were "normalized", such as entity refereneces
            and controlled vocabularies, it is usually a Identifiers.org URL.
            Multiple IDs can be provided using list
            uri=[http://identifiers.org/uniprot/Q06609,
            http://identifiers.org/uniprot/Q549Z0']
            See also about MIRIAM and Identifiers.org.
        :param str format: output format (values)

        :return: a complete BioPAX representation for the record
            pointed to by the given URI is returned. Other output
            formats are produced by converting the BioPAX record on
            demand and can be specified by the optional format
            parameter. Please be advised that with some output formats
            it might return "no result found" error if the conversion is
            not applicable for the BioPAX result. For example,
            BINARY_SIF output usually works if there are some
            interactions, complexes, or pathways in the retrieved set
            and not only physical entities.


        .. doctest::

            >>> from bioservices import PathwayCommons
            >>> pc2 = PathwayCommons(verbose=False)
            >>> res = pc2.get("col5a1")
            >>> res = pc2.get("http://identifiers.org/uniprot/Q06609")


        """

        self.services.devtools.check_param_in_list(frmt, self._valid_format)

        # validates the URIs
        if isinstance(uri, str):
            url = "pc2/get?uri=" + uri
        elif instance(uri, list):
            url = "pc2/get?uri=" + uri[0]
            if len(uri) > 1:
                for u in uri[1:]:
                    url += "&uri=" + u

        # ?uri=http://identifiers.org/uniprot/Q06609
        # http://www.pathwaycommons.org/pc2/get?uri=COL5A1

        if frmt != "BIOPAX":
            url += "&format=%s" % frmt

        if frmt.lower() in ["biopax", "sbgn"]:
            frmt = "xml"
        else:
            frmt = "txt"
        res = self.services.http_get(url, frmt=frmt)

        return res

    def top_pathways(self, query="*", datasource=None, organism=None):
        """This command returns all *top* pathways

                Pathways can be top or pathways that are neither
                'controlled' nor 'pathwayComponent' of another process.

                :param query: a keyword, name, external identifier or lucene query
                    string like in 'search'. Default is "*"
                :param str datasource: filter by data source (same as search)
                :param str organism: organism filter. 9606 for human.

                :return: dictionary with information about top pathways. Check the
                    "searchHit" key for information about "dataSource" for instance


                .. doctest::

                    >>> from bioservices import PathwayCommons
                    >>> pc2 = PathwayCommons(verbose=False)
                    >>> res = pc2.top_pathways()


        https://www.pathwaycommons.org/pc2/top_pathways?q=TP53

        """
        if self.default_extension == "json":
            url = "pc2/top_pathways.json"
        else:
            url = "pc2/top_pathways"

        params = {}
        if datasource:
            params["datasource"] = datasource
        if organism:
            params["organism"] = organism
        params["q"] = query

        res = self.services.http_get(url, frmt=self.default_extension, params=params)

        if self.default_extension == "xml":
            res = self.easyXML(res)
        return res

    def graph(
        self,
        kind,
        source,
        target=None,
        direction=None,
        limit=1,
        frmt=None,
        datasource=None,
        organism=None,
    ):
        """Finds connections and neighborhoods of elements

        Connections can be for example the shortest path between two proteins
        or the neighborhood for a particular protein state or all states.

        Graph searches take detailed BioPAX semantics such as generics or
        nested complexes into account and traverse the graph accordingly.
        The starting points can be either physical entites or entity references.

        In the case of the latter the graph search starts from ALL
        the physical entities that belong to that particular entity references,
        i.e.  all of its states. Note that we integrate BioPAX data from
        multiple databases  based on our proteins and small molecules data
        warehouse and consistently normalize UnificationXref, EntityReference,
        Provenance, BioSource, and ControlledVocabulary objects when we are
        absolutely sure that two objects of the same type are equivalent. We,
        however, do not merge physical entities and reactions from different
        sources as matching and aligning pathways at that level is still an
        open research problem. As a result, graph searches can return
        several similar but disconnected sub-networks that correspond to
        the pathway data from different providers (though some physical
        entities often refer to the same small molecule or protein reference
        or controlled vocabulary).


        :param str kind: graph query
        :param str source:  source object's URI/ID. Multiple source URIs/IDs
            must be encoded as list of valid URI
            **source=['http://identifiers.org/uniprot/Q06609',
            'http://identifiers.org/uniprot/Q549Z0']**.
        :param str target: required for PATHSFROMTO graph query.  target
            URI/ID. Multiple target URIs must be encoded as list (see source
            parameter).
        :param str direction: graph search  direction in [BOTHSTREAM,
            DOWNSTREAM, UPSTREAM] see :attr:`_valid_directions` attribute.
        :param int limit: graph query search distance limit (default = 1).
        :param str format: output format. see :attr:`_valid-format`
        :param str datasource: datasource filter (same as for 'search').
        :param str organism: organism filter (same as for 'search').


        :return:  By default, graph queries return a complete BioPAX
            representation of the subnetwork matched by the algorithm.
            Other output formats are available as specified by the optional
            format parameter. Please be advised that some output format
            choices might cause "no result found" error if the conversion
            is not applicable for the BioPAX result (e.g., BINARY_SIF output
            fails if there are no interactions, complexes, nor pathways
            in the retrieved set).

        .. doctest::

            >>> from bioservices import PathwayCommons
            >>> pc2 = PathwayCommons(verbose=False)
            >>> res = pc2.graph(source="http://identifiers.org/uniprot/P20908",
                    kind="neighborhood", format="EXTENDED_BINARY_SIF")



        """
        url = "pc2/graph"
        params = {}
        params["source"] = source
        params["kind"] = kind
        params["limit"] = limit

        params = {}
        if target:
            params["target"] = target
        if frmt:
            params["format"] = frmt
        if datasource:
            params["datasource"] = datasource
        if organism:
            params["organism"] = organism

        res = self.services.http_get(url, frmt="txt", params=params)
        return res

    def traverse(self, uri, path):
        """Provides XPath-like access to the PC.


        The format of the path query is in the form::

            [InitialClass]/[property1]:[classRestriction(optional)]/[property2]... A "*"

        sign after the property instructs path accessor to transitively traverse
        that property. For example, the following path accessor will traverse
        through all physical entity components within a complex::

            "Complex/component*/entityReference/xref:UnificationXref"

        The following will list display names of all participants of
        interactions, which are components (pathwayComponent) of a pathway
        (note: pathwayOrder property, where same or other interactions can be
        reached, is not considered here)::

            "Pathway/pathwayComponent:Interaction/participant*/displayName"

        The optional parameter classRestriction allows to restrict/filter the
        returned property values to a certain subclass of the range of that
        property. In the first example above, this is used to get only the
        Unification Xrefs. Path accessors can use all the official BioPAX
        properties as well as additional derived classes and parameters in
        paxtools such as inverse parameters and interfaces that represent
        anonymous union classes in OWL. (See Paxtools documentation for more
        details).

        :param str uri: a biopax element URI - specified similar to the 'GET'
            command. multiple IDs are allowed as a list of strings.
        :param str path: a BioPAX propery path in the form of
                property1[:type1]/property2[:type2]; see above, inverse
                properties, Paxtools,
                org.biopax.paxtools.controller.PathAccessor.

        .. seealso:: `properties
            <http://www.pathwaycommons.org/pc2/#biopax_properties>`_

        :return:  XML result that follows the Search Response XML Schema
            (TraverseResponse type; pagination is disabled: returns all values at
            once)

        ::


            from bioservices import PathwayCommons
            pc2 = PathwayCommons(verbose=False)
            res = pc2.traverse(uri=['http://identifiers.org/uniprot/P38398','http://identifiers.org/uniprot/Q06609'], path="ProteinReference/organism")
            res = pc2.traverse(uri="http://identifiers.org/uniprot/Q06609",
                path="ProteinReference/entityReferenceOf:Protein/name")
            res = pc2.traverse("http://identifiers.org/uniprot/P38398",
                path="ProteinReference/entityReferenceOf:Protein")
            res = pc2.traverse(uri=["http://identifiers.org/uniprot/P38398",
                "http://identifiers.org/taxonomy/9606"], path="Named/name")


        """
        url = "pc2/traverse?"

        if isinstance(uri, str):
            url += "?uri=" + uri
        elif isinstance(uri, list):
            url += "?uri=" + uri[0]
            for u in uri[1:]:
                url += "&uri=" + u

        url += "&path=" + path

        res = self.services.http_get(url, frmt="json")
        return res

    def get_sifgraph_neighborhood(self, source, limit=1, direction="BOTHSTREAM", pattern=None):
        """finds the neighborhood sub-network in the Pathway Commons Simple Interaction
        Format (extented SIF) graph (see http://www.pathwaycommons.org/pc2/formats#sif)


        :param source: set of gene identifiers (HGNC symbol). Can be a list of
            identifiers or just one string(if only one identifier)
        :param int limit: Graph traversal depth. Limit > 1 value can result
            in very large data or error.
        :param str direction: Graph traversal direction. Use UNDIRECTED if you want
            to see interacts-with relationships too.
        :param str pattern: Filter by binary relationship (SIF edge) type(s).
            one of "BOTHSTREAM", "UPSTREAM", "DOWNSTREAM", "UNDIRECTED".

        returns: the graph in SIF format. The output must be stripped and
            returns one line per relation. In each line, items are separated by
            a tabulation. You can save the text with .sif extensions and it
            should be ready to use e.g. in cytoscape viewer.

        ::

            res = pc.get_sifgraph_neighborhood('BRD4')

        """
        self.services.devtools.check_param_in_list(direction, self._valid_directions)
        if pattern:
            self.services.devtools.check_param_in_list(pattern, self._valid_patterns)
        assert limit >= 1

        if isinstance(source, str):
            source = [source]
        assert isinstance(source, list)
        source = ",".join(source)

        params = {"source": source, "limit": limit, "direction": direction}

        if pattern:
            params["pattern"] = pattern

        res = self.services.http_get(
            "sifgraph/v1/neighborhood",
            params=params,
            headers=self.services.get_headers(content="text"),
        )

        return res.content

    def get_sifgraph_common_stream(self, source, limit=1, direction="DOWNSTREAM", pattern=None):
        """finds the common stream for them; extracts a sub-network from the loaded
        Pathway Commons SIF model.

        :param source: set of gene identifiers (HGNC symbol). Can be a list of
            identifiers or just one string(if only one identifier)
        :param int limit: Graph traversal depth. Limit > 1 value can result
            in very large data or error.
        :param str direction: Graph traversal direction. Use UNDIRECTED if you want
            to see interacts-with relationships too.
        :param str pattern: Filter by binary relationship (SIF edge) type(s).
            one of "BOTHSTREAM", "UPSTREAM", "DOWNSTREAM", "UNDIRECTED".

        returns: the graph in SIF format. The output must be stripped and
            returns one line per relation. In each line, items are separated by
            a tabulation. You can save the text with .sif extensions and it
            should be ready to use e.g. in cytoscape viewer.

        ::

            res = pc.get_sifgraph_common_stream(['BRD4', 'MYC'])
        """
        self.services.devtools.check_param_in_list(direction, self._valid_directions)
        if pattern:
            self.services.devtools.check_param_in_list(pattern, self._valid_patterns)
        assert limit >= 1

        if isinstance(source, str):
            source = [source]
        assert isinstance(source, list)
        source = ",".join(source)

        params = {"source": source, "limit": limit, "direction": direction}

        if pattern:
            params["pattern"] = pattern

        res = self.services.http_get(
            "sifgraph/v1/commonstream",
            params=params,
            headers=self.services.get_headers(content="text"),
        )
        try:
            return res.content
        except:
            # if no match, returns code 406 and ""
            return None

    def get_sifgraph_pathsbetween(self, source, limit=1, directed=False, pattern=None):
        """finds the paths between them; extracts a sub-network from the Pathway Commons SIF graph.

        :param source: set of gene identifiers (HGNC symbol). Can be a list of
            identifiers or just one string(if only one identifier)
        :param int limit: Graph traversal depth. Limit > 1 value can result
            in very large data or error.
        :param bool directed: Directionality: 'true' is for DOWNSTREAM/UPSTREAM, 'false' - UNDIRECTED
        :param str pattern: Filter by binary relationship (SIF edge) type(s).
            one of "BOTHSTREAM", "UPSTREAM", "DOWNSTREAM", "UNDIRECTED".

        returns: the graph in SIF format. The output must be stripped and
            returns one line per relation. In each line, items are separated by
            a tabulation. You can save the text with .sif extensions and it
            should be ready to use e.g. in cytoscape viewer.
        """
        if pattern:
            self.services.devtools.check_param_in_list(pattern, self._valid_patterns)
        assert limit >= 1

        if isinstance(source, str):
            source = [source]
        assert isinstance(source, list)
        source = ",".join(source)

        params = {"source": source, "limit": limit, "directed": directed}

        if pattern:
            params["pattern"] = pattern

        res = self.services.http_get(
            "sifgraph/v1/pathsbetween",
            params=params,
            headers=self.services.get_headers(content="text"),
        )

        return res.content

    def get_sifgraph_pathsfromto(self, source, target, limit=1, pattern=None):
        """finds the paths between them; extracts a sub-network from the Pathway Commons SIF graph.

        :param source: set of gene identifiers (HGNC symbol). Can be a list of
            identifiers or just one string(if only one identifier)
        param target: A target set of gene identifiers.
        :param int limit: Graph traversal depth. Limit > 1 value can result
            in very large data or error.
        :param str pattern: Filter by binary relationship (SIF edge) type(s).
            one of "BOTHSTREAM", "UPSTREAM", "DOWNSTREAM", "UNDIRECTED".

        returns: the graph in SIF format. The output must be stripped and
            returns one line per relation. In each line, items are separated by
            a tabulation. You can save the text with .sif extensions and it
            should be ready to use e.g. in cytoscape viewer.
        """
        if pattern:
            self.services.devtools.check_param_in_list(pattern, self._valid_patterns)
        assert limit >= 1

        if isinstance(source, str):
            source = [source]
        assert isinstance(source, list)
        source = ",".join(source)
        if isinstance(target, str):
            target = [target]
        assert isinstance(target, list)
        target = ",".join(target)

        params = {"source": source, "target": target, "limit": limit}

        if pattern:
            params["pattern"] = pattern

        res = self.services.http_get(
            "sifgraph/v1/pathsfromto",
            params=params,
            headers=self.services.get_headers(content="text"),
        )

        return res.content
