from services import WSDLService
import copy


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
    
       import wikipathways
       w = wikipathways.WikiPath()
       w.methods
       
       w.organism #'Homo sapiens', by default

      Examples:
            w.findPathwaysByText('MTOR')
            w.getPathway('WP1471')
            w.getPathwaysByOntologyTerm('DOID:344')
            w.findPathwaysByXref('P45985')
    """

    def __init__(self, verbose = True, debug = False, url = None):
        """Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """

        if url == None:
            url = 'http://www.wikipathways.org/wpi/webservice/webservice.php?wsdl' 
            # url = 'http://soap.genome.jp/KEGG.wsdl'
        super(Wikipath, self).__init__(name="Wikipathway",url='http://www.wikipathways.org/wpi/webservice/webservice.php?wsdl' 
, verbose = verbose)
#        self._pathways = {}
#        self.path
        self._keywords = '' 
#        print self.methods[:]
        self._organism = 'Homo sapiens' ## This function is redundant (see class service)
        if self.verbose:
            print "Fetching organisms..."
        self.organisms = Items2(self.serv.listOrganisms(),'organisms',self.verbose)

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
#    chosen_pathways = Items2(self.serv.findPathwaysByText())#query = self.keywords))
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

#    extract_pathways = property(_get_pathwayInfo_by_keywords)
#    chosen_pathways = Items2(get_pathwayInfo_by_keywords(self,'mTOR'))
    def findPathwaysByXref(self, id_list):
        if isinstance(id_list,str):
            res = self.serv.findPathwaysByXref(ids = id_list)
#        get_pathways_by_external_id.test = 
        return res 

#    def get_pathway_by_pathID(self, 

    def findInteractions(self, id_list):
        return self.serv.findInteractions(query = id_list)

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

    def getPathwayAs(self, filetype, pathwayId, revisionNumb = 0):
        return self.serv.getPathwayAs(fileType = filetype, pwId = pathwayId, revision = revisionNumb)

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

    def getColoredPathway(self, pathwayId, graphIds, revisionNumb = 0, colors = None, filetype = 'pdf'):
        if colors == None:
            colors = 'FF0000' 
        return self.serv.getColoredPathway(pwId = pathwayId, revision = revisionNumb, graphId = graphIds, color = colors, fileType = filetype)

    def getXrefList(self, pathwayId, sysCode):
        return self.serv.getXrefList(pwId = pathwayId, code = sysCode)  

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

