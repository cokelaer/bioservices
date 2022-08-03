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


convert from KEGG ID to UniProt and vice versa (gene)
-------------------------------------------------------

In order to convert KEGG gene names into uniprot gene name, we can also
use the UniProt web service from BioServices as follows:

.. doctest::

    >>> from bioservices import *
    >>> u = UniProt()
    >>> u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query='P43403')
    {'results': [{'from': 'P43403', 'to': 'hsa:7535'}]}


You can get accession number or protein name identifier from the KEGG
identifier as follows::

Due to an API change in 2022 and for back compatiblity, the mapping from KEGG to e.g. uniprot is a bit more complex than it used to be. First, the conversion::

    >>> res = u.mapping(fr='KEGG', to='UniProtKB', query='hsa:7535')

Then, we extract the results (the first element) and the 'to' key. We can then extract e.g. the uniprot ID ::

    >>> res['results'][0]['to']['uniProtkbId']
    'ZAP70_HUMAN'

and the primary accession as follows::

    >>> res['results'][0]['to']['primaryAccession']
    'P43403'


One can also use the :meth:`bioservices.kegg.KEGG.conv` method::

    >>> k = KEGG()
    >>> mapping_kegg_uniprot = k.conv("hsa", "uniprot")

