Bioservices  provides a framework to easily implement wrapper of Web Services. 
It focuses on  Biological Web Services based WSDL/SOAP or REST protocols.

The primary goal of **BioServices** is to use Python as a glue language to provide
a programmatic access to several Web Services. By doing so, elaboration of  new
applications that combine several of the wrapped Web Services should be
fostered.

One of the main philosophy of **BioServices** is to make use of the existing
SOAP/WSDL facilities provided in biological databases, not to  re-invent new
databases.

So far, BioServices provides wrappers for about 10 Web Services including `KEGG <http://www.genome.jp/kegg/pathway.html>`_, `UniProt <http://www.uniprot.org/>`_, `BioModels <http://www.ebi.ac.uk/biomodels-main/>`_, `WikiPathway <http://www.wikipathways.org/index.php/WikiPathways>`_, `quickGO <http://www.ebi.ac.uk/QuickGO/WebServices.html>`_, `PSIQUIC <http://code.google.com/p/psicquic/>`_.

Example using the UniProt Web Service to search for the zap70 specy in human
organism::

    >>> from bioservices import UniProt
    >>> u = UniProt(verbose=False)
    >>> data = u.search("zap70+and+taxonomy:9606", format="tab", limit=3, columns="entry name,length,id, genes")
    >>> print(data)
    Entry name  Length  Entry   Gene names
    ZAP70_HUMAN 619 P43403  ZAP70 SRK
    B4E0E2_HUMAN    185 B4E0E2  
    RHOH_HUMAN  191 Q15669  RHOH ARHH TTF



