



.. _developer:


Developer Guide
===================

Creating a service class (REST case)
--------------------------------------------------
.. warning:: since version 1.3.0, RESTService is deprecated and REST should be
    used. The changes should be easy: get method is now called http_get and
    requestPost is now http_post.

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

    >>> ols.methods

and call one (getVersion) using the :meth:`bioservices.services.WSDLService.serv`::

    >>> ols.serv.getVersion()

You can then look at something more complex and extract relevant information::

    >>> [x.value for x in ols.serv.getOntologyNames()[0]]

Of course, you can add new methods to ease the access to any functionalities::

    >>> ols.getOnlogyNames() # returns the values

Similarly to the previous case using REST, you can wrap this example into a
proper class. 


Others
========

When wrapper a WSDL services, it may be difficult to know what parameters
to provide. This can be knwon as follows. First, you need the name of the
method::

    s.methods

Then, the name of the structure that contains the parameter::

    ?

Finally, introspect the structure itself::

    s.suds.factory.resolver.find("db2dbParams")


For eutils, this was more difficult::

    m1 = list(e.suds.wsdl.services[0].ports[0].methods.values())[2]
    m1.soap.input.body.parts[0]
    the service is in m1.soap.input.body.parts[0] check for the element in the
    root attribute


suds and client auth
=======================
http://stackoverflow.com/questions/6277027/suds-over-https-with-cert

