.. image:: https://raw.githubusercontent.com/cokelaer/bioservices/main/doc/_static/bioservices2_logo_256.png
    :target: https://raw.githubusercontent.com/cokelaer/bioservices/main/doc/_static/bioservices2_logo_256.png


#################################################################################
BIOSERVICES: access to biological web services programmatically
#################################################################################


.. image:: https://badge.fury.io/py/bioservices.svg
    :target: https://pypi.python.org/pypi/bioservices

.. image:: https://github.com/cokelaer/bioservices/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/cokelaer/bioservices/actions/workflows/ci.yml

.. image:: http://readthedocs.org/projects/bioservices/badge/?version=main
    :target: http://bioservices.readthedocs.org/en/main/?badge=main
    :alt: Documentation Status

.. image:: https://static.pepy.tech/personalized-badge/bioservices?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads
    :target: https://pepy.tech/project/bioservices

.. image:: https://anaconda.org/conda-forge/bioservices/badges/version.svg   
    :target: https://anaconda.org/conda-forge/bioservices


|Codacy-Grade|



:Python_version_available: BioServices is tested for Python 3.7, 3.8, 3.9, 3.10
:Contributions: Please join https://github.com/cokelaer/bioservices 
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

Contributors
============

Maintaining BioServices would not have been possible without users and contributors. 
Each contribution has been an encouragement to pursue this project. Thanks to all:

.. image:: https://contrib.rocks/image?repo=cokelaer/bioservices
    :target: https://github.com/cokelaer/bioservices/graphs/contributors


Quick example
=============

Here is a small example using the UniProt Web Service to search for the zap70 specy in human
organism::

    >>> from bioservices import UniProt
    >>> u = UniProt(verbose=False)
    >>> data = u.search("zap70+and+taxonomy_id:9606", frmt="tsv", limit=3, 
    ...                 columns="id,length,accession, gene_names")
    >>> print(data)
    Entry name   Length  Entry   Gene names
    ZAP70_HUMAN  619     P43403  ZAP70 SRK
    B4E0E2_HUMAN 185     B4E0E2
    RHOH_HUMAN   191     Q15669  RHOH ARHH TTF


.. note:: major changes of UniProt API changed all columns names in June 2022. The code above is valid for bioservices
   versions >1.10. Earlier version used::

        >>> data = u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, 
        ...                 columns="entry name,length,id, genes")

   Note that columns names have changed, the frmt was changed from tab to tsv 
   and taxonomy is now taxonomy_id. Names correspondences can be found in::

        u._legacy_names


More examples and tutorials are available in the `On-line documentation <http://bioservices.readthedocs.io/>`_

Current services
================
Here is the list of services available and their testing status.


==================== ================================================================================================
Service              CI testing
==================== ================================================================================================
arrayexpress          .. image:: https://github.com/cokelaer/bioservices/actions/workflows/arrayexpress.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/arrayexpress.yml
bigg                  .. image:: https://github.com/cokelaer/bioservices/actions/workflows/bigg.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/bigg.yml
biocontainers         .. image:: https://github.com/cokelaer/bioservices/actions/workflows/biocontainers.yml/badge.svg
                         :target: https://github.com/cokelaer/bioservices/actions/workflows/biocontainers.yml
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

Bioservices command
====================

In version 1.8.2, we included a bioservices command. For now it has only one subcommand to download a NCBI accession number and possibly it genbank or GFF file (if available)::

    bioservices download-accession --accession K01711.1 --with-gbk 


Changelog
=========


========= ====================================================================
Version   Description
========= ====================================================================
1.11.2    * Update COG service to be more user-friendly and return all pages
            by default
          * uniprot set progress to False in the search method
          * Merged #250 and #249 user PRs (compress option in uniprot module 
            and logging issue in biodbnet)
1.11.1    * Fix regression i uniprot.mapping 
            (https://github.com/cokelaer/bioservices/issues/245)
1.11.0    * Fix uniprot limitation of 25 results only (
          * For developers: all services are now refactorised to use services
            as an attribute rather than a parent class.
          * Remove ReactomeOld and ReactomeAnalysis (deprecated)
          * move rnaseq_ebi (deprecated) to attic for book_keeping
1.10.4    * Fix v1.10.3 adding missing requirements.txt
1.10.3    * Update pdb service to use v2 API
          * remove biocarta (website not accesible anymore)
          * Update Chembl (no API changes)
1.10.2    * Fix #226 and applied PR from Fix from @GianArauz
            https://github.com/cokelaer/bioservices/pull/232 about UniProt 
            error
          * Update MANIFEST to fix #232
1.10.1    * allow command line to download genbank and GFF
          * update pride module to use new PRIDE API (July 2022)
          * Fixed KEGG bug #225
1.10.0    * Update uniprot to use the new API (june 2022)
1.9.0     * Update unichem to reflect new API
1.8.4     * biomodels. Fix #208
          * KEGG: fixed #204 #202 and #203
1.8.3     * Eutils: remove warning due to unreachable URL. Set REST as
            attribute rather and inheritance. 
          * NEW biocontainers module
          * KEGG: add save_pathway method. Fix parsing of structure/pdb entry
          * remove deprecated function from Reactome
1.8.2     * Fix suds package in code and requirements
1.8.1     * Integrated a change made in KEGG service (DEFINITON was changed to
            ORG_CODE)
          * for developers: applied black on all modules
          * switch suds-jurko to new suds community 
1.8.0     * add main standalone application. 
          * moved chemspider and clinvitae to the attic
          * removed picr service, not active anymore
1.4.X     * NEW RNAseq from EBI in rnaseq_ebi module
          * Replaced deprecated HGNC with the official web service from genenames.org
          * Fully updated EUtils since WSDL is now down; implementation uses REST now.
          * Removed the apps/taxonomy module now part of http://github.com/biokit. 
1.3.X     * CACHE files are now stored in a general directory in the home
          * New REST class to use **requests** package instead of urllib2. 
          * Creation of a global configuration file in .config/bioservice/bioservices.cfg
          * NEW services: Reactome, Readseq, Ensembl, EUtils
1.2.X     * NEW services: BioDBnet, BioDBNet, MUSCLE, PathwayCommons, GeneProf
1.1.X     * NEW services: biocarta, pfam, ChEBI, UniChem
1.0.0:    * first stable release
0.9.X:    * NEW services: BioModels, Kegg, Reactome, Chembl, PICR, QuickGO, 
            Rhea, UniProt,WSDbfetch, NCBIblast, PSICQUIC, Wikipath
========= ====================================================================


.. |Codacy-Grade| image:: https://app.codacy.com/project/badge/Grade/9b8355ff642f4de9acd4b270f8d14d10
   :target: https://app.codacy.com/gh/cokelaer/bioservices/dashboard
