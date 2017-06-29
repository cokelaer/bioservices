GeneProf tutorial
=====================

.. topic:: GeneProf tutorial

    .. versionadded:: 1.2.0
    .. sectionauthor:: Thomas Cokelaer, Dec 2013

`GeneProf <http://www.geneprof.org/GeneProf/index.jsp>`_ is a web-based, graphical software suite that allows users to analyse data produced using high-throughput sequencing platforms (RNA-seq and ChIP-seq; "Next-Generation Sequencing" or NGS): Next-gen analysis for next-gen data


BioServices uses the GeneProf Web Services to enable programmatic access to the public data stored in GeneProf's databases via Python.

.. note:: GeneProf services is quite versatile and contains many resources and examples. For any technical or scientific questions related to the service itself, please see `GeneProf About&Help <http://www.geneprof.org/GeneProf/help_and_tutorials.jsp>`_.


Here below you will find a couple of examples related to GeneProf.



Histogram expression data
--------------------------------------
:Reference: https://www.geneprof.org/GeneProf/media/bpsm-2013/


In the example below, we use geneprof to 

#. search for Gene identifiers related to an organism (mouse) and keyword (nanog).
#. From the gene identifiers, retrieve the gene expression values for a given gene in all experiments
#. plot histogram of the log values found above.


.. .. plot::
    :include-source:
    :width: 80%

.. note:: broken example on June 2017. Service should be fix soon. Issue
   reported to the author.

::

    >>> from bioservices import GeneProf
    >>> g = GeneProf(verbose=True)
    >>> res = g.search_gene_ids("nanog", "mouse")
    >>> print(res)
    {10090: [29640, 14899]}
    >>> expr1 = g.get_expression("mouse", 29640)['values']
    >>> expr2  = g.get_expression("mouse", 14899)['values']

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
-------------------------------------------------------

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
    >>> samples = g.get_list_experiment_samples("mouse")['samples']
    >>> # look at entries that contains "Gene"
    >>> graph = {}
    >>> mapgene = {}
    >>> for i, entry in enumerate(samples): 
    ...     print("progress %s/%s" % (i+1, len(samples)))

    ...     # keep only entries that have cell type "embryonic stem cell" in the celltype
    ...     if "Gene" in entry.keys() and "Cell_Type" in entry.keys() and entry["Cell_Type"]=="embryonic stem cell":
    ...
    ...         # aliases
    ...         sampleId = entry['sample_id']
    ...         gene = entry["Gene"]

    ...         # get gene id and save mapping in a dictionary to be used later
    ...         geneId = g.get_gene_id("mouse",  "C_NAME", gene)['ids']
    ...         mapgene[geneId[0]] = gene 

    ...         # get targets and print them
    ...         targets =  g.get_targets_by_experiment_sample("mouse", sampleId)

    ...         # could be simplied inside the geneprof.py module
    ...         if 'targets' in targets.keys():
    ...             targets = targets['targets']

    ...         # print the results
    ...         for x in targets:
    ...             print gene, geneId[0], " ", x['feature_id']
    ...         graph[gene] = [x['feature_id'] for x in targets]

    >>> # The graph saved in the graph variables is quite large. Let us simplified keeping target that
    >>> # are in the list of genes only
    >>> simple_graph = {}
    >>> for k, v in graph.iteritems():
    ...     simple_graph[k] = [mapgene[x] for x in v if x in mapgene.keys()]
    >>> len(simple_graph.keys())
    72
    >>> sum([len(simple_graph[x]) for x in simple_graph.keys()])
    2137


Finally, you can look at the graph with your favorite tool such as Cytoscape, Gephi. 

Here below, I'm using a basic graph visualisation tool implemented in `CellNOpt <http://www.cellnopt.org>`_, which is not dedicated
for Network visualisation but contains a small interface to graphviz useful in this context (it has a python interface)::

    >>> from cno import CNOGraph
    >>> c = CNOGraph()
    >>> for k in simple_graph.keys():
    ...     for v in simple_graph[k]:
    ...         c.add_edge(k, v, link="+")
    >>> c.centrality_degree()
    >>> c.graph['graph'] = {"splines":"true", "size":(20,20), 
        "dpi":200, "fixedsize":True}
    >>> c.graph['node'] = {"width":.01, "height":.01, 
        'size':0.01, "fontsize":8}
    >>> c.plotdot(prog="fdp", node_attribute="degree")

.. image:: geneprof_network.png



Integrating expression data in pathways
-------------------------------------------------------

:References: https://www.geneprof.org/GeneProf/media/recomb-2013/



This is another example from the reference above but based on tools available in bioservices so as to  overlaid highthroughput gene expression
onto pathways and models from KEGG database.

Fold changes in lymphoma vs. kidney
on selected KEGG pathways

::

    >>> from bioservices import KEGG, GeneProf, UniProt
    >>> import StringIO
    >>> import pandas
    >>> g = GeneProf()
    >>> k = KEGG()
    >>> u = UniProt()

    >>> # load ENCODE RNA-seq into a DataFrame for later
    >>> data = g.get_data("11_683_28_1", "txt")
    >>> rnaseq = pandas.read_csv(StringIO.StringIO(data), sep="\t")
    >>> gene_names = rnaseq['Ensembl Gene ID']

    >>> # get a pathway diagram for the KEGG path hsa05202 ("Transcriptional 
    >>> # misregulation in cancers")
    >>> res = k.parse(k.get("hsa05202"))
    >>> # extract KEGG identifiers corresponding to the genes found in the pathway
    >>> keggids = ["hsa:"+x for x in res['GENE'].keys()]

    >>> # we need to map the KEGG Ids to Ensembl Ids. We will use KEGG mapping and uniprot mapping
    >>> # for cases where the former does not have associated mapping.
    >>> ensemblids = {}
    >>> for id_ in keggids:
    ...     res = k.parse(k.get(id_))['DBLINKS']
    ...     if 'Ensembl' in res.keys(): 
    ...         print id_, res['Ensembl']
    ...         ensemblids[id_] = res['Ensembl']
    ...     else:
    ...         if "UniProt" in res.keys():
    ...             ids = res['UniProt'].split()[0]
    ...             m = u.mapping("ACC", "ENSEMBL_ID", query=ids)
    ...             if len(m): ensemblids[id_] = m[ids][0]
    ...         pass # no links to ensembl DB found

    >>> # what are the KEGG id transformed into Ensembl Ids that are in the ENCODE data set ?
    >>> found = [x for x in ensemblids.values() if x in [str(y) for y in gene_names]]
    >>> indices = [i for i, x in enumerate(rnaseq['Ensembl Gene ID']) if x in found]
    >>>
    >>> # now, we can pick out the log2 fold change values for visualization:
    >>> data = rnaseq.ix[indices][['Ensembl Gene ID', 'log2FC Lymphoma / EmbryonicKidney']]
    >>> # and keep only those that have a negative or positive value
    >>> mid = 1.5
    >>> low = data[data['log2FC Lymphoma / EmbryonicKidney']<-mid]
    >>> geneid_low = list(low['Ensembl Gene ID'])
    >>> up = data[data['log2FC Lymphoma / EmbryonicKidney']>mid]
    >>> geneid_up = list(up['Ensembl Gene ID'])
    >>> mid = data[abs(data['log2FC Lymphoma / EmbryonicKidney'])<mid]
    >>> geneid_mid = list(mid['Ensembl Gene ID'])

    >>> # now that we have the genes (in ensembl format), we need the kegg id 
    >>> keggid_low = [this for this in keggids if ensemblids[this] in geneid_low]
    >>> keggid_mid = [this for this in keggids if ensemblids[this] in geneid_mid]
    >>> keggid_up = [this for this in keggids if ensemblids[this] in geneid_up]
    >>> # it is now time to look at the expression on the diagram
    >>> colors = {}
    >>> for id_ in keggids:  colors[id_[4:]] = "gray,"
    >>> for id_ in keggid_low: colors[id_[4:]] = "blue,"
    >>> for id_ in keggid_up:  colors[id_[4:]] = "orange,"
    >>> for id_ in keggid_mid: colors[id_[4:]] = "yellow,"
    >>> k.show_pathway("hsa05202", dcolor="white", keggid=colors)

The last command will popup the KEGG diagram with the expression data on top of the diagram, as shown in the following picture:

.. image:: geneprof_kegg_expression.png
    :width: 100%
    





