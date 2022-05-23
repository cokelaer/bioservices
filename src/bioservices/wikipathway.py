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
"""Interface to the WikiPathway service

.. topic:: What is WikiPathway ?

    :URL: http://www.wikipathways.org/index.php/WikiPathways
    :REST: http://webservice.wikipathways.org/
    :Citation: `doi:10.1371/journal.pone.0006447 <http://www.plosone.org/article/info:doi/10.1371/journal.pone.0006447>`_

    .. highlights::

        " WikiPathways is an open, public platform dedicated to the curation of
        biological pathways by and for the scientific community."

        -- From WikiPathway web site. Dec 2012

"""
from bioservices.services import REST
import copy, webbrowser, base64

import pandas as pd

__all__ = ["WikiPathways"]


class WikiPathways(REST):
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

      * u'getCurationTagHistory': No API found in Wikipathway web page
      * u'getRelations': No API found in Wikipathway web page
    """

    _url = "http://webservice.wikipathways.org/"

    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(WikiPathways, self).__init__(name="WikiPathways", url=WikiPathways._url, verbose=verbose, cache=cache)
        self._organism = "Homo sapiens"  # This function is redundant (see class service)
        self.logging.info("Fetching organisms...")

        #: Get a list of all available organisms.
        self.organisms = self.listOrganisms()

    def listOrganisms(self):
        res = self.http_get(self.url + "/listOrganisms?format=json")
        return res["organisms"]

    def _set_organism(self, organism):
        if organism in self.organisms:
            self._organism = organism
        else:
            raise ValueError("'%s' is not supported in WikiPathways. See :attr:`organisms`" % organism)

    def _get_organism(self):
        return self._organism

    organism = property(_get_organism, _set_organism, doc="Read/write attribute for the organism")

    def findPathwaysByLiterature(self, query):
        """Find pathways by their literature references.

        :param str query: The query, can be a pubmed id, author name
            or title keyword.
        :return:  dictionary with Pathway as keys

        ::

            res = s.findPathwaysByLiterature(18651794)

        """
        params = {"format": "json", "query": query}
        res = self.http_get(self.url + "findPathwaysByLiterature", params=params)

        return res["result"]

    def findPathwaysByXref(self, ids, codes=None):
        """Find pathways by searching on the external references of DataNodes.

        :param str string ids: One or mode DataNode identifier(s) (e.g. 'P45985').
            Datanodes can be (gene/protein/metabolite identifiers). For one
            node, you can use a string (or number) or list of one identifier.
            you can also provide a list of identifiers.
        :param str codes: You can restrict the search to a specific database.
            See http://developers.pathvisio.org/wiki/DatabasesMapps#Supporteddatabasesystems
            for details. Examples are "L" for entrez gene, "En" for ensembl. See
            also the note here below for multiple identifiers/codes.
        :return:  a dictionary

        ::

            >>> s.findPathwaysByXref(ids="P45985")
            >>> s.findPathwaysByXref(ids="P45985", codes="L")
            >>> s.findPathwaysByXref(ids=["P45985"], codes=["L"])
            >>> s.findPathwaysByXref(ids=["P45985", "ENSG00000130164"], codes=["L", "En"])


        Note that in the last example, we specify multiple ids and codes
        parameters to query for multiple xrefs at once. In that case, the
        number of ids and codes parameters should match. Moreover, they will
        be paired to form xrefs, so P45985 is searched for in the "L"
        database while "ENSG00000130164" is searched for in the En" database
        only.
        """
        url = self.url + "/findPathwaysByXref?ids="
        if isinstance(ids, (str, int, float)):
            url += "{}".format(ids)
        elif isinstance(ids, list):
            if len(ids) == 0:
                raise ValueError("ids must be a non-empty list")
            if len(ids) >= 1:
                url += "{}".format(ids[0])
            if len(ids) > 1:
                for this in ids[1:]:
                    url += "&ids={}".format(this)
        else:
            raise ValueError("ids must be a list, or a string or a number")

        if codes and isinstance(codes, (str, int)):
            codes = [codes]
        if codes:
            for code in codes:
                url += "&codes={}".format(code)
        res = self.http_get(url + "&format=json")

        # results = pd.DataFrame(results)

        return res

    def findInteractions(self, query):
        """Find interactions defined in WikiPathways pathways.


        :param str query:  The name of an entity to find interactions for (e.g. 'P53')
        :returns: list of dictionaries

        ::

            res = w.findInteractions("P53")

        """
        url = self.url + "findInteractions?query={}&format=json".format(query)
        res = self.http_get(url)["result"]

    def listPathways(self, organism=None):
        """Get a list of all available pathways.

        :param str organism: If provided, the data is filtered to keep only
            the organism  provided, which must be a valid name (check out
            :attr:`organism` attribute)
        :return: dataframe. Index are the pathways identifiers (e.g. WP1)

        .. plot::

            from bioservices import WikiPathways
            w = WikiPathways()
            df = w.listPathways()
            df.groupby("species").count()['name'].sort_values().plot(kind="barh")
        """
        if organism:
            self.devtools.check_param_in_list(organism, self.organisms)
            request = self.http_get("/listPathways?%s&format=json" % organism)
        else:
            request = self.http_get("/listPathways?format=json")
        pathways = request["pathways"]

        pathways = pd.DataFrame(pathways).set_index("id")
        return pathways

    def getPathway(self, pathwayId, revision=0):
        """Download a pathway from WikiPathways.

        :param str pathwayId: the pathway identifier.
        :param int revision: the revision number of the pathway (use '0'
            for most recent version).
        :Returns: The pathway as a dictionary. The pathway is stored in gpml
            format.

        ::

            s.getPathway("WP2320")
        """
        url = "getPathway?pwId=%s" % pathwayId
        url += "&revision=%s&format=json" % revision
        request = self.http_get(url)

        return request["pathway"]

    def getPathwayInfo(self, pathwayId):
        """Get some general info about the pathway.

        :param str pathwayId: the pathway identifier.
        :return: The pathway info.

        ::

            >>> from bioservices import *
            >>> s = Wikipathway()
            >>> s.getPathwayInfo("WP2320")
        """
        url = "/getPathwayInfo?pwId=%s" % pathwayId
        request = self.http_get(url)
        data = self.easyXML(request.content)
        data = data.findAll("ns1:pathwayinfo")
        pathway = {}
        for this in data:
            for tag in ["id", "url", "name", "species", "revision"]:
                text = this.find("ns2:%s" % tag).getText()
                pathway[tag] = text
        return pathway

    def getPathwayHistory(self, pathwayId, date):
        """Get the revision history of a pathway.

        :param str pathwayId: the pathway identifier.
        :param str date: limit the results by date, only history items after
            the given date (timestamp format) will be included. Can be a string
            or number of the form YYYYMMDDHHMMSS.
        :return: The revision history.

        .. warning:: seems unstable does not return the results systematically.

        ::

            s.getPathwayHistory("WP4", 20110101000000)

        """

        query = self.url + "/getPathwayHistory?pwId=%s&timestamp=%s" % (
            pathwayId,
            str(date),
        )
        query += "&format=json"
        return self.http_get(query)

    def getRecentChanges(self, timestamp):
        """Get the recently changed pathways.

        :param str timestamp: Only get changes from after this time. Timestamp
            format: yyyymmddMMHHSS (string or number)
        :return: The changed pathways in XML format

        ::

            s.getRecentChanges(20110101000000)

        .. todo:: interpret XML
        """
        res = self.http_get(self.url + "/getRecentChanges?timestamp=%s&format=json" % timestamp)
        return res

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
        # d = {"name":usrname, "pass":password}
        # return self.serv.login(**d)

    def getPathwayAs(self, pathwayId, filetype="png", revision=0):
        """Download a pathway in the specified file format.

        :param str pathwayId: the pathway identifier.
        :param str filetype: the file format (default is .owl).
        :param int revision: the revision number of the pathway (use '0' for most recent version - this is default).
        :return: The file contents

        .. versionchanged:: 1.3.0 return raw output of the service without any parsing

        .. note:: use :meth:`savePathwayAs` to save into a file.
        """
        self.devtools.check_param_in_list(filetype, ["gpml", "png", "svg", "pdf", "txt", "pwf", "owl"])

        url = self.url + "/getPathwayAs?fileType=%s" % filetype
        url += "&pwId=%s " % pathwayId
        url += "&revision=%s&format=json" % revision
        res = self.http_get(url)
        return res["data"]

    def savePathwayAs(self, pathwayId, filename, revision=0, display=True):
        """Save a pathway.

        :param str pathwayId: the pathway identifier.
        :param str filename: the name of the file. If a filename extension
            is not provided the pathway will be saved as a pdf (default).
        :param int revisionNumb: the revision number of the pathway (use
            '0 for most recent version).
        :param bool display: if True the pathway will be displayed in your
            browser.

        .. note:: Method from bioservices. Not a WikiPathways function
        .. versionchanged:: 1.7 return PNG by default instead of PDF. PDF
            not working as of 20 Feb 2020 even on wikipathway website.
        """
        if filename.find(".") == -1:
            filename = "%s.%s" % (filename, "pdf")
        filetype = filename.split(".")[-1]

        res = self.getPathwayAs(pathwayId, filetype=filetype, revision=revision)

        with open(filename, "wb") as f:
            import binascii

            try:
                # python3
                newres = binascii.a2b_base64(bytes(res, "utf-8"))
            except:
                newres = binascii.a2b_base64(res)
            f.write(newres)

        if display:
            webbrowser.open(filename)
        f.close()

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
        raise NotImplementedError
        # return self.serv.updatePathway(pwId = pathwayId,
        # description = describeChanges, gpml = gpmlCode, revision = revisionNumb, auth = authInfo)

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
        # return self.serv.createPathway(gpml = gpmlCode, auth = authInfo)

    def saveCurationTag(self, pathwayId, name, revision):
        """Apply a curation tag to a pathway. This operation will overwrite any existing tag with the same name.

        .. warning:: Interface not exposed in bioservices.

        :param str pathwayId: the pathway identifier.
        """
        raise NotImplementedError

    def removeCurationTag(self, pathwayId, name):
        """Remove a curation tag from a pathway.

        .. warning:: Interface not exposed in bioservices.

        """
        raise NotImplementedError

    def getCurationTags(self, pathwayId):
        """Get all curation tags for the given pathway.

        :param str pathwayId: the pathway identifier.
        :returns: Array of WSCurationTag. The curation tags.

        ::

            s.getCurationTags("WP4")
        """
        raise NotImplementedError

    def getCurationTagsByName(self, name):
        """Get all curation tags for the given tag name.

        Use this method if you want to find all pathways that are tagged with a specific curation tag.


        :param str tagName: The tag name.
        :return: Array of WSCurationTag. The curation tags (one instance for each pathway that has been tagged).

        ::

            s.getCurationTagsByName("Curation:FeaturedPathway")
        """
        raise NotImplementedError

    def getColoredPathway(self, pathwayId, filetype="svg", revision=0, color=None, graphId=None):
        """Get a colored image version of the pathway.

        :param str pwId: The pathway identifier.
        :param int revision: The revision number of the pathway (use '0' for most recent version).
        :param str fileType:  The image type (One of 'svg', 'pdf' or 'png'). Not
            yet implemented. svg is returned for now.
        :returns: Binary form of the image.

        .. todo:: graphId, color parameters
        """

        url = self.url + "getColoredPathway?pwId={}".format(pathwayId)
        if revision:
            url += "&revision={}".format(revision)
        url += "&format=json"
        request = self.http_get(url)
        try:
            data = request["data"]
            return base64.b64decode(data)
        except:
            return request

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

        .. warning:: AND or OR must be in big caps
        """
        url = self.url + "/findPathwaysByText?query=%s" % query
        if species:
            url += "&species=%s" % species
        url += "&format=json"
        request = self.http_get(url)
        data = request["result"]

        try:
            data = pd.DataFrame(data).set_index("id")
        except:
            pass
        return data

    def getOntologyTermsByPathway(self, pathwayId):
        """Get a list of ontology terms for a given pathway.


        :param str pathwayId: the pathway identifier.
        :return: Array of WSOntologyTerm. The ontology terms.

        ::

            s.getOntologyTermsByPathway("WP4")
        """
        url = self.url + "getOntologyTermsByPathway?pwId={}".format(pathwayId)
        url += "&format=json"
        request = self.http_get(url)
        results = request["terms"]

        return results

    def getPathwaysByOntologyTerm(self, terms):
        """Get a list of pathways tagged with a given ontology term.

        :param str terms: the ontology term identifier.
        :returns: dataframe with pathways infomation.

        ::

            >>> from bioservices import WikiPathways
            >>> s = Wikipathway()
            >>> s.getPathwaysByOntologyTerm('PW:0000724')

        """
        url = self.url + "getPathwaysByOntologyTerm?term={}".format(terms)
        url += "&format=json"
        request = self.http_get(url)
        return request["pathways"]

    def getPathwaysByParentOntologyTerm(self, term):
        """Get a list of pathways tagged with any ontology term that is the child of the given Ontology term.

        :param str term: the ontology term identifier.
        :returns: List of WSPathwayInfo The pathway information.

        """
        url = self.url + "getPathwaysByParentOntologyTerm?term={}".format(term)
        url += "&format=json"
        request = self.http_get(url)
        return request["pathways"]

    def showPathwayInBrowser(self, pathwayId):
        """Show a given Pathway into your favorite browser.

        :param str pathwayId: the pathway identifier.

        .. note: This is an additional bioservices functionality (not a
            wikipathway one) showing a wikipathway URL.

        """
        url = self.getPathwayInfo(pathwayId)["url"]
        webbrowser.open(url)
