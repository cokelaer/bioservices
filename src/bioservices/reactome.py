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


from bioservices.services import REST

__all__ = ["Reactome"]


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


