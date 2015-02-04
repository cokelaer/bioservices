# -*- python -*-
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
#$Id$
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
from bioservices.services import WSDLService, REST
import webbrowser
import copy

__all__ = ['Reactome', 'ReactomeAnalysis']
# for reactome, content-type could be
#  "Content-Type", "multipart/form-data; boundary=" +    boundary);


class Reactome(REST):
    """Reactome interface

    some data can be download on the main `website <http://www.reactome.org/pages/download-data/>`_
    """

    _url = "http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/RESTfulWS"

    def __init__(self, verbose=True, cache=False):
        super(Reactome, self).__init__("Reactome(URL)",url=Reactome._url,
            verbose="ERROR", cache=False)
        self.debugLevel = verbose
        self.test = 2

        # for buffering
        self._list_pathways = None

    def _download_list_pathways(self):
        if self._list_pathways is None:
            res =  self.session.get("http://www.reactome.org/download/current/ReactomePathways.txt")
            if res.status_code == 200:
                res = res.text # content does not work in python 3.3
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

        .. seealso:: `Pathway Browser <http://www.reactome.org/PathwayBrowser/>`_
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

        ::

            res = s.http_post("highlightPathwayDiagram/68875/PNG", frmt="txt",
                data="CDC2")
            with open("test.png", 'wb') as f:
                f.write(res.decode("base64"))
                f.close()

        .. todo:: Saving the image above returns a blank image ...


        """
        self.devtools.check_param_in_list(frmt, ['PDF', 'PNG'])

        url = "highlightPathwayDiagram/{0}/{1}"
        genes = self.devtools.list2string(genes)

        res = self.http_post(url.format(identifier, frmt), frmt="txt",
                data=genes)
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
        res = self.http_post(url, frmt='json', data=kargs,
                headers={'Content-Type': "application/json;odata=verbose"})
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
        self.devtools.check_param_in_list(frmt, ['PDF', 'PNG', 'XML'])
        url = 'pathwayDiagram/{0}/{1}'.format(identifier, frmt)
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
        res = self.http_get("pathwayHierarchy/{0}".format(species),
                            frmt="xml")
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
        res = self.http_get("pathwayParticipants/{0}".format(identifier),
                            frmt='json')
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
        res = self.http_get("pathwayComplexes/{0}".format(identifier),
                frmt="json")
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
        res = self.http_get(url, frmt='json')
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
        #headers={'Content-Type': "application/json"})
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
        res = self.http_post("queryHitPathways", frmt='json', data=identifiers)
        return res

    def query_pathway_for_entities(self, identifiers):
        """Get pathway objects by specifying an array of PhysicalEntity database identifiers.


        The returned Pathways should
        contain the passed EventEntity objects. All passed EventEntity database
        identifiers should be in the database.

        """
        identifiers = self.devtools.list2string(identifiers, space=False)
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


        ::

            >>> from bioservices import Reactome
            >>> s = Reactome()
            >>> xml = s.SBML_exporter(109581)

        """
        url = "sbmlExporter/{0}".format(identifier)
        res = self.http_get(url, frmt='xml')
        return res


    def get_all_reactions(self):
        """Return list of reactions from the Pathway"""
        res = self.get_list_pathways()
        return [x[0] for x in res]

    def bioservices_get_reactants_from_reaction_identifier(self, reaction):
        """Fetch information from the reaction HTML page

        .. note:: draft version
        """
        res = self.http_get('http://www.reactome.org/content/detail/%s' % reaction) 
        res = res.content

        try:
            reactants = [x for x in res.split("\n") if '<title>' in x]
            reactants = reactants[0].split("|")[1].strip().strip('</title>')
        except  Exception as err:
            print('Could not interpret title')
            return res

        if reactants.count(':') == 1:
            reactants = reactants.split(":")
        else:
            #self.logging.warning('Warning: did not find unique sign : for %s' % reaction)
            #reactants = reactants.split(":", 1)
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
    
    #"identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL",

    def __init__(self, verbose=True, cache=False):
        super(ReactomeAnalysis, self).__init__("Reactome(URL)",url=ReactomeAnalysis._url,
            verbose=verbose, cache=False)
        self.logging.warning("Class in development. Some methods are already  working but those required POST do not. Coming soon ")



    def identifiers(self, genes):
        """

        s.identfiers("TP53")
        .. warning:: works for oe gene only for now
        """
        url = "identifiers/projection?pageSize=8000&page=1&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL"

        genes = self.devtools.list2string(genes)
        genes = genes.replace(" ","")
        print(genes)
        res = self.http_post(url, frmt="json", data=genes,
                headers={"Content-Type": "text/plain;charset=UTF-8", 
                    "Accept": "application/json"})
        return res





