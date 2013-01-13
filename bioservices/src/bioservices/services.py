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


from SOAPpy import SOAPProxy, WSDL
import urllib2
import platform
import logging

__all__ = ["Service", "WSDLService", "RESTService"]



class Service(object):
    """Base class for WSDL and REST classes


    .. seealso:: :class:`RESTService`, :class:`WSDLService`

    """
    def __init__(self, name, url=None, verbose=True):
        """.. rubric:: Constructor


        :param str name: a name for this service
        :param str url: its URL
        :param bool verbose: prints informative message if True (default is
            True)

        The attribute :attr:`debugLevel` can be used to further refine the
        logging messages that uses the standard :mod:`logging` module. If
        verbose is True, the debugLebel is set to INFO. If verbose if False, the
        debugLevel is set to WARNING. However, you can use the
        :attr:`debugLevel` attribute to change it to one of DEBUG, INFO,
        WARNING, ERROR, CRITICAL. debugLevel=WARNING means that only WARNING,
        ERROR and CRITICAL messages are shown/

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
        valid_level = ["INFO", "DEBUG", "WARNING", "CRITIAL", "ERROR"]
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
    debugLevel = property(_get_level, _set_level)

    def _get_url(self):
        return self._url
    def _set_url(self, url):
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
        """
        import xmltools
        return xmltools.easyXML(res)

    def urlencode(self, params):
        """Returns a string compatible with URL request.

        The pair of key/value are converted into a single string by concatenated
        the "&key=value" string for each key/value in the dictionary.

        :param dict params: a dictionary. Keys are parameters.

        ::

            >>> params = {'a':1, 'b':2}
            >>> urlencode(params)
            "a=1&b=2"

        returns "a=1&b=2" or "b=2&a=1" since dictionary are not ordered. Note
        that the first parameter is not preceded by a & sign that you will need
        to add. 

        """
        if isinstance(params, dict)==False:
            raise TypeError("Params must be a dictionary.")
        import urllib
        postData = urllib.urlencode(params)
        return postData



class WSDLService(Service):
    """A common class to ease access to web services (WSDL protocol)"""

    def __init__(self, name, url, verbose=True):
        """.. rubric:: Constructor

        :param str name: a name e.g. Kegg, Reactome, ...
        :param str url: the URL of the WSDL service
        :param bool verbose: prints informative messages

        Attributes are:

        * :attr:`Pathway.serv` 

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
        except:
            logging.critical("The URL (%s) provided cannot be reached" % self.url)

    def getUserAgent(self):
        logging.info('getUserAgent: Begin')
        urllib_agent = 'Python-urllib/%s' % urllib2.__version__
        clientRevision = '$Id$'
        clientVersion = '1'
        user_agent = 'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
            clientVersion, os.path.basename( __file__ ), 
            platform.python_version(), platform.system(),
            urllib_agent
        )
        logging.info('getUserAgent: user_agent: ' + user_agent)
        logging.info('getUserAgent: End')
        return user_agent


    def request(self, url, format="xml"):
        """Send a request via an URL to a web service.

        :param str url: the well formed URL
        :param str format: If the expected output is in XML
            format it will be converted with :meth:`easyXML`. If the returned document
            is not in XML, format should be set to any other value.

        """
	print self.name
	print url
        logging.info("REST.bioservices.%s request begins" % self.name)
        logging.info("--Fetching url=%s" % url)

        try:
            res = urllib2.urlopen(url).read()
            if format=="xml":
                if self.easyXMLConversion:
                    logging.warning("--Conversion to easyXML"),
                    try:
                        res = self.easyXML(res)
                    except:
                        logging.error("--Conversion to easyXML failed. returns the original XML file"),
            self.last_response = res
            return res
        except Exception, e:
            logging.error(e)
            logging.error("An exception occured while reading the URL")
            logging.error(url)
            logging.error("Error caught within bioservices. Invalid requested URL ? ")
            raise

"""
    # Wrapper for a REST (HTTP GET) request
    def restRequest(self,url):
        # kept as an example.
        raise NotImplementedError
        # need to be checked before using it.
        printDebugMessage('restRequest', 'Begin', 11)
        printDebugMessage('restRequest', 'url: ' + url, 11)
        try:
            # Set the User-agent.
            user_agent = getUserAgent()
            http_headers = { 'User-Agent' : user_agent }
            req = urllib2.Request(url, None, http_headers)
            # Make the request (HTTP GET).
            reqH = urllib2.urlopen(req)
            result = reqH.read()
            reqH.close()
        # Errors are indicated by HTTP status codes.
        except urllib2.HTTPError, ex:
            # Trap exception and output the document to get error message.
            print >>sys.stderr, ex.read()
            raise
        printDebugMessage('restRequest', 'End', 11)
        return result

"""
