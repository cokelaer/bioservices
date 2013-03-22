Protein test case study
==========================

.. topic:: Application: retrieving information about a given protein

    This section uses BioServices to demonstrate the interest of combining
    several services together within a single framework using the Python
    language as a glue language.


.. testsetup:: protein

    from bioservices import *
    u = UniProt(verbose=False)

Get a unique identifier and gene names from a name
----------------------------------------------------

In this tutorial we are interested in using BioServices to obtain information
about a specific protein. Let us focus on ZAP70 protein (homo sapiens).

From **Uniprot**, we can obtain its unique accession number, which may be
useful later on. Let us try to use the :meth:`~bioservices.uniprot.UniProt.search` method:: 

    >>> from bioservices import *
    >>> u = UniProt(verbose=False)
    >>> u.search("ZAP70_HUMAN") # could be lower case


The default format of the returned answer is in HTML format, which is not very convenient. So, let us request a tabular answer instead::

    >>> res = u.search("ZAP70_HUMAN", format="tab")
    >>> print(res)
    Entry   Entry name  Status  Protein names   Gene names  Organism    Length
    P43403  ZAP70_HUMAN reviewed    Tyrosine-protein kinase ZAP-70 (EC 2.7.10.2) (70 kDa zeta-chain associated protein) (Syk-related tyrosine kinase)    ZAP70 SRK Homo sapiens (Human)    619

It is better, but let us simplify even further. We are interesd in the ID
(accession number) and let us say gene names::

    >>> res = u.search("ZAP70_HUMAN", format="tab", columnds="id,genes")
    >>> print(res)
    Entry   Gene names
    P43403  ZAP70 SRK

So here we got the Entry P43403. Entry and Gene names can be saved in two
variables as follows::

    >>> res = u.search("ZAP70_HUMAN", format="tab", columnds="id,genes")
    >>> entry, gene_names = res.split("\n")[1].split("\t") 


Getting the fasta sequence
---------------------------

It is then straightforward to obtain the FASTA sequence of ZAP70 using another
method from the UniProt class called :meth:`~bioservices.uniprot.UniProt.searchUniProtId`:


.. doctest:: protein

    >>> sequence = u.searchUniProtId("P43403", "fasta")
    >>> print(sequence)
    >sp|P43403|ZAP70_HUMAN Tyrosine-protein kinase ZAP-70 OS=Homo sapiens GN=ZAP70 PE=1 SV=1
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

You can then analyse this sequence with your favorite tool.

For instance, with bioservices, you can use NCIBlast but first let us extract
the sequence itself(without the header)

    sequence = sequence.split("\n", 1)[1].strip("\n") 

then, ::

    blast = NCBIblast(verbose=False)
    jobid = s.run(program="blastp", sequence=sequence, stype="protein", \
        database="uniprotkb", email="cokelaer@ebi.ac.uk")
    print s.getResult(jobid, "out")

The last command waits for the job to be finised before printing the results


Searching for relevant pathways
------------------------------------------

Let us start with KEGG. First we need to know the KEGG Id that corresponds to
ZAP70. We can use the **find** method form KEGG service::

    >>> from bioservices import KeggParser
    >>> k = KeggParser(verbose=False)
    >>> k.find("hsa", "zap70")  # "hsa" stands for homo sapiens
    hsa:7535 ZAP70, SRK, STCD, STD, TZK, ZAP-70; zeta-chain (TCR) associated protein kinase 70kDa (EC:2.7.10.2); K07360 tyrosine-protein kinase ZAP-70 [EC:2.7.10.2


Now, let us get the pathways that contains this ID::

    >>> k.get_pathway_by_gene("7535", "hsa")
    {'hsa04064': ' NF-kappa B signaling pathway',
    'hsa04650': 'Natural killer cell mediated cytotoxicity',
     'hsa04660': 'T cell receptor signaling pathway',
     'hsa05340': 'Primary immunodeficiency'}

We can look at them in  browser::

    >>> k.show_pathway("hsa04060")

Searching for binary Interactions
-----------------------------------


For this purpose, we could use PSICQUIC services::

    >>> from bioservices import PSICQUIC
    >>> s = PSICQUIC(verbose=False)
    >>> data = s.query("intact", "ZAP70 AND species:9606")

where 9606 is the taxonomy Id for home sapiens. We could also figure out how
many interctions could be found in ech dabase for this particular query::

    >>> p.getInteractionCounter("zap70 AND species:9606")
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


We see for instance that intact has 11 intercations. Coming back to the interactions returned by s.query, we find indeed 11 intercations
between ZAP70 and other proteins::

    >>> len(data)
    11

Let us look at the first one::

    >>> data[0]
    ['uniprotkb:Q9Y2R2',
     'uniprotkb:P43403',
     'intact:EBI-1211241|uniprotkb:E9PPI1|uniprotkb:B1ALC8|uniprotkb:Q8WVM1|uniprotkb:Q6IPX8|uniprotkb:D4NZ71|uniprotkb:O95064|uniprotkb:O95063|uniprotkb:A0N0K6',
     'intact:EBI-1211276|uniprotkb:Q9UBS6|uniprotkb:Q8IXD6|uniprotkb:Q6PIA4|uniprotkb:A6NFP4',
     'psi-mi:ptn22_human(display_long)|uniprotkb:PTPN22(gene name)|psi-mi:PTPN22(display_short)|uniprotkb:PTPN8(gene name synonym)|uniprotkb:Hematopoietic cell protein-tyrosine phosphatase 70Z-PEP(gene name synonym)|uniprotkb:Lymphoid phosphatase(gene name synonym)|uniprotkb:PEST-domain phosphatase(gene name synonym)',
    'psi-mi:zap70_human(display_long)|uniprotkb:ZAP70(gene name)|psi-mi:ZAP70(display_short)|uniprotkb:SRK(gene name synonym)|uniprotkb:Syk-related tyrosine kinase(gene name synonym)|uniprotkb:70kDa zeta-chain associated protein(gene name synonym)',
     'psi-mi:"MI:0096"(pull down)',
     'Wu et al. (2006)',
     'pubmed:16461343',
     'taxid:9606(human)|taxid:9606(Homo sapiens)',
     'taxid:9606(human)|taxid:9606(Homo sapiens)',
     'psi-mi:"MI:0914"(association)',
     'psi-mi:"MI:0469"(IntAct)',
     'intact:EBI-1211263',
     'intact-miscore:0.60']

The First two element are the entries for specy A and B. The last element is the
score. The 11th element the type of interaction and so on.

What could be useful is to convert these elements into uniprot ID only. Witrh
intact DB it is irrelevant but with other DBs, it may be useful (e.g., biogrid).

There is such a function called convertQuery::


    >>> data = s.query("biogrid", "ZAP70 AND species:9606")
    >>> data2 = s.convertQuery(data, "biogrid")



you can also query and convert for each database that is active. THis can be
done manually:

    for each db in s.database_active:

or 

   >>> res = s.queryAll("ZAP70 AND species:9606")
   >>> res2 = s.convertQuery(res)

res2 contains N entry with uniprot ID as first and second element. 


   >>> len(set(res2))



For instance all human interactions reported in MArch 2013
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



    >>> p = psicquic.PPI()
    >>> p.queryAll("ZAP70 AND species:9606")
    >>> p.summary()
    >>> for i in range(1,p.N+1):
    ...    print i, len(p.relevant_interactions[i])
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



