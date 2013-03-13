Protein test case study
==========================

.. testsetup:: protein

    from bioservices import *
    u = UniProt(verbose=False)

Get a unique identifier and gene names from a name
----------------------------------------------------

In this tutorial we are interested in using BioServices to obtain information
about a specific protein. Let us use the ZAP70 protein for the human organism. 

From **Uniprot**, we can obtain its unique accession number, which may be
useful later on. Let us try to use the search method:: 

    >>> from bioservices import *
    >>> u = UniProt(verbose=False)
    >>> u.search("ZAP70_HUMAN") # could be lower case


The output from this request is quite verbose because the default behaviour is to
return the HTML file. We want something more user friendly, so let us use this
command instead::

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

It is then straightforward to obtain the FASTA sequence of ZAP70:


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
    >>> data = s.query("biogrid", "ZAP70 and species:human")

how many interactions were found and in this DB ?


    >>> 


