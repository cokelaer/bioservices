**Bioservices**  provides a single framework to easily implement wrapper of Web Services. 
It focuses on  Life Sciences Web Services (based WSDL/SOAP or REST protocols).

The primary goal of **BioServices** is to use Python as a glue language to provide
a programmatic access to several Web Services. By doing so, elaboration of  new
applications that combine several of the wrapped Web Services should be
fostered.

One of the main philosophy of **BioServices** is to make use of the existing
biological databases (not to re-invent new databases) and to alleviates the
needs for expertise in web services for the developers/users.

So far, BioServices provides wrappers for about 17 Web Services including 

* `BioModels <http://www.ebi.ac.uk/biomodels-main/>`_
* `KEGG <http://www.genome.jp/kegg/pathway.html>`_
* `UniProt <http://www.uniprot.org/>`_
* `quickGO <http://www.ebi.ac.uk/QuickGO/WebServices.html>`_
* `PSICQUIC <http://code.google.com/p/psicquic/>`_
* `WikiPathway <http://www.wikipathways.org/index.php/WikiPathways>`_

Example using the UniProt Web Service to search for the zap70 specy in human
organism::

    >>> from bioservices import UniProt
    >>> u = UniProt(verbose=False)
    >>> data = u.search("zap70+and+taxonomy:9606", format="tab", limit=3, columns="entry name,length,id, genes")
    >>> print(data)
    Entry name   Length  Entry   Gene names
    ZAP70_HUMAN  619     P43403  ZAP70 SRK
    B4E0E2_HUMAN 185     B4E0E2
    RHOH_HUMAN   191     Q15669  RHOH ARHH TTF

Up-to-date list of Web Services is provided within the `documentation <http://pythonhosted.org/bioservices/>`_.
