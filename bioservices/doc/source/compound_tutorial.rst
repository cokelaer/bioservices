Manipulating compound identifiers
=======================================

.. topic:: Application: retrieving information about a compound

    This section uses BioServices to demonstrate the interest of combining
    several services together within a single framework using the Python language as
    a glue language

In this tuturial, we are interested in using BioServices to obtain information
about a specific compound.
Let us look at a compound called Lysine. Let us search for information about
that compound in several databases and manage the differnt Identifiers. 

First, ket us retrieve information on KEGG database::

    >>> from bioservices import *
    >>> k = Kegg(verbose=False)


    >>> res3 = k.conv("compound", "chebi")

    len(k.compoundIds)
    Out[11]: 17012


    >>> print(k.find("compound", "lysine"))
    cpd:C00047  L-Lysine; Lysine acid; 2,6-Diaminohexanoic acid
    cpd:C00449  N6-(L-1,3-Dicarboxypropyl)-L-lysine; Saccharopine; L-Saccharopine;N-[(S)-5-Amino-5-carboxypentyl]-L-glutamic acid

Let us look at the first one (L-Lysine with Kegg id cpd:C00047). We can get lots
of information from KEGG already by using::

    >>> print(k.get("C00047"))

Form which, there is a link to other databases in particular chEBI
(ChEBI:18019). Of course here there is no programmatic call. What about using
the converter from KEGG::

    >>> k.conv("chebi","cpd:c00047")
    (['cpd:C00047'], ['chebi:18019'])

There is no links to chembl database in KEGG. Although UniProt and KEGG conv
functon provides some mapping, the KEGG to ChEMBL or CHEBI to CHEMBL cannot be
found. We could 

So, we have now the chebi ID of the L-Lysine compound from KEGG. LEt us search
in ArrayExpress 

::

    res = c.get_compounds_by_chemblId("CHEMBL8085")
    INFO:root:http://www.ebi.ac.uk/chemblws/compounds/CHEMBL8085.json
    INFO:root:REST.bioservices.ChEMBLdb request begins
    INFO:root:--Fetching url=http://www.ebi.ac.uk/chemblws/compounds/CHEMBL8085.json
    
    In [32]: res['compound']['molecularWeight']
    Out[32]: 146.19
    
    In [33]: print k.get("cpd:C00047")
i


tumor protein p53
 >>> uni = UniChem()

 >>> mapping = uni.get_mapping("kegg_ligand", "chembl")

 >>> mapping['C11222']

  'CHEMBL278315'

For sanity check, let us see that the ChEBI is indeed 5292 as given within the
KEGG database:

 >>> mapping = uni.get_mapping("kegg_ligand", "chebi")

 >>> mapping['C11222']

  '5292'


(2) In order to convert KEGG gene names into uniprot gene name, we can also use
the UniProt web service from BioServices as follows

   >>> from bioservices import *

   >>> u = UniProt()

   >>> u.mapping(fr='ID', to='KEGG_ID', format='tab', query=ZAP70_HUMAN)

   ['From:ID', 'To:KEGG_ID', 'P43403', 'hsa:7535']

You can get accession number or protein name identifier from the KEGG identifier
as follows

   >>> u.mapping(fr='KEGG_ID', to='ID', format='tab', query='hsa:7535')

   'ZAP70_HUMAN'

   >>> u.mapping(fr='KEGG_ID', to='ACC', format='tab', query='hsa:7535')

   'P43403'
