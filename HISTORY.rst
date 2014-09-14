.. :changelog:

Release History
------------------
This is a summary of the changelog, which can be found in the main
documentation.

1.3.X
+++++++++++

* Source code moved to github.com
* New REST class to use requests package instead of urllib2. 
* Creation of a global configuration file in .config/bioservice/bioservices.cg
* NEW services: Reactome, Readseq

1.2.X
+++++++++++

* add try/except for pandas library.
* fixing typo in the init that fails bioservices ito be used if pkg_resources is not available.
* added sub-package called apps with some useful tools (fasta,peptides, taxon) in bioservices.apps directory
* NEW the BioDBnet service.
* NEW Pathway Common
* NEW Service: BioDBNet
* Kegg class has now an alias called KEGG
* NEW Services: MUSCLE
* NEW Service: PathwayCommons
* NEW Service: GeneProf service

1.1.X
+++++++++++ 
* add biocarta, pfam modules (and htmltools. maybe not required.)
* add documentation and examples related to Galaxy/BioPython.
* NEW Service : HGNC
* Use BeautifulSoup4 instead of 3
* add the ChEBI  Web Service.
* add the UniChem  Web Service.

1.0.X
+++++++++++ 
* add PDB
* add ArrayExpress
* add biomart + doc + test
* add chemspider draft
* complete eutils 
* Add miriam module
* Add arrayexpress 

1.0.0:
+++++++++++ 
* First release of bioservices


0.9.X: 
+++++++++++ 
* Stable version of bioservices including the following services:
	BioModels, Kegg, Reactome, Chembl, PICR, QuickGO, Rhea, UniProt,
	WSDbfetch, NCBIblast, PSICQUIC, Wikipath

