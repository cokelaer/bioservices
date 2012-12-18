# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2012 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://www.ebi.ac.uk/~cokelaer/bioservices
#
##############################################################################
"""This module provides a class :class:`~Reactome` that allows an easy access MIRIAM registry service.

"""


from services import Service
import webbrowser
import copy



class Reactome(Service):
    """Interface to the Reactome service

    ::


    """
    def __init__(self, verbose=True, debug=False, url=None):
        """Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """
        if url == None:
            url = "http://www.reactome.org:8080/caBIOWebApp/services/caBIOService?wsdl"

        super(Reactome, self).__init__(name="Reactome", url=url, verbose=verbose)


    def queryPathwaysForReferenceIdentifiers(self, list_ids):
        """

            res = r.queryPathwaysForReferenceIdentifiers(["Q9Y266", "P17480", "P20248"])

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

        """
	return self.serv.listTopLevelPathways()

"""
[u'generatePathwayDiagramInSVG',
 u'generatePathwayDiagramInSVGForId',
 u'getMaxSizeInListObjects',
i
 u'listByQuery',
 u'listObjects',
 u'listPathwayParticipants',
 u'listPathwayParticipantsForId',
 u'listTopLevelPathways',

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

class ReactomeBioPAXExporter(Service):
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

