from importlib import metadata


def get_package_version(package_name):
    try:
        version = metadata.version(package_name)
        return version
    except metadata.PackageNotFoundError:
        return f"{package_name} not found"


version = get_package_version("bioservices")


from easydev import CustomConfig
from easydev.logging_tools import Logging

logger = Logging("bioservices", "WARNING", text_color="green")


import colorlog

logger = colorlog.getLogger(logger.name)

# Initialise the config directory if not already done
configuration = CustomConfig("bioservices", verbose=False)
bspath = configuration.user_config_dir

# Add bioservices.uniprot to sys.modules to prevent cycles in our imports
# import bioservices.uniprot
# bioservices.uniprot  # Stop flake8 error

# sub packages inside bioservices.
from . import (
    apps,
    arrayexpress,
    bigg,
    biocontainers,
    biodbnet,
    biomart,
    biomodels,
    chebi,
    chembl,
    cog,
    dbfetch,
    ena,
    ensembl,
    eutils,
    eva,
    hgnc,
    intact,
    kegg,
    muscle,
    ncbiblast,
    omicsdi,
    omnipath,
    pathwaycommons,
    pdb,
    pdbe,
    pfam,
    pride,
    pubchem,
    quickgo,
    reactome,
    rhea,
    services,
    settings,
    unichem,
    uniprot,
    wikipathway,
    xmltools,
)
from .arrayexpress import *
from .bigg import BiGG
from .biocontainers import Biocontainers
from .biodbnet import *
from .biomart import *
from .biomodels import *
from .chebi import *
from .chembl import *
from .cog import *
from .dbfetch import *
from .ena import ENA
from .ensembl import *
from .eutils import *
from .eva import *
from .hgnc import *
from .intact import *
from .kegg import *
from .muscle import *
from .ncbiblast import *
from .omicsdi import OmicsDI
from .omnipath import *
from .pathwaycommons import *
from .pdb import *
from .pdbe import *
from .pfam import *
from .pride import *
from .pubchem import *
from .quickgo import *
from .reactome import *
from .rhea import *
from .services import *
from .settings import *
from .unichem import *
from .uniprot import *
from .wikipathway import *
from .xmltools import *

# moved to attic in bioservices v1.6
# from . import geneprof
# from .geneprof import *
