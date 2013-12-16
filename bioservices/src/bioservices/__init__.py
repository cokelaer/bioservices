#from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import pkg_resources
try:
    version = pkg_resources.require("bioservices")[0].version
    __version__ = version
except:
    version = __version__


try:
    import pandas as pd
except:
    print("BioServices v%s warning: pandas is not installed on your system" % version)
    print("Some features requires this library and future version of BioServices may use it.")


import services
from services import *

import biomodels
from biomodels import *

import chebi
from chebi import *

import geneprof
from geneprof import *

import kegg
from kegg import *

import hgnc
from hgnc import *

import rhea
from rhea import *

import xmltools
from xmltools import *

import wikipathway
from wikipathway import *

import pdb
from pdb import *

import uniprot
from uniprot import *

import unichem
from unichem import *

import wsdbfetch
from wsdbfetch import *

import unicodefix

import xmltools
from xmltools import *

import reactome
from reactome import *

import quickgo
from quickgo import *

import chembldb
from chembldb import *

import picr
from picr import *

import psicquic
from psicquic import *

import ncbiblast
from ncbiblast import *

import biogrid
from biogrid import *

import miriam
from miriam import *

import arrayexpress
from arrayexpress import *

import biomart
from biomart import *

import eutils
from eutils import *

import pathwaycommons
from pathwaycommons import *


import muscle
from muscle import *

import biodbnet
from biodbnet import *
# sub packages inside bioservices.

#import mapping
import apps
#import dev
