BioServices
##############

.. image:: https://badge.fury.io/py/bioservices.svg
    :target: https://pypi.python.org/pypi/bioservices

.. image:: https://secure.travis-ci.org/cokelaer/bioservices.png
    :target: http://travis-ci.org/cokelaer/bioservices

.. image:: https://img.shields.io/pypi/dw/bioservices.svg
    :target: https://img.shields.io/pypi/dw/bioservices.svg
    :alt: Number of PyPI downloads

.. image:: https://coveralls.io/repos/cokelaer/bioservices/badge.png?branch=master 
   :target: https://coveralls.io/r/cokelaer/bioservices?branch=master 

.. image:: https://landscape.io/github/cokelaer/bioservices/master/landscape.png
   :target: https://landscape.io/github/cokelaer/bioservices/master

.. image:: https://badge.waffle.io/cokelaer/bioservices.png?label=ready&title=Ready 
   :target: https://waffle.io/cokelaer/bioservices

:Python version available: BioServices is tested for Python 2.6,2.7, 3.3, 3.4, 3.5
:Contributions: Please join https://github.com/cokelaer/bioservices and share your notebooks https://github.com/bioservices/notebooks/
:Issues: Please use https://github.com/cokelaer/bioservices/issues
:How to cite: Cokelaer et al. *BioServices: a common Python package to access biological Web Services programmatically*
     `Bioinformatics <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_ (2013) 29 (24): 3241-3242
:Documentation: `Pypi documentation <http://pythonhosted.org/bioservices/>`_.

**Bioservices** is a Python package that provides access to many Bioinformatices Web Services (e.g.,
UniProt) and a framework to easily implement Web Services wrappers (based on 
WSDL/SOAP or REST protocols).

.. image:: http://pythonhosted.org//bioservices/_images/bioservices.png
    :target: http://pythonhosted.org//bioservices/_images/bioservices.png


The primary goal of **BioServices** is to use Python as a glue language to provide
a programmatic access to several Bioinformatics Web Services. By doing so, elaboration of  new
applications that combine several of the wrapped Web Services is fostered.

One of the main philosophy of **BioServices** is to make use of the existing
biological databases (not to re-invent new databases) and to alleviates the
needs for expertise in Web Services for the developers/users.

BioServices provides access to 25 Web Services including. For a quick start,
look at some notebooks related to 

* UniProt on `uniprot nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org//bioservices/_downloads/UniProt.ipynb>`_
* BioModels on `biomodels nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org//bioservices/_downloads/BioModels.ipynb>`_
* ChEMBL on `chembl nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org//bioservices/_downloads/ChEMBL.ipynb>`_
* Ensembl on `Ensembl nbviewer <https://github.com/bioservices/notebooks/tree/master/ensembl>`_
* KEGG on `KEGG nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/KEGG.ipynb>`_
* MUSCLE on `MUSCLE  nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/MUSCLE.ipynb>`_
* NCBIBlast on `ncbiblast nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/NCBIBlast.ipynb>`_
* WikiPathway on `wikipathway nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/WikiPathway.ipynb>`_

and more on `nbviewer <http://nbviewer.ipython.org/github/cokelaer/bioservices/tree/master/doc/source/notebook/>`_.

An up-to-date list of Web Services is provided within 
the online `documentation <http://pythonhosted.org/bioservices/>`_.

Here is a small example using the UniProt Web Service to search for the zap70 specy in human
organism::

    >>> from bioservices import UniProt
    >>> u = UniProt(verbose=False)
    >>> data = u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, 
    ...                 columns="entry name,length,id, genes")
    >>> print(data)
    Entry name   Length  Entry   Gene names
    ZAP70_HUMAN  619     P43403  ZAP70 SRK
    B4E0E2_HUMAN 185     B4E0E2
    RHOH_HUMAN   191     Q15669  RHOH ARHH TTF

More examples and tutorials are available in the exhaustive 
`On-line documentation <http://pythonhosted.org//bioservices>`_




Release History
------------------
This is a summary of the changelog. Complete change can be found in the 
`main documentation <http://pythonhosted.org//bioservices/ChangeLog.html>`_.



1.4.X
---------------

* Update uniprot valid column names.
* Renamed kegg.KEGG.info into dbinfo , which was overloaded with Logging
* Replaced deprecated HGNC with the official web service from genenames.org
* Fully updated EUtils since WSDL is now down; implementation uses REST now.
* Removed the apps/taxonomy module now part of http://github.com/biokit. 
* added http_delete in services.py





1.3.X
+++++++++++

* Source code moved to github.com
* New REST class to use **requests** package instead of urllib2. 
* Creation of a global configuration file in .config/bioservice/bioservices.cfg
* NEW services: Reactome, Readseq, Ensembl, EUtils, PRIDE, clinvitae, Intact
  (complex)
* CHANGES: all parameters called format have been renamed frmt (to avoid using Python keyword)

1.2.X
+++++++++++

* add try/except for pandas library.
* added sub-package called apps with some useful tools (fasta,peptides, taxon) in bioservices.apps directory
* NEW services: BioDBnet, BioDBNet, MUSCLE, PathwayCommons, GeneProf

1.1.X
+++++++++++ 
* NEW services: biocarta, pfam, ChEBI, UniChem
* Add documentation and examples related to Galaxy/BioPython.
* NEW Service : HGNC
* Use BeautifulSoup4 instead of 3

1.0.X
+++++++++++ 
* add PDB, ArrayExpress,  biomart, chemspider draft, eutils, miriam, arrayexpress 

1.0.0
++++++

* First release of bioservices including the following services:
  BioModels, Kegg, Reactome, Chembl, PICR, QuickGO, Rhea, UniProt,
  WSDbfetch, NCBIblast, PSICQUIC, Wikipath
