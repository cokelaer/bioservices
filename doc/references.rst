.. contents::



Utilities
##############

Service module (REST or WSDL)
===================================================================

.. automodule:: bioservices.services
    :members:
    :undoc-members:
    :synopsis: 

xmltools module
========================

.. automodule:: bioservices.xmltools
    :members:
    :undoc-members:
    :synopsis:



Services
#############

ArrayExpress
===================

.. .. automodule:: bioservices.arrayexpress
    :members:
    :undoc-members:
    :synopsis:

Biocontainers
=============

.. automodule:: bioservices.biocontainers
    :members:
    :undoc-members:
    :synopsis:

BiGG
====

.. automodule:: bioservices.bigg
    :members:
    :undoc-members:
    :synopsis:


BioDBnet
============

.. automodule:: bioservices.biodbnet
    :members:
    :undoc-members:
    :synopsis:

BioGrid
====================

.. automodule:: bioservices.biogrid
    :members:
    :undoc-members:
    :synopsis:

BioMart
====================

.. automodule:: bioservices.biomart
    :members:
    :undoc-members:
    :synopsis:

BioModels
====================

.. automodule:: bioservices.biomodels
    :members:
    :undoc-members:
    :synopsis:

ChEBI
=======

.. automodule:: bioservices.chebi
    :members:
    :undoc-members:
    :synopsis:


ChEMBL
==========

.. automodule:: bioservices.chembl
    :members:
    :undoc-members:
    :synopsis:

COG
===

.. automodule:: bioservices.cog
    :members:
    :undoc-members:
    :synopsis:


ENA
==========

.. automodule:: bioservices.ena
    :members:
    :undoc-members:

EUtils
==========

.. automodule:: bioservices.eutils
    :members:
    :undoc-members:
    :synopsis:

GeneProf
============

Currently removed from the main API from version 1.6.0 onwards. You can still get
the code in earlier version or in the github repository in the attic/ directory

.. .. automodule:: bioservices.geneprof
    :members:
    :undoc-members:
    :synopsis:

QuickGO
================

.. automodule:: bioservices.quickgo
    :members:
    :undoc-members:
    :synopsis: 

Kegg
===================================================================


.. automodule:: bioservices.kegg
    :members:
    :undoc-members:
    :synopsis:

HGNC
=====

.. automodule:: bioservices.hgnc
    :members:
    :undoc-members:
    :synopsis:

Intact (complex)
======================

.. automodule:: bioservices.intact
    :members:
    :undoc-members:
    :synopsis:


MUSCLE
==============

.. automodule:: bioservices.muscle
    :members:
    :undoc-members:
    :synopsis:

MyGeneInfo
==========

.. automodule:: bioservices.mygeneinfo
    :members:
    :undoc-members:
    :synopsis:


NCBIblast
================

.. automodule:: bioservices.ncbiblast
    :members:
    :undoc-members:
    :synopsis:

OmniPath Commons
=========================

.. automodule:: bioservices.omnipath
    :members:
    :undoc-members:
    :synopsis:

Panther
=========================

.. automodule:: bioservices.panther
    :members:
    :undoc-members:
    :synopsis:


Pathway Commons
=========================

.. automodule:: bioservices.pathwaycommons
    :members:
    :undoc-members:
    :synopsis:

PDB/PDBe modules
========================

.. automodule:: bioservices.pdb
    :members:
    :undoc-members:
    :synopsis:

.. automodule:: bioservices.pdbe
    :members:
    :undoc-members:
    :synopsis:


PRIDE module
=====================================

.. automodule:: bioservices.pride
    :members:
    :undoc-members:
    :synopsis:


PSICQUIC
================

.. automodule:: bioservices.psicquic
    :members:
    :undoc-members:
    :synopsis:

Rhea
==============

.. automodule:: bioservices.rhea
    :members:
    :undoc-members:
    :synopsis:

Reactome
=====================

.. automodule:: bioservices.reactome
    :members:
    :undoc-members:
    :synopsis:

Readseq
============

.. automodule:: bioservices.seqret
    :members:
    :undoc-members:
    :synopsis:


UniChem
=========

.. automodule:: bioservices.unichem
    :members:
    :undoc-members:
    :synopsis:

UniProt
================

.. automodule:: bioservices.uniprot
    :members:
    :undoc-members:
    :synopsis:

DBFetch
===============

.. automodule:: bioservices.dbfetch
    :members:
    :undoc-members:
    :synopsis:

Wikipathway
====================

.. automodule:: bioservices.wikipathway
    :members:
    :undoc-members:
    :synopsis:


Applications and extra tools
##################################

Web services have lots of overlap amongst themselves. For instance, fetching a FASTA sequence 
can be done using many different services. Yet, once a FASTA is retrieved, one may want to perform additional tasks or save the FASTA into a file or whatever repetitive functionalities not included in Web Services anymore.

The goal of this sub-package is to provide convenient tools, which are not web services per se but that makes use of one or several Web Services already available within BioServices.

.. warning:: this is experimental and was added in version 1.2.0 so it may change quite a lot.

Peptides
============

.. automodule:: bioservices.apps.peptides
    :members:
    :undoc-members:
    :synopsis:

FASTA
=======

.. automodule:: bioservices.apps.fasta
    :members:
    :undoc-members:
    :synopsis:
