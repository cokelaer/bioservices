#################################################################################
BIOSERVICES: access to biological web services programmatically
#################################################################################


.. image:: https://badge.fury.io/py/bioservices.svg
    :target: https://pypi.python.org/pypi/bioservices

.. image:: https://github.com/cokelaer/bioservices/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/cokelaer/bioservices/actions/workflows/ci.yml

.. image:: http://readthedocs.org/projects/bioservices/badge/?version=master
    :target: http://bioservices.readthedocs.org/en/master/?badge=master
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/cokelaer/bioservices/master/doc/bioservices.png
    :target: https://raw.githubusercontent.com/cokelaer/bioservices/master/doc/bioservices.png

:Python_version_available: BioServices is tested for Python 3.6, 3.7, 3.8
:Contributions: Please join https://github.com/cokelaer/bioservices and share your notebooks https://github.com/bioservices/notebooks/
:Issues: Please use https://github.com/cokelaer/bioservices/issues
:How to cite: Cokelaer et al. *BioServices: a common Python package to access biological Web Services programmatically*
     `Bioinformatics <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_ (2013) 29 (24): 3241-3242
:Documentation: `RTD documentation <http://bioservices.readthedocs.io/>`_.

**Bioservices** is a Python package that provides access to many Bioinformatices Web Services (e.g.,
UniProt) and a framework to easily implement Web Services wrappers (based on 
WSDL/SOAP or REST protocols).


The primary goal of **BioServices** is to use Python as a glue language to provide
a programmatic access to several Bioinformatics Web Services. By doing so, elaboration of  new
applications that combine several of the wrapped Web Services is fostered.

One of the main philosophy of **BioServices** is to make use of the existing
biological databases (not to re-invent new databases) and to alleviates the
needs for expertise in Web Services for the developers/users.

BioServices provides access to about 40 Web Services. 

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

More examples and tutorials are available in the `On-line documentation <http://bioservices.readthedocs.io/>`_

Here is the list of services available and their testing status.


==================== ================================================================================================
Service              CI testing
==================== ================================================================================================
arrayexpress          .. image:: https://github.com/cokelaer/bioservices/actions/workflows/arrayexpress.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/arrayexpress.yml
bigg                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/bigg.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/bigg.yml
biocarta              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/biocarta.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/biocarta.yml
biodbnet              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/biodbnet.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/biodbnet.yml
biogrid               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/biogrid.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/biogrid.yml
biomart               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/biomart.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/biomart.yml
biomodels             .. image:: https://github.com/cokelaer/bioservices/actions/workflows/biomodels.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/biomodels.yml
chebi                 .. image:: https://github.com/cokelaer/bioservices/actions/workflows/chebi.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/chebi.yml
chembl                .. image:: https://github.com/cokelaer/bioservices/actions/workflows/chembl.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/chembl.yml
cog                   .. image:: https://github.com/cokelaer/bioservices/actions/workflows/cog.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/cog.yml
dbfetch               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/dbfetch.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/dbfetch.yml
ena                   .. image:: https://github.com/cokelaer/bioservices/actions/workflows/ena.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/ena.yml
ensembl               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/ensembl.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/ensembl.yml
eutils                .. image:: https://github.com/cokelaer/bioservices/actions/workflows/eutils.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/eutils.yml
eva                   .. image:: https://github.com/cokelaer/bioservices/actions/workflows/eva.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/eva.yml
hgnc                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/hgnc.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/hgnc.yml
intact_complex        .. image:: https://github.com/cokelaer/bioservices/actions/workflows/intact_complex.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/intact_complex.yml
kegg                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/kegg.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/kegg.yml
muscle                .. image:: https://github.com/cokelaer/bioservices/actions/workflows/muscle.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/muscle.yml
mygeneinfo            .. image:: https://github.com/cokelaer/bioservices/actions/workflows/mygeneinfo.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/mygeneinfo.yml
ncbiblast             .. image:: https://github.com/cokelaer/bioservices/actions/workflows/ncbiblast.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/ncbiblast.yml
omicsdi               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/omicsdi.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/omicsdi.yml
omnipath              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/omnipath.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/omnipath.yml
panther               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/panther.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/panther.yml
pathwaycommons        .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pathwaycommons.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/pathwaycommons.yml
pdb                   .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pdb.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/pdb.yml
pdbe                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pdbe.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/pdbe.yml
pfam                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pfam.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/pfam.yml
pride                 .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pride.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/pride.yml
psicquic              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/psicquic.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/psicquic.yml
pubchem               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/pubchem.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/pubchem.yml
quickgo               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/quickgo.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/quickgo.yml
reactome              .. image:: https://github.com/cokelaer/bioservices/actions/workflows/reactome.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/reactome.yml
rhea                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/rhea.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/rhea.yml
rnaseq_ebi            .. image:: https://github.com/cokelaer/bioservices/actions/workflows/rnaseq_ebi.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/rnaseq_ebi.yml
seqret                .. image:: https://github.com/cokelaer/bioservices/actions/workflows/seqret.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/seqret.yml
unichem               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/unichem.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/unichem.yml
uniprot               .. image:: https://github.com/cokelaer/bioservices/actions/workflows/uniprot.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/uniprot.yml
wikipathway           .. image:: https://github.com/cokelaer/bioservices/actions/workflows/wikipathway.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/wikipathway.yml
==================== ================================================================================================


.. note:: Contributions to implement new wrappers are more than welcome. 
    See `BioServices github page <https://github.com/cokelaer/bioservices/>`_
    to join the development, and the Developer guide on how to implement new
    wrappers.


========= ====================================================================
Version   Description
========= ====================================================================
1.8.0     * add main standalone application. 
          * moved chemspider and clinvitae to the attic
          * removed picr service, not active anymore
========= ====================================================================


