.. _cli:

Command-Line Interface
######################

.. contents::

BioServices ships with a ``bioservices`` command-line tool that lets you query
biological databases directly from your terminal — no Python script required.

.. code-block:: bash

    $ bioservices --help

     Usage: bioservices [OPTIONS] COMMAND [ARGS]...

      This is the main entry point for a set of BioServices applications

     Options:
       --version      Show the version and exit.
       --help  -h     Show this message and exit.

     Commands:
       download-accession  Download Fasta related to an accession and possibly
                           other type (e.g gff)
       gene                Commands for querying gene data across multiple
                           databases
       protein             Commands for querying protein data across multiple
                           databases
       taxonomy            Download information related to a taxid


gene
====

The ``gene`` sub-command group provides seven commands to query gene-related
information across multiple databases (MyGene.info, HGNC, QuickGO, ArrayExpress,
Reactome/KEGG, Panther, UniProt).

.. code-block:: bash

    $ bioservices gene --help

.. rubric:: gene info

Retrieve gene information from `MyGene.info <https://mygene.info>`_ by Entrez
gene ID:

.. code-block:: bash

    $ bioservices gene info --gene-id 1017

.. rubric:: gene name

Look up HGNC-approved gene names and symbols:

.. code-block:: bash

    $ bioservices gene name --symbol BRAF

.. rubric:: gene ontology

Retrieve Gene Ontology annotations from QuickGO:

.. code-block:: bash

    $ bioservices gene ontology --query GO:0003824

.. rubric:: gene expression

Search ArrayExpress for gene expression experiments:

.. code-block:: bash

    $ bioservices gene expression --query cancer

.. rubric:: gene pathway

Find pathways associated with a gene using Reactome or KEGG:

.. code-block:: bash

    $ bioservices gene pathway --query TP53

.. rubric:: gene ortholog

Search for orthologs of a gene using the Panther database:

.. code-block:: bash

    $ bioservices gene ortholog --gene zap70 --taxid 9606

.. rubric:: gene map-id

Convert gene identifiers between databases via UniProt ID mapping:

.. code-block:: bash

    $ bioservices gene map-id --from uniprot --to kegg --id P43403


protein
=======

The ``protein`` sub-command group provides six commands to query protein-related
information (UniProt, PDB, STRING).

.. code-block:: bash

    $ bioservices protein --help

.. rubric:: protein search

Search for proteins in UniProt:

.. code-block:: bash

    $ bioservices protein search --query ZAP70 --organism human

.. rubric:: protein sequence

Fetch the FASTA sequence for a protein from UniProt:

.. code-block:: bash

    $ bioservices protein sequence --uniprot-id P43403

.. rubric:: protein structure

Find PDB 3D structures for a protein given its UniProt accession:

.. code-block:: bash

    $ bioservices protein structure --uniprot-id P43403

.. rubric:: protein annotation

Fetch UniProt annotations for a protein:

.. code-block:: bash

    $ bioservices protein annotation --uniprot-id P43403

.. rubric:: protein interaction

Fetch protein-protein interactions from the STRING database:

.. code-block:: bash

    $ bioservices protein interaction --gene ZAP70 --taxid 9606

.. rubric:: protein map-id

Convert protein identifiers between databases via UniProt ID mapping:

.. code-block:: bash

    $ bioservices protein map-id --from uniprot --to kegg --id P43403


taxonomy
========

Download taxonomic information for a given taxon ID using EUtils:

.. code-block:: bash

    $ bioservices taxonomy --id 9606

Options:

* ``--id TEXT`` — A valid taxon ID (e.g., 9606).
* ``--method TEXT`` — Method to use (EUtils is currently the only option).


download-accession
==================

Download a FASTA file (and optionally GFF3 / GenBank) for a given sequence
accession.  Input files can be gzipped or plain text.

.. code-block:: bash

    $ bioservices download-accession --accession FN433596.1

Options:

* ``--accession TEXT`` *(required)* — A valid accession number (e.g., ``FN433596.1``).
* ``--prefix TEXT`` — Rename the output file instead of using the accession number.
* ``--method [ENA|EUtils]`` — Download backend (default: ENA).
* ``--with-gff3`` — Also download the GFF3 annotation file.
* ``--with-gbk`` — Also download the GenBank flat file.
