#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the Reactome webs services

.. topic:: What is Reactome?

    :URL: http://www.reactome.org/ReactomeGWT/entrypoint.html
    :Citation: http://www.reactome.org/citation.html
    :REST: http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS

    .. highlights::

        "REACTOME is an open-source, open access, manually curated and peer-reviewed
        pathway database. Pathway annotations are authored by expert biologists, in
        collaboration with Reactome editorial staff and cross-referenced to many
        bioinformatics databases. These include NCBI Entrez Gene, Ensembl and UniProt
        databases, the UCSC and HapMap Genome Browsers, the KEGG Compound and ChEBI
        small molecule databases, PubMed, and Gene Ontology. ... "

        -- from Reactome web site

"""

import sys
import webbrowser
import copy

from bioservices.services import REST

__all__ = ["Reactome", "ReactomeOld", "ReactomeAnalysis"]


class Reactome:
    """



    .. todo:: interactors, orthology, particiapnts, person,
        query, refernces, schema



    """

    _url = "https://reactome.org/ContentService"

    def __init__(self, verbose=True, cache=False):
        self.services = REST(name="Reactome", url=Reactome._url, verbose="ERROR", cache=False)
        self.debugLevel = verbose

    @property
    def version(self):
        return self.services.http_get("data/database/version", frmt="txt")

    @property
    def name(self):
        return self.services.http_get("data/database/name", frmt="txt")

    def get_discover(self, identifier):
        """The schema.org for an Event in Reactome knowledgebase

        For each event (reaction or pathway) this method generates a
        json file representing the dataset object as defined by
        schema.org (http). This is mainly used by search engines in
        order to index the data

        ::

            r.data_discover("R-HSA-446203")

        """
        res = self.services.http_get("data/discover/{}".format(identifier), frmt="json")
        return res

    def get_diseases(self):
        """list of diseases objects"""
        return self.services.http_get("data/diseases", frmt="json")

    def get_diseases_doid(self):
        """retrieves the list of disease DOIDs annotated in Reactome

        return: dictionary with DOID contained in the values()
        """
        res = self.services.http_get("data/diseases/doid", frmt="txt")
        res = dict([x.split() for x in res.split("\n")])
        return res

    def get_interactors_psicquic_molecule_details(self):
        """Retrieve clustered interaction, sorted by score, of a given accession by resource."""
        raise NotImplementedError

    def get_interactors_psicquic_molecule_summary(self):
        """Retrieve a summary of a given accession by resource"""
        raise NotImplementedError

    def get_interactors_psicquic_resources(self):
        """Retrieve a list of all Psicquic Registries services"""
        raise NotImplementedError

    def get_interactors_static_molecule_details(self):
        """Retrieve a detailed interaction information of a given accession"""
        raise NotImplementedError

    def get_interactors_static_molecule_pathways(self):
        """Retrieve a list of lower level pathways where the interacting molecules can be found"""
        raise NotImplementedError

    def get_interactors_static_molecule_summary(self):
        """Retrieve a summary of a given accession"""
        raise NotImplementedError

    def get_exporter_fireworks(self):
        raise NotImplementedError

    def get_exporter_reaction(self):
        raise NotImplementedError

    def get_exporter_diagram(
        self,
        identifier,
        ext="png",
        quality=5,
        diagramProfile="Modern",
        analysisProfile="Standard",
        filename=None,
    ):
        """Export a given pathway diagram to raster file

        This method accepts identifiers for Event class instances.
        When a diagrammed pathway is provided, the diagram is exported
        to the specified format. When a subpathway is provided, the
        diagram for the parent is exported and the events that are part
        of the subpathways are selected. When a reaction is provided,
        the diagram containing the reaction is exported and the reaction
        is selected.

        :param identifier: Event identifier (it can be a pathway with
            diagram, a subpathway or a reaction)
        :param ext: File extension (defines the image format) in png,
            jpeg, jpg, svg, gif
        :param quality: Result image quality between [1 - 10]. It
            defines the quality of the final image (Default 5)
        :param flg: not implemented
        :param sel: not implemented
        :param diagramProfile: Diagram Color Profile
        :param token: not implemented
        :param analysisProfile: Analysis Color Profile
        :param expColumn: not implemented
        :param filename: if given, save the results in the provided filename

        return: raw data if filename parameter is not set. Otherwise, the data
            is saved in the filename and the function returns None

        """
        assert ext in ["png", "jpg", "jpeg", "svg", "gif"]
        assert quality in range(11)
        assert diagramProfile in ["Modern", "Standard"]
        assert analysisProfile in ["Standard", "Strosobar", "Copper Plus"]

        params = {
            "diagramProfile": diagramProfile,
            "analysisProfile": analysisProfile,
            "quality": quality,
        }

        res = self.services.http_get("exporter/diagram/{}.{}".format(identifier, ext), params=params, frmt=ext)
        if filename:
            if ext != "svg":
                with open(filename, "wb") as fout:
                    fout.write(res)
            else:
                with open(filename, "w") as fout:
                    fout.write(content)
        else:
            return res

    def get_complex_subunits(self, identifier, excludeStructuresSpecifies=False):
        """A list with the entities contained in a given complex

        Retrieves the list of subunits that constitute any given complex.
        In case the complex comprises other complexes, this method
        recursively traverses the content returning each contained
        PhysicalEntity. Contained complexes and entity sets can be
        excluded setting the ‘excludeStructures’ optional parameter to ‘true’

        :param identifier: The complex for which subunits are requested
        :param excludeStructures: Specifies whether contained complexes
            and entity sets are excluded in the response

        ::

            r.get_complex_subunits("R-HSA-5674003")
        """
        params = {"excludeStructuresSpecifies": excludeStructuresSpecifies}
        res = self.services.http_get("data/complex/{}/subunits".format(identifier), params=params, frmt="json")
        return res

    def get_complexes(self, resources, identifier):
        """A list of complexes containing the pair (identifier, resource)

        Retrieves the list of complexes that contain a given (identifier,
        resource). The method deconstructs the complexes into all its
        participants to do so.

        :param resource: The resource of the identifier for complexes are
            requested (e.g. UniProt)
        :param identifier: The identifier for which complexes are requested

        ::

            r.get_complexes(resources, identifier)
            r.get_complexes("UniProt", "P43403")

        """
        res = self.services.http_get("data/complexes/{}/{}".format(resources, identifier), frmt="json")
        return res

    def get_entity_componentOf(self, identifier):
        """A list of larger structures containing the entity

        Retrieves the list of structures (Complexes and Sets) that
        include the given entity as their component. It should be
        mentioned that the list includes only simplified entries
        (type, names, ids) and not full information about each item.

        ::

            r.get_entity_componentOf("R-HSA-199420")

        """
        res = self.services.http_get("data/entity/{}/componentOf".format(identifier), frmt="json")
        return res

    def get_entity_otherForms(self, identifier):
        """All other forms of PhysicalEntity

        Retrieves a list containing all other forms of the given
        PhysicalEntity. These other forms are PhysicalEntities that
        share the same ReferenceEntity identifier, e.g. PTEN
        H93R[R-HSA-2318524] and PTEN C124R[R-HSA-2317439] are two
        forms of PTEN.

        ::

            r.get_entity_otherForms("R-HSA-199420")

        """
        res = self.services.http_get("data/entity/{}/otherForms".format(identifier), frmt="json")
        return res

    def get_event_ancestors(self, identifier):
        """The ancestors of a given event

        The Reactome definition of events includes pathways and reactions.
        Although events are organised in a hierarchical structure, a single
        event can be in more than one location, i.e. a reaction can take
        part in different pathways while, in the same way, a sub-pathway
        can take part in many pathways. Therefore, this method retrieves
        a list of all possible paths from the requested event to the top
        level pathway(s).

        :param identifier: The event for which the ancestors are requested

        ::

            r.get_event_ancestors("R-HSA-5673001")

        """
        res = self.services.http_get("data/event/{}/ancestors".format(identifier), frmt="json")
        return res

    def get_eventsHierarchy(self, species):
        """The full event hierarchy for a given species

        Events (pathways and reactions) in Reactome are organised in a
        hierarchical structure for every species. By following all
        ‘hasEvent’ relationships, this method retrieves the full event
        hierarchy for any given species. The result is a list of tree
        structures, one for each TopLevelPathway. Every event in these trees is
        represented by a PathwayBrowserNode. The latter contains the stable identifier,
        the name, the species, the url, the type, and the diagram of the particular
        event.

        :param species: Allowed species filter: SpeciesName (eg: Homo sapiens)
            SpeciesTaxId (eg: 9606)

        ::

            r.get_eventsHierarchy(9606)
        """

        res = self.services.http_get("data/eventsHierarchy/{}".format(species), frmt="json")
        return res

    def get_exporter_sbml(self, identifier):
        """Export given Pathway to SBML


        :param identifier: DbId or StId of the requested database object

        ::

            r.exporter_sbml("R-HSA-68616")

        """
        res = self.services.http_get("exporter/sbml/{}.xml".format(identifier), frmt="xml")
        return res

    def get_pathway_containedEvents(self, identifier):
        """All the events contained in the given event

        Events are the building blocks used in Reactome to represent
        all biological processes, and they include pathways and reactions.
        Typically, an event can contain other events. For example, a
        pathway can contain smaller pathways and reactions. This method
        recursively retrieves all the events contained in any given event.

        ::

            res = r.get_pathway_containedEvents("R-HSA-5673001")

        """
        res = self.services.http_get("data/pathway/{}/containedEvents".format(identifier), frmt="json")
        return res

    def get_pathway_containedEvents_by_attribute(self, identifier, attribute):
        """A single property for each event contained in the given event

        Events are the building blocks used in Reactome to represent all
        biological processes, and they include pathways and reactions.
        Typically, an event can contain other events. For example, a
        pathway can contain smaller pathways (subpathways) and reactions.
        This method recursively retrieves a single attribute for each of
        the events contained in the given event.


        :param identifier: The event for which the contained events are requested
        :param attribute: Attrubute to be filtered

        ::

             r.get_pathway_containedEvents_by_attribute("R-HSA-5673001", "stId")

        """
        res = self.services.http_get(
            "data/pathway/{}/containedEvents/{}".format(identifier, attribute),
            frmt="txt",
        )
        try:
            res = [x.strip() for x in res[1:-1].split(",")]
        except:
            pass
        return res

    def get_pathways_low_diagram_entity(self, identifier):
        """A list of lower level pathways with diagram containing
        a given entity or event

        This method traverses the event hierarchy and retrieves the
        list of all lower level pathways that have a diagram and
        contain the given PhysicalEntity or Event.

        :param identifier: The entity that has to be present in the pathways
        :param species:  The species for which the pathways are requested.
            Taxonomy identifier (eg: 9606) or species name (eg: ‘Homo sapiens’)

        ::

            r.get_pathways_low_diagram_entity("R-HSA-199420")

        """
        res = self.services.http_get("data/pathways/low/diagram/entity/{}".format(identifier), frmt="json")
        return res

    def get_pathways_low_diagram_entity_allForms(self, identifier):
        """

        ::

            r.get_pathways_low_diagram_entity_allForms("R-HSA-199420")
        """
        res = self.services.http_get(
            "data/pathways/low/diagram/entity/{}/allForms".format(identifier),
            frmt="json",
        )
        return res

    def get_pathways_low_entity(self, identifier):
        """A list of lower level pathways containing a given entity or event

        This method traverses the event hierarchy and retrieves the
        list of all lower level pathways that contain the given
        PhysicalEntity or Event.

        ::

            r.get_pathways_low_entity("R-HSA-199420")
        """
        res = self.services.http_get("data/pathways/low/entity/{}".format(identifier), frmt="json")
        return res

    def get_pathways_low_entity_allForms(self, identifier):
        """A list of lower level pathways containing any form of a given entity

        This method traverses the event hierarchy and retrieves the list of all
        lower level pathways that contain the given PhysicalEntity in any of
        its variant forms. These variant forms include for example different
        post-translationally modified versions of a single protein, or the
        same chemical in different compartments.

        ::

            r.get_pathways_low_entity_allForms("R-HSA-199420")
        """
        res = self.services.http_get("data/pathways/low/entity/{}/allForms".format(identifier), frmt="json")
        return res

    def get_pathways_top(self, species):
        res = self.services.http_get("data/pathways/top/{}".format(species), frmt="json")
        return res

    def get_references(self, identifier):
        """All referenceEntities for a given identifier

        Retrieves a list containing all the reference entities for a given
        identifier.

        ::

            r.get_references(15377)

        """
        res = self.services.http_get("references/mapping/{}".format(identifier), frmt="json")
        return res

    def get_mapping_identifier_pathways(self, resource, identifier):
        res = self.services.http_get("data/mapping/{}/{}/pathways".format(resource, identifier), frmt="json")
        return res

    def get_mapping_identifier_reactions(self, resource, identifier):
        res = self.services.http_get("data/mapping/{}/{}/reactions".format(resource, identifier), frmt="json")

    def search_facet(self):
        """A list of facets corresponding to the whole Reactome search data

        This method retrieves faceting information on the whole Reactome search data.


        """
        res = self.services.http_get("search/facet", frmt="json")
        return res

    def search_facet_query(self, query):
        """A list of facets corresponding to a specific query

        This method retrieves faceting information on a specific query

        """
        res = self.services.http_get("search/facet_query?query={}".format(query), frmt="json")
        return res

    def search_query(self, query):
        """Queries Solr against the Reactome knowledgebase

        This method performs a Solr query on the Reactome knowledgebase.
        Results can be provided in a paginated format.

        """
        res = self.services.http_get("search/query?query={}".format(query), frmt="json")
        return res

    def search_spellcheck(self, query):
        """Spell-check suggestions for a given query

        This method retrieves a list of spell-check suggestions
        for a given search term.

        """
        res = self.services.http_get("search/spellcheck?query={}".format(query), frmt="json")
        return res

    def search_suggest(self, query):
        """Autosuggestions for a given query


        This method retrieves a list of suggestions for a given search term.

        ::

            >>> r.http_get("search/suggest?query=apopt")
            ['apoptosis', 'apoptosome', 'apoptosome-mediated', 'apoptotic']

        """
        res = self.services.http_get("search/suggest?query={}".format(identifier), frmt="json")
        return res

    def get_species_all(self):
        """the list of all species in Reactome"""
        res = self.services.http_get("data/species/all", frmt="json")
        return res

    def get_species_main(self):
        """the list of main species in Reactome

        ::

            r.get_species_main()


        """
        res = self.services.http_get("data/species/main", frmt="json")
        return res


class ReactomeOld(REST):
    """Reactome interface

    some data can be download on the main `website <http://www.reactome.org/pages/download-data/>`_
    """

    _url = "http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS"

    def __init__(self, verbose=True, cache=False):
        super(ReactomeOld, self).__init__("Reactome(URL)", url=ReactomeOld._url, verbose="ERROR", cache=False)
        self.debugLevel = verbose
        self.test = 2

        # for buffering
        self._list_pathways = None

    def _download_list_pathways(self):
        if self._list_pathways is None:
            res = self.session.get("http://www.reactome.org/download/current/ReactomePathways.txt")
            if res.status_code == 200:
                res = res.text  # content does not work in python 3.3
                res = res.strip()
                self._list_pathways = [x.split("\t") for x in res.split("\n")]
            else:
                self.logging.error("could not fetch the pathways")
        return self._list_pathways

    def get_list_pathways(self):
        """Return list of pathways from reactome website

        :return: list of lists. Each sub-lis contains 3 items: reactome pathway
            identifier, description and species

        """
        res = self._download_list_pathways()
        return res

    def get_species(self):
        """Return list of species from all pathways"""
        res = self._download_list_pathways()
        res = set([x[2] for x in self.get_list_pathways()])
        return res

    def biopax_exporter(self, identifier, level=2):
        """Get BioPAX file

        The passed identifier has to be a valid event identifier. If there is no matching ID in
        the database, it will return an empty string.

        :param int level: BioPAX level: one of two values: 2 or 3
        :param int identfier: event database identifier
        :return: BioPAX RDF document


        ::

            >>> # for Apoptosis:
            >>> s = Reactome()
            >>> res = s.biopax_exporter(109581)
        """
        res = self.http_get("biopaxExporter/Level{0}/{1}".format(level, identifier), frmt=None)
        return res

    def front_page_items(self, species):
        """Get list of front page items listed in the Reactome Pathway Browser

        :param str species: Full species name that should be encoded for URL (e.g.
            homo+sapiens for human, or mus+musculus for mouse) + can be replaced
            by spaces.

        :return:  list of fully encoded Pathway objects in JSON

        ::

            >>> s = Reactome()
            >>> res = s.front_page_items("homo sapiens")
            >>> print(res[0]['name'])
            ['Apoptosis']

        .. seealso:: `Pathway Browser <http://www.reactome.org/PathwayBrowser/>`_
        """
        species = species.replace("+", " ")
        res = self.http_get("frontPageItems/{0}".format(species), frmt="json")
        return res

    def highlight_pathway_diagram(self, identifier, genes, frmt="PNG"):
        """Highlight a diagram for a specified pathway based on its identifier

        :param int identifier: a valid pathway  identifier
        :param list genes: a list of string to indicate the genes to highlight
        :param int frmt: PNG or PDF
        :return:  This  method should be used after method queryHitPathways.

        ::

            res = s.http_post("highlightPathwayDiagram/68875/PNG", frmt="txt",
                data="CDC2")
            with open("test.png", 'wb') as f:
                import binascii
                f.write(binascii.a2b_base64(res))


        """
        self.devtools.check_param_in_list(frmt, ["PDF", "PNG"])

        url = "highlightPathwayDiagram/{0}/{1}"
        genes = self.devtools.list2string(genes)

        res = self.http_post(url.format(identifier, frmt), frmt="txt", data=genes)
        return res

    def list_by_query(self, classname, **kargs):
        """Get list of objecs from Reactome database

        :param str class name:
        :param kargs: further attribute values encoded in key-value pair
        :return: list of dictionaries. Each dictionary contains information
            about a given pathway

        To query a list of pathways with names as "Apoptosis"::

            >>> s = Reactome()
            >>> res = list_by_query("Pathway", name="apoptosis")
            >>> identifiers = [x['dbId'] for x in res]

        """
        url = "listByQuery/{0}".format(classname)
        # NOTE: without the content-type this request fails with error 415
        # fixed by
        res = self.http_post(
            url,
            frmt="json",
            data=kargs,
            headers={"Content-Type": "application/json;odata=verbose"},
        )
        return res

    def pathway_diagram(self, identifier, frmt="PNG"):
        """Retrieve pathway diagram

        :param int identifier: Pathway database identifier
        :param str frmt: PNG, PDF, or XML.
        :return:  Base64 encoded pathway diagram for PNG or PDF. XML text for the XML file type.

        ::

            >>> s = Reactome()
            >>> s.pathway_diagram('109581', 'PNG',view=True)
            >>> s.pathway_diagram('109581', 'PNG', save=True)

        .. todo:: if PNG or PDF, the output is base64 but there is no
            facility to easily save the results in a file for now
        """
        self.devtools.check_param_in_list(frmt, ["PDF", "PNG", "XML"])
        url = "pathwayDiagram/{0}/{1}".format(identifier, frmt)
        res = self.http_get(url, frmt=frmt)
        return res

    def pathway_hierarchy(self, species):
        """Get the pathway hierarchy for a species as displayed in  Reactome pathway browser.

        :param str species: species name that should be with + or spaces (e.g.
            'homo+sapiens' for  human, or 'mus musculus' for mouse)
        :return: XML text containing  pathways and reactions

        ::

            s.pathway_hierarchy("homo sapiens")
        """
        species = species.replace("+", " ")
        res = self.http_get("pathwayHierarchy/{0}".format(species), frmt="xml")
        return res

    def pathway_participants(self, identifier):
        """Get list of pathway participants for a pathway using

        :param int identifier: Pathway database identifier
        :return: list of fully encoded PhysicalEntity objects in the pathway
            (in JSON)

        ::

            >>> s = Reactome()
            >>> s.pathway_participants(109581)
        """
        res = self.http_get("pathwayParticipants/{0}".format(identifier), frmt="json")
        return res

    def pathway_complexes(self, identifier):
        """Get complexes belonging to a pathway

        :param int identifier: Pathway database identifier
        :return: list of all PhysicalEntity objects that participate in the
            Pathway.(in JSON)

        ::

            >>> s = Reactome()
            >>> s.pathway_complexes(109581)

        """
        res = self.http_get("pathwayComplexes/{0}".format(identifier), frmt="json")
        return res

    def query_by_id(self, classname, identifier):
        """Get Reactome Database for a specific object.


        :param str classname: e.g. Pathway
        :param int identifier: database identifier or stable identifier if available

        It returns a full object, including full class information about
        all the attributes of the returned object. For example, if the object has
        one PublicationSource attribute, it will return a full PublicationSource
        object within the returned object.

        ::

            >>> s.query_by_id("Pathway", "109581")

        """
        url = "queryById/{0}/{1}".format(classname, identifier)
        res = self.http_get(url, frmt="json")
        return res

    def query_by_ids(self, classname, identifiers):
        """

        :param str classname: e.g. Pathway
        :param list identifiers: list of strings or int


        ::

            >>> s.quey_by_ids("Pathway", "CDC2")

        .. warning:: not sure the wrapping is correct
        """

        identifiers = self.devtools.list2string(identifiers)
        url = "queryByIds/{0}".format(classname)
        res = self.http_post(url, frmt="json", data=identifiers)
        # headers={'Content-Type': "application/json"})
        return res

    def query_hit_pathways(self, query):
        """Get pathways that contain one or more genes passed in the query list.

        In the Reactome data model, pathways are organized in a
        hierarchical structure. The returned pathways in this method are pathways
        having detailed manually drawn pathway diagrams. Currently only human
        pathways will be returned from this method.

        ::

            s.query_hit_pathways('CDC2')
            s.query_hit_pathways(['CDC2'])

        """
        identifiers = self.devtools.list2string(query)
        res = self.http_post("queryHitPathways", frmt="json", data=identifiers)
        return res

    def query_pathway_for_entities(self, identifiers):
        """Get pathway objects by specifying an array of PhysicalEntity database identifiers.


        The returned Pathways should
        contain the passed EventEntity objects. All passed EventEntity database
        identifiers should be in the database.

        """
        identifiers = self.devtools.list2string(identifiers, space=False)
        url = "pathwayForEntities"
        res = self.http_post(url, frmt="json", data={"ID": identifiers})
        return res

    def species_list(self):
        """Get the list of species used Reactome"""
        url = "speciesList"
        res = self.http_get(url, frmt="json")
        return res

    def SBML_exporter(self, identifier):
        """Get the SBML XML text of a pathway identifier

        :param int identifier: Pathway database identifier
        :return: SBML object in XML format as a string


        ::

            >>> from bioservices import Reactome
            >>> s = Reactome()
            >>> xml = s.SBML_exporter(109581)

        """
        url = "sbmlExporter/{0}".format(identifier)
        res = self.http_get(url, frmt="xml")
        return res

    def get_all_reactions(self):
        """Return list of reactions from the Pathway"""
        res = self.get_list_pathways()
        return [x[0] for x in res]

    def bioservices_get_reactants_from_reaction_identifier(self, reaction):
        """Fetch information from the reaction HTML page

        .. note:: draft version
        """
        res = self.http_get("http://www.reactome.org/content/detail/%s" % reaction)
        res = res.content

        try:
            reactants = [x for x in res.split("\n") if "<title>" in x]
            reactants = reactants[0].split("|")[1].strip().strip("</title>")
        except Exception as err:
            print("Could not interpret title", file=sys.stderr)
            return res

        if reactants.count(":") == 1:
            reactants = reactants.split(":")
        else:
            # self.logging.warning('Warning: did not find unique sign : for %s' % reaction)
            # reactants = reactants.split(":", 1)
            pass

        return reactants


"""
class ReactomePathway(object):

    def __init__(self, entry):
        self.raw_data = copy.deepcopy(entry)
        # just adding the attributes to make life easier
        for k in self.raw_data._keyord:
            setattr(self, k, getattr(self.raw_data, k))

    def __str__(self):

        txt = "id: " + str(self.id)
        txt += "\nname: " + str(self.name)

        txt += "\nhasComponent:"
        if self.hasComponent:
            txt += str(len(self.hasComponent))

        if self.raw_data.compartment:
            txt += "\ncompartment:" + str(len(self.raw_data.compartment))
        else:
            txt += "\ncompartment: " + str(self.raw_data.compartment)

        txt += "\nliteratureReference:"
        this = self.raw_data.literatureReference
        if this:
            for i,x in enumerate(this):
                txt += " --- %s: %s %s\n" % (i, x.id, x.name)

        txt += "\nspecies:"
        this = self.raw_data.species
        if this:
            txt += "  %s (%s)" % (this.scientificName, this.id)

        txt += "\nsummation:"
        this = self.raw_data.summation
        if this:
            for x in this:
                txt += " - %s \n" % (self.raw_data.id)

        txt += "\ngoBiologicalProcess:"
        this = self.raw_data.goBiologicalProcess
        if this: txt += "\n - %s %s\n" % (this.id, this.name)

        txt += "\ninferredFrom:" + str(self.raw_data.inferredFrom)
        txt += "\northologousEvent: "
        this = self.raw_data.orthologousEvent
        if this:
            txt += str(len(this))

        txt += "\nprecedingEvent: " + str(self.raw_data.precedingEvent)
        txt += "\nevidence Type: " + str(self.raw_data.evidenceType) + "\n"

        return txt
"""


class ReactomeAnalysis(REST):
    _url = "http://www.reactome.org:80/AnalysisService"

    # "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL",

    def __init__(self, verbose=True, cache=False):
        super(ReactomeAnalysis, self).__init__("Reactome(URL)", url=ReactomeAnalysis._url, verbose=verbose, cache=False)
        self.logging.warning(
            "Class in development. Some methods are already  working but those required POST do not. Coming soon "
        )

    def identifiers(self, genes):
        """

        s.identfiers("TP53")
        .. warning:: works for oe gene only for now
        """
        url = "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL"

        genes = self.devtools.list2string(genes)
        genes = genes.replace(" ", "")
        # print(genes)
        res = self.http_post(
            url,
            frmt="json",
            data=genes,
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Accept": "application/json",
            },
        )
        return res
