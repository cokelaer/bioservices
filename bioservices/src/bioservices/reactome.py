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
#$Id: $
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


from services import WSDLService, RESTService
import webbrowser
import copy



class ReactomeURL(RESTService):

    _url = "http://www.reactome.org/cgi-bin"
    def __init__(self, verbose=True):
        super(ReactomeURL, self).__init__("Reactome(URL)",url=ReactomeURL._url,
            verbose=verbose)

    def link(self, source, identifier):
        """Linking to Reactome

        This can be achieved by creating URLs containing the name of and
        an identifier from an "external" database in the following format::

            r.link("COMPOUND", "C00002") #  COMPOUND identifiers, e.g. COMPOUND:C00002
            r.link("UNIPROT", "P30304")  #  UniProt accession numbers and identifiers, e.g. UNIPROT:P30304
            r.link("CHEBI", "15422")     #  ChEBI identifiers, e.g. CHEBI:15422

        """
        url = self.url + "/link?SOURCE" +  source + "&ID=" + identifier
        res = self.request(url)
        return res



class Reactome(WSDLService):
    """Interface to the `Reactome <http://www.reactome.org>`_ service

    :in progress: dont use


    """
    _url = "http://www.reactome.org:8080/caBIOWebApp/services/caBIOService?wsdl"
    def __init__(self, verbose=True):
        """Constructor

        :param bool verbose:

        """
        super(Reactome, self).__init__(name="Reactome", url=Reactome._url, verbose=verbose)

    def version(self):
        r = WSDLService("version", "http://www.reactome.org:8080/caBIOWebApp/services/Version?wsdl")
        res = r.serv.getVersion()
        print res

    def queryPathwaysForReferenceIdentifiers(self, list_ids):
        """

            res = r.queryPathwaysForReferenceIdentifiers(["Q9Y266", "P17480", "P20248"])
            res[0]
            res[0].species.scientificName

        """
        results = self.serv.queryPathwaysForReferenceIdentifiers(list_ids)

        # We could return the raw results but it is not really readable.
        # Let use ReactomePathway class
        queries = []
        for res in results:
            queries.append(ReactomePathway(res))
        return queries

    def generatePathwayDiagramInSVG(self, Id):
        return self.serv.generatePathwayDiagramInSVG(Id)


    def listTopLevelPathways(self):
        """

            res = r.listTopLevelPathways()
            [x.id for x in res]

        """
        return self.serv.listTopLevelPathways()

    def getMaxSizeInListObjects(self, value):
        res = self.serv.getMaxSizeInListObjects(value)
        return res

"""
[u'generatePathwayDiagramInSVG',
 u'generatePathwayDiagramInSVGForId',
 u'listByQuery',
 u'listObjects',
 u'listPathwayParticipants',
 u'listPathwayParticipantsForId',
u'loadPathwayForId',
 u'loadPathwayForObject',
 u'queryById',
 u'queryByIds',
 u'queryByObject',
 u'queryByObjects',
 u'queryPathwaysForEntities',
 u'queryPathwaysForEntityIds',
"""





#caBIOService: http://www.reactome.org:8080/caBIOWebApp/services/caBIOService?wsdl

class ReactomeBioPAXExporter(WSDLService):
    """http://www.reactome.org/entitylevelview/PathwayBrowser.html#DB=gk_current&FOCUS_SPECIES_ID=48887&FOCUS_PATHWAY_ID=177929&ID=177929"""

    def __init__(self, verbose=True, debug=False, url=None):
        self.url = "http://www.reactome.org:8080/caBIOWebApp/services/BioPAXExporter?wsdl"
        super(ReactomeBioPAXExporter, self).__init__(name="ReactomeBioPAXExporter",
            url=self.url, verbose=verbose)




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

