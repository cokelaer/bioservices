




.. topic:: BioServices |version| (|today|)



.. include:: ../README.rst


.. toctree::
    :maxdepth: 2

.. warning:: Some of the services may be down. BioServices developers are not responsible for the
  maintenance or failure of underlying services. Generally speaking (and by
  experience) the services are up most of the time but failure may occur because
  the site is under maintenance or too many requests have been sent. Another
  common reason is the fact that the API of the web services has changed: If so,
  BioServices need to be updated. You may contribute or report such API changes on
  our `Issue <https://github.com/cokelaer/bioservices/issues>`_ page


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
