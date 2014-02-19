


#################################################################################
BIOSERVICES: a Python package to access biological web services programmatically
#################################################################################

.. topic:: BioServices

    .. image:: bioservices.png
        :width: 50%

    :Citations: If you use BioServices, please cite *Cokelaer et al, Bioinformatics (2013)*. See `bioinformatics link <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_ for details.


.. note:: Contributions to implement new wrappers are more than welcome. 
    See `BioServices wiki <https://www.assembla.com/spaces/bioservices/wiki>`_
    to join the development, and the :ref:`developer` on how to implement new
    wrappers. Although contributors have their names in the header files, you
    can also look at the :ref:`contributors` directly.

.. toctree::
    :maxdepth: 2

Overview and Installation
##############################

Overview
==========

`BioServices <http://pypi.python.org/pypi/bioservices>`_  is a Python package
that provides access to many Bioinformatics Web Services (e.g., UniProt) and 
a framework to easily implement Web Service wrappers (based on WSDL/SOAP or 
REST protocols).

The primary goal of **BioServices** is to use Python as a glue language to provide 
a programmatic access to Biological Web Services. By doing so, elaboration of 
new applications that combine several Web Services should be fostered.

One of the main philosophy of **BioServices** is to make use of the
existing REST or SOAP/WSDL Web Services and therefore existing databases, not to 
re-invent new databases.

The first release of **BioServices** provides a wrapping to more than 18 Web
Services (more if we consider **BioMart** and **PSICQUIC** portals that link to
many other Web Services). 

Here is a list of Web Services that can already be accessed from **BioServices**:

.. autosummary::
    :nosignatures:

    bioservices.arrayexpress.ArrayExpress
    bioservices.biodbnet.BioDBNet
    bioservices.biomodels.BioModels
    bioservices.biomart.BioMart
    bioservices.chebi.ChEBI
    bioservices.chembldb.ChEMBLdb
    bioservices.eutils.EUtils
    bioservices.geneprof.GeneProf
    bioservices.kegg.Kegg
    bioservices.hgnc.HGNC
    bioservices.miriam.Miriam
    bioservices.muscle.MUSCLE
    bioservices.pdb.PDB
    bioservices.pathwaycommons.PathwayCommons
    bioservices.picr.PICR
    bioservices.quickgo.QuickGO
    bioservices.rhea.Rhea
    bioservices.unichem.UniChem
    bioservices.uniprot.UniProt
    bioservices.wsdbfetch.WSDbfetch
    bioservices.ncbiblast.NCBIblast
    bioservices.psicquic.PSICQUIC
    bioservices.wikipathway.Wikipathway


The links above refers to the official web site of each service (right column)
and our reference guide (left column) that provides an exhaustive documentation.
For tutorials and quick start please follow the links below. 



.. _installation:


Installation
===============

**BioServices** is available on `PyPi <http://pypi.python.org/pypi/bioservices>`_, the Python package repository. The following command should install **BioServices** and its dependencies automatically provided you have **pip** on your system:: 

    pip install bioservices

If not, please see the external `pip installation page <http://www.pip-installer.org/en/latest/installing.html>`_ or `pip installation <http://thomas-cokelaer.info/blog/2013/02/python-pip-installation/>`_ entry. You may also find information in the :ref:`troubleshootings page <troubleshootings>` section about known issues.

Regarding the dependencies, BioServices depends on the following
packages: **BeautifulSoup4** (for parsing XML), **SOAPpy** and **suds** (to access to
SOAP/WSDL services; suds is used by ChEBI only for which SOAPpy fails to
correctly fetch the service) and **easydev**. All those packages should be
installed automatically when using **pip** installer.


.. toctree::
    :maxdepth: 3

User guide
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    quickstart.rst
    tutorials.rst
    applications.rst
    developers.rst


.. toctree::
    :maxdepth: 2

References
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    references



Others
#################################

.. toctree::
    :maxdepth: 2
    :numbered:

    external_references.rst
    faqs
    ChangeLog.rst
    contributors
