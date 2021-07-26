BioServices
##############

.. image:: https://badge.fury.io/py/bioservices.svg
    :target: https://pypi.python.org/pypi/bioservices

.. image:: https://github.com/cokelaer/bioservices/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/cokelaer/bioservices/actions/workflows/ci.yml

.. image:: http://readthedocs.org/projects/bioservices/badge/?version=master
    :target: http://bioservices.readthedocs.org/en/master/?badge=master
    :alt: Documentation Status


:Python_version_available: BioServices is tested for Python 2.7, 3.6, 3.7
:Contributions: Please join https://github.com/cokelaer/bioservices and share your notebooks https://github.com/bioservices/notebooks/
:Issues: Please use https://github.com/cokelaer/bioservices/issues
:How to cite: Cokelaer et al. *BioServices: a common Python package to access biological Web Services programmatically*
     `Bioinformatics <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_ (2013) 29 (24): 3241-3242
:Documentation: `RTD documentation <http://bioservices.readthedocs.io/>`_.

**Bioservices** is a Python package that provides access to many Bioinformatices Web Services (e.g.,
UniProt) and a framework to easily implement Web Services wrappers (based on 
WSDL/SOAP or REST protocols).

.. image:: https://raw.githubusercontent.com/cokelaer/bioservices/master/doc/bioservices.png
    :target: https://raw.githubusercontent.com/cokelaer/bioservices/master/doc/bioservices.png


The primary goal of **BioServices** is to use Python as a glue language to provide
a programmatic access to several Bioinformatics Web Services. By doing so, elaboration of  new
applications that combine several of the wrapped Web Services is fostered.

One of the main philosophy of **BioServices** is to make use of the existing
biological databases (not to re-invent new databases) and to alleviates the
needs for expertise in Web Services for the developers/users.

BioServices provides access to 43 Web Services. For a quick start,
look at some notebooks here `github cokelaer/bioservices <https://github.com/cokelaer/bioservices/tree/master/notebooks/>`_ and here `github bioservices <https://github.com/bioservices/notebooks>`_.

An up-to-date list of Web Services is provided within
the online `documentation <http://bioservices.readthedocs.io/>`_.

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

More examples and tutorials are available in the `On-line documentation <http://bioconvert.readthedocs.io/>`_


Here is the list of services available and their testing status

================= =============================================================================================
Service           CI testing
================= =============================================================================================
ChEBI             .. image:: https://github.com/cokelaer/bioservices/actions/workflows/chebi.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/chebi.yml
ChEMBL            .. image:: https://github.com/cokelaer/bioservices/actions/workflows/chembl.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/chembl.yml
ENA               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/ena.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/ena.yml
KEGG              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/kegg.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/kegg.yml
PFAM              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pfam.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/pfam.yml
PSICQUIC          .. image:: https://github.com/cokelaer/bioservices/actions/workflows/psicquic.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/psicquic.yml
Rhea              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/rhea.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/rhea.yml
Uniprot           .. image:: https://github.com/cokelaer/bioservices/actions/workflows/uniprot.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/uniprot.yml
EUtils            .. image:: https://github.com/cokelaer/bioservices/actions/workflows/eutils.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/eutils.yml
UniChem           .. image:: https://github.com/cokelaer/bioservices/actions/workflows/unichem.yml/badge.svg
                      :target: https://github.com/cokelaer/bioservices/actions/workflows/unichem.yml
================= =============================================================================================






