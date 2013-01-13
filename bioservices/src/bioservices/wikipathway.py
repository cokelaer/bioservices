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


from services import WSDLService

import copy, webbrowser, xmltools, base64


class Items2(object):
    def __init__(self, data, name = 'item', verbose = True):
        self.data = data
        
        self._items = copy.deepcopy(data)
        self.definitions = self._items  ## Consider replace self_items with this variable 
#    def _get_entry_ids(self):
#    def _get_definitions(self):
#        ids = [x[

    def _get_entry_ids(self):
        ids = [x['id'] for x in self.items]
        return ids
    entry_ids = property(_get_entry_ids, doc = "return list of ids")

    def _get_names(self):
        name = [x['name'] for x in self.items]
        return name
    name = property(_get_names, doc = "return list of names")

    def _get_items(self):
        return self._items    
    items = property(_get_items,doc=_get_items.__doc__)
    #def _get_entry_ids(self):


class Wikipath(WSDLService):
    """Interface to the WikiPathways database
    
    ::
    
       import wikipathway
       w = wikipathway.WikiPath()
       w.methods
       
       w.organism #'Homo sapiens', by default

      Examples:
            w.findPathwaysByText('MTOR')
            w.getPathway('WP1471')
            w.getPathwaysByOntologyTerm('DOID:344')
            w.findPathwaysByXref('P45985')
    """
    _url = 'http://www.wikipathways.org/wpi/webservice/webservice.php?wsdl' 
    def __init__(self, verbose = True):
        """Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """

        super(Wikipath, self).__init__(name="Wikipathway", url=Wikipath._url, verbose = verbose)
#        self._pathways = {}
#        self.path
        self._keywords = '' 
#        print self.methods[:]
        self._organism = 'Homo sapiens' ## This function is redundant (see class service)
        self.logging.info("Fetching organisms...")
        self.organisms = self.serv.listOrganisms()

#        self.recentChanges = Items2(self.serv.getRecentChanges(time

    def _set_organism(self, organism):
        if organism in self.organisms.items:
            self._organism = organism         
        else:
            print "'%s' is not supported in Wikipathways" % organism

    def _get_organism(self):
        return self._organism
    organism = property(_get_organism, _set_organism, doc = "read/write attribute for the organism")

    def _set_keywords(self, keywords):
        self._keywords = keywords    

    def _get_keywords(self):
        return self._keywords
    keywords = property(_get_keywords, _set_keywords, doc = "read/write attribute for the organism")

    def findPathwaysByText(self, keywords, organism = None): 
        """Set "organism == ''" to search on all organisms
           Find a nice way to implemen the AND/OR"""
        if organism == None:
            organism = self.organism
            res = self.serv.findPathwaysByText(query = keywords, species = organism)
        else: 
            res = self.serv.findPathwaysByText(query = keywords, species = organism)
        return res

    def findPathwaysByXref(self, id_list):
        if isinstance(id_list,str):
            res = self.serv.findPathwaysByXref(ids = id_list)
        return res 

    def findInteractions(self, id_list, organism = None, raw = False, verbose = False):
        if raw:
            return self.serv.findInteractions(query = id_list)
        else:
            output = {'interactions':[],'scores':[],'pathway_ids':[],'revision':[],}
            intA = []
            intB = []
            if organism == None:
                organism = self.organism
            for x in self.serv.findInteractions(query = id_list):
                if x['species'] == organism:
                    intA.append(x['fields'][1]['values'])
                    intB.append(x['fields'][2]['values'])
                    output['scores'].append(x['score'])
                    output['pathway_ids'].append(x['id'])
                    output['revision'].append(x['revision'])
            output['interactions'] = zip(intA,intB)
            if verbose:
                return output 
            else:
                return output['interactions']

    def listPathways(self, organism = None):
        if organism == None:
            return self.serv.listPathways(organism = self.organism)
        else:
            return self.serv.listPathways(organism = organism)
#    def lookfor_pathway(

    def getPathway(self, pathwayId, revisionNumb = 0):
        return self.serv.getPathway(pwId = pathwayId, revision = revisionNumb) 

    def getPathwayInfo(self, pathwayId):
        return self.serv.getPathwayInfo(pwId = pathwayId)

    def getPathwayHistory(self, pathwayId, date):
        return self.serv.getPathwayHistory(pwId = pathwayId, timestamp = date)

    def getRecentChanges(self, dateNtime):
        return self.serv.getRecentChanges(timestamp = dateNtime)

#    def login(self, usrname, password):
#        return self.serv.login(name = usrname, pass = password)

    def getPathwayAs(self, pathwayId, filetype = 'owl', revisionNumb = 0, verbose = False):
        res = self.serv.getPathwayAs(fileType = filetype, pwId = pathwayId, revision = revisionNumb)
        if verbose:
            return res
        else:
            return base64.b64decode(res)

    def savePathwayAs(self, pathwayId, filename, revisionNumb = 0, display = True):
        if filename.find('.') == -1:
            filename = "%s.%s" %(filename,'pdf')  
        filetype = filename.split('.')[-1]
        res = self.serv.getPathwayAs(fileType = filetype, pwId = pathwayId, revision = revisionNumb)
        f = open(filename,'w')
        f.write(base64.b64decode(res))
        if display:
            webbrowser.open(filename)
        f.close()

    def displaySavedPathwayInBrowser(self, filename):
        webbrowser.open(filename)
        
    def updatePathway(self, pathwayId, describeChanges, gpmlCode, revisionNumb, authInfo):
        return self.serv.updatePathway(pwId = pathwayId, description = describeChanges, gpml = gpmlCode, revision = revisionNumb, auth = authInfo) 

    def createPathway(self, gpmlCode, authInfo):
        return self.serv.createPathway(gpml = gpmlCode, auth = authInfo) 

    def saveCurationTag(self, pathwayId, name, revisionNumb, authInfo, text = None):
        if text == None:
           res = self.serv.saveCurationTag(pwId = pathwayId, tagName = name, revision = revisionNumb, auth = authInfo)
        else:
           res =  self.serv.saveCurationTag(pwId = pathwayId, tagName = name, tagText = text, revision = revisionNumb, auth = authInfo) 
        return res

    def removeCurationTag(self, pathwayId, name, authInfo):
        return self.serv.removeCurationTag(pwId = pathwayId, tagName = name, auth = authInfo)

    def getCurationTags(self, pathwayId):
        return self.serv.getCurationTags(pwId = pathwayId)

    def getCurationTagsByName(self, name):
        return self.serv.getCurationTagsByName(tagName = name)

#    def getColoredPathway(self, pathwayId, graphIds, revisionNumb = 0, colors = None, filetype = 'pdf', verbose = False):
#        if colors == None:
#            colors = 'FF0000' 
#        res = self.serv.getColoredPathway(pwId = pathwayId, revision = revisionNumb, graphId = graphIds, color = colors, fileType = filetype)
#        if verbose:
#            return res
#        else:
#            return base64.b64decode(res)

#    def getXrefList(self, pathwayId, sysCode):
#        return self.serv.getXrefList(pwId = pathwayId, code = sysCode)  

    def findPathwaysByLiterature(self, refQuery):
        return self.serv.findPathwaysByLiterature(query = refQuery)

    def getOntologyTermsByPathway(self, pathwayId):
        return self.serv.getOntologyTermsByPathway(pwId = pathwayId) 

    def getOntologyTermsByOntology(self, ontologyTerm):
        return self.serv.getOntologyTermsByOntology(ontology = ontologyTerm) 

    def getPathwaysByOntologyTerm(self, ontologyTermId):
        return self.serv.getPathwaysByOntologyTerm(term = ontologyTermId)

    def getPathwaysByParentOntologyTerm(self, ontologyTermId):
        return self.serv.getPathwaysByParentOntologyTerm(term = ontologyTermId)

    def showPathwayInBrowser(self, pathwayId):
        url = self.serv.getPathwayInfo(pwId=pathwayId).url
        webbrowser.open(url)

#    def get_genes_by_pathway(self, pathwayId):
#        
        
