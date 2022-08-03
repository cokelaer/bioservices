Protein test case study
==========================

.. topic:: Application: retrieving information about a given protein

    This section uses BioServices to demonstrate the interest of combining
    several services together within a single framework using the Python
    language as a glue language.

In this tutorial we are interested in using **BioServices** to obtain information
about a specific protein. Let us focus on ZAP70 protein (homo sapiens).

.. testsetup:: protein

    from bioservices import *
    u = UniProt(verbose=False)

Get a unique identifier and gene names from a name
----------------------------------------------------

From **Uniprot**, we can obtain the unique accession number of ZAP70, which may be
useful later on. Let us try to use the :meth:`~bioservices.uniprot.UniProt.search` method:: 

    >>> from bioservices import *
    >>> u = UniProt(verbose=False)
    >>> u.search("ZAP70_HUMAN") # could be lower case


The default format of the returned answer is "tabulated"::

    >>> res = u.search("ZAP70_HUMAN", frmt="tab")
    >>> print(res)
    Entry   Entry name  Status  Protein names   Gene names  Organism    Length
    P43403  ZAP70_HUMAN reviewed    Tyrosine-protein kinase ZAP-70 (EC 2.7.10.2) (70 kDa zeta-chain associated protein) (Syk-related tyrosine kinase)    ZAP70 SRK Homo sapiens (Human)    619

It is better, but let us simplify even further. In **BioServices**, the output
of the tabulated format contains several columns but we can select only a subset
such as the Entry (accession number) and the gene names, which are coded as "id"
and "genes" in uniprot database::

    >>> res = u.search("ZAP70_HUMAN", frmt="tab", columns="id,genes")
    >>> print(res)
    Entry   Gene names
    P43403  ZAP70 SRK

So here we got the Entry P43403. Entry and Gene names can be saved in two
variables as follows::

    >>> res = u.search("ZAP70_HUMAN", frmt="tab", columns="id,genes")
    >>> entry, gene_names = res.split("\n")[1].split("\t") 


Getting the fasta sequence
---------------------------

It is then straightforward to obtain the FASTA sequence of ZAP70 using another
method from the UniProt class called :meth:`~bioservices.uniprot.UniProt.retrieve`:


.. doctest:: protein

    >>> sequence = u.retrieve("P43403", "fasta")
    >>> print(sequence)
    >sp|P43403|ZAP70_HUMAN Tyrosine-protein kinase ZAP-70 OS=Homo sapiens OX=9606 GN=ZAP70 PE=1 SV=1
    MPDPAAHLPFFYGSISRAEAEEHLKLAGMADGLFLLRQCLRSLGGYVLSLVHDVRFHHFP
    IERQLNGTYAIAGGKAHCGPAELCEFYSRDPDGLPCNLRKPCNRPSGLEPQPGVFDCLRD
    AMVRDYVRQTWKLEGEALEQAIISQAPQVEKLIATTAHERMPWYHSSLTREEAERKLYSG
    AQTDGKFLLRPRKEQGTYALSLIYGKTVYHYLISQDKAGKYCIPEGTKFDTLWQLVEYLK
    LKADGLIYCLKEACPNSSASNASGAAAPTLPAHPSTLTHPQRRIDTLNSDGYTPEPARIT
    SPDKPRPMPMDTSVYESPYSDPEELKDKKLFLKRDNLLIADIELGCGNFGSVRQGVYRMR
    KKQIDVAIKVLKQGTEKADTEEMMREAQIMHQLDNPYIVRLIGVCQAEALMLVMEMAGGG
    PLHKFLVGKREEIPVSNVAELLHQVSMGMKYLEEKNFVHRDLAARNVLLVNRHYAKISDF
    GLSKALGADDSYYTARSAGKWPLKWYAPECINFRKFSSRSDVWSYGVTMWEALSYGQKPY
    KKMKGPEVMAFIEQGKRMECPPECPPELYALMSDCWIYKWEDRPDFLTVEQRMRACYYSL
    ASKVEGPPGSTQKAEAACA
    <BLANKLINE>

.. note:: There are many services that provides access to the FASTA sequence. We chose
   uniprot but you could use the Entrez utilities as well as other services.

Using BLAST on the sequence 
------------------------------

You can then analyse this sequence with your favorite tool. As an example, within **BioServices** you can use :class:`~bioservices.services.nciblast.NCIBlast` but first let us extract the sequence itself (without the header)::

    sequence = sequence.split("\n", 1)[1].strip("\n") 

then, ::

    >>> s = NCBIblast(verbose=False)
    >>> jobid = s.run(program="blastp", sequence=sequence, stype="protein", \
    ...    database="uniprotkb", email="cokelaer@ebi.ac.uk")
    >>> print(s.getResult(jobid, "out")[0:1000])
    BLASTP 2.2.26 [Sep-21-2011]


    Reference: Altschul, Stephen F., Thomas L. Madden, Alejandro A. Schaffer, 
    Jinghui Zhang, Zheng Zhang, Webb Miller, and David J. Lipman (1997), 
    "Gapped BLAST and PSI-BLAST: a new generation of protein database search
    programs",  Nucleic Acids Res. 25:3389-3402.

    Query= EMBOSS_001
             (619 letters)

    Database: uniprotkb 
               32,727,302 sequences; 10,543,978,207 total letters

    Searching..................................................done



                                                                     Score    E
    Sequences producing significant alignments:                      (bits) Value

    SP:ZAP70_HUMAN P43403 Tyrosine-protein kinase ZAP-70 OS=Homo sap...  1279   0.0  
    TR:H2QIE3_PANTR H2QIE3 Tyrosine-protein kinase OS=Pan troglodyte...  1278   0.0  
    TR:G3QGN8_GORGO G3QGN8 Tyrosine-protein kinase OS=Gorilla gorill...  1278   0.0  
    TR:G1QLX3_NOMLE G1QLX3 Tyrosine-protein kinase OS=Nomascus leuco...  1249   0.0  
    TR:F6SWY7_CALJA F6SWY7 Tyrosin

The last command waits for the job to be finised before printing the results,
which may be quite long. We could look at the beginnin of the reported results
and select only HUMAN sequences to see that the best sequence found is indeed
ZAP70_HUMAN as expected::

    >>> [x for x in s.getResult(jobid, "out").split("\n") if "HUMAN" in x]
    ['SP:ZAP70_HUMAN P43403 Tyrosine-protein kinase ZAP-70 OS=Homo sap...  1279 0.0  ',
     'SP:KSYK_HUMAN P43405 Tyrosine-protein kinase SYK OS=Homo sapiens...   691 0.0  ',
     'TR:A8K4G2_HUMAN A8K4G2 Tyrosine-protein kinase OS=Homo sapiens P...   691 0.0  ',
    ...


Searching for relevant pathways
------------------------------------------

The KEGG services provides pathways, so let try to find pathways that contains
our targetted protein. First we need to know the KEGG Id that corresponds to
ZAP70. We can use the **find** method form KEGG service::

    >>> from bioservices import KEGG
    >>> k = KEGG(verbose=False)
    >>> k.find("hsa", "zap70")  # "hsa" stands for homo sapiens
    hsa:7535 ZAP70, SRK, STCD, STD, TZK, ZAP-70; zeta-chain (TCR) associated protein kinase 70kDa (EC:2.7.10.2); K07360 tyrosine-protein kinase ZAP-70 [EC:2.7.10.2

There are other ways to perform this conversion using the :meth:`bioservices.uniprot.UniProt.mapping`  or :meth:`bioeservices.KEGG.conv` methods (e.g., \textit{k.conv("hsa", "up:P43403")}).

Now, let us get the pathways that contains this ID::

    >>> k.get_pathway_by_gene("7535", "hsa")
    {'hsa04064': ' NF-kappa B signaling pathway',
    'hsa04650': 'Natural killer cell mediated cytotoxicity',
     'hsa04660': 'T cell receptor signaling pathway',
     'hsa05340': 'Primary immunodeficiency'}

We can look at the first pathway in a browser (highlighting the ZAP70 node)::

    >>> k.show_pathway("hsa04064", keggid={"7535": "red"})

Searching for binary Interactions
-----------------------------------


For this purpose, we could use PSICQUIC services to find the interactions that
involve ZAP70 in the **mint** database::

    >>> from bioservices import PSICQUIC
    >>> s = PSICQUIC(verbose=False)
    >>> data = s.query("mint", "ZAP70 AND species:9606")

where 9606 is the taxonomy Id for homo sapiens. We could also figure out how
many interactions could be found in each dabase for this particular query::

    >>> s.getInteractionCounter("zap70 AND species:9606")
    {'apid': 82,
     'bar': 0,
     'bind': 4,
     'bindingdb': 29,
     'biogrid': 73,
     'chembl': 161,
     'dip': 0,
     'i2d-imex': 0,
     'innatedb': 13,
     'innatedb-imex': 0,
     'intact': 11,
     'interoporc': 0,
     'irefindex': 273,
     'matrixdb': 0,
     'mbinfo': 0,
     'mint': 34,
     'molcon': 0,
     'mpidb': 0,
     'reactome': 0,
     'reactome-fis': 134,
     'spike': 47,
     'string': 319,
     'topfind': 0,
     'uniprot': 0}


We see for instance that the **mint** database has 34 interactions. Coming back to the interactions returned by s.query, we find indeed 34 intercations
between ZAP70 and another component::

    >>> len(data)
    34

Let us look at the first one::

    >>> for x in data[0]: print(x)
    uniprotkb:P15498
    uniprotkb:P43403
    -
    -
    uniprotkb:VAV1(gene name)|uniprotkb:VAV(gene name synonym)
    uniprotkb:ZAP70(gene name)|uniprotkb:SRK(gene name synonym)|uniprotkb:70 kDa
    zeta-associated protein(gene name synonym)|uniprotkb:Syk-related tyrosine
    kinase(gene name synonym)
    psi-mi:"MI:0019"(coimmunoprecipitation)
    -
    pubmed:9151714
    taxid:9606(Homo sapiens)
    taxid:9606(Homo sapiens)
    psi-mi:"MI:0914"(association)
    psi-mi:"MI:0471"(mint)
    mint:MINT-8035351
    mint-score:0.28(free-text)|homomint-score:0.28(free-text)'intact-miscore:0.60']

The First two elements are the entries for specy A and B. The last element is the
score. The 11th element is the type of interaction and so on.

What could be useful is to convert these elements into uniprot ID only. With
mint database it is irrelevant for this particular entry but with other DBs or entries, it may be useful (e.g., biogrid).

BioServices provides such a function called :meth:`~bioservices.services.psicquic.convert`::

    >>> data = s.query("biogrid", "ZAP70 AND species:9606")
    >>> data2 = s.convert(data, "biogrid")

.. warning:: some databases may be offline. If so, try we another database. Type
   "s.activeDBs".

**convert** method converts all entries from data into uniprot ID. If this is
not possible, the entry is removed. The **query** and **convert** works on a single database but you we could query all
or a subset of all databases using the queryAll and convertAll functions::

   >>> data = s.queryAll("ZAP70 AND species:9606", databases=["mint", "biogrid"])
   >>> data2 = s.convertAll(data)

However, extra cleaning is required to remove entries that are not relevant (no match
to uniprot ID, redundant, not a protein, self interactions, ...). In order to
ease this tast, the psicquic.AppsPPI class is very useful. 


.. plot::
    :width: 80%
    :include-source:

    from bioservices import psicquic
    s = psicquic.AppsPPI()
    s.queryAll("ZAP70 AND species:9606", databases=["mint", "biogrid", "intact", "reactome-fis"])
    s.summary()
    s.show_pie()



The summary function print a useful summary about the number of found
interactions and overlap between databases:

.. doctest:: 
   :options: +SKIP
 
    >>> s.summary()
    Found 8 interactions within intact database
    Found 124 interactions within reactome-fis database
    Found 19 interactions within mint database
    Found 67 interactions within biogrid database
    -------------
    Found 152 interactions in 1 common databases
    Found 14 interactions in 2 common databases
    Found 0 interactions in 3 common databases
    Found 1 interactions in 4 common databases

This may be different depending on the available databases.    
Finally, you can obtain the relation that was found in the 4 databases:

.. doctest:: 
   :options: +SKIP

    >>> s.relevant_interactions[4]
    [['LCK_HUMAN', 'ZAP70_HUMAN']]


What's next ?
-------------------

There are lots of other services that could be usefule. An example is the
wikipathway (see :class:`~bioservices.wikipathway.Wikipathway`) to retrieve even more pathways that include the ZAP70 protein.
Another example is the BioMart portal. You could use it to retrieve pathways
from REACTOME (see :class:`~bioservices.biomart.BioMart`). You can also retrieve
target from ChEMBL given the uniprot ID ( get_target_by_uniprotId("P43403") )
and so on.










.. For instance all human interactions reported in MArch 2013
    ----------------------------------------------------------------
    =========== =============== ===================================
    Status              name      number of interactions
    =========== =============== ===================================
    ONLINE      APID            123,427  
    ONLINE      BAR             0    
    ONLINE      BIND            38,419   
    ONLINE      BindingDB       74,082   
    ONLINE      BioGrid         182,911  
    ONLINE      ChEMBL          399,482  
    ONLINE      DIP             18,434   
    OFFLINE     DrugBank      
    OFFLINE     GeneMANIA 
    OFFLINE     I2D     
    ONLINE      I2D-IMEx        915  
    ONLINE      InnateDB        14,734   
    ONLINE      InnateDB-IMEx   352  
    ONLINE      IntAct          84,692   
    ONLINE      Interoporc      17,284   
    ONLINE      iRefIndex       396,368  
    ONLINE      MatrixDB        604  
    ONLINE      MBInfo          307  
    ONLINE      MINT            36,741   
    ONLINE      MolCon          242  
    ONLINE      MPIDB           28   
    ONLINE      Reactome        113,204  
    ONLINE      Reactome-FIs    209,988  
    ONLINE      Spike           36,248   
    ONLINE      STRING          656,493  
    ONLINE      TopFind         4,986    
    ONLINE      UniProt         5,564    
    OFFLINE     VirHostNet      
    =========== =============== ===================================
    res = p.queryAll("species:9606", databases=["uniprot", "apid"])
    data1 = res['uniprot']
    data2 = p.preCleaning(data1)
    mapping = p.convertUniprot(data2)
    len(set(p.postCleaning(mapping)))
    ('Before removing anything: ', 5558)
    ('After removing the None: ', 5545)
    ('Before removing the !: ', 5107)
    ("Before removing entries that don't match HUMAN : ", 4242)
    Finally, a set can be use to extract unique entries
    a further cleanup: A-B is same as B-A
    >>> p = psicquic.AppsPPI()
    >>> p.queryAll("ZAP70 AND species:9606")
    >>> p.summary()
    >>> for i in range(1,p.N+1):
    ...    print(i, len(p.relevant_interactions[i]))
    1 265
    2 62
    3 31
    4 12
    5 11
    6 7
    7 4
    8 2
    9 1
    >>> labels = range(1, p.N + 1 )
    >>> counting = [len(p.relevant_interactions[i]) for i in labels]
    >>> pie(counting, labels = [str(x) for x in labels])



