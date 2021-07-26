


#################################################################################
BIOSERVICES: access to biological web services programmatically
#################################################################################


.. topic:: BioServices |version| (|today|)

    .. image:: bioservices.png
        :width: 50%


:Citations: If you use BioServices, please cite *Cokelaer et al, Bioinformatics (2013)*. 
    See `bioinformatics link <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_ 
    for details.



.. raw:: html

    <div style="width:80%"><p>

    <a href="https://pypi.python.org/pypi/bioservices">
    <img src="https://badge.fury.io/py/bioservices.svg"></a>

    <a href="https://github.com/cokelaer/bioservices/actions/workflows/ci.yml">
    <img src="https://github.com/cokelaer/bioservices/actions/workflows/ci.yml/badge.svg"></a>

    <a href="https://anaconda.org/conda-forge/spectrum/badges/license.svg">
    <img src="https://anaconda.org/conda-forge/spectrum/badges/license.svg"></a>

    <a href="http://bioservices.readthedocs.org/en/master/?badge=master">
    <img src='https://readthedocs.org/projects/bioservices/badge/?version=master' alt='Documentation Status' />

    </p>
    </div>



:Python version: Python 2.7, 3.6, 3.7
:Source: See  `http://github.com/cokelaer/bioservices <https://github.com/cokelaer/bioservices/>`_.
:Issues: Please fill a report on `github <https://github.com/cokelaer/bioservices/issues>`_


.. note:: Contributions to implement new wrappers are more than welcome. 
    See `BioServices github page <https://github.com/cokelaer/bioservices/>`_
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
that provides access to many Bioinformatics Web Services (e.g., UniProt, KeGG,
PDB, etc) as well as a framework to easily implement Web Service wrappers 
(based on WSDL/SOAP protocol or nowadays mostly REST protocol).

The primary goal of **BioServices** is to use Python as a glue language to provide 
a programmatic access to Biological Web Services. By doing so, elaboration of 
new applications that combine several Web Services should be fostered.

One of the main philosophy of **BioServices** is to make use of the
existing REST or SOAP/WSDL Web Services and therefore existing databases, not to 
re-invent new databases.

The first release of **BioServices** provides a wrapping to more than 18 Web
Services (more if we consider **BioMart** and **PSICQUIC** portals that link to
many other Web Services). 

Here are only some of Web Services that are available in **BioServices** (from
EBI mostly but not only; NCBI, KEGG, etc):


.. autosummary::
    :nosignatures:

    bioservices.arrayexpress.ArrayExpress
    bioservices.biomodels.BioModels
    bioservices.chembl.ChEMBL
    bioservices.chebi.ChEBI
    bioservices.eutils.EUtils
    bioservices.ensembl.Ensembl
    bioservices.kegg.KEGG
    bioservices.muscle.MUSCLE
    bioservices.panther.PantherDB
    bioservices.pdb.PDB
    bioservices.uniprot.UniProt
    bioservices.unichem.UniChem
    bioservices.ncbiblast.NCBIblast
    bioservices.wikipathway.Wikipathway



Full list is available in the User Guide and Reference here below. Some of the
services may be down. BioServices developers are not responsible for the
maintenance or failure of underlying services. Generally speaking (and by
experience) the services are up most of the time.


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
installed automatically when using **pip** installer. Since version 1.6.0, we
also make use of pandas and matplotlib to offer some extra functionalities. 


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
    auto_examples/index
    notebooks.rst
    references
    external_references.rst
    faqs
    ChangeLog.rst
    contributors
