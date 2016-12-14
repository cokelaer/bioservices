"""
KEGG module example
====================

Histogram of KEGG pathways relations
"""
#################################################
#
from pylab import *


# extract all relations from all pathways
from bioservices.kegg import KEGG
s = KEGG()
s.organism = "hsa"

# retrieve more than 260 pathways so it takes time
max_pathways = 10
results = [s.parse_kgml_pathway(x) for x in s.pathwayIds[0:max_pathways]]
relations = [x['relations'] for x in results]

# plot
hist([len(this) for this in relations], 20)
xlabel('number of relations')
ylabel('#')
title("number of relations per pathways")
grid(True)
