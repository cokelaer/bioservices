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



:Python_version_available: BioServices is tested for Python 3.9, 3.10, 3.11, 3.12
:Contributions: Please join https://github.com/cokelaer/bioservices
:Issues: Please use https://github.com/cokelaer/bioservices/issues
:How to cite: Cokelaer et al. *BioServices: a common Python package to access biological Web Services programmatically*
     `Bioinformatics <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_ (2013) 29 (24): 3241-3242
:Documentation: `RTD documentation <http://bioservices.readthedocs.io/>`_.

**Bioservices** is a Python package that provides access to many Bioinformatics Web Services (e.g.,
UniProt) and a framework to easily implement Web Services wrappers (based on
WSDL/SOAP or REST protocols).


The primary goal of **BioServices** is to use Python as a glue language to provide
a programmatic access to several Bioinformatics Web Services. By doing so, elaboration of new
applications that combine several of the wrapped Web Services is fostered.

One of the main philosophies of **BioServices** is to make use of the existing
biological databases (not to re-invent new databases) and to alleviate the
need for expertise in Web Services for developers and users.

BioServices provides access to about 40 Web Services.

Installation
============

Install the latest stable release from `PyPI <https://pypi.python.org/pypi/bioservices>`__::

    pip install bioservices

or from `conda-forge <https://anaconda.org/conda-forge/bioservices>`_::

    conda install conda-forge::bioservices


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

Command-Line Interface
======================

BioServices also ships a ``bioservices`` command-line tool for quick lookups
without writing any Python code::

    $ bioservices --help

Four top-level commands are available:

* **gene** — query gene data (info, name, ontology, expression, pathway, ortholog, id mapping)
* **protein** — query protein data (search, sequence, structure, annotation, interaction, id mapping)
* **taxonomy** — retrieve taxonomic information for a taxon ID
* **download-accession** — download FASTA (and optionally GFF3/GenBank) for a sequence accession

Examples::

    $ bioservices gene info --gene-id 1017
    $ bioservices gene name --symbol BRAF
    $ bioservices protein search --query ZAP70 --organism human
    $ bioservices protein structure --uniprot-id P43403
    $ bioservices taxonomy --id 9606
    $ bioservices download-accession --accession FN433596.1

Full CLI reference: `CLI documentation <http://bioservices.readthedocs.io/en/main/cli.html>`_

Notebooks
=========

The following Jupyter notebooks provide worked examples for many of the
services. They can be viewed directly on `nbviewer <https://nbviewer.org>`_ or
downloaded and run locally.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Notebook
     - Description
   * - `Overview <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/Overview.ipynb>`_
     - Introduction and overview of BioServices
   * - `UniProt <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/UniProt.ipynb>`_
     - Searching and retrieving data from UniProt
   * - `BioModels <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/BioModels.ipynb>`_
     - Accessing BioModels database
   * - `ChEMBL <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/ChEMBL.ipynb>`_
     - Drug and compound data from ChEMBL
   * - `Entrez/EUtils <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/Entrez_EUtils.ipynb>`_
     - NCBI Entrez utilities cookbook (ESearch, EFetch, EPost, ELink)
   * - `EUtils <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/EUtils.ipynb>`_
     - EUtils quick example (ESummary and ESearch)
   * - `KEGG <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/KEGG.ipynb>`_
     - KEGG pathways and databases
   * - `MUSCLE <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/MUSCLE.ipynb>`_
     - Multiple sequence alignment with MUSCLE
   * - `NCBIBlast <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/NCBIBlast.ipynb>`_
     - Running BLAST searches via NCBI
   * - `WikiPathway <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/WikiPathway.ipynb>`_
     - WikiPathways data access
   * - `Gene Mapping <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/Gene_Mapping.ipynb>`_
     - Mapping gene identifiers across databases
   * - `BioMart <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/BioMart.ipynb>`_
     - Querying BioMart data warehouses
   * - `Ensembl <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/Ensembl.ipynb>`_
     - Ensembl genome browser REST API
   * - `InterPro <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/InterPro.ipynb>`_
     - Protein families and domains from InterPro
   * - `ENA <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/ENA.ipynb>`_
     - European Nucleotide Archive
   * - `Drug Discovery Pipeline <https://nbviewer.org/github/cokelaer/bioservices/blob/main/doc/notebooks/DrugDiscovery.ipynb>`_
     - Integrated multi-service drug discovery workflow

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
1.15.0    * **Drop WSDL support**: ``WSDLService`` class and ``suds-community``
            dependency removed — all active services now use REST exclusively
          * Remove obsolete ``_compat`` module (Python 2 shims); replace
            ``pkg_resources`` with ``importlib.metadata``
          * Documentation overhauled: new Quick Start, merged changelog,
            contributors folded into Help & Credits, ChangeLog page removed
          * Docstrings and code quality improvements
          * CI: notebook test suite extended to all 17 notebooks; slow
            ``unichem`` and ``quickgo`` tests marked ``flaky``
1.14.0    * New ``proteins`` module (EBI Proteins API)
          * New ``string`` module (STRING protein interaction database)
          * New ``geo`` module (NCBI Gene Expression Omnibus)
          * PubChem: update to current PUG REST API
          * Remove deprecated BioGRID and PSICQUIC services
1.13.0    * ChEBI: new REST API (replacing SOAP)
1.12.2    * Add ``taxonomy`` CLI subcommand (via EUtils)
1.11.0    * Remove ReactomeOld, ReactomeAnalysis, rnaseq_ebi (deprecated)
1.10.3    * PDB: update to v2 API; remove biocarta (website no longer accessible)
1.10.1    * PRIDE: update to new API (July 2022)
1.10.0    * UniProt: update to new API (June 2022)
1.9.0     * UniChem: update to new API
1.8.3     * New ``biocontainers`` module
1.8.0     * Remove chemspider, clinvitae, picr (deprecated)
          * Add standalone ``bioservices`` CLI application
1.7.12    * New ``cog`` module
          * Deprecate PICR and TCGA modules
          * PDB, ChEMBL, QuickGO, BioDBNet: new API
1.7.5     * New ``mygeneinfo``, ``pdbe`` modules
1.7.4     * New ``bigg`` module (BiGG models)
          * BioModels: new REST API (replacing WSDL)
          * Move miriam to attic (deprecated)
1.7.0     * New ``panther`` module
1.6.0     * ChEMBL: fully rewritten to new API
1.5.2     * Reactome: new API
1.5.0     * BioDBNet, WikiPathways: migrate from WSDL to REST
          * QuickGO, DBFetch: new API
          * Rename ``readseq`` to ``seqret`` (new API)
1.4.8     * New ``omnipath`` module
1.4.6     * New ``rnaseq_ebi`` module
1.4.4     * New ``ena`` module
1.4.1     * HGNC: replaced deprecated module with genenames.org service
1.4.0     * EUtils: migrate from WSDL to REST
          * Remove apps/taxonomy (moved to biokit)
1.3.5     * New ``intact`` module (Intact Complex)
1.3.4     * New ``pride`` module
1.3.3     * New ``ensembl``, ``clinvitae`` modules
1.3.1     * New ``readseq`` module
1.3.0     * New REST class using ``requests`` (replacing urllib2)
          * New ``eutils`` module
          * Rename ``chembldb`` to ``chembl``; rename ``WikiPathway`` to ``WikiPathways``
1.2.3     * New ``biodbnet``, ``pathwaycommons`` modules
1.2.0     * New ``muscle``, ``geneprof`` modules
1.1.2     * New ``biocarta``, ``pfam`` modules
1.1.1     * New ``hgnc`` module
1.1.0     * New ``chebi``, ``unichem`` modules
1.0.4     * New ``pdb`` module (draft)
1.0.0     * First stable release
0.9.0     * Initial services: BioModels, KEGG, Reactome, ChEMBL, PICR, QuickGO,
            Rhea, UniProt, WSDbfetch, NCBIblast, PSICQUIC, WikiPathways
========= ====================================================================


.. |Codacy-Grade| image:: https://app.codacy.com/project/badge/Grade/9b8355ff642f4de9acd4b270f8d14d10
   :target: https://app.codacy.com/gh/cokelaer/bioservices/dashboard
