.. _quickstart:

Quick Start
#################

Bioservices provides several services. Each service requires some expertise so
we will neither cover all the services nor all their functionalities in this quickstart. However by the end of this tutorials you should be able to play with all services provided in bioservices. 

There are two main technology involved in web services: the WSDL and the REST
styles. The Kegg and Biomodels services presented uses WSDL whereas uniprot uses
REST.

.. contents::


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

    >>> res = u.search("P09958", format="xml")
    >>> u.search("P09958", format="fasta")
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


PICR, the Protein Identifier Cross Reference service. It provides 2 serives 
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
