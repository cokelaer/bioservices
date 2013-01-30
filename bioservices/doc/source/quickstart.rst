.. _quickstart:

Quick Start
#################

Bioservices provides several services. Each service requires some expertise so
we will neither cover all the services nor all their functionalities in this quickstart. However by the end of this tutorials you should be able to play with all services provided in bioservices. 

There are two main technology involved in web services: the WSDL and the REST
styles. The Kegg and Biomodels services presented uses WSDL whereas uniprot uses
REST.


#.  RESTful URLs are useful in that there is no need for any external
    dependency. You simply need to build a well-formatted URL and you will retrieve
    an XML docum    ent that you can consume with your preferred technology
    platform. The XML document that is returned will contain elements defined in the
    WSDL schema.


Web services is an integration and inter-operation technology, to ensure client and server software from various sources will work well together, the technology is built on open standards:

    Representational state transfer (REST): a software architecture style.
    Simple Object Access Protocol (SOAP): a messaging protocol for transporting information.
    Web Services Description Language (WSDL): a method for describing Web Services and their capabilities.




Kegg service
=============


Start a kegg interface (default organism is human, that is called hsa)::

    from bioservices.kegg import Kegg
    k = Kegg(verbose=False)

There are 5-6 main functions (e.g., :meth:`~bioservices.kegg.Kegg.list`) 
that allow access to the KEGG database. First, you can obtain information about
the data base itself. Just type::

    print k

to obtain statistics. You can refine your search by using the info method.::

    >>> print k.info("pathway")
    pathway          KEGG Pathway Database
    path             Release 65.0+/01-15, Jan 13
                     Kanehisa Laboratories
                     218,277 entries

In order to get the list of valid organisms, type::

    print k.organismIds

The human organism is coded as "hsa". You can also get the T number instead of
Ids::

    print k.orgamisms_tnumbers


Every elements is referred to with a Kegg ID, which may be difficult to handle
at first. There are methods to retrieve the IDs though. For instance, get the list of 
pathways ids for the current organism as follows::

    k.pathwayIDs

For a given gene, you can get the full information related to that gene by using
the method :meth:`~bioservices.kegg.Kegg.bget`::

    print k.get("hsa:3586")

or a pathway::

    print k.get("path:hsa05416")



.. seealso:: Reference guide of :class:`bioservices.kegg.KEGG` for more details
.. seealso:: Reference guide of :ref:`kegg_tutorial` for more details

WSDbfetch service
==================

There is a uniprot module that allows to access to the uniprot WSDL. However,
there are really few service and the only relevant method returns raw data that
the user will need to scan. For instance::



    >>> from bioservices import WSDbfetch
    >>> w = WSDbfetch()
    >>> data = w.fetchBatch("uniprot" ,"zap70_human", "xml", "raw")



.. seealso:: Reference guide of :class:`bioservices.wsdbfetch.WSDbfetch` for more details


UniProt service
================

With this module, you can map an ID from a database to another one. For instance
to convert the uniprotKB ID into KEGG ID, use:

.. doctest::

    >>> from bioservices.uniprot import UniProt
    >>> u = UniProt(verbose=False)
    >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403')
    ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535']

Note that the returned response from uniprot web service is converted into a list.

You can also search for a specific UniProtKB id to get exhaustive information
about an ID::

    >>> res = u.searchUniProtId("P09958", format="xml")
    >>> u.searchUniProtId("P09958", format="fasta")
    '>sp|P09958|FURIN_HUMAN Furin OS=Homo sapiens GN=FURIN PE=1SV=2\nMELRPWLLWVVAATGTLVLLAADAQGQKVFTNTWAVRIPGGPAVANSVARKHGFLNLGQI\nFGDYYHFWHRGVTKRSLSPHRPRHSRLQREPQVQWLEQQVAKRRTKRDVYQEPTDPKFPQ\nQWYLSGVTQRDLNVKAAWAQGYTGHGIVVSILDDGIEKNHPDLAGNYDPGASFDVNDQDP\nDPQPRYTQMNDNRHGTRCAGEVAAVANNGVCGVGVAYNARIGGVRMLDGEVTDAVEARSL\nGLNPNHIHIYSASWGPEDDGKTVDGPARLAEEAFFRGVSQGRGGLGSIFVWASGNGGREH\nDSCNCDGYTNSIYTLSISSATQFGNVPWYSEACSSTLATTYSSGNQNEKQIVTTDLRQKC\nTESHTGTSASAPLAAGIIALTLEANKNLTWRDMQHLVVQTSKPAHLNANDWATNGVGRKV\nSHSYGYGLLDAGAMVALAQNWTTVAPQRKCIIDILTEPKDIGKRLEVRKTVTACLGEPNH\nITRLEHAQARLTLSYNRRGDLAIHLVSPMGTRSTLLAARPHDYSADGFNDWAFMTTHSWD\nEDPSGEWVLEIENTSEANNYGTLTKFTLVLYGTAPEGLPVPPESSGCKTLTSSQACVVCE\nEGFSLHQKSCVQHCPPGFAPQVLDTHYSTENDVETIRASVCAPCHASCATCQGPALTDCL\nSCPSHASLDPVEQTCSRQSQSSRESPPQQQPPRLPPEVEAGQRLRAGLLPSHLPEVVAGL\nSCAFIVLVFVTVFLVLQLRSGFSFRGVKVYTMDRGLISYKGLPPEAWQEECPSDSEEDEG\nRGERTAFIKDQSAL\n'


.. seealso:: Reference guide of :class:`bioservices.uniprot.UniProt` for more details

QuickGO
=========

Quick access to the GO interface
.. doctest::

    >>> from bioservices import QuickGO
    >>> g = QuickGO(verbose=False)
    >>> res = g.Term("GO:0003824")

PICR service
=============


PICR, the Protein Identifier Cross Reference service. It provides 2 services 
in WSDL and REST protocols. We implemented only the REST interface. The 
methods available in the REST service are very similar to those available 
via SOAP, save for one major difference: only one accession or sequence 
can be mapped per request.


The following example returns a XML document containing information about the
protein P29375 found in two specific databases::

    >>> from bioservices.picr import PICR
    >>> p = PICR()
    >>> res = p.getUPIForAccession("P29375", ["IPI", "ENSEMBL"])
    

.. seealso:: Reference guide of :class:`bioservices.picr.PICR` for more details


Biomodels service
===================

You can access the biomodels service and obtain a model as follows::


    >>> from bioservices import biomodels
    >>> b = biomodels.BioModels()
    >>> model = b.getModelSBMLById('BIOMD0000000299')

Then you can play with the SBML file with your favorite tools.

In order to get the model IDs, you can look at the full list::

    >>> b.modelsId

Of course it does not tell you anything about a model; there are more useful functions such as 
:meth:`~bioservices.services.biomodels.getModelsIdByUniprotId` and others from the getModelsIdBy family.


.. seealso:: Reference guide of :class:`bioservices.biomodels.BioModels` for more details

Rhea service 
==============

Create a :class:`~bioservices.rhea.Rhea` instance as follows:

.. doctest::

    from bioservices import Rhea
    r = Rhea()

Rhea provides only 2 type of requests with a REST interface that are available with the :meth:`~bioservices.rhea.Rhea.search` and :meth:`~bioservices.rhea.Rhea.entry` methods. Let us first find information about the chemical product **caffein** using the :meth:`search` method::

    xml_response = r.search("caffein*")

The output is in XML format. Python provides lots of tools to deal with xml so
you can surely found good tools. 


Within bioservices, we wrap all returned XML document into a BeautifulSoup
object that ease the manipulaiton of XML documents.

As an example, we can extract all fields "id" as follows::

    >>> ids = [x.getText() for x in xml_response.findAll("id")]
    [u'27902', u'10280', u'20944', u'30447', u'30319', u'30315', u'30311', u'30307']

The second method provided is the :meth:`entry` method. Given an Id, 
you can query the Rhea database using Id found earlier (e.g., 10280)::

    >>> xml_response = r.entry(10280, "biopax2")

.. warning:: the r.entry output is also in XML format but we do not provide a
   specific XML parser for it unlike for the "search" method.

output format can be found in ::

    >>> r.format_entry
    ['cmlreact', 'biopax2', 'rxn']

.. note:: Id may be in only a subset of the above formats


Create your own wrapper around WSDL service
==============================================

If a web service interface is not provided within bioservices, you can still easily access its functionalities. As an example, let us look at the `Ontology Lookup service <http://www.ebi.ac.uk/ontology-lookup/WSDLDocumentation.do>`_, which provides a WSDL service. In order to easily access this service, use the :class:`WSDLService` class as follows::

    >>> from bioservices import WSDLService
    >>> ols = WSDLService("OLS", " http://www.ebi.ac.uk/ontology-lookup/OntologyQuery.wsdl")

You can now see which methods are available::

    >>> ols.methods

and call one (getVersion) using the :meth:`bioservices.services.WSDLService.serv`::

    >>> ols.serv.getVersion()

You can then look at something more complex and extract relevant information::

    >>> [x.value for x in ols.serv.getOntologyNames()[0]]

Of course, you can add new methods to ease the access to any functionalities::

    >>> ols.getOnlogyNames() # returns the values
