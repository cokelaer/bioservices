from SOAPpy import SOAPProxy, WSDL
import urllib2

#from SOAPpy import SOAPProxy            1
#>>> url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
#>>> namespace = 'urn:xmethods-Temperature'  2
#>>> server = SOAPProxy(url, namespace)      3
##>>> server.getTemp('27502')                 4


__all__ = ["WSDLService", "RESTService"]


class WSDLService(object):
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
        self.url = url
        self.verbose = verbose
        self.name = name
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



class RESTService(object):

    def __init__(self, name, verbose=True):
        self.name = name
        self.verbose = verbose

    def request(self, url):
        try:
            if self.verbose: 
                print("Fetching url=%s" % url)
            res = urllib2.urlopen(url).read()

            return res
        except Exception, e:
            print(e)
            print("An exception occured while reading the URL")
            print(url)
            print("Error caught within bioservices. Invalid requested URL ? ")
            raise ValueError(e)

