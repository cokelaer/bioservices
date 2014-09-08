BioServices
##############

.. image:: https://badge.fury.io/py/bioservices.svg
    :target: https://pypi.python.org/pypi/bioservices

.. image:: https://pypip.in/d/bioservices/badge.png
    :target: https://crate.io/packages/bioservices/

.. image:: https://secure.travis-ci.org/cokelaer/bioservices.png
    :target: http://travis-ci.org/cokelaer/bioservices

.. image:: https://coveralls.io/repos/cokelaer/bioservices/badge.png?branch=master 
   :target: https://coveralls.io/r/cokelaer/bioservices?branch=master 

.. image:: https://landscape.io/github/cokelaer/bioservices/master/landscape.png
   :target: https://landscape.io/github/cokelaer/bioservices/master

.. image:: https://badge.waffle.io/cokelaer/bioservices.png?label=ready&title=Ready 
   :target: https://waffle.io/cokelaer/bioservices


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
* ChhEMBL on `chembl nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org//bioservices/_downloads/ChEMBL.ipynb>`_
* KEGG on `KEGG nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/KEGG.ipynb>`_
* MUSCLE on `MUSCLE  nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/MUSCLE.ipynb>`_
* NCBIBlast on `ncbiblast nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/NCBIBlast.ipynb>`_
* WikiPathway on `wikipathway nbviewer <http://nbviewer.ipython.org/url/pythonhosted.org/bioservices/_downloads/WikiPathway.ipynb>`_

and more on `github <https://github.com/cokelaer/bioservices/tree/master/doc/source/notebook>`_.

An up-to-date list of Web Services is provided within 
the online `documentation <http://pythonhosted.org/bioservices/>`_.

Here is a little example using the UniProt Web Service to search for the zap70 specy in human
organism::

    >>> from bioservices import UniProt
    >>> u = UniProt(verbose=False)
    >>> data = u.search("zap70+and+taxonomy:9606", format="tab", limit=3, 
    ...                 columns="entry name,length,id, genes")
    >>> print(data)
    Entry name   Length  Entry   Gene names
    ZAP70_HUMAN  619     P43403  ZAP70 SRK
    B4E0E2_HUMAN 185     B4E0E2
    RHOH_HUMAN   191     Q15669  RHOH ARHH TTF

More examples and tutorials are available in the exhaustive 
`On-line documentation <http://pythonhosted.org//bioservices>`_
