.. _quickstart:

Quick Start
#################

Bioservices provides several services. Each service requires some expertise so
we will neither cover all the services nor all their functionalities in this quickstart. However by the end of this tutorials you should be able to play with all services provided in bioservices. 

There are two main technology involved in web services: the WSDL and the REST
styles. The Kegg and Biomodels services presented uses WSDL whereas uniprot uses
REST.

Kegg service
=============


Start a kegg interface (default organism is human, that is called hsa)::

    from bioservices.kegg import Kegg
    k = Kegg()


By default, the organism is human (hsa) but you can change it::

    k.organism = "dosa"
    k.organism = "hsa"

In order to get the list of valid organisms, type::

    print k.organisms

Every elements is referred to with a Kegg ID, which may be difficult to handle
at first. There are methods to retrieve the IDs though. For instance, get the list of 
pathways ids for the current organism as follows::

    k.pathways

Now, you can various requests but let us first open a pathway in a browser::

    k.color_pathway_by_elements('path:hsa04660')

Genes within a pathway can be retrieved with the method::

    k.get_genes_by_pathway("path:hsa04660")

For a given gene, you can get the full information related to that gene by using
the method :meth:`~bioservices.kegg.Kegg.bget`::

    k.bget("hsa:3586")

Commands shown so far are part of the Kegg WSDL service. Most of the Kegg
methods are directly available. To obtain all methods, type ::

    k.methods

If a method is not found, you can still directly access to the
service method via the attribute :meth:`~bioservices.kegg.Kegg.serv`.

In addition to the Kegg service, we implemented extra commands. 
The tutorial links here below provides more examples.

Uniprot service
==================

There is a uniprot module that allows to access to the uniprot WSDL. However,
there are really few service and the only relevant method returns raw data that
the user will need to scan. For instance::



    >>> from bioservices import uniprot
    >>> u = uniprot.Uniprot()
    >>> data = u.fetchBatch("uniprot" ,"zap70_human", "xml", "raw")


Then, you need to scan it with xml standard python module::

    >>> import xml.etree.ElementTree as ET
    >>> root = ET.fromstring(data)


Biomodels service
===================

You can access to the biomodels service and obtain a model as follows::


    >>> from bioservices import biomodels
    >>> b = biomodels.BioModels()
    >>> model = b.getModelSBMLById('BIOMD0000000299')

Then you can play with the SBML file with your favorite tools.


Rhea service 
==============

Create a :class:`~bioservices.rhea.Rhea` instance as follows:

.. doctest::

    from bioservices import Rhea
    r = Rhea()

Rhea provides only 2 type of requests with a REST interface that are available with the :meth:`~bioservices.rhea.Rhea.search` and :meth:`~bioservices.rhea.Rhea.entry` methods. Let us first find information about the chemical product **caffein** using the :meth:`search` method::

    xml_response = r.search("caffein")

The output is in XML format. Python provides lots of tools to deal with xml so
you can surely found good tools. However, we provide a couple of tools for basic
usage that are gathered in the :meth:`xmltools` module. As an example, we can
extract the Ids found in the **xml_response** variable as follows::

    >>> from bioservices import xmltools
    >>> ex = xmltools.easyXML_RheaSearch(xml_response)
    >>> ex.get_reactions_ids()
    ['27902', '10280', '20944', '30447', '30319', '30315', '30311', '30307']

The second method provided is the :meth:`entry` method. Given an Id, 
you can query the Rhea database using Id found earlier (e.g., 10280)::

    >>> xml_response = r.entry(10280, "biopax2")

.. warning:: the r.entry output is also in XML format but we do not provide a
   specific XML parser for it unlike for the "search" method.

output format can be found in ::

    >>> r.format_entry
    ['cmlreact', 'biopax2', 'rxn']

.. note:: Id may be in only a subset of the above formats
