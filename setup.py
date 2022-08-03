import os
from setuptools import setup, find_packages
import glob


_MAJOR               = 1
_MINOR               = 10
_MICRO               = 1
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {
        'Cokelaer':('Thomas Cokelaer','thomas.cokelaer@pasteur.fr'),
        },
    'version': version,
    'license' : 'GPLv3',
    'download_url' : 'http://pypi.python.org/pypi/bioservices',
    'url' : 'http://github.com/cokelaer/bioservices',
    'bugtrack_url': 'https://github.com/cokelaer/bioservices/issues',
    'description':'Access to Biological Web Services from Python' ,
    "long_description_content_type": "text/x-rst",
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : [
        "BioServices", "WebServices", "Biology", "BioDBNet",
        "ChEBI", "UniChem", "Kegg", "KEGG", "BioModels",
        "EUtils", "UniProt", "PICR", "ArrayExpress", "MUSCLE",
        "QuickGO", "PDB", "PSICQUIC", "Blast", "BioMART", "PantherDB",
        "BioGRID", "MIRIAM", "BioMart", "GeneProf", "ChEMBL",
        "ChemSpider",  "HGNC", "PathwayCommons", "Rhea", "Ensembl"],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }


with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()



on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# sphinx-gallery and numpydoc are used for the doc only.
# Could have a if on_rtd
install_requires = ["grequests", "requests",
        "requests_cache", "easydev>=0.9.36", "beautifulsoup4", "xmltodict",
        "lxml",
        "suds-community", "appdirs", 'wrapt', "pandas", "colorlog"],


setup(
    name             = 'bioservices',
    version          = version,
    maintainer       = metainfo['authors']['Cokelaer'][0],
    maintainer_email = metainfo['authors']['Cokelaer'][1],
    author           = metainfo['authors']['Cokelaer'][0],
    author_email     = metainfo['authors']['Cokelaer'][1],
    long_description = readme + '\n\n' + history,
    long_description_content_type = metainfo["long_description_content_type"],
    keywords         = metainfo['keywords'],
    description = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    download_url     = metainfo['download_url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    package_dir = {'':'src'},
    packages = ['bioservices', 'bioservices.apps', 'bioservices.mapping'],
    #package_dir  = package_dir,

    # If user of python2.6 ordereddict must be installed manually
    install_requires = install_requires,
    entry_points = {
        'console_scripts':[
           'bioservices=bioservices.main:main',
        ]
    }

    )


