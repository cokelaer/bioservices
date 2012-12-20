

.. contents::


.. _kegg_tutorial:

Kegg Tutorial
==============

Introduction
--------------
Start a kegg interface (default organism is human, that is called **hsa**):


.. doctest::

    from bioservices.kegg import Kegg
    k = Kegg()

look at the list of organisms::

    print k.organisms

In general, methods require an access to the on-line Kegg database
therefore it takes time. For instance, the command above takes a couple of
seconds. However, it is buffered so next time you call it, it will be much faster.

The list of methods is available as follows::

    k.methods

Some of the function have been wrapped and therefore are accesible from the
methods of the Kegg class itself. For instance, **bget** allows to query an
entry::

    k.bget("hsa:7535")    #hsa:7535 is also known as ZAP70

If a WSDL method is not visible, you can still call it via the serv attribute as
follows::

    k.serv.bget("hsa:7535")

Finally, not that the bget function can be used quite a lot but needs to access
to the Kegg server. So it takes time. If you need to perform same request again
and again, use :meth:`~bioservices.kegg.Kegg.bget_buffer` that buffers the output of bget. 

Searching for an organism
---------------------------

You can search for an organism id using :meth:`~bioservices.kegg.Kegg.lookfor_organism`, where you can enter an
id or a part of the full name (lower and upper case are not important)::

    >>> k.lookfor_organism('droso')
    [('Drosophila melanogaster (fruit fly)', 'dme'),
     ('Drosophila pseudoobscura pseudoobscura', 'dpo'),
     ('Drosophila ananassae', 'dan'),
     ('Drosophila erecta', 'der'),
     ('Drosophila persimilis', 'dpe'),
     ('Drosophila sechellia', 'dse'),
     ('Drosophila simulans', 'dsi'),
     ('Drosophila willistoni', 'dwi'),
     ('Drosophila yakuba', 'dya'),
     ('Drosophila grimshawi', 'dgr'),
     ('Drosophila mojavensis', 'dmo'),
     ('Drosophila virilis', 'dvi')]


Look for pathways (by name)
------------------------------------

Searching for pathways is quite similar. The output is just not formatted in the
same way::

    >>> k.lookfor_pathway("B cell")
    Out[9]: [<SOAPpy.Types.structType item at 58640288>: {'definition': 'B cell
        receptor signaling pathway - Homo sapiens (human)', 'entry_id':
        'path:hsa04662'}]


You can also search for a pathway knowing some genes but first, we need to
introspect the pathway to get the genes IDs.


Look for pathway (by genes i.e., IDs or usual name)
--------------------------------------------------------

One issue for end-users is to deal with the Kegg IDs. It's hard to search for a
pathway if you do not know the Kegg IDs of a given specy (e.g., ZAP70). 

We provide some methods to ease the search for a pathway given IDs or usual
names. As an example, let us consider the specy **ZAP70**. Let us consider for
now that we know its Kegg Id (**hsa:7535**) although in practice we don't. We
will see later on how to find this Id. 

In order to obtain the Id, you would need to search for all genes within the organism::

    >>> genes = k.get_genes_by_organism()
    >>> len(genes)
    25945

and, for each gene Id, you would need to introspect the description of the Id using
for instance::

    print k.get("hsa:7535")
    print k.btit("hsa:7535")


Here we see that the usual names are::

    hsa:7535 ZAP70, SRK, STD, TZK, ZAP-70; zeta-chain (TCR) associated protein
    kinase 70kDa (EC:2.7.10.2); K07360 zeta-chain (TCR) associated protein kinase
    [EC:2.7.10.2]


We need to look at all genes to be able to build a reverse
dictionary so that given a name, we get the Kegg Id. This is obviously
cumbersome and therefore we provide a method that does it automatically. It is called `lookfor_specy`::

    k.lookfor_specy("zap70")

The first time you call the method, it will search for a zipped file that is provided with the package and 
stores a snapshot of a mapping between species and their Kegg Ids. The file may
be out-dated but you can rebuild it (takes a few minutes)::

    k.build_specy_ids_mapping()

and save it so that you can load the results another time::

    k.save_mapping("test.dat")
    k.load_mapping("test.dat")

Once the dictionary us built, it is easy and fast to search for a pathway given the specy
name::

    >>> k.lookfor_specy("zap70")
    [{'description': 'ZAP70, SRK, STD, TZK, ZAP-70; zeta-chain (TCR) associated
    protein kinase 70kDa (EC:2.7.10.2); K07360 zeta-chain (TCR) associated protein
    kinase [EC:2.7.10.2]',
      'keggid': 'hsa:7535'}]

Here, you see that zap70 has Id **hsa:7535**. Now, you can search for a pathway
that contain that Id::

    >>> k.get_pathways_by_genes("hsa:7535")
    ['path:hsa04064', 'path:hsa04650', 'path:hsa04660', 'path:hsa05340']

If you have several gene Ids, you can provide them within a list::

    >>> k.get_pathways_by_genes(["hsa:6363", "hsa:7535"])
    ['path:hsa04064']




Introspecting a pathway
--------------------------

Let us focus on one pathway, which entry is **path:hsa4660**. You can obtain all
gene entries contained in the pathway as follows::

    pid = "path:hsa4660"
    k.get_genes_by_pathway(pid)

and all relations within the pathways as follows::

    relations = k.get_element_relations_by_pathway(pid)

The output is a list of dictionaries, each dictionary representing a relation in the pathway. For instance, the first relation above contains::

    <SOAPpy.Types.structType item at 84641120>:
        {   'element_id2': 63,
            'element_id1':61,
            'type': 'PPrel',
            'subtypes': [<SOAPpy.Types.structType item at 79054320>:
                {   'type': '---',
                    'element_id': None,
                    'relation': 'binding/association'}]
        }

As you can see, elements of the relation or ids (element_id1 and element_id2),
and the type of the edge are provided in **type** and **subtypes**.

.. warning:: the element ids are ids within the pathway itself NOT the ids of the genes! So, you
    need to get the mapping. 

To build a mapping between the element Ids and genes Ids, you need the elements of the pathways::

    elements = k.get_elements_by_pathway(pid)


for instance, the first element is ::

    >>> elements[0]
    >>> Out[563]: <SOAPpy.Types.structType item at 90802944>: {'element_id': 1, 'type':
           'compound', 'names': ['cpd:C05981'], 'components': []}

so now, we know that the element with id=1 is a compound, which entry is
cpd:C05981.

The unique types can be extracted with a simple python statement::

    set([e['type'] for e in elements])
    Out[565]: set(['ortholog', 'map', 'gene', 'group', 'compound'])

If we are interested in the gene only, we can use::

    k.get_elements_by_pathway_and_type(pid, 'gene')



Building a histogram of all relations in human pathways
------------------------------------------------------------------

Scanning all relations of the Human organism takes about 5-10 minutes. You can
look at a subset by setting Nmax to a small value (e.g., Nmax=10).

.. note:: relations are buffered when using extra_get_all_relations method.

::

    from pylab import *
    # extract all relations from all pathways
    from bioservices.kegg import Kegg
    k = Kegg()
    Nmax = None  # set to None to get all relations (for 258 pathways)
    all_relations = k.extra_get_all_relations(Nmax)for 
    hist([len(r) for r in all_relations], 20)
    xlabel('number of relations')
    ylabel('\#')
    title("number of relations per pathways")
    grid(True)

.. image:: all_relations.png
    :width: 80%


You can then extract more information such as the type of relations::

    # scan all relations looking for the type of relations
    counter = k.extra_count_relations(all_relations)

    # For 258 pathways, we obtained:

    {'activation': 3171,
     'binding/association': 1051,
     'compound': 5216,
     'dephosphorylation': 16,
     'dissociation': 76,
     'expression': 532,
     'indirect effect': 155,
     'inhibition': 665,
     'methylation': 2,
     'missing interaction': 77,
     'phosphorylation': 196,
     'repression': 12,
     'state change': 28,
     'ubiquitination': 17}

    



Access to compound, reactions, ko, drugs...
--------------------------------------------

This example uses the NFkB signalling pathway. Let us search for its id within
the database using the :meth:`lookfor_pathway` command::

    >>> k.lookfor_pathway("NF")
    [<SOAPpy.Types.structType item at 98402888>: {'definition': 
        'NF-kappa B signaling pathway - Homo sapiens (human)', 'entry_id': 'path:hsa04064'},
     <SOAPpy.Types.structType item at 98450176>: {'definition': 
        'Vibrio cholerae infection - Homo sapiens (human)', 'entry_id': 'path:hsa05110'},
    ...


The first pathway is the one we are looking for. Its entry_id is
"path:hsa04064". Now, we can obtain a list of genes ids corresponding to this
pathway::

    >>> pw = k.lookfor_pathway("NF")[0]
    >>> pid = pw.entry_id
    >>> genes = k.get_genes_by_pathway(pid)
    >>> len(genes)
    93

If you do not know the name of a pathwya but know some species in it (given
their name, not kegg id), then you can use the following command::


    >>> k.lookfor_specy("ZAP70")
    'hsa:7535'
    >>> k.get_pathways_by_genes("hsa:7535")
    ['path:hsa04064', 'path:hsa04650', 'path:hsa04660', 'path:hsa05340']

You can see the pathway "path:hsa04064"  (NF-kappaB).


From a pathway, you can obtain the number of compounds:: 

    >>> compounds = k.get_compounds_by_pathway(pid)
    >>> print(compounds)
    ['cpd:C00076', 'cpd:C00165', 'cpd:C01245']

Now, you may want to do the inverse and search for pathways that contains these
compounds::

    >>> k.get_pathways_by_compounds(['cpd:C00076', 'cpd:C00165', 'cpd:C01245'])
     ['path:ko04010', 'path:ko04012', 'path:ko04020', 'path:ko04062',
    'path:ko04064', 'path:ko04066', 'path:ko04070', 'path:ko04270', 'path:ko04370',
    'path:ko04540', 'path:ko04650', 'path:ko04660', 'path:ko04662', 'path:ko04664',
    'path:ko04666', 'path:ko04720', 'path:ko04722', 'path:ko04723', 'path:ko04724',
    'path:ko04725', 'path:ko04726', 'path:ko04728', 'path:ko04730', 'path:ko04745',
    'path:ko04912', 'path:ko04916', 'path:ko04961', 'path:ko04970', 'path:ko04971',
    'path:ko04972', 'path:ko05143', 'path:ko05146', 'path:ko05200', 'path:ko05214',
    'path:ko05223']

There are quite a few pathways containing these compounds, in particular **path:ko04064**, which can be visualized::

    k.view_pathways(["path:ko04064"])

The pathway **path:hsa04064** does not contain drugs or reactions. If you consider **path:hsa00010** you could also use more functions to retrieve elements::

    >>> reactions = k.get_reactions_by_pathway("path:hsa00010")
    >>> drugs = k.get_drugs_by_pathway("path:hsa00010")
    >>> enzymes = k.get_enzymes_by_pathway("path:hsa00010")
    >>> glycans = k.get_enzymes_by_pathway("path:hsa00010") # nothing

and conversely::

    >>> k.get_pathways_by_reactions(reactions)
    ['path:rn00010']
    >>> k.get_pathways_by_enzymes(['path:map00010'])
    ['path:map00010']


.. note:: not that the pathway name is now rn00010 or map00010, dr:D00010but it corresponds to
   hsa00010. rn stands for reactions, map for enzymes ??.

.. note:: get_pathways_by_drugs does not seem to work.






Notes about KO
------------------

KO stands for Kegg Orthology, several methods are available::


    >>> kos = k.get_kos_by_pathway(pid)
    >>> ko = kos[0] # ko:K01116
    >>> k.get_genes_by_ko(ko, "hsa").entry_id
    ["hsa:5335"]
    >>> k.get_ko_by_gene("hsa:5335")
    ['ko:K01116']
    >>> k.serv.get_ko_by_ko_class("00903", "hsa",1,100)



Drugs
---------------

Some pathways contains drugs::

    >>> k.get_drugs_by_pathway("path:hsa00010")
    ['dr:D00009', 'dr:D00010', 'dr:D00068', 'dr:D02798', 'dr:D04855', 'dr:D06542']

From the Drug Ids, you can get information::

    >>> data = k.bget("dr:D00009") # gives you information
    # we see that its name is d-glucose, its mass is around180.15
    # Given the name, you can get the drug id. 

You have also search drugs by name or  mass::

    >>> k.serv.search_drugs_by_name("d-glucose")
    ['dr:D00009', 'dr:D02325']
    # and check its mass or find drugs with similar mass
    >>> k.search_drugs_by_mass(180,.2)
    ['dr:D00009', 'dr:D00109', 'dr:D00114', 'dr:D00371', 'dr:D01195',
    'dr:D01422', 'dr:D03201', 'dr:D04291', 'dr:D05033', 'dr:D06055', 'dr:D08079',
    'dr:D08482', 'dr:D09007', 'dr:D09924']

You can also obtain the drug Ids in other databases::

    >>> drugs = k.get_drugs_by_pathway("path:hsa00010")
    ['dr:D00009', 'dr:D00010', 'dr:D00068', 'dr:D02798', 'dr:D04855','dr:D06542']
    >>> print k.bconv("dr:D00010")




KEGG WSDL methods
-------------------------------------------------------




Here is an organigram of the functions (from Kegg website) available in kegg
module. functions without links can still be accessed using the :attr:`serv`
attribute:


* Meta information
    * :meth:`~bioservices.kegg.Kegg.list_databases`
    * :meth:`~bioservices.kegg.Kegg.list_organisms`
    * :meth:`~bioservices.kegg.Kegg.list_pathways`
    * :meth:`~bioservices.kegg.Kegg.list_ko_classes` (deprecated?)
* DBGET
    * :meth:`~bioservices.kegg.Kegg.binfo`
    * :meth:`~bioservices.kegg.Kegg.bfind`
    * :meth:`~bioservices.kegg.Kegg.bget`
    * :meth:`~bioservices.kegg.Kegg.btit`
    * :meth:`~bioservices.kegg.Kegg.bconv`
* LinkDB
    * Database cross references
        * :meth:`~bioservices.kegg.Kegg.get_linkdb_by_entry`
        * :meth:`~bioservices.kegg.Kegg.get_linkdb_between_databases`
    * Relation among genes and enzymes
          * :meth:`~bioservices.kegg.Kegg.get_genes_by_enzyme`
          * :meth:`~bioservices.kegg.Kegg.get_enzymes_by_gene`
    * Relation among enzymes, compounds and reactions
        * :meth:`~bioservices.kegg.Kegg.get_enzymes_by_compound`
        * :meth:`~bioservices.kegg.Kegg.get_enzymes_by_glycan`
        * :meth:`~bioservices.kegg.Kegg.get_enzymes_by_reaction`
        * :meth:`~bioservices.kegg.Kegg.get_compounds_by_enzyme`
        * :meth:`~bioservices.kegg.Kegg.get_compounds_by_reaction`
        * :meth:`~bioservices.kegg.Kegg.get_glycans_by_enzyme`
        * :meth:`~bioservices.kegg.Kegg.get_glycans_by_reaction`
        * :meth:`~bioservices.kegg.Kegg.get_reactions_by_enzyme`
        * :meth:`~bioservices.kegg.Kegg.get_reactions_by_compound`
        * :meth:`~bioservices.kegg.Kegg.get_reactions_by_glycan`
    * SSDB
        * :meth:`~bioservices.kegg.Kegg.get_best_best_neighbors_by_gene`
        * :meth:`~bioservices.kegg.Kegg.get_best_neighbors_by_gene`
        * :meth:`~bioservices.kegg.Kegg.get_reverse_best_neighbors_by_gene`
        * :meth:`~bioservices.kegg.Kegg.get_paralogs_by_gene`
* Motif
    * :meth:`~bioservices.kegg.Kegg.get_motifs_by_gene`
    * :meth:`~bioservices.kegg.Kegg.get_genes_by_motifs`
* KO (Kegg orthology)
    * :meth:`~bioservices.kegg.Kegg.get_ko_by_gene`
    * :meth:`~bioservices.kegg.Kegg.get_ko_by_ko_class`
    * :meth:`~bioservices.kegg.Kegg.get_genes_by_ko_class`
    * :meth:`~bioservices.kegg.Kegg.get_genes_by_ko`
* PATHWAY
    * Coloring pathways
        * :meth:`~bioservices.kegg.Kegg.mark_pathway_by_objects`
        * :meth:`~bioservices.kegg.Kegg.color_pathway_by_objects`
        * :meth:`~bioservices.kegg.Kegg.color_pathway_by_elements`
        * :meth:`~bioservices.kegg.Kegg.get_html_of_marked_pathway_by_objects`
        * :meth:`~bioservices.kegg.Kegg.get_html_of_colored_pathway_by_objects`
        * :meth:`~bioservices.kegg.Kegg.get_html_of_colored_pathway_by_elements`
    * References for the pathway
        * :meth:`~bioservices.kegg.Kegg.get_references_by_pathway`
    * Relations of objects on the pathway
        * :meth:`~bioservices.kegg.Kegg.get_element_relations_by_pathway`
    * Objects on the pathway
        * :meth:`~bioservices.kegg.Kegg.get_elements_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_genes_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_enzymes_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_compounds_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_drugs_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_glycans_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_reactions_by_pathway`
        * :meth:`~bioservices.kegg.Kegg.get_kos_by_pathway`
    * Pathways by objects
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_genes`
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_enzymes`
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_compounds`
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_drugs`
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_glycans`
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_reactions`
        * :meth:`~bioservices.kegg.Kegg.get_pathways_by_kos`
    * Relation among pathways
        * :meth:`~bioservices.kegg.Kegg.get_linked_pathways`
* GENES
    * :meth:`~bioservices.kegg.Kegg.get_genes_by_organism`
* GENOME
    * :meth:`~bioservices.kegg.Kegg.get_number_of_genes_by_organism`
* LIGAND
    * :meth:`~bioservices.kegg.Kegg.convert_mol_to_kcf`
    * :meth:`~bioservices.kegg.Kegg.search_compounds_by_name`
    * :meth:`~bioservices.kegg.Kegg.search_drugs_by_name`
    * :meth:`~bioservices.kegg.Kegg.search_glycans_by_name`
    * :meth:`~bioservices.kegg.Kegg.search_compounds_by_composition`
    * :meth:`~bioservices.kegg.Kegg.search_drugs_by_composition`
    * :meth:`~bioservices.kegg.Kegg.search_glycans_by_composition`
    * :meth:`~bioservices.kegg.Kegg.search_compounds_by_mass`
    * :meth:`~bioservices.kegg.Kegg.search_drugs_by_mass`
    * :meth:`~bioservices.kegg.Kegg.search_glycans_by_mass`
    * :meth:`~bioservices.kegg.Kegg.search_compounds_by_subcomp`
    * :meth:`~bioservices.kegg.Kegg.search_drugs_by_subcomp`
    * :meth:`~bioservices.kegg.Kegg.search_glycans_by_kcam`

