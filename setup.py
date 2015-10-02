# -*- coding: utf-8 -*-
__revision__ = "$Id$"
import os
from setuptools import setup, find_packages
import glob


_MAJOR               = 1
_MINOR               = 4
_MICRO               = 0
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {
        'Cokelaer':('Thomas Cokelaer','cokelaer@ebi.ac.uk'),
        },
    'version': version,
    'license' : 'GPL',
    'download_url' : ['http://pypi.python.org/pypi/bioservices'],
    'url' : ['http://pypi.python.org/pypi/bioservices'],
    'bugtrack_url': 'https://github.com/cokelaer/bioservices/issues',
    'description':'Access to Biological Web Services from Python' ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : [
        "BioServices", "WebServices", "Biology", "BioDBNet", "ChEBI", "UniChem", "Kegg", "KEGG", "BioModels",
        "EUtils", "UniProt", "PICR", "ArrayExpress", "MUSCLE", "QuickGO", "PDB", "PSICQUIC", "Blast",
        "BioMART", "BioGRID", "MIRIAM", "BioMart", "GeneProf", "ChEMBL", "ChemSpider", 
        "HGNC", "PathwayCommons", "Rhea", "Ensembl"],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
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


setup(
    name             = 'bioservices',
    version          = version,
    maintainer       = metainfo['authors']['Cokelaer'][0],
    maintainer_email = metainfo['authors']['Cokelaer'][1],
    author           = metainfo['authors']['Cokelaer'][0],
    author_email     = metainfo['authors']['Cokelaer'][1],
    long_description = readme + '\n\n' + history,
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
    install_requires = ["grequests", "requests", "requests_cache",
        "easydev>=0.8.2", "beautifulsoup4",  "suds-jurko", "appdirs", 'wrapt'],
    )


