"""BioServices

import bioservices
u = bioservices.uniprot.UniProt()
u.search("ZAP70")


see online documentation for details on pypi or github.

"""
#from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import pkg_resources
__version__ = "$Id$$, $Rev$"
try:
    version = pkg_resources.require("bioservices")[0].version
    __version__ = version
except:
    version = __version__

try:
    # This is not striclty speaking required to run and use bioservices
    # However, some functions and python notebooks included in bioservices do
    import pandas as pd
except:
    print("BioServices %s warning: pandas is not installed on your system." % version)
    print("Some features requires this library and future version of BioServices may use it.")


# Initialise the config directory if not already done
from easydev import CustomConfig
configuration = CustomConfig("bioservices", verbose=False)
bspath = configuration.user_config_dir



# Add bioservices.uniprot to sys.modules to prevent cycles in our imports
#import bioservices.uniprot
#bioservices.uniprot  # Stop flake8 error


from . import settings
from .settings import *

from . import services
from .services import *

from . import biomodels
from .biomodels import *

from . import chebi
from .chebi import *

from . import ensembl
from .ensembl import *

from . import geneprof
from .geneprof import *

from . import kegg
from .kegg import *

from . import hgnc
from .hgnc import *

from . import intact
from .intact import *

from . import rhea
from .rhea import *

from . import xmltools
from .xmltools import *

from . import wikipathway
from .wikipathway import *

from . import pdb
from .pdb import *

from . import pride
from .pride import *

from . import uniprot
from .uniprot import *

from . import unichem
from .unichem import *

from . import wsdbfetch
from .wsdbfetch import *


from . import reactome
from .reactome import *

from . import quickgo
from .quickgo import *


from . import chembl
from .chembl import *

from . import picr
from .picr import *

from . import psicquic
from .psicquic import *

from . import ncbiblast
from .ncbiblast import *

#from . import readseq
#from .readseq import *

from . import biogrid
from .biogrid import *

from . import miriam
from .miriam import *

from . import arrayexpress
from .arrayexpress import *

from . import biomart
from .biomart import *

from . import eutils
from .eutils import *

from . import pathwaycommons
from .pathwaycommons import *


from . import muscle
from .muscle import *

from . import biodbnet
from .biodbnet import *
# sub packages inside bioservices.

#import mapping
from . import apps
#import dev


from . import clinvitae
from .clinvitae import Clinvitae
