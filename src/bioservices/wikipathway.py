# -*- python -*-
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
# $Id: $
"""Interface to the WikiPathway service

.. topic:: What is WikiPathway ?


    :URL: http://www.wikipathways.org/index.php/WikiPathways
    :WSDL: http://www.wikipathways.org/index.php/Help:WikiPathways_Webservice/API
    :Citation: `doi:10.1371/journal.pone.0006447 <http://www.plosone.org/article/info:doi/10.1371/journal.pone.0006447>`_

    .. highlights::

        " WikiPathways is an open, public platform dedicated to the curation of
        biological pathways by and for the scientific community."

        -- From WikiPathway web site. Dec 2012



"""
from bioservices.services import WSDLService, RESTService
import copy, webbrowser,  base64


__all__ = ["Wikipathway", "WikiPathways"]


# this is useless but let us keep for now
class _Items2(object):
    def __init__(self, data, name='item', verbose=True):
        self.data = data

        self._items = copy.deepcopy(data)
        self.definitions = self._items  # Consider replace self_items with this variable
#    def _get_entry_ids(self):
#    def _get_definitions(self):
#        ids = [x[

    def _get_entry_ids(self):
        ids = [x['id'] for x in self.items]
        return ids
    entry_ids = property(_get_entry_ids, doc="return list of ids")

    def _get_names(self):
        name = [x['name'] for x in self.items]
        return name
    name = property(_get_names, doc="return list of names")

    def _get_items(self):
        return self._items
    items = property(_get_items, doc=_get_items.__doc__)
    #def _get_entry_ids(self):

class Wikipathway(object):
    def __init__(self):
        raise(ValueError("Please use WikiPathways class instead. Renamed in version 1.3.0"))

class WikiPathways(WSDLService):
    """Interface to `Pathway <http://www.wikipathways.org/index.php>`_ service

    .. doctest::

       >>> from bioservices import WikiPathways
       >>> s = Wikipathway()
       >>> s.organism  # default organism
       'Homo sapiens'

    Examples::

        s.findPathwaysByText('MTOR')
        s.getPathway('WP1471')
        s.getPathwaysByOntologyTerm('DOID:344')
        s.findPathwaysByXref('P45985')

    The methods that require a login are not implemented (:meth:`login`,
    :meth:`updatePathway`, :meth:`removeCurationTag`, :meth:`saveCurationTag`,
    :meth:`createPathway`)

    Methods not implemented at all:

      * getXrefList: Neither WSDL or REST seemed to work
      * u'getCurationTagHistory': No API found in Wikipathway web page
      * u'getRelations': No API found in Wikipathway web page
    """
    _url = 'http://www.wikipathways.org/wpi/webservice/webservice.php?wsdl'
    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param bool verbose:

        """

        super(WikiPathways, self).__init__(name="WikiPathways", 
                url=WikiPathways._url, verbose=verbose, cache=cache)
        self._organism = 'Homo sapiens' # This function is redundant (see class service)
        self.logging.info("Fetching organisms...")

        #: Get a list of all available organisms.
        self.organisms = self.serv.listOrganisms()

#        self.recentChanges = Items2(self.serv.getRecentChanges(time

    def _set_organism(self, organism):
        if organism in self.organisms:
            self._organism = organism
        else:
            raise ValueError("'%s' is not supported in WikiPathways. See :attr:`organisms`" % organism)

    def _get_organism(self):
        return self._organism
    organism = property(_get_organism, _set_organism, doc = "Read/write attribute for the organism")

    # REST /findPathwaysByLiterature?query=18651794
    def findPathwaysByLiterature(self, query):
        """Find pathways by their literature references.

        :param str query: The query, can be a pubmed id, author name or title keyword.
        :return:  Array of WSSearchResult descr=The search results. {{{descr}}}

        ::

            s.findPathwaysByLiterature(18651794)
        """
        res = self.serv.findPathwaysByLiterature(query=query)
        return res

    def findPathwaysByXref(self, ids):
        """Find pathways by searching on the external references of DataNodes.


        This function supports only 1 ids and 1 code at a time. To specify
        multiple ids and codes parameters to query for multiple xrefs at once,
        the REST syntax should be used. In that case, the number of ids and
        codes parameters should match, they will be paired to form xrefs,
        e.g.::

            >>> from bioservices import RESTService
            >>> r = RESTService("test", url=s.url[:-5])
            >>> r.request('/findPathwaysByXref?ids=1234&ids=ENSG00000130164&codes=L&codes=EnHs')
            >>> r.request('/findPathwaysByXref?ids=1234&codes=L')

        :param str string ids: One DataNode identifier(s) (e.g. 'P45985').
            Datanodes can be (gene/protein/metabolite identifiers). 
        :param str codes: One code of the database system to limit the search
            to. **Not implemented**.
        :return:  List of WSSearchResult. An array of search results with DataNode GraphId stored in the 'field' hash.


        ::

            >>> s.findPathwaysByXref(ids="P45985")


        .. warning:: **codes** is not available. Does not seem to work in WSDLinterface.
        """
        # codes=code but does not seem to work
        res = self.serv.findPathwaysByXref(ids=ids)
        return res

    # REST: s.url[:-5] + ?query=P53
    def findInteractions(self, query, organism=None,
            interactionOnly=True, raw=False):
        """Find interactions defined in WikiPathways pathways.


        :param str query:  The name of an entity to find interactions for (e.g. 'P53')
        :param str organism:  The name of the organism to refine the search
            (default is the :attr: 'organism' attribute).
        :param bool interactionOnly: Returns only the interactions (default). If
            false, returns also scores, revision, pathways
        :param bool raw: If True, returns the output of the request without post processing (also ignoring organism)
        :returns: Depends on the parameters **raw** and **interactionOnly**. By default, 
            the output from WikiPathways is processed and only the interactions
            are returned (for the default organism). You can change this behaviour
            by changing the default arguments (raw, organism, interactionOnly)

        .. warning:: Interface different from the service, unless raw is set to True

        """
        if raw:
            return self.serv.findInteractions(query=query)
        else:
            output = {'interactions':[],'scores':[],'pathway_ids':[],'revision':[],}
            intA = []
            intB = []
            if organism is None:
                organism = self.organism
            for x in self.serv.findInteractions(query=query):
                if len(x) == 0:
                    continue
                if hasattr(x, 'species') is False:
                    continue
                if x['species'] == organism:
                    intA.append(x['fields'][1]['values'])
                    intB.append(x['fields'][2]['values'])
                    output['scores'].append(x['score'])
                    output['pathway_ids'].append(x['id'])
                    output['revision'].append(x['revision'])
            output['interactions'] = zip(intA,intB)
            if interactionOnly is False:
                return output
            else:
                return output['interactions']

    def listPathways(self, organism = None):
        """Get a list of all available pathways.

        :param str organism: a valid organism (default is the :attr:`organism` attribute)
        :return: List of pathways for the selected organism.

        """
        if organism is None:
            return self.serv.listPathways(organism = self.organism)
        else:
            self.devtools.check_param_in_list(organism, self.organisms)
            return self.serv.listPathways(organism = organism)

    def getPathway(self, pathwayId, revision=0):
        """Download a pathway from WikiPathways.

        :param str pathwayId: the pathway identifier.
        :param int revision: the revision number of the pathway (use '0'
            for most recent version).
        :Returns: The pathway.

        ::

            s.getPathway("WP2320")
        """
        return self.serv.getPathway(pwId=pathwayId, revision=revision)

    def getPathwayInfo(self, pathwayId):
        """Get some general info about the pathway.

        :param str pathwayId: the pathway identifier.
        :return: The pathway info.

        ::

            >>> from bioservices import *
            >>> s= Wikipathway(verbose=False)
            >>> s.getPathwayInfo("WP2320")
        """
        return self.serv.getPathwayInfo(pwId=pathwayId)

    def getPathwayHistory(self, pathwayId, date):
        """Get the revision history of a pathway.

        :param str pathwayId: the pathway identifier.
        :param str date: limit the results by date, only history items after
            the given date (timestamp format) will be included. Can be a string
            or number of the form YYYYMMDDHHMMSS.
        :return: The revision history.

        .. warning:: Does not seem to work with WSDL. Replaced by a REST version but
            unstable: Does not return the results systematically.

        ::

            s.getPathwayHistory("WP4", 20110101000000)
        """
        s = RESTService("WP", url=self.url[:-5], verbose=False)
        res = s.request("getPathwayHistory?pwId=%s&timestamp=%s" % (pathwayId, str(date)))
        return res
        # does not seem to work
        #return self.serv.getPathwayHistory(pwId=pathwayId, timestamp=date)

    def getRecentChanges(self, timestamp):
        """Get the recently changed pathways.

        :param str timestamp: Only get changes from after this time. Timestamp
            format: yyyymmddMMHHSS (string or number)
        :return: The changed pathways

        ::

            s.getRecentChanges(20110101000000)
        """
        return self.serv.getRecentChanges(timestamp=timestamp)

    def login(self, usrname, password):
        """Start a logged in session using an existing WikiPathways account.

        .. warning:: Interface not exposed in bioservices.

        This function will return an authentication code that can
        be used to excecute methods that need authentication (e.g.
        updatePathway).

        :param str name: The username of the WikiPathways account.
        :param str password: The password of the WikiPathways account.


        :Returns: The authentication code for this session.

        """
        raise NotImplementedError
        # for future usage. pass is a python keyword so we must use a dictionary
        #d = {"name":usrname, "pass":password}
        #return self.serv.login(**d)

    def getPathwayAs(self, pathwayId, filetype='owl', revisionNumb=0):
        """Download a pathway in the specified file format.

        :param str pathwayId: the pathway identifier.
        :param str filetype: the file format (default is .owl).
        :param int revision: the revision number of the pathway (use '0' for most recent version - this is default).
        :return: The file contents

        .. warning:: Argument pathwayId and filetype are inversed as compared to the
            WSDL prototype (if you want to call it directly)

        .. versionchanged:: 1.3.0 return raw output of the service without any parsing

        .. note:: use :meth:`savePathwayAs` to save into a file.
        """
        self.devtools.check_param_in_list(filetype, ['gpml', 'png', 'svg', 'pdf', 'txt', 'pwf', 'owl'])
        res = self.serv.getPathwayAs(fileType=filetype, pwId=pathwayId, 
             revision = revisionNumb)
        return res

    def savePathwayAs(self, pathwayId, filename, revisionNumb=0, display=True):
        """Save a pathway.

        :param str pathwayId: the pathway identifier.
        :param str filename: the name of the file. If a filename extension 
            is not provided the pathway will be saved as a pdf (default).
        :param int revisionNumb: the revision number of the pathway (use 
            '0 for most recent version).
        :param bool display: if True the pathway will be displayed in your 
            browser.

        .. note:: Method from bioservices. Not a WikiPathways function
        """
        if filename.find('.') == -1:
            filename = "%s.%s" %(filename,'pdf')
        filetype = filename.split('.')[-1]

        res = self.getPathwayAs(pathwayId, filetype=filetype,
            revisionNumb=revisionNumb)
        with open(filename,'wb') as f:
            import binascii
            try:
                #python3
                newres = binascii.a2b_base64(bytes(res, "utf-8"))
            except:
                newres = binascii.a2b_base64(res)
            f.write(newres)

        if display:
            webbrowser.open(filename)
        f.close()

    def displaySavedPathwayInBrowser(self, filename):
        """Show a saved document in a browser.

        :param str filename:
        :return: Nothing
        
        .. note:: Method from Bioservices. Not a WikiPathways function.
        """
        webbrowser.open(filename)

    def updatePathway(self, pathwayId, describeChanges, gpmlCode, revision=0):
        """Update a pathway on WikiPathways website with a given GPML code.

        .. warning:: Interface not exposed in bioservices.

        .. note:: To create/modify pathways via the web service, you need to
            have an account with web service write permissions. Please contact
            us to request write access for the web service.

        :param str pwId:  The pathway identifier.
        :param str description:  A description of the modifications.
        :param str gpml: The updated GPML code.
        :param int revision: The revision number of the version this GPML
            code was based on. This is used to prevent edit conflicts in
            case another client edited the pathway after this client downloaded it.
        :param object WSAuth_auth:  The authentication info.

        :returns: Boolean. True if the pathway was updated successfully.
        """
        #self.authInfo
        raise NotImplementedError
        #return self.serv.updatePathway(pwId = pathwayId,
        #description = describeChanges, gpml = gpmlCode, revision = revisionNumb, auth = authInfo)

    def createPathway(self, gpmlCode, authInfo):
        """Create a new pathway on the WikiPathways website with a given GPML code.

        .. warning:: Interface not exposed in bioservices.

        .. note:: To create/modify pathways via the web service, you need to
            have an account with web service write permissions. Please
            contact us to request write access for the web service.

        :param str gpml: The GPML code.
        :param object WSAuth auth: The authentication info.
        :returns: WSPathwayInfo The pathway info for the created pathway
            (containing identifier, revision, etc.).

        """
        raise NotImplementedError
        #return self.serv.createPathway(gpml = gpmlCode, auth = authInfo)

    #def saveCurationTag(self, pathwayId, name, revisionNumb, authInfo, text = None):
    def saveCurationTag(self, pathwayId, name, revisionNumb):
        """Apply a curation tag to a pathway. This operation will overwrite any existing tag with the same name.

        .. warning:: Interface not exposed in bioservices.

        :param str pathwayId: the pathway identifier.
        """
        raise NotImplementedError
        # use the login function to store the authInfo argument
        #if text is None:
        #   res = self.serv.saveCurationTag(pwId = pathwayId, tagName = name, revision = revisionNumb, auth = authInfo)
        #else:
        #   res =  self.serv.saveCurationTag(pwId = pathwayId, tagName = name, tagText = text, revision = revisionNumb, auth = authInfo)
        #return res

    def removeCurationTag(self, pathwayId, name):
        """Remove a curation tag from a pathway.

        .. warning:: Interface not exposed in bioservices.

        """
        #self.authInfo
        raise NotImplementedError
        #return self.serv.removeCurationTag(pwId = pathwayId, tagName = name, auth = authInfo)

    #REST getCurationTags?pwId=WP4
    def getCurationTags(self, pathwayId):
        """Get all curation tags for the given pathway.

        :param str pathwayId: the pathway identifier.
        :returns: Array of WSCurationTag. The curation tags.

        ::

            s.getCurationTags("WP4")
        """
        return self.serv.getCurationTags(pwId = pathwayId)

    # REST getCurationTagsByName?tagName=Curation:FeaturedPathway
    def getCurationTagsByName(self, name):
        """Get all curation tags for the given tag name.

        Use this method if you want to find all pathways that are tagged with a specific curation tag.


        :param str tagName: The tag name.
        :return: Array of WSCurationTag. The curation tags (one instance for each pathway that has been tagged).

        ::

            s.getCurationTagsByName("Curation:FeaturedPathway")
        """
        return self.serv.getCurationTagsByName(tagName = name)

    def getColoredPathway(self, pathwayId, filetype="svg", revision=0):
        """Get a colored image version of the pathway. 


        :param str pwId: The pathway identifier.
        :param int revision: The revision number of the pathway (use '0' for most recent version). 
        :param str fileType:  The image type (One of 'svg', 'pdf' or 'png'). Not
            yet implemented. svg is returned.
        :returns: Binary form of the image.


        .. todo:: graphId, color parameters
        """
        #graphIds, revisionNumb = 0, colors = None, filetype = 'pdf', verbose = False):
        #if colors is None:
        #    colors = 'FF0000'
        #res = self.serv.getColoredPathway(pwId = pathwayId, revision = revisionNumb, graphId = graphIds, color = colors, fileType = filetype)
        res = self.serv.getColoredPathway(pwId=pathwayId, revision=revision)
        #if verbose:
        #    return res
        #else:
        return base64.b64decode(res)

    #def getXrefList(self, pathwayId, sysCode):
    #    """http://www.pathvisio.org/wiki/DatabasesMapps#Supporteddatabasesystems"""
    #    return self.serv.getXrefList(pwId = pathwayId, code = sysCode)

    def findPathwaysByText(self, query, species=None):
        """Find pathways using a textual search on the description and text labels of the pathway objects.

        The query syntax offers several options:

        * Combine terms with AND and OR. Combining terms with a space is equal
          to using OR ('p53 OR apoptosis' gives the same result as 'p53 apoptosis').
        * Group terms with parentheses, e.g. '(apoptosis OR mapk) AND p53'
        * You can use wildcards * and ?. * searches for one or more
          characters, ? searches for only one character.
        * Use quotes to escape special characters. E.g. '"apoptosis*"' will
          include the * in the search and not use it as wildcard.

        This function supports REST-style invocation.
        Example: http://www.wikipathways.org/wpi/webservice/webservice.php/findPathwaysByText?query=apoptosis

        :param str query: The search query (e.g. 'apoptosis' or 'p53').
        :param str species:  The species to limit the search to (leave blank to search on all species).
        :return: Array of WSSearchResult An array of search results.

        ::

            s.findPathwaysByText(query="p53 OR mapk",species='Homo sapiens')
        """
        if species is None:
            return self.serv.findPathwaysByText(query=query)
        else:
            return self.serv.findPathwaysByText(query=query,species=species)

    def getOntologyTermsByPathway(self, pathwayId):
        """Get a list of ontology terms for a given pathway.


        :param str pathwayId: the pathway identifier.
        :return: Array of WSOntologyTerm. The ontology terms.

        ::

            s.getOntologyTermsByPathway("WP4")
        """
        return self.serv.getOntologyTermsByPathway(pwId=pathwayId)

    # REST getOntologyTermsByOntology?ontology=Disease
    def getOntologyTermsByOntology(self, ontologyTerm):
        """Get a list of ontology terms from a given ontology.


        :param str ontology: The ontology term (for possible values, see the Ontology Tags section on the pathway page at WikiPathways website.
        :return: List of WSOntologyTerm The ontology terms.

        ::

            >>> from bioservices import WikiPathways
            >>> s = WikiPathway()
            >>> s.getOntologyTermsByOntology("Disease")

        """
        return self.serv.getOntologyTermsByOntology(ontology = ontologyTerm)

    #REST getPathwaysByOntologyTerm?term=DOID:344
    def getPathwaysByOntologyTerm(self, ontologyTermId):
        """Get a list of pathways tagged with a given ontology term.


        :param str ontologyTermId: the ontology term identifier.
        :returns: List of WSPathwayInfo. The pathway information.

        ::

            >>> from bioservices import WikiPathways
            >>> s = Wikipathway()
            >>> s.getPathwaysByOntologyTerm('DOID:344')

        """
        return self.serv.getPathwaysByOntologyTerm(term=ontologyTermId)

    #REST getPathwaysByParentOntologyTerm?term=DOID:344
    def getPathwaysByParentOntologyTerm(self, ontologyTermId):
        """Get a list of pathways tagged with any ontology term that is the child of the given Ontology term.


        :param str ontologyTermId: the ontology term identifier.
        :returns: List of WSPathwayInfo The pathway information.


        """
        return self.serv.getPathwaysByParentOntologyTerm(term = ontologyTermId)

    def showPathwayInBrowser(self, pathwayId):
        """Show a given Pathway into your favorite browser.

        :param str pathwayId: the pathway identifier.

        .. note: This is an additional bioservices functionality (not a
            wikipathway one) showing a wikipathway URL.

        """
        url = self.serv.getPathwayInfo(pwId=pathwayId).url
        webbrowser.open(url)

