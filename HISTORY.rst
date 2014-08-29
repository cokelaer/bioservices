.. :changelog:

Relase History
------------------
This is a summary of the changelog, which can be found in the main
documentation.

1.3.0
+++++++++++

* Source code moved to github.com
* New REST class to use requests package instead of urllib2

1.2.X
+++++++++++

* add try/except for pandas library.
* fixing typo in the init that fails bioservices ito be used if pkg_resources is not available.
* added sub-package called apps with some useful tools (fasta,peptides, taxon) in bioservices.apps directory
* NEW the BioDBnet service.
* NEW Pathway Common
* NEW Service: :class:`bioservices.biodbnet.BioDBNet`
* Kegg class has now an alias called KEGG
* NEW Services: :class:`bioservices.muscle.MUSCLE`
* NEW Service: :class:`bioservices.pathwaycommons.PathwayCommons`
* NEW Service: :class:`bioservices.geneprof.GeneProf` service

1.1.X
+++++++++++ 
* add biocarta, pfam modules (and htmltools. maybe not required.)
* add documentation and examples related to Galaxy/BioPython.
* NEW Service : class:`bioservices.hgnc.HGNC` + doc + test
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

