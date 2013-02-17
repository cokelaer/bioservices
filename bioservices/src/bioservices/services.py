# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s): 
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
"""


"""

from SOAPpy import SOAPProxy, WSDL
import urllib
import urllib2
import platform
import logging
import easydev
from  easydev import checkParam


__all__ = ["Service", "WSDLService", "RESTService", "BioServicesError"]


class BioServicesError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Service(object):
    """Base class for WSDL and REST classes


    .. seealso:: :class:`RESTService`, :class:`WSDLService`

    """

    response_codes = {
        200 : 'OK',
        400 : 'Bad Request',
        404 : 'Not found'}

    def __init__(self, name, url=None, verbose=True):
        """.. rubric:: Constructor


        :param str name: a name for this service
        :param str url: its URL
        :param bool verbose: prints informative messages if True (default is
            True)

        All instances have an attribute called :attr:`~Service.logging` that is an instance 
        of the :mod:`logging` module. It can be used to print information, warning, 
        error messages::

            self.logging.info("informative message")
            self.logging.warning("warning message")
            self.logging.error("error message")
 
        The attribute :attr:`~Service.debugLevel`  can be used to set the behaviour 
        of the logging messages. If the argument verbose is True, the debugLebel 
        is set to INFO. If verbose if False, the debugLevel is set to WARNING. 
        However, you can use the :attr:`debugLevel` attribute to change it to 
        one of DEBUG, INFO, WARNING, ERROR, CRITICAL. debugLevel=WARNING means 
        that only WARNING, ERROR and CRITICAL messages are shown.

        """
        self._url = None
        self.url = url
        self.name = name
        self._easyXMLConversion = True

        self._debugLevel = None
        if verbose:
            self.debugLevel = "INFO"
        else:
            self.debugLevel = "WARNING"
        self.logging = logging

        
    
    def _set_level(self, level):
        valid_level = ["INFO", "DEBUG", "WARNING", "CRITICAL", "ERROR"]
        if level in valid_level:
            self._debugLevel = level
        else:
            raise ValueError("The level of debugging must be in %s " % valid_level)
        # I'm not sure this is the best solution, but basicConfig can be called
        # only once and populatse root.handlers list with one instance of
        # logging.StreamHandler. So, I reset it before calling basicConfig so
        # that it is effectively changing the logginh behaviour
        logging.root.handlers = []
        logging.basicConfig(level=self._debugLevel)
    def _get_level(self):
        return self._debugLevel
    debugLevel = property(_get_level, _set_level, 
        doc="One of INFO, DEBUG, WARNING, CRITICAL, ERROR")

    def _get_url(self):
        return self._url
    def _set_url(self, url):
        # something more clever here to check the URL e.g. starts with http
        if url!= None:
            url = url.rstrip("/")
            self._url = url
    url = property(_get_url, _set_url, doc="URL of this service")

    def _get_easyXMLConversion(self):
        return self._easyXMLConversion
    def _set_easyXMLConversion(self, value):
        if type(value) != bool:
            raise TypeError("value must be a boolean value (True/False)")
        self._easyXMLConversion = value
    easyXMLConversion = property(_get_easyXMLConversion, 
        _set_easyXMLConversion, doc="""If True, xml output from a request are converted to
easyXML object (Default behaviour).""")


    def easyXML(self, res):
        """Use this method to convert a XML document into an
            :class:`~bioservices.xmltools.easyXML` object

        The easyXML object provides utilities to ease access to the XML
        tag/attributes.

        Here is a simple example starting from the following XML

        .. doctest::

            >>> from bioservices import *
            >>> doc = "<xml> <id>1</id> <id>2</id> </xml>"
            >>> s = Service("name")
            >>> res = s.easyXML(doc)
            >>> res.findAll("id")
            [<id>1</id>, <id>2</id>]

        """
        import xmltools
        return xmltools.easyXML(res)

    def urlencode(self, params):
        """Returns a string compatible with a URL request.

        :param dict params: a dictionary. Keys are parameters.

        The pair of key/value are converted into a single string by concatenated
        the "&key=value" string for each key/value in the dictionary. 

        ::

            >>> params = {'a':1, 'b':2}
            >>> urlencode(params)
            "a=1&b=2"

        .. note:: returns "a=1&b=2" or "b=2&a=1" since dictionary are not ordered. Note
            that the first parameter is not preceded by a & sign that you will need
            to add. 

        """
        if isinstance(params, dict)==False:
            raise TypeError("Params must be a dictionary.")
        import urllib
        postData = urllib.urlencode(params)
        return postData

    def checkParam(self, param, valid_values):
        """Simple utility to check that a parameter has a valid value 

        :param param:
        :param valid_values:

        Calls :func:`easydev.tools.checkParam`

        ::

            checkParam(aboolean, [True, False])
            checkParam(mode, ["mean", "std", "skew"])
        """        
        easydev.tools.checkParam(param, valid_values)

    def __str__(self):
        txt = "This is an instance of %s service" % self.name
        return txt

    def pubmed(self, Id):
        """Open a pubmed Id into a browser tab

        :param Id: a valid pubmed Id in string or integer format.

        The URL is a concatenation of the pubmed URL
        http://www.ncbi.nlm.nih.gov/pubmed/ and the provided Id.

        """
        url = "http://www.ncbi.nlm.nih.gov/pubmed/"
        import webbrowser
        webbrowser.open(url + str(Id))


class WSDLService(Service):
    """Class dedicated to the web services based on WSDL/SOAP protocol.

    .. seealso:: :class:`RESTService`, :class:`Service`

    """

    def __init__(self, name, url, verbose=True):
        """.. rubric:: Constructor

        :param str name: a name e.g. Kegg, Reactome, ...
        :param str url: the URL of the WSDL service
        :param bool verbose: prints informative messages

        The :attr:`serv` give  access to all WSDL functionalities of the service.

        The :attr:`methods` is an alias to self.serv.methods and returns 
        the list of functionalities.

        """
        super(WSDLService, self).__init__(name, url, verbose=verbose)

        #self.serv = SOAPProxy(self.url) # what's that ? can we access to a method directly ?
        logging.info("Initialising %s service (WSDL)" % self.name)

        try:
            #: attribute to access to the methods provided by this WSDL service
            self.serv = WSDL.Proxy(self.url)
        except Exception, e:
            print "Could not connect to the service %s " % self.url
            raise Exception

    def _get_methods(self):
        return sorted(self.serv.methods.keys())
    methods = property(_get_methods, doc="returns methods available in the WSDL service")

    def _get_dump_out(self):
        return self.serv.soapproxy.config.dumpSOAPOut
    def _set_dump_out(self, value):
        self.serv.soapproxy.config.dumpSOAPOut = value
    dumpOut = property(_get_dump_out, _set_dump_out, 
        doc="set the dumpSOAPOut mode of the SOAP proxy (0/1)")

    def _get_dump_in(self):
        return self.serv.soapproxy.config.dumpSOAPIn
    def _set_dump_in(self, value):
        self.serv.soapproxy.config.dumpSOAPIn = value
    dumpIn = property(_get_dump_in, _set_dump_in, 
        doc="set the dumpSOAPIn mode of the SOAP proxy (0/1)")



class RESTService(Service):
    """Class to manipulate REST service

    You can request an URL with this class that also inherits from
    :class:`Service`.

    """

    def __init__(self, name, url=None, verbose=True):
        """.. rubric:: Constructor

        :param str name: a name e.g. Kegg, Reactome, ...
        :param str url: the URL of the REST service
        :param str debugLevel: logging level. See :class:`Service`.

        """
        super(RESTService, self).__init__(name, url, verbose=verbose)
        self.last_response = None
        logging.info("Initialising %s service (REST)" % self.name)
        try:
            import urllib
            urllib.urlopen(self.url)
        except e:
            logging.critical("The URL (%s) provided cannot be reached" % self.url)
            print e

    def getUserAgent(self):
        import os
        logging.info('getUserAgent: Begin')
        urllib_agent = 'Python-urllib/%s' % urllib2.__version__
        clientRevision = ''
        clientVersion = ''
        user_agent = 'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
            clientVersion, os.path.basename( __file__ ), 
            platform.python_version(), platform.system(),
            urllib_agent
        )
        logging.info('getUserAgent: user_agent: ' + user_agent)
        logging.info('getUserAgent: End')
        return user_agent



    def request(self, path, format="xml", baseUrl=True):
        """Send a request via an URL to the web service.

        :param str path: the request will be formed as self.url+/+path 
        :param str format: If the expected output is in XML
            format then it will be converted with :meth:`easyXML`. If the 
            returned document is not in XML, format should be set to any other 
            value.
        :param str baseUrl: By default, the path argument is appended to the 
            :attr:`url` attribute (the main REST URL). However, sometimes, you
            would prefer to provide the entire URL yourself (e.g. in psicquic service)
            If so, set this baseUrl argument to False. 


        .. note:: this is a HTTP GET request 
        """
        if path.startswith(self.url):
            url = path
        elif baseUrl == False:
            url = path
        else:
            url = self.url + "/" +  path

        logging.info("REST.bioservices.%s request begins" % self.name)
        logging.info("--Fetching url=%s" % url)

        try:
            res = urllib2.urlopen(url).read()
            if format=="xml":
                if self.easyXMLConversion:
                    #logging.warning("--Conversion to easyXML"),
                    try:
                        res = self.easyXML(res)
                    except:
                        logging.error("--Conversion to easyXML failed. returns the raw response"),
            self.last_response = res
            return res
        except Exception, e:
            logging.error(e)
            logging.error("An exception occured while reading the URL")
            logging.error(url)
            logging.error("Error caught within bioservices. Invalid requested URL ? ")
            raise

    def requestPost(self, requestUrl, params, extra=None):
        """request with a POST method.

        :param str requestUrl: the entire URL to request
        :param dict params: the dictionary of parameter/value pairs
        :param str extra: an additional string to add after the params if
            needed. Could be usefule if a parameter/value can not be added to the
            dictionary. For instance is a parameter has several values

        .. todo:: parameter paranName with a list of values [v1,v2] can be interpreted as
            paramName=v1&paramName=v2

        .. note:: this is a HTTP POST request 
        .. note:: use only by ::`ncbiblast` service so far.
        """
        import sys
        requestData = urllib.urlencode(params)
        print requestData
        if extra != None:
            requestData += extra
        # Concatenate the two parts.
        # Errors are indicated by HTTP status codes.
        try:
            # Set the HTTP User-agent.
            user_agent = self.getUserAgent()
            http_headers = { 'User-Agent' : user_agent }
            req = urllib2.Request(requestUrl, None, http_headers)
            # Make the submission (HTTP POST).
            print req
            reqH = urllib2.urlopen(req, requestData)
            jobId = reqH.read()
            reqH.close()
        except urllib2.HTTPError, ex:
            # Trap exception and output the document to get error message.
            print(sys.stderr, ex.read())
            raise
        return jobId


