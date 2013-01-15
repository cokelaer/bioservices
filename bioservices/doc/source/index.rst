

#################################################################################
BIOSERVICES: a Python package to access biological web services programmaticaly
#################################################################################

.. toctree::
    :maxdepth: 2

Overview and Installation
##############################

Overview
==========

`bioservices <http://pypi.python.org/pypi/bioservices>`_  is a python package that provides 
utilities to access biological databases that uses WSDL/SOAP or REST protocols.
The primary goal is to obtain an easy programmatic access to pathways. However,
by extension it allows access to other type of services (e.g., chemical
reactions, protein identifier, ...). The philosophy of **bioservices** is to make use of the
existing SOAP/WSDL facilities provided in biological databases, not to re-invent new databases.

There are a lot of databases from many institutes. Some are free, some are not. The
main motivation of bioservices is to provide a glue interface using python to some
of them (mostly the free ones...).

Here is a list of services that you can access from **bioservices**:

.. autosummary::
    :nosignatures:

    bioservices.biomodels.BioModels
    bioservices.kegg.Kegg
    bioservices.reactome.Reactome
    bioservices.chembldb.Chembl
    bioservices.picr.PICR
    bioservices.quickgo.QuickGO
    bioservices.rhea.Rhea
    bioservices.uniprot.UniProt
    bioservices.wsdbfetch.WSDbfetch

The links above refers to the offical web site of each service (right column)
and our reference guide (left column) that provides an exhaustive documentation.
For tutorials and quick start please follow the links below. Before that let us
show you how to install bioservices.



.. _installation:


Installation
===============

**bioservices** is available on `PyPi <http://pypi.python.org/pypi/bioservices>`_, the Python package repository. The following command should install **bioservices** and its dependencies automatically provided you have **pip** on your system:: 

    pip install bioservices

If not, please see the external `pip installation page <http://www.pip-installer.org/en/latest/installing.html>`_. Another alternative if you have python 2.7 (not python 3.X) is to install ipython. The interactive ipython tool install an alternative to pip that is called easy_install. Once ipython is installed, type::

    easy_install bioservices


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


.. todo:: rename Chembl into ChEMBLdb
.. todo:: in biomodels: doc difference betzeen CHEId qnd CHEIId
