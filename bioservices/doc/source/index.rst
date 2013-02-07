


#################################################################################
BIOSERVICES: a Python package to access biological web services programmaticaly
#################################################################################

.. toctree::
    :maxdepth: 2

Overview and Installation
##############################

Overview
==========

`BioServices <http://pypi.python.org/pypi/bioservices>`_  is a Python package
that provides a framework to easily implement wrapper of Web Services. It focuses on
Biological Web Services based WSDL/SOAP or REST protocols.

The primary goal of BioServices is to use Python as a glue language to provide 
a programmatic access to several Web Services. By doing so, elaboration of 
new applications that combine several of the wrapped Web Services should be
fostered.

One of the main philosophy of **BioServices** is to make use of the
existing SOAP/WSDL facilities provided in biological databases, not to 
re-invent new databases.

There are a lot of Web Services from many institutes; some are free, some are not. The
first release of BioServices provides a wrapping to more than 10 Web
Services. Contributions to implement new wrapper are more than welcome. See
`BioServices wiki <https://www.assembla.com/spaces/bioservices/wiki>`_


Here is a list of services that you can already access from **BioServices**:

.. autosummary::
    :nosignatures:

    bioservices.biomodels.BioModels
    bioservices.kegg.Kegg
    bioservices.chembldb.ChEMBLdb
    bioservices.picr.PICR
    bioservices.quickgo.QuickGO
    bioservices.rhea.Rhea
    bioservices.uniprot.UniProt
    bioservices.wsdbfetch.WSDbfetch
    bioservices.ncbiblast.NCBIblast
    bioservices.psicquic.PSICQUIC
    bioservices.wikipathway.Wikipathway



The links above refers to the offical web site of each service (right column)
and our reference guide (left column) that provides an exhaustive documentation.
For tutorials and quick start please follow the links below. Before that let us
show you how to install BioServices.



.. _installation:


Installation
===============

**BioServices** is available on `PyPi <http://pypi.python.org/pypi/bioservices>`_, the Python package repository. The following command should install **BioServices** and its dependencies automatically provided you have **pip** on your system:: 

    pip install bioservices

If not, please see the external `pip installation page <http://www.pip-installer.org/en/latest/installing.html>`_ or `pip installation <http://thomas-cokelaer.info/blog/2013/02/python-pip-installation/>`_


.. toctree::
    :maxdepth: 3

User guide
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    quickstart.rst
    tutorials.rst
                           


.. toctree::
    :maxdepth: 2

References
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    references


