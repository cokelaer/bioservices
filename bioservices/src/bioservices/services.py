from SOAPpy import SOAPProxy, WSDL
import urllib2

#from SOAPpy import SOAPProxy            1
#>>> url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
#>>> namespace = 'urn:xmethods-Temperature'  2
#>>> server = SOAPProxy(url, namespace)      3
##>>> server.getTemp('27502')                 4


__all__ = ["Service", "WSDLService", "RESTService"]



class Service(object):
    def __init__(self, name, url=None, verbose=True):
        self.url = url
        self.verbose = verbose
        self.name = name
        self._easyXMLConversion = True

    def _get_easyXMLConversion(self):
        return self._easyXMLConversion
    def _set_easyXMLConversion(self, value):
        if type(value) != bool:
            raise TypeError("value must be a boolean value (True/False)")
        self._easyXMLConversion = value
    easyXMLConversion = property(_get_easyXMLConversion, 
        _set_easyXMLConversion, doc=""""Output from request method are converted to
easyXML object if this attribute is True (Default behaviour).""")


    def easyXML(self, res):
        """Use this method to convert a XML document into an easyXML object

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
    """A common database class for service using WSDL



    """

    def __init__(self, name, url, verbose=True):
        """Constructor

        :param str name: a name e.g. Kegg
        :param str url: the URL of the WSDL service
        :param bool verbose:


        Attributes are:

        * :attr:`Pathway.serv` 
        * :attr:`~pathway.pathway.Pathway.organism` default is 'hsa' for Human
        """
        super(WSDLService, self).__init__(name, url, verbose)

        #self.serv = SOAPProxy(self.url) # what's that ? can we access to a method directly ?
        if self.verbose:
            print("Initialising %s database" % self.name)

        try:
            #: attribute to access to the SWDL service
            self.serv = WSDL.Proxy(self.url)
        except Exception, e:
            print "Could not connect to the service %s " % self.url
            raise Exception

        #: default organism is 'hsa' for 'Human'
        self._organism = 'hsa'

    def _get_methods(self):
        return sorted(self.serv.methods.keys())
    methods = property(_get_methods, doc="returns methods of the WSDL service")

    def _get_dump_out(self):
        return self.serv.soapproxy.config.dumpSOAPOut
    def _set_dump_out(self, value):
        self.serv.soapproxy.config.dumpSOAPOut = value
    dumpOut = property(_get_dump_out, _set_dump_out, 
        doc="set the dumpSOAPOut mode of the SOAP proxy")

    def _get_dump_in(self):
        return self.serv.soapproxy.config.dumpSOAPIn
    def _set_dump_in(self, value):
        self.serv.soapproxy.config.dumpSOAPIn = value
    dumpIn = property(_get_dump_in, _set_dump_in, 
        doc="set the dumpSOAPIn mode of the SOAP proxy")



class RESTService(Service):

    def __init__(self, name, url=None, verbose=True):
        super(RESTService, self).__init__(name, url, verbose)

    def _get_baseURL(self):
        return self.url
    baseURL = property(_get_baseURL)

    def request(self, url):
        if self.verbose:
            print("REST.bioservices.%s request begins" % self.name)
            print("--Fetching url=%s" % url),

        try:
            res = urllib2.urlopen(url).read()
            if self.verbose:
                print("done")
                if self.easyXMLConversion:
                    print("--Conversion to easyXML"),
                    res = self.easyXML(res)
                    print("done")
            return res
        except Exception, e:
            print(e)
            print("An exception occured while reading the URL")
            print(url)
            print("Error caught within bioservices. Invalid requested URL ? ")
            raise


    # Wrapper for a REST (HTTP GET) request
    def restRequest(self,url):
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


