GeneProf tutorial
=====================

`GeneProf <http://www.geneprof.org/GeneProf/index.jsp>`_ is a web-based, graphical software suite that allows users to analyse data produced using high-throughput sequencing platforms (RNA-seq and ChIP-seq; "Next-Generation Sequencing" or NGS): Next-gen analysis for next-gen data


BioServices uses the GeneProf Web Services to enable programmatic access to the public data stored in GeneProf's databases via Python.

.. note:: GeneProf services is quite versatile and contains many resources and examples. For any technical or scientific questions related to the service itself, please see `GeneProf About&Help <http://www.geneprof.org/GeneProf/help_and_tutorials.jsp>`_.


Here below you will find a couple of examples related to GeneProf.



Histogram expression data
============================
:Reference: https://www.geneprof.org/GeneProf/media/bpsm-2013/


In the example below, we use geneprof to 

#. search for Gene identifiers related to an organism (mouse) and keyword (nanog).
#. From the gene identifiers, retrieve the gene expression values for a given gene in all experiments
#. plot histogram of the log values found above.


.. plot::
    :include-source:
    :width: 80%

    >>> from bioservices import GeneProf
    >>> g = GeneProf(verbose=True)
    >>> res = g.search_gene_ids("nanog", "mouse")
    >>> print(res)
    {10090: [29640, 14899]}
    >>> expr1 = g.get_expression("mouse", 29640)
    >>> expr2  = g.get_expression("mouse", 14899)

    >>> import math
    >>> values1 = [math.log(x["RPKM"]+1, 2.) for x in expr1]
    >>> values2 = [math.log(x["RPKM"]+1, 2.) for x in expr2]

    >>> from pylab import clf, subplot, hist
    >>> clf()
    >>> subplot(2,1,1)
    >>> hist(values1)
    >>> subplot(2,1,2)
    >>> hist(values2)


Transcription factor network of stem cells
===============================================

:References: https://www.geneprof.org/GeneProf/media/recomb-2013/


Another example, here below consists in retrieving
the binding targets of transcription factors (about 70) in mouse
embryonic stem cells, and generate a SIF network that could be open and visualised in Cytoscape.

The example below can probably be simplified and make use of tools such as networkx to manipulate
and visualise the final network. Please use with care::

    >>> # first import and create a GenProf instance
    >>> from bioservices import GeneProf
    >>> g = GeneProf(verbose=False)
    >>>
    >>> # find all pubic experimental mouse samples in geneprof
    >>> samples = g.get_list_experiment_samples("mouse")
    >>> # look at entries that contains "Gene"
    >>> graph = {}
    >>> mapgene = {}
    >>> for i, entry in enumerate(samples): 
    ...     print("progress %s/%s" % (i+1, len(samples)))

    ...    # keep only entries that have cell type "embryonic stem cell" in the celltype
    ...    if "Gene" in entry.keys() and "Cell_Type" in entry.keys() and\
    ...        entry["Cell_Type"]=="embryonic stem cell":
    ...
    ...     # aliases
    ...     sampleId = entry['sample_id']
    ...     gene = entry["Gene"]

    ...     # get gene id and save mapping in a dictionary to be used later
    ...     geneId = g.get_gene_id("mouse",  "C_NAME", gene)['ids']
    ...      mapgene[geneId[0]] = gene 

    ...     # get targets and print them
    ...     targets =  g.get_targets_by_experiment_sample("mouse", sampleId)

    ...     # could be simplied inside the geneprof.py module
    ...     if 'targets' in targets.keys():
    ...         targets = targets['targets']

    ...     # print the results
    ...     for x in targets:
    ...         print gene, geneId[0], " ", x['feature_id']
    ...     graph[gene] = [x['feature_id'] for x in targets]

    >>> # The graph saved in the graph variables is quite large. Let us simplified keeping target that
    >>> # are in the list of genes only
    >>> simple_graph = {}
    >>> for k, v in graph.iteritems():
    ...     simple_graph[k] = [mapgene[x] for x in v if x in mapgene.keys()]
    >>> len(simple_grapg.keys())
    72
    >>> sum([len(simple_graph[x]) for x in simple_graph.keys()])
    2137


Finally, you can look at the graph with your favorite tool such as Cytoscape, Gephi. 
I tried to visualise it within CellNopt, which is not dedicated to Network visualisation but contains
a small interface to graphviz quite suitable to visualise small network::

    >>> from cellnopt.core import CNOgraph
    >>> c = CNOGraph()
    >>> for k in simple_graph.keys():
    ...     for v in simple_graph[k]:
    ...         c.add_edge(k, v, link="+")
    >>> c.centrality_degree()
    >>> c.degree_histogram()
    >>> c.plotdot(prog="fdp", node_attribute="degree")
    >>> c.graph['graph'] = {"splines":"true", "size":(20,20), "dpi":200, "fixedsize":True}
    >>> c.plotdot(prog="fdp", node_attribute="degree")
    >>> c.centrality_degree()
    >>> c.graph['node'] = {"width":.01, "height":.01, 'size':0.01, "fontsize":8}
    >>> c.plotdot(prog="fdp", node_attribute="degree")

.. image:: geneprof_network.png



Integrating expression data in pathways
==========================================

:Reference: 

This is another example from the reference above but based on tools available in bioservices so as to  overlaid highthroughput gene expression
onto pathways and models from KEGG database.

::

    >>> from bioservices import KeggParser, GeneProf, uniProt
    >>> g = GeneProf()
    >>> k = KeggParser()
    >>> u = UniProt()

    >>> # load ENCODE RNA-seq
    >>> data = g.get_data("11_683_28_1", "txt")
    >>> rnaseq = pandas.read_csv(StringIO.StringIO(data), sep="\t")
    
    >>> # pick out the log2 fold change values for visualization:
    >>> gene_data = rnaseq['log2FC Lymphoma / EmbryonicKidney']
    >>> gene_names = rnaseq['Ensembl Gene ID']

    # pick example workflows:
    data(demo.paths)

    # generate a pathway diagram for the KEGG path hsa05202 ("Transcriptional 
    # misregulation in cancers") with fold change values from the RNA-seq data above:

    # get pathway
    res = k.parsePathway(k.get("hsa05202"))
    # extract gene and build up a list of identifiers for uniprot mapping
    keggids = ["hsa:"+x for x in res['gene'].keys()]

    # convert to uniprot using uniprot mapping
    uniprotids = u.mapping(fr="KEGG_ID", to="ID", query=",".join(keggids))
    # to fix: to get get not only first value but all of them:
    ensgids = u.mapping(fr="ID", to="ENSEMBL_ID", query=",".join([x[0] for x in uniprotids.values()]))

    k.show_pathway("hsa05202", dcolor="white", keggid={4297:'blue'})

pathview(gene.data = gene.data, pathway.id="05202", species="hsa", cpd.idtype="ENSEMBL", gene.idtype="ENSEMBL", na.col='lightgrey', low=list(gene='darkblue',cpd='darkblue'), mid=list(gene='gold',cpd='gold'), high=list(gene='darkred',cpd='darkred'), limit = list(gene = 3, cpd = 3), width=3200, height=2400)






