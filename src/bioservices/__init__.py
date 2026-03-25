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
# settings and services must be imported first as many other modules depend on them
from . import settings  # isort: skip
from .settings import *  # isort: skip

from . import services  # isort: skip
from .services import *  # isort: skip

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
    geo,
    hgnc,
    intact,
    interpro,
    kegg,
    muscle,
    mygeneinfo,
    ncbiblast,
    ncbiblastapi,
    omicsdi,
    omnipath,
    panther,
    pathwaycommons,
    pdb,
    pdbe,
    pfam,
    pride,
    proteins,
    pubchem,
    quickgo,
    reactome,
    rhea,
    string,
    unichem,
    uniprot,
    wikipathway,
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
from .geo import *
from .hgnc import *
from .intact import *
from .interpro import *
from .kegg import *
from .muscle import *
from .mygeneinfo import *
from .ncbiblast import *
from .ncbiblastapi import *
from .omicsdi import OmicsDI
from .omnipath import *
from .panther import *
from .pathwaycommons import *
from .pdb import *
from .pdbe import *
from .pfam import *
from .pride import *
from .proteins import *
from .pubchem import *
from .quickgo import *
from .reactome import *
from .rhea import *
from .string import *
from .unichem import *
from .uniprot import *
from .wikipathway import *

# moved to attic in bioservices v1.6
# from . import geneprof
# from .geneprof import *
