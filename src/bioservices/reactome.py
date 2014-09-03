# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
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
#$Id$
"""Interface to the Reactome webs services

:STATUS: in progress/draft don't use !

.. topic:: What is Reactome?

    :URL: http://www.reactome.org/ReactomeGWT/entrypoint.html
    :Citation: http://www.reactome.org/citation.html
    :WSDL: http://www.reactome.org:8080/caBIOWebApp/services/caBIOService?wsdl

    .. highlights::

        "REACTOME is an open-source, open access, manually curated and peer-reviewed
        pathway database. Pathway annotations are authored by expert biologists, in
        collaboration with Reactome editorial staff and cross-referenced to many
        bioinformatics databases. These include NCBI Entrez Gene, Ensembl and UniProt
        databases, the UCSC and HapMap Genome Browsers, the KEGG Compound and ChEBI
        small molecule databases, PubMed, and Gene Ontology. ... "

        -- from Reactome web site

"""


from bioservices.services import WSDLService, REST
import webbrowser
import copy


# for reactome, content-type could be 
#  "Content-Type", "multipart/form-data; boundary=" +    boundary);

class Reactome(REST):

    _url = "http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS"
    def __init__(self, verbose=True, cache=False):
        super(Reactome, self).__init__("Reactome(URL)",url=Reactome._url,
            verbose=verbose, cache=False)
        self.logging.warning("Class in development. Some methods are already  working but those required POST do not. Coming soon ")

    def biopax_exporter(self, identifier, level=2):
        """Get BioPAX

        Pass an Event database identifier, and get the BioPAX exported in either XML
        or JSON. The passed Id has to be an Event Id. If there is no matching ID in
        the database, it will return an empty string.

        :param int level: BioPAX level: one of two values: 2 or 3
        :param int identfir: event database identifier
        :return: BioPAX RDF document


        ::

            >>> # for Apoptosis:
            >>> s = Reactome()
            >>> res = s.biopax_exporter(109581)
        """
        res = self.http_get("biopaxExporter/Level{0}/{1}".format(level, identifier),
                frmt=None)
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

        .. seealso::   `Pathway Browser <http://www.reactome.org/PathwayBrowser/`_
        """
        species = species.replace("+", " ")
        res = self.http_get("frontPageItems/{0}".format(species),
                frmt="json")
        return res

    def highlight_pathway_diagram(self, identifier, genes, frmt="PNG"):
        """Highlight a diagram for a specified pathway based on its identifier

        :param int identifier: a valid pathway  identifier
        :param list genes: a list of string to indicate the genes to highlight
        :param int frmt: PNG or PDF
        :return:  This  method should be used after method queryHitPathways.

        """
        self.devtools.check_param_in_list(frmt, ['PDF', 'PNG'])

        url = "highlightPathwayDiagram/{0}/{1}"
        params = {'genes': genes}

        res = self.http_post(url.format(identifier, frmt), frmt="txt", data=params)
        return res


    def list_by_query(self, classname, **kargs):
        """Query Reactome database for a list of objects using Key/Value pairs based on an object's attributes.


         For example, to query pathways with names as "Apoptosis", post "name=Apoptosis" to the server.

        :param str class name:
        :param further attribute values encoded in key-value pair
        :return: json object

        To query a list of pathways with names as "Apoptosis", try XML or JSON result

        ::
            >>> s = Reactome()
            >>> res = list_by_query("Pathway", name="apostosis")

        """
        url = "ListByQuery/{0}".format(classname)
        res = self.http_post(url, frmt='json', data=kargs)
        return res

    def pathway_diagram(self, identifier, frmt="PNG", save=False, view=False):
        """Retrieve pathway diagram

        :param int identifier: Pathway database identifier
        :param str frmt: PNG, PDF, or XML.
        ;param bool save: if True, save the output into a file called
            identifier.ext where ext is the lower-case versiob of the frmt
            parameter
        :param view: show image in a browser
        :return:  Base64 encoded pathway diagram for PNG or PDF. XML text for the XML file type.

        ::

            >>> s = Reactome()
            >>> s.pathway_diagram('109581', 'PNG',view=True)
            >>> s.pathway_diagram('109581', 'PNG', save=True)
        """
        self.devtools.check_param_in_list(frmt, ['PDF', 'PNG', 'XML'])
        url = 'pathwayDiagram/{0}/{1}'.format(identifier, frmt)
        res = self.http_get(url, frmt=frmt)


        if save:
            filename = str(identifier)+"."+frmt.lower()
            self.save_str_to_image(res, filename)
        if view and save:
            filename = str(identifier)+"."+frmt.lower()
            self.on_web(filename)

        return res

    def pathway_hierarchy(self, species):
        """Get the pathway hierarchy for a species as displayed in  Reactome pathway browser.

        :param str species: species name that should be with + or spaces (e.g.
            'homo+sapiens' for  human, or 'mus musculus' for mouse)
        :return: XML text containing  pathways and reactions


        """
        species = species.replace("+", " ")
        res = self.http_get("pathwayHierarchy/{0}".format(species),
                frmt="json")
        return res

    def pathway_participant(self, identifier):
        """Get list of pathway participants for a pathway using

        a Pathway database identifier. It returns a list of
            all PhysicalEntity objects that participate in the Pathway.

        :param int identifier: Pathway database identifier
        :return: list of fully encoded PhysicalEntity objects in the pathway (in
            JSON)

        ::

            >>> s = Reactome()
            >> s.pathway_participants(109581)
        """
        res = self.http_get("pathwayParticipant/{0}".format(identifier),
                frmt=None)
        return res

    def pathway_complexes(self, identifier):
        res = self.http_get("pathwayComplexes/{0}".format(identifier),
                frmt=None)
        return res

    def query_by_id(self, classname, identifier):
        """


        classname can be Pathway

        """
        url = "queryById/{0}/{1}".format(classname, identifier)
        res = self.http_get(url, frmt='json')
        return res

    def query_by_ids(self, classname, identifiers):
        """


        :param list identifiers: list of strings or int

        other options could be but not implemented
        FOCUS_SPECIES_ID=48887
        FOCUS_PATHWAY_ID=109581
        """

        identifiers = ",".join([str(x) for x in identifiers])
        params = {'ID':identifiers}

        url = "queryByIds/{0}".format(classname)
        res = self.http_post(url, frmt="txt", data=params)
        return res

    def query_hit_pathways(self, query):
        """ Query for a list of pathways that contain one or more genes passed in the
         query list. In the Reactome data model, pathways are organized in a
         hierarchical structure. The returned pathways in this method are pathways
     having detailed manually drawn pathway diagrams. Currently only human
     pathways will be returned from this method. 



        """
        identifiers = ",".join([str(x) for x in identifiers])
        params = {'ID':identifiers}
        url = "queryHitPathways"
        res = self.http_post(url, frmt='json', data=params)
        return res

    def query_pathway_for_entities(self, identifiers):
        """     Query for pathway objects by specifying an array of
        PhysicalEntity database identifiers. The returned Pathways should
        contain the passed EventEntity objects. All passed EventEntity database
        identifiers should be in the database. 

        """
        identifiers = ",".join([str(x) for x in identifiers])
        url = "pathwayForEntities"
        res = self.http_post(url, frmt='json', data={'ID':identifiers})
        return res

    def species_list(self):
        """Get the list of species used Reactome"""
        url = "speciesList"
        res = self.http_get(url, frmt='json')
        return res

    def SBML_exporter(self, identifier):
        """Get the SBML XML text of a pathway identifier

        :param int identifier: Pathway database identifier
        :return: SBML object in XML format as a string

        """
        url = "sbmlExporter/{0}".format(identifier)
        res = self.http_get(url, frmt='xml')
        return res



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

