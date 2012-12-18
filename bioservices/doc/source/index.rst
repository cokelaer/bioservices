

#############################
BIOSERVICES from Python
#############################

Overview and Installation
##############################

`bioservices <http://pypi.python.org/pypi/bioservices>`_  is a python package that provides 
utilities to access biological databases that uses WSDL/SOAP or REST protocols.
The primary goal is to obtain an easy programmatic access to pathways. However,
by extension it allows access to other biological data if they are provided
within the database. The philosophy of **bioservices** is to make use of the 
existing SOAP/WSDL facilities provided in biological databases, not to re-invent new databases.

There are a lot of databases from many institutes;  some are free, some are not. The 
main motivation of bioservices is to provide a glue interface using python to some
of them (the free ones...). Right now, only the Kegg and biomodels interfaces have been written but
more should come soon (e.g., wikipathways, nci, ...).

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

