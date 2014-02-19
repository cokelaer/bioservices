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

.. automodule:: bioservices.arrayexpress
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


ChEMBLdb
==========

.. automodule:: bioservices.chembldb
    :members:
    :undoc-members:
    :synopsis:

ChemSpider
===============

.. automodule:: bioservices.chemspider
    :members:
    :undoc-members:
    :synopsis:

EUtils
==========

.. automodule:: bioservices.eutils
    :members:
    :undoc-members:
    :synopsis:

GeneProf
============

.. automodule:: bioservices.geneprof
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

MUSCLE
==============

.. automodule:: bioservices.muscle
    :members:
    :undoc-members:
    :synopsis:


Miriam
======================

.. automodule:: bioservices.miriam
    :members:
    :undoc-members:
    :synopsis:



NCBIblast
================

.. automodule:: bioservices.ncbiblast
    :members:
    :undoc-members:
    :synopsis:

Pathway Commons
=========================

.. automodule:: bioservices.pathwaycommons
    :members:
    :undoc-members:
    :synopsis:

PDB module
========================

.. automodule:: bioservices.pdb
    :members:
    :undoc-members:
    :synopsis:

PICR module
=====================================

.. automodule:: bioservices.picr
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

.. Reactome
.. =====================

.. .. automodule:: bioservices.reactome
    :members:
    :undoc-members:
    :synopsis:

UniChem
===================================================================

.. automodule:: bioservices.unichem
    :members:
    :undoc-members:
    :synopsis:

UniProt
===================================================================

.. automodule:: bioservices.uniprot
    :members:
    :undoc-members:
    :synopsis:

wsdbfetch
===================================================================

.. automodule:: bioservices.wsdbfetch
    :members:
    :undoc-members:
    :synopsis:

Wikipathway
===================================================================

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

Taxonomy
=============
.. automodule:: bioservices.apps.taxonomy
    :members:
    :undoc-members:
    :synopsis:
