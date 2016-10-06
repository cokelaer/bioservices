
Release History
------------------
This is a summary of the changelog. Complete change can be found in the 
`<main documentation <http://pythonhosted.org//bioservices/ChangeLog.html>`_.




1.4.X
---------------

* Include RNASEQ (EBI) in module rnaseq_ebi
* Renamed kegg.KEGG.info into dbinfo , which was overloaded with Logging
* Replaced deprecated HGNC with the official web service from genenames.org
* Fully updated EUtils since WSDL is now down; implementation uses REST now.
* Removed the apps/taxonomy module now part of http://github.com/biokit. 
* added http_delete in services.py



1.3.X
+++++++++++

* CACHE files are now stored in a general directory in the home, rather than
  locally
* Source code moved to github.com
* New REST class to use **requests** package instead of urllib2. 
* Creation of a global configuration file in .config/bioservice/bioservices.cfg
* NEW services: Reactome, Readseq, Ensembl, EUtils

1.2.X
+++++++++++

* add try/except for pandas library.
* added sub-package called apps with some useful tools (fasta,peptides, taxon) in bioservices.apps directory
* NEW services: BioDBnet, BioDBNet, MUSCLE, PathwayCommons, GeneProf

1.1.X
+++++++++++ 
* NEW services: biocarta, pfam, ChEBI, UniChem
* Add documentation and examples related to Galaxy/BioPython.
* NEW Service : HGNC
* Use BeautifulSoup4 instead of 3

1.0.X
+++++++++++ 
* add PDB, ArrayExpress,  biomart, chemspider draft, eutils, miriam, arrayexpress 

1.0.0:
+++++++++++ 
* First release of bioservices


0.9.X: 
+++++++++++ 
* Stable version of bioservices including the following services:
	BioModels, Kegg, Reactome, Chembl, PICR, QuickGO, Rhea, UniProt,
	WSDbfetch, NCBIblast, PSICQUIC, Wikipath

