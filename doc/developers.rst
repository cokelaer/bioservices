



.. _developer:


Developer Guide
===================

Naming convention
-----------------

To add a web services in BioServices, decide on a name for the python module. By
convention we have the module name in lower case. Internally, class uses
standard Python convention (Upper case for first letter).

The module name (e.g. uniprot) should be use to name the module (uniprot.py).

It will also be used to add a test or the continuous integration

Creating a service class (REST case)
--------------------------------------------------

You can test directly a SOAP/WSDL or REST service in a few lines. For instance,
to access to the biomart REST service, type::

    >>> s = REST("BioMart" ,"http://www.biomart.org/biomart/martservice")

The first parameter is compulsary but can be any word. You can retrieve the base
URL by typing::

    >>> s.url
    'http://www.biomart.org/biomart/martservice'

and then send a request to retrieve registry information for instance (see
www.biomart.org.martservice.html for valid request::

    >>> s.http_get("?type=registry")
    <bioservices.xmltools.easyXML at 0x3b7a4d0>


The request method available from RESTService class concatenates the url and the
parameter provided so it request the "http://www.biomart.org.biomart/martservice" URL.

As a developer, you should ease the life of the user by wrapping up the previous
commands. An example of a BioMart class with a unique method dedicated to the
registry would look like::

    >>> class BioMart(REST):
    ...    def __init__(self):
    ...        url = "http://www.biomart.org/biomart/martservice"
    ...        super(BioMart, self).__init__("BioMart", url=url)
    ...    def registry(self):
    ...        ret = self.request("?type=registry")
    ...        return ret

and you would use it as follows::

    >>> s = BioMart()
    >>> s.registry()
    <bioservices.xmltools.easyXML at 0x3b7a4d0>

Creating a service class (WSDL case)
-----------------------------------------------


If a web service interface is not provided within bioservices, you can still
easily access its functionalities. As an example, let us look at the 
`Ontology Lookup service <http://www.ebi.ac.uk/ontology-lookup/WSDLDocumentation.do>`_, which provides a
WSDL service. In order to easily access this service, use the :class:`WSDLService` class as follows::

    >>> from bioservices import WSDLService
    >>> ols = WSDLService("OLS", "http://www.ebi.ac.uk/ontology-lookup/OntologyQuery.wsdl")

You can now see which methods are available::

    >>> ols.wsdl_methods

and call one (getVersion) using the :meth:`bioservices.services.WSDLService.serv`::

    >>> ols.serv.getVersion()

You can then look at something more complex and extract relevant information::

    >>> [x.value for x in ols.serv.getOntologyNames()[0]]

Of course, you can add new methods to ease the access to any functionalities::

    >>> ols.getOnlogyNames() # returns the values

Similarly to the previous case using REST, you can wrap this example into a
proper class. 


Others
------

When wrapper a WSDL services, it may be difficult to know what parameters
to provide if the API doc is not clear. This can be known as follows using 
the **suds** factory. In this previous examples, we could use::

    >>> ols.suds.factory.resolver.find('getTermById')
    <Element:0xa848b50 name="getTermById" />


For eutils, this was more difficult::

    m1 = list(e.suds.wsdl.services[0].ports[0].methods.values())[2]
    m1.soap.input.body.parts[0]
    the service is in m1.soap.input.body.parts[0] check for the element in the
    root attribute


suds and client auth
------------------------
http://stackoverflow.com/questions/6277027/suds-over-https-with-cert



How to include tests ?
------------------------

We use pytest. There are many web services included in BioServices. Consequently
there are many tests. It is common to have failed tests on Travis and the
continuous integration. 

Some tests are known to be long or failing from time to time (e.g. service is
down). 

When a test is known to fail sometimes, we can add this decorator::

    @pytest.mark.flaky(max_runs=3, min_passes=1)

On travis we allows 8 failures. 

For long tests, we allows 60s at most. You can mark a tests if you knw it will
fail on travis (e.g. too long)::

    pytest.mark.xfail

Finally, we skip some tests for some conditions::

    skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
      reason="On travis")
    @skiptravis
    def test():
        ...


Continuous integration
----------------------

1. add a test in ./test/webservices/test_**yourmodule**.py
2. add a continous integration file named after **yourmodule**.yml. See example
in .github/workflows/template.txt and replace **__name__** by your module name


