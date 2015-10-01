# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      https://github.com/cokelaer/bioservices
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  source: http://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id$
"""Modules with common tools to access web resources"""
from __future__ import print_function
import os
import sys
import socket
import platform
import json
import easydev

from bioservices.settings import BioServicesConfig

# fixing compatiblity python 2 and 3 related to merging or urllib and urllib2 in python 3
try:
    #python 3
    from urllib.request import urlopen
    from urllib.parse import urlparse, urlencode
    from urllib.error import HTTPError
    from urllib.request import Request
except:
    from urllib import urlencode
    from urllib2  import urlopen, Request, HTTPError

# This is a hack in case suds is already installed.
# Indded, we want suds_jurko instead
sys.path = [x for x in sys.path if 'suds-' not in x]


from easydev import Logging, DevTools


__all__ = ["Service", "WSDLService", "RESTService",
           "BioServicesError", "REST"]


class BioServicesError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Service(Logging):
    """Base class for WSDL and REST classes

    .. seealso:: :class:`REST`, :class:`WSDLService`
    """

    #: some useful response codes
    response_codes = {
        200: 'OK',
        201: 'Created',
        400: 'Bad Request. There is a problem with your input',
        404: 'Not found. The resource you requests does not exist',
        406: "Not Acceptable. Usually headers issue",
        410:  'Gone. The resource you requested was removed.',
        415: "Unsupported Media Type",
        500: 'Internal server error. Most likely a temporary problem',
        503: 'Service not available. The server is being updated, try again later'
        }

    def __init__(self, name, url=None, verbose=True, requests_per_sec=3):
        """.. rubric:: Constructor

        :param str name: a name for this service
        :param str url: its URL
        :param bool verbose: prints informative messages if True (default is
            True)
        :param requests_per_sec: maximum number of requests per seconds
            are restricted to 3. You can change that value. If you reach the
            limit, an error is raise. The reason for this limitation is
            that some services (e.g.., NCBI) may black list you IP. 
            If you need or can do more (e.g., ChEMBL does not seem to have
            restrictions), change the value. You can also have several instance
            but again, if you send too many requests at the same, your future
            requests may be retricted. Currently implemented for REST only


        All instances have an attribute called :attr:`~Service.logging` that
        is an instanceof the :mod:`logging` module. It can be used to print
        information, warning, error messages::

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
        super(Service, self).__init__(level=verbose)
        self.requests_per_sec = requests_per_sec

        self._url = url
        try:
            if self.url is not None:
                urlopen(self.url)
        except Exception as err:
            self.logging.warning("The URL (%s) provided cannot be reached." % self.url)
        self.name = name
        self._easyXMLConversion = True

        # used by HGNC where some XML contains non-utf-8 characters !!
        # should be able to fix it with requests once HGNC works again
        #self._fixing_unicode = False
        #self._fixing_encoding = "utf-8"

        self.devtools = DevTools()
        self.settings = BioServicesConfig()
    
    def _get_caching(self):
        return self.settings.params['cache.on'][0]
    def _set_caching(self, caching):
        self.devtools.check_param_in_list(caching, [True, False])
        self.settings.params['cache.on'][0] = caching
        # reset the session, which will be automatically created if we
        # access to the session attribute
        self._session = None
    CACHING = property(_get_caching, _set_caching)

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        # something more clever here to check the URL e.g. starts with http
        if url is not None:
            url = url.rstrip("/")
            self._url = url
    url = property(_get_url, _set_url, doc="URL of this service")

    def _get_easyXMLConversion(self):
        return self._easyXMLConversion

    def _set_easyXMLConversion(self, value):
        if isinstance(value, bool) is False:
            raise TypeError("value must be a boolean value (True/False)")
        self._easyXMLConversion = value
    easyXMLConversion = property(_get_easyXMLConversion,
            _set_easyXMLConversion, 
            doc="""If True, xml output from a request are converted to easyXML object (Default behaviour).""")

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
        from bioservices import xmltools
        return xmltools.easyXML(res)


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

    def on_web(self, url):
        """Open a URL into a browser"""
        import webbrowser
        webbrowser.open(url)

    def save_str_to_image(self, data, filename):
        """Save string object into a file converting into binary"""
        with open(filename,'wb') as f:
            import binascii
            try:
                #python3
                newres = binascii.a2b_base64(bytes(data, "utf-8"))
            except:
                newres = binascii.a2b_base64(data)
            f.write(newres)


class WSDLService(Service):
    """Class dedicated to the web services based on WSDL/SOAP protocol.

    .. seealso:: :class:`RESTService`, :class:`Service`

    """
    _service = "WSDL"

    def __init__(self, name, url, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param str name: a name e.g. Kegg, Reactome, ...
        :param str url: the URL of the WSDL service
        :param bool verbose: prints informative messages

        The :attr:`serv` give  access to all WSDL functionalities of the service.

        The :attr:`methods` is an alias to self.serv.methods and returns
        the list of functionalities.

        """
        super(WSDLService, self).__init__(name, url, verbose=verbose)

        self.logging.info("Initialising %s service (WSDL)" % self.name)
        self.CACHING = cache

        try:
            #: attribute to access to the methods provided by this WSDL service
            from suds.client import Client
            from suds.cache import ObjectCache
            oc = ObjectCache(self.settings.user_config_dir, days=0)
            if self.CACHING is True:
                self.suds = Client(self.url, cache=oc, cachingpolicy=1)
            else:
                self.suds = Client(self.url)
            # reference to the service
            self.serv = self.suds.service
            self._update_settings()
        except Exception :
            self.logging.error("Could not connect to the service %s " % self.url)
            raise Exception

    def _update_settings(self):
        self.TIMEOUT = self.settings.TIMEOUT

    def wsdl_methods_info(self):
        methods = self.suds.wsdl.services[0].ports[0].methods.values()
        for method in methods:
            try:
                print('%s(%s) ' % (
                    method.name,
                    ', '.join('type:%s: %s - element %s' %
                            (part.type, part.name, part.element) for part in
                            method.soap.input.body.parts)))
            except:
                print(method)
    def _get_methods(self):
        return [x.name for x in
                self.suds.wsdl.services[0].ports[0].methods.values()]
    wsdl_methods = property(_get_methods, 
            doc="returns methods available in the WSDL service")

    def wsdl_create_factory(self, name, **kargs):
        params = self.suds.factory.create(name)

        # e.g., for eutils
        if "email" in dict(params).keys():
            params.email = self.settings.params['user.email'][0]

        if "tool" in dict(params).keys():
            import bioservices
            params.tool = "BioServices, " + bioservices.__version__

        for k,v in kargs.items():
            from suds import sudsobject
            keys = sudsobject.asdict(params).keys()
            if k in keys:
                params[k] = v
            else:
                msg = "{0} incorrect. Correct ones are {1}"
                self.logging.error(msg.format(k, keys))
        return params

    def _get_timeout(self):
        return self.suds.options.timeout
    def _set_timeout(self, value):
        self.suds.set_options(timeout=value)
        self.settings.TIMEOUT = value
    TIMEOUT = property(_get_timeout, _set_timeout)


class RESTbase(Service):
    _service = "REST"
    def __init__(self, name, url=None, verbose=True):
        super(RESTbase, self).__init__(name, url, verbose=verbose)
        self.logging.info("Initialising %s service (REST)" % self.name)
        self.last_response = None

    def http_get(self):
        # should return unicode
        raise NotImplementedError

    def http_post(self):
        raise NotImplementedError

    def http_put(self):
        raise NotImplementedError

    def http_delete(self):
        raise NotImplementedError


class RESTService(RESTbase):
    """Class to manipulate REST service

    You can request an URL with this class that also inherits from
    :class:`Service`.


    For debugging:

    * last_response contains

    """
    def __init__(self, name, url=None, verbose=True):
        """.. rubric:: Constructor

        :param str name: a name e.g. Kegg, Reactome, ...
        :param str url: the URL of the REST service
        :param str debugLevel: logging level. See :class:`Service`.

        """
        super(RESTService, self).__init__(name, url, verbose=verbose)
        self.logging.error("Please use REST class instead of RESTService")
        self.trials = 5
        self.timesleep = 1

    def getUserAgent(self):
        self.logging.info('getUserAgent: Begin')
        try:
            import urllib2
            urllib_agent = 'Python-urllib/%s' % urllib2.__version__
        except:
            import urllib
            urllib_agent = 'Python-urllib/%s' % urllib.__version__
        #clientRevision = ''
        clientVersion = ''
        user_agent = 'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
            clientVersion, os.path.basename(__file__),
            platform.python_version(), platform.system(),
            urllib_agent
        )
        self.logging.info('getUserAgent: user_agent: ' + user_agent)
        self.logging.info('getUserAgent: End')
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

        .. seealso:: for developers see also the :meth:`_request_timeout`
            if the site is down or busy.

        .. note:: you can set the timeout of the connection, which is 1000
            seconds by default by changing the :attr:`timeout`.
        """
        for i in range(0, self.trials):
            res = self._get_request(path, format=format, baseUrl=baseUrl)
            if res is not None:
                break
            import time
            self.logging.warning("request seemed to have failed.")
            if i!=self.trials-1:
                print("Trying again trial {}/{}".format(i+1, self.trials))
            time.sleep(self.timesleep)
        return res

    def http_get(self, path, format="xml", baseUrl=True):
        return self.request(path, format=format, baseUrl=baseUrl)

    def _get_request(self, path, format="xml", baseUrl=True):
        if path.startswith(self.url):
            url = path
        elif baseUrl is False:
            url = path
        else:
            url = self.url + "/" +  path

        self.logging.debug("REST.bioservices.%s request begins" % self.name)
        self.logging.debug("--Fetching url=%s" % url)

        if len(url)> 2000:
            print(url)
            raise ValueError("URL length (%s) exceeds 2000. Please use a differnt URL" % len(url))

        try:
            res = urlopen(url).read()
            if format=="xml":
                if self.easyXMLConversion:
                    #logging.warning("--Conversion to easyXML"),
                    try:
                        res = self.easyXML(res)
                    except Exception as err:
                        self.logging.warning(err.message)
                        self.logging.warning("--Conversion to easyXML failed. returns the raw response"),
            self.last_response = res
            return res
        except socket.timeout:
            self.logging.warning("Time out. consider increasing the timeout attribute (currently set to {})".format(self.timeout))
        except Exception as err:
            self.logging.debug(err.message)
            self.logging.debug("An exception occured while reading the URL")
            self.logging.debug(url)
            self.logging.debug("Error caught within bioservices. Invalid requested URL ? ")


    def requestPost(self, requestUrl, params, extra=None):
        """request with a POST method.

        :param str requestUrl: the entire URL to request
        :param dict params: the dictionary of parameter/value pairs
        :param str extra: an additional string to add after the params if
            needed. Could be usefule if a parameter/value can not be added to the
            dictionary. For instance is a parameter has several values
            Solved in requests module.
        .. todo:: parameter paranName with a list of values [v1,v2] can be interpreted as
            paramName=v1&paramName=v2

        .. note:: this is a HTTP POST request
        .. note:: use only by ::`ncbiblast` service so far.
        """
        requestData = urlencode(params)
        print(requestData)
        if extra is not None:
            requestData += extra
        # Concatenate the two parts.
        # Errors are indicated by HTTP status codes.
        try:
            # Set the HTTP User-agent.
            user_agent = self.getUserAgent()
            http_headers = {'User-Agent': user_agent}
            print(requestUrl)
            req = Request(requestUrl, None, http_headers)
            # Make the submission (HTTP POST).
            print(req)
            reqH = urlopen(req, requestData)
            jobId = reqH.read()
            reqH.close()
        except HTTPError as err:
            # Trap exception and output the document to get error message.
            print(sys.stderr, ex.read())
            raise
        return jobId

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
        if isinstance(params, dict)is False:
            raise TypeError("Params must be a dictionary.")
        postData = urlencode(params)
        return postData


import requests         # replacement for urllib2 (2-3 times faster)
from requests.models import Response
import requests_cache   # use caching wihh requests
#import grequests        # use asynchronous requests with gevent
# Note that grequests should be imported after requests_cache. Otherwise,
# one should use a session instance when calling grequests.get, which we do
# here below


class REST(RESTbase):
    """

    The ideas (sync/async) and code using requests were inspired from the chembl
    python wrapper but significantly changed.

    Get one value::

        >>> from bioservices import REST
        >>> s = REST("test", "https://www.ebi.ac.uk/chemblws")
        >>> res = s.get_one("targets/CHEMBL2476.json", "json")
        >>> res['organism']
        u'Homo sapiens'

    The caching has two major interests. First one is that it speed up requests if
    you repeat requests. ::


        >>> s = REST("test", "https://www.ebi.ac.uk/chemblws")
        >>> s.CACHING = True
        >>> # requests will be stored in a local sqlite database
        >>> s.get_one("targets/CHEMBL2476")
        >>> # Disconnect your wiki and any network connections.
        >>> # Without caching you cannot fetch any requests but with
        >>> # the CACHING on, you can retrieve previous requests:
        >>> s.get_one("targets/CHEMBL2476")


    Advantages of requests over urllib

    requests length is not limited to 2000 characters
    http://www.g-loaded.eu/2008/10/24/maximum-url-length/
    """
    content_types = {
        'bed': 'text/x-bed',
        'default': "application/x-www-form-urlencoded",
        'gff3': 'text/x-gff3',
        'fasta': 'text/x-fasta',
        'json': 'application/json',
        "jsonp": "text/javascript",
        "nh": "text/x-nh",
        'phylip': 'text/x-phyloxml+xml',
        'phyloxml': 'text/x-phyloxml+xml',
        'seqxml': 'text/x-seqxml+xml',
        'txt': 'text/plain',
        'text': 'text/plain',
        'xml': 'application/xml',
        'yaml': 'text/x-yaml'
    }
    #special_characters = ['/', '#', '+']

    def __init__(self, name, url=None, verbose=True, cache=False):
        super(REST, self).__init__(name, url, verbose=verbose)
        bspath = self.settings.user_config_dir
        self.CACHE_NAME = bspath + os.sep + self.name + "_bioservices_db"

        self._session = None

        self.settings.params['cache.on'][0] = cache

        if self.CACHING:
            #import requests_cache
            self.logging.info("Using local cache %s" % self.CACHE_NAME)
            requests_cache.install_cache(self.CACHE_NAME)

    def delete_cache(self):
        import os
        if os.path.exists(self.CACHE_NAME + '.sqlite'):
            msg = "You are about to delete this bioservices cache %s. proceed y/n"
            res = raw_input(msg % self.CACHE_NAME)
            if res == "y":
                os.remove(self.CACHE_NAME + '.sqlite')
                print("Removed cache")
            else:
                print("reply 'y' to delete the file")

    def clear_cache(self):
        from requests_cache import clear
        clear()

    def _get_session(self):
        if self._session is None:
            if self.CACHING is True:
                self._session = self._create_cache_session()
            else:
                self._session = self._create_session()
        return self._session
    session = property(_get_session)

    def _create_session(self):
        """Creates a normal session using HTTPAdapter

        max retries is defined in the :attr:`MAX_RETRIES`
        """
        self.logging.debug("Creating session (uncached version)")
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.settings.MAX_RETRIES)
        #, pool_block=True does not work with asynchronous requests
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        return self._session

    def _create_cache_session(self):
        """Creates a cached session using requests_cache package"""
        self.logging.debug("Creating session (cache version)")
        if not self._session:
            #import requests_cache
            self.logging.debug("No cached session created yet. Creating one")
            self._session = requests_cache.CachedSession(self.CACHE_NAME,
                         backend='sqlite', fast_save=self.settings.FAST_SAVE)
        return self._session

    def _get_timeout(self):
        return self.settings.TIMEOUT
    def _set_timeout(self, value):
        self.settings.TIMEOUT = value
    TIMEOUT = property(_get_timeout, _set_timeout)

    def _process_get_request(self, url, session, frmt, data=None, **kwargs):
        try:
            res = session.get(url, **kwargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            return res
        except Exception:
            return None

    def _interpret_returned_request(self, res, frmt):
        # must be a Response
        if isinstance(res, Response) is False:
            return res
        # if a response, there is a status code that should be ok
        if not res.ok:
            reason = res.reason
            self.logging.warning("status is not ok with {0}".format(reason))
            return res.status_code
        if frmt == "json":
            try:
                return res.json()
            except:
                return res
        # finally
        return res.content

    def _apply(self, iterable, fn, *args, **kwargs):
        return [fn(x, *args, **kwargs) for x in iterable if x is not None]

    def _get_async(self, keys, frmt='json', params={}):
        # does not work under pyhon3 so local import
        import grequests
        session = self._get_session()
        try:
            # build the requests
            urls = self._get_all_urls(keys, frmt)
            self.logging.debug("grequests.get processing")
            rs = (grequests.get(url, session=session, params=params)  for key,url in zip(keys, urls))
            # execute them
            self.logging.debug("grequests.map call")
            ret = grequests.map(rs, size=min(self.settings.CONCURRENT, len(keys)))
            self.last_response = ret
            self.logging.debug("grequests.map call done")
            return ret
        except Exception as err:
            self.logging.warning("Error caught in async. " + err.message)
            return []

    def _get_all_urls(self, keys, frmt=None):
        return ('%s/%s' % (self.url, query) for query in keys)

    def get_async(self, keys, frmt='json', params={}, **kargs):
        ret = self._get_async(keys, frmt, params=params, **kargs)
        return self._apply(ret, self._interpret_returned_request, frmt)

    def get_sync(self, keys, frmt='json', **kargs):
        return [self.get_one(key, frmt=frmt, **kargs) for key in keys]

    def http_get(self, query, frmt='json', params={}, **kargs):
        """

        * query is the suffix that will be appended to the main url attribute.
        * query is either a string or a list of strings.
        * if list is larger than ASYNC_THRESHOLD, use asynchronous call.


        """
        if isinstance(query, list) and len(query) > self.settings.ASYNC_THRESHOLD:
            self.logging.debug("Running async call for a list")
            return self.get_async(query, frmt, params=params, **kargs)
        if isinstance(query, list) and len(query) <= self.settings.ASYNC_THRESHOLD:
            self.logging.debug("Running sync call for a list")
            return [self.get_one(key, frmt, params=params, **kargs) for key in query]
            #return self.get_sync(query, frmt)
        # OTHERWISE
        self.logging.debug("Running http_get (single call mode)")
        #return self.get_one(**{'frmt': frmt, 'query': query, 'params':params})
        return self.get_one(query, frmt, params=params, **kargs)

    def get_one(self, query, frmt='json', params={}, **kargs):
        """

        if query starts with http:// do not use self.url
        """
        if query is None:
            url = self.url
        else:
            if query.startswith("http"):
                # assume we do want to use self.url
                url = query
            else:
                url = '%s/%s' % (self.url, query)
        self.logging.debug(url)
        try:
            kargs['params'] = params
            kargs['timeout'] = self.TIMEOUT
            #res = self.session.get(url, **{'timeout':self.TIMEOUT, 'params':params})
            res = self.session.get(url, **kargs)

            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                # for python 3 compatibility
                res = res.decode()
            except:
                pass
            return res
        except Exception as err:
            print(err)
            print("""Issue. Maybe your current timeout is {0} is not sufficient. 
Consider increasing it with settings.TIMEOUT attribute""".format(self.settings.TIMEOUT))

    def http_post(self, query, params=None, data=None,
                    frmt='xml', headers=None, files=None, **kargs):
        # query and frmt are bioservices parameters. Others are post parameters
        # NOTE in requests.get you can use params parameter
        # BUT in post, you use data
        # only single post implemented for now unlike get that can be asynchronous
        # or list of queries
        if headers is None:
            headers = {}
            headers['User-Agent'] = self.getUserAgent()
            headers['Accept'] = self.content_types[frmt]

        self.logging.debug("Running http_post (single call mode)")
        kargs.update({'query':query})
        kargs.update({'headers':headers})
        kargs.update({'files':files})
        kargs.update({'params':params})
        kargs.update({'data':data})
        kargs.update({'frmt':frmt})
        return self.post_one(**kargs)

    def post_one(self, query, frmt='json', **kargs):
        self.logging.debug("BioServices:: Entering post_one function")
        if query is None:
            url = self.url
        else:
            url = '%s/%s' % (self.url, query)
        self.logging.debug(url)
        try:
            res = self.session.post(url, **kargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                return res.decode()
            except:
                self.debug("BioServices:: Could not decode the response")
                return res
        except Exception as err:
            print(err)
            return None

    def getUserAgent(self):
        self.logging.info('getUserAgent: Begin')
        urllib_agent = 'Python-requests/%s' % requests.__version__
        #clientRevision = ''
        clientVersion = ''
        user_agent = 'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
            clientVersion, os.path.basename(__file__),
            platform.python_version(), platform.system(),
            urllib_agent
        )
        self.logging.info('getUserAgent: user_agent: ' + user_agent)
        self.logging.info('getUserAgent: End')
        return user_agent

    def get_headers(self, content='default'):
        """
        :param str content: ste to default that is application/x-www-form-urlencoded
            so that it has the same behaviour as urllib2 (Sept 2014)

        """
        headers = {}
        headers['User-Agent'] = self.getUserAgent()
        headers['Accept'] = self.content_types[content]
        headers['Content-Type'] = self.content_types[content]
        #"application/json;odata=verbose" required in reactome
        #headers['Content-Type'] = "application/json;odata=verbose" required in reactome
        return headers

    def debug_message(self):
        print(self.last_response.content)
        print(self.last_response.reason)
        print(self.last_response.status_code)

    def http_delete(self, query, params=None, 
                    frmt='xml', headers=None,  **kargs):
        kargs.update({'query': query})
        kargs.update({'params': params})
        kargs.update({'frmt': frmt})
        return self.delete_one(**kargs)

    def delete_one(self, query, frmt='json', **kargs):
        self.logging.debug("BioServices:: Entering delete_one function")
        if query is None:
            url = self.url
        else:
            url = '%s/%s' % (self.url, query)
        self.logging.debug(url)
        try:
            res = self.session.delete(url, **kargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                return res.decode()
            except:
                self.debug("BioServices:: Could not decode the response")
                return res
        except Exception as err:
            print(err)
            return None
        except:
            pass
