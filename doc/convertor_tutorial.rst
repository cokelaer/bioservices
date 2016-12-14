.. _mapping:

.. testsetup:: mapping

    from bioservices import *
    k = KEGG(verbose=False)
    u = UniProt()

Mapping identifiers
=======================
There are quite a few functions from different Web Services that can help to map
identifiers from one database to the other. This tutorial presents some of them.


Convert from KEGG ID to ChEBI (compound)
--------------------------------------------

.. doctest::

    >>> from bioservices import *
    >>> k = KEGG(verbose=False)
    >>> map_kegg_chebi = k.conv("chebi", "compound")
    >>> map_kegg_chebi['cpd:C11222']
    'chebi:5292'

you could also use :class:`bioesrvices.unichem.UniChem` (see below).

Convert from KEGG ID to ChEMBL (compound)
---------------------------------------------

.. doctest::

    >>> from bioservices import UniChem
    >>> uni = UniChem()
    >>> mapping = uni.get_mapping("kegg_ligand", "chembl")
    >>> mapping["C11222"]
    'CHEMBL278315'



convert from KEGG ID to UniProt and vice versa (gene)
-------------------------------------------------------

In order to convert KEGG gene names into uniprot gene name, we can also
use the UniProt web service from BioServices as follows:

.. doctest::

    >>> from bioservices import *
    >>> u = UniProt()
    >>> u.mapping(fr='ID', to='KEGG_ID', query="ZAP70_HUMAN")
    ['From:ID', 'To:KEGG_ID', 'ZAP70_HUMAN', 'hsa:7535']


You can get accession number or protein name identifier from the KEGG
identifier as follows::

 
   >>> u.mapping(fr='KEGG_ID', to='ID', query='hsa:7535')
   'ZAP70_HUMAN'
   >>> u.mapping(fr='KEGG_ID', to='ACC', query='hsa:7535')
   'P43403'


One can also use the :meth:`bioservices.kegg.KEGG.conv` method::

    >>> k = KEGG()
    >>> mapping_kegg_uniprot = k.conv("hsa", "uniprot")

