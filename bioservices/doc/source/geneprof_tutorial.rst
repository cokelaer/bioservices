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


    #find all pubic experimental mouse samples in geneprof
    results = g.get_list_experiment_samples("mouse")

    # look at entries that contains "Gene"
    for entry in results: 
        # ignore entries that have cell type "embryonic stem cell"
        if "Gene" in entry.keys() and entry["Cell_Type"]!="embryonic stem cell":
            sampleId = entry['sample_id']
            gene = entry["Gene"]

            # get gene id 
            geneId = g.get_gene_id("mouse",  "C_NAME", gene)['ids']
            assert len(geneId) == 1

            # get targets and print them
            targets =  g.get_targets_by_experiment_sample("mouse", sampleId)
            targets = targets['targets']
            for x in targets['targets']:
                print geneId, " ", x['feature_id']







