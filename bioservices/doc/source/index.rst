

#############################
BIOSERVICES from Python
#############################

Overview and Installation
##############################

`bioservices <http://pypi.python.org/pypi/bioservices>`_  is a python package that provides 
utilities to access biological databases that uses WSDL protocol.
The primary goal is to obtain an easy programmatic access to pathways. However,
by extension it allows access to other biological data if they are provided
within the database. The philosophy of **bioservices** is to make use of the 
existing SOAP/WSDL facilities provided in biological databases, not to re-invent new databases.

There are a lot of databases in signalling pathways, some free, some not, and
this package main motivation is to provide a glue interface using python to some
of them (the free ones...). Right now, only the Kegg interface has been written but
more should come soon (e.g., wikipathways, nci, ...).

This package allows to retrieve information and ease introspection of DB. It
does not provide an ouput standard such as SBML, which is done by other projects such
as BioModels, or more generally by the databases authors.



.. _installation:

Installation
===============


**bioservices** is available on `PyPi <http://pypi.python.org/pypi/bioservices>`_. The following command should install **bioservices** and its dependencies automatically:: 

    easy_install bioservices

or::

    pip install bioservices




User guide
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    quickstart.rst


References
##################


.. toctree::
    :maxdepth: 2
    :numbered:

    references

