Whats' new, what has changed
================================




Revision 1.3
------------------

* 1.3.8 (progress)
  * CHANGES: cache files are now stored in the ./config/bioservices directory,
    this fixes https://github.com/cokelaer/bioservices/issues/40

* 1.3.7
  * CHANGES
    * ArrayExpress: add new 2 methods to ease the usage

  * BUG FIXES
    * KEGG: fix https://github.com/cokelaer/bioservices/issues/39


* 1.3.6
  * BUG FIXES
    * KEGG: Fixed during the major changes described here below
            https://github.com/cokelaer/bioservices/issues/29
  * CHANGES
    * IntactL rename Intact class into IntactComplex
    * KEGG: revisited the parsing following requests from user
      https://github.com/cokelaer/bioservices/issues/30
    * KEGG: remove useless function (check_dbentries) 
    * KEGG: The KEGGParser does not inherit from KEGG anymore and there is
            now a parse() method inside KEGG so user do not need to play with the 
            2 classes. Only KEGG is required. KEGGParser can still be used but
            will not have the KEGG methods anymore

* 1.3.5

  * BUG FIXES
    * quickgo: fix bug https://github.com/cokelaer/bioservices/issues/22 
    * uniprot: add missing columns (https://github.com/cokelaer/bioservices/issues/23)
    * kegg: fix parser related to reaction in the Compound data structure (https://github.com/cokelaer/bioservices/issues/27)

  * NEWS

    * add Intact complex web services


* 1.3.4

  * BUG FIXES

  * CHANGES
    * clinvitae: tests and doc added
    * services modules: DevTools class moved to easydev

  * NEWS

    * add PRIDE service + test + doc

* 1.3.3

  * BUG FIX
     * uniprot fixing a python 3 typo

  * CHANGES
    * pdb: add a method
    * hgnc: add new class related to HGNC

  * NEWS 
    * services.py: add a method to ease conversion of dict to json. add
      attribute to limit number of requests per seconds but not yet used.
    * taxonomy module: add new method in Taxon to look for a taxon identifier given a name
    * NEW module ensembl completed
    * NEW module clinvitae added (contribution from Patrick Short)

* 1.3.2

  * CHANGES:

    * services: http_get and http_post now accepts all optional arguments from requests.
    * services: get_headers default content is now same as urrlib2
    * pdb module: more functions added
    * ensembl module added with some functionalities

* 1.3.1

  * CHANGES:

    * uniprot: multi_mapping is deprecated. mapping can now handle long queries by itself.
    * services/settings:

      * removed get_bioservices_env function, which is not used anymore
      * move urlencode in Service class into WSDLService, which will be deprecated
      * add TIMEOUT in WSDLService and REST as alias to settings.TIMEOUT so timeout
        can now be used in both REST and WSDL.

  * NEWS:

    * readseq module added. 

  * BUG fixes: 

    * CACHING attribute had a typo

* 1.3.0

  * NEWS

    * added REST class that uses the requests module. This class replaces
      of instance of RESTservice that uses urllib2, which will be deprecated
      later on. This speeds up the code significantly not only 
      because requests is faster but also because we now do not need trial/time
      hack that was implemented inside RESTService. We also use the 
      requests_cache module that could be used to speed go but requires
      to store cache files locally. Asynchronous requests is available but used
      only in a few places for now. 
    * EUtils has been fully implemented excepting EPost. API may still change to
      make its usage easier but functionalities are there.

  * CHANGES

    * update code to be python-3 compatible. There are still issues with suds/requests/gevent
      but the code itself is python3 executable.
    * WSDLservice now uses suds instead of SOAP package by default
    * all paramters called format have been renamed frmt (format is a python
      keyword)
    * chembldb module and class renamed to chembl and :class:`bioservices.chembl.ChEMBL`
    * All classes that depends on RESTService have been updated to use the new
      REST class.
    * chembldb: 

      * get_assay_by_chemblId renamed in get_assays_by_chemblId
      * renamed  get_target_by_refSeqId into get_target_by_refseq
      * kegg module: all Kegg strings replaced by KEGG so the kegg.Kegg class is
        now kegg.KEGG
    * ChEBI:  getUpdatedPolymer: remove useless parameters (was failing with python3)
    * Wikipathway class renamed as WikiPathways to agree with official name
    * biomart now uses python3 and we had to remove the threaded_request module,
      which does not seem to ba available. So, we used the new implementation
      using requests but gevent is not available for python3 either so, we use
      requests but without the asynchronous call. This is working for now.
      Transparent for the user.
    * geneprof: parameter called type and format are renamed output and frmt to
      not clash with python keywords. Use REST class instead of RESTService but
      should be transparent for the users.
    * services do not have the checkParam method. use
      devtools.check_param_in_list instead.

  * BUG FIXES:

    * Fixing bug #24/25 posted on assembla related to parse_kgml_pathway
      second argument can now be used. 
    * wikipathway: findInteractions had a typo in i

Revision 1.2
------------------

* 1.2.6:
	* fixing bug report 22 related to KEGG.pathway2sif function that was	failing.
	* add option in biomart to use different host. This is to fix an issue where biomart hangs forever. This was reported by Daniel D bug report 23 on assembla.


* 1.2.5: 
    * add try/except for pandas library.

* 1.2.4: 
    * fixing typo in the init that fails bioservices ito be used if pkg_resources is not available.

* 1.2.3
    * updating some apps (fasta,peptides, taxon) in bioservices.apps directory
	* Improves UniProt module by adding a dataframe export where performing a search
	* added the BioDBnet service.
	* added Pathway Common
	* fixed UniChem: add new database identifiers and fix interpretation of the output

* 1.2.2:
    * NEW Service: :class:`bioservices.biodbnet.BioDBNet`
    * uniprot: add multi_mapping method to use mapping method on large queries and
      added timeout/trials inside uniprot functions

* 1.2.1:
    * same as 1.2.0 but fixed missing mapping and apps directory in the distribution available on pypi

* 1.2.0
   * Kegg class has now an alias called KEGG
   * NEW Services: :class:`bioservices.muscle.MUSCLE`
   * fix bug in get_fasta from uniprot class
   * add aliases to quickGO to retrieve annotation
   * NEW Service: :class:`bioservices.pathwaycommons.PathwayCommons`
   * NEW Service: :class:`bioservices.geneprof.GeneProf` service
   * uniprot add function to get uniprot fasta sequence
   * add apps.peptides module

Revision 1.1
------------------

* 1.1.3
    * fix bug in chembldb.get_all_targets() that was failing to return the
	json/dictionary as expected.

* 1.1.2
    * add biocarta, pfam modules (and htmltools. maybe not required.)
	* fix bug in uniprot.mapping to return list of values instead of a string
	  (assembla ticket 19).

* 1.1.1:
    * services.py: move print statements into loggin.warning
	* add documentation and examples related to Galaxy/BioPython.
    * uniprot mapping function now returns a dictionary instead of a list
    * NEW Service : class:`bioservices.hgnc.HGNC` + doc + test

Revision 1.1
------------------
* 1.1.0:
    * in psicquic when performing the conversion, we now use a try/except since some fields (in rare case) may be missing
	* add faqs in the doc + update of the README and metadata.
	* fix typo in the list of uniprot mapping
	* Use BeautifulSoup4 instead of 3
	* add the ChEBI  Web Service.
	* add the UniChem  Web Service.
	* logging ERROR in Service when data cannot be converted to XML is now a simple warning
	* kegg.conv method now returns a dictionary instead of list of tuples.

Revision 1.0
------------------

* 1.0.4
	* 	add a draft version of PDB just to be able to fetch PDB data and use it
		with external tool such as PyMOL as shown in the new pymol.rst
	  	documentation.
	* add a missing docstring in uniprot +  check to/fr parameters in UniProt.mapping
	  method.
	* Fix a typo in PSICQUIC module.
	

* 1.0.3
    * uniprot.UniPort.search method: default value of the parameter format is now "tab"
	* fix 1 quickgo test
	* a few documentation updates in biomart/uniprot/chembldb and tutorial.

* 1.0.2:
    * add SOAPpy in the setup requirements
	* finished ArrayExpress +doc + tests
	* fixed a bug in KEGGParser.parseGene
	* add methods in psicquic to parse all databases and convert to uniprot if
      possible. These methods are used to build an application provided in the
	  tutorial
    * add biomart + doc + test
    * add onWeb method in Service class
    * add chemspider draft
	* complete eutils 

* 1.0.1
    * Add miriam module
    * Add arrayexpress 

* 1.0.0:
    * First release of bioservices

Revision 0.9
------------------

* 0.9.7: 
    * add new feature in KEgg module to instrospect kgml data sets
	* add biogrid test and documentation.
	* chembldb improvments
	* uniprot bug fixes (search if working as expected now)
* 0.9.6:
    * Finalising the Kegg module
* 0.9.5: 
    * add parser for all KEGG entries (enzyme, genome, pathway, ...) 
	* add a show_pathway to highlight element in a pathway
* 0.9.4:
    * cleaning up the modules

* 0.9.3:
    * documentation cleanup
    * fix tests
    * fix a few small bugs in biomodels 
    * adding getattr method for all databases in kegg model
    * Service class has new method call pubmed to load pubmed in browser

* 0.9.2:
    * uniprot search method improved


* 0.9.1: fix typo in biomodel. add uniprot search method. add keggParser class

* 0.9.0: Stable version of bioservices including the following services:
	BioModels, Kegg, Reactome, Chembl, PICR, QuickGO, Rhea, UniProt,
	WSDbfetch, NCBIblast, PSICQUIC, Wikipath


Up to Revision 0.5
------------------- 
* 0.4.9: finalise wikipathway
* 0.4.8: finalise doc of half of the services.
* 0.4.7: add psicquic service and carry on reactome
* 0.4.6: finalise kegg module and test
* 0.4.5: finalise biomodels. keff WSDL is not maintained anymore: started REST version. 
* 0.4.4: finalise quickgo,rhea, picr, uniprot. Update servie to use logging module.
* 0.4.3: add quickgo
* 0.4.2: add wsdbfetch/uniprot
* 0.4.1: add wikipathways module +test .
* 0.4.0: add rhea service + test. Updating the documentation.
* 0.3.0: add reactome + uniprot.
* 0.2.0: finalise biomodels and add picr service + test for biomdodel service..
* 0.1.0: add database and kegg modules + its documentation and tests


