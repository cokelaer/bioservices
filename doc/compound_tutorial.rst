Manipulating compound identifiers
=======================================
.. testsetup:: compound

    from bioservices import KEGG
    k = KEGG(verbose=False)

.. topic:: Application: retrieving information about a compound

    This section uses BioServices to demonstrate the interest of combining
    several services together within a single framework using the Python language as
    a glue language


Retrieve a compound identifier from KEGG, ChEBI and ChEMBL
--------------------------------------------------------------

Let us look at a compound called **Geldanamycin** that inhibits Hsp90.
Let us search for information about that compound in several databases
and manipulate the different identifiers.

First, let us retrieve information on KEGG database::

    >>> from bioservices import KEGG
    >>> k = KEGG(verbose=False)

KEGG compounds have links to other databases. It is not systematic but the ChEBI
database is often referenced. So we will want to convert the KEGG identifer to a
ChEBI identifier. Later, we can convert a ChEBI to a ChEMBL identifier using
another Web Service such as UniChem.

We can get a mapping dictionary from the KEGG compound to ChEBI as follows:

.. doctest:: compound

    >>> map_kegg_chebi = k.conv("chebi", "compound")
    >>> len(map_kegg_chebi) # doctest: +SKIP
    15845

    >>> print(k.find("compound", "geldanamycin"))
    cpd:C11222  Geldanamycin
    cpd:C15823  Progeldanamycin
    <BLANKLINE>

Let us look at the first one (KEGG id cpd:C11222). We can get lots
of information from KEGG already by using:

.. doctest::
    :options: +SKIP

    >>> print(k.get("C11222"))

Form which, there is a link to other databases in particular ChEBI
(ChEBI:5292). We could use the mapping dictionary created above:

.. doctest:: compound

    >>> map_kegg_chebi['cpd:C11222']
    'chebi:5292'

Unfortunately, there is no mapping function from KEGG to ChEMBL in KEGG Web Service.
There was a mapping function in  :mod:`bioservices.unichem` servive that was dropped
in 2022. We can still use another service. In order to convert KEGG gene names into uniprot gene name, we can also use
the UniProt web service from BioServices as follows::

   >>> from bioservices import UniProt
   >>> u = UniProt()
   >>> u.mapping(fr='UniProtKB_AC-ID', to='KEGGD', query="ZAP70_HUMAN")
   {'ZAP70_HUMAN':  'hsa:7535'}
