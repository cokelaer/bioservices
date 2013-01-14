# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s): 
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#      https://www.assembla.com/spaces/bioservices/team
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id$
"""This module provides a class :class:`~Kegg` that allows an easy access to all the
WDSL Kegg interface as well as additional methods to obtain statistics about the
Kegg database. See below for details about the functionalities available and the
tutorial/quickstart :ref:`kegg_tutorial`.


.. topic:: What is KEGG ?

    :URL: http://www.kegg.jp/
    :REST: http://www.kegg.jp/kegg/rest/keggapi.html
    :REST: http://www.genome.jp/kegg/rest/weblink.html
    :REST: http://www.genome.jp/kegg/rest/dbentry.html


.. seealso:: `<http://www.kegg.jp/kegg/soap/doc/keggapi_manual.html>`_

Some terminology 
--------------------

This list is taken from Kegg API page and slightly edited.


* organisms (**org**) are made of a three-letter (or four-letter) code (e.g., hsa
  stands for Human Sapiens) used in KEGG (see
  :meth:`~bioservices.kegg.Kegg.organisms`). 
* **db** is a database name used in GenomeNet service. See
  :meth:`~bioservices.kegg.Kegg.databases`
* **entry_id** is a unique identifier that is a combination of the database name
  and the identifier of an entry joined by a colon sign (e.g. 'embl:J00231'
  means an EMBL entry 'J00231').
  **entry_id** includes:

    * **genes_id**: identifier consisting of 'keggorg' and a gene name (e.g. 'eco:b0001' means an E. coli gene 'b0001').
    * **enzyme_id**: identifier consisting of database name 'ec' and an enzyme code used in KEGG/LIGAND ENZYME database. (e.g. 'ec:1.1.1.1' means an alcohol dehydrogenase enzyme)
    * **compound_id**: identifier consisting of database name 'cpd' and a
      compound number used in KEGG COMPOUND / LIGAND database (e.g. 'cpd:C00158'
      means a citric acid). Some compounds also have 'glycan_id' and
      both IDs are accepted and converted internally.
    * **drug_id**: identifier consisting of database name 'dr' and a compound
      number used in KEGG DRUG / LIGAND database (e.g. 'dr:D00201' means a
      tetracycline).
    * **glycan_id**: identifier consisting of database name 'gl' and a glycan
      number used in KEGG GLYCAN database (e.g. 'gl:G00050' means a
      Paragloboside). Some glycans also have 'compound_id' and both
      IDs are accepted and converted internally.
    * **reaction_id**:  identifier consisting of database name 'rn' and a
      reaction number used in KEGG/REACTION (e.g. 'rn:R00959' is a reaction
      which catalyze cpd:C00103 into cpd:C00668).
    * **pathway_id**: identifier consisting of 'path' and a pathway number used
      in KEGG/PATHWAY. Pathway numbers prefixed by 'map' specify the reference
      pathway and pathways prefixed by the 'keggorg' specify pathways specific
      to the organism (e.g. 'path:map00020' means a reference pathway for the
      cytrate cycle and 'path:eco00020' means a same pathway of which E. coli
      genes are marked).
    * **motif_id** is a motif identifier consisting of motif database names
      ('ps' for prosite, 'bl' for blocks, 'pr' for prints, 'pd' for prodom, and
      'pf' for pfam) and a motif entry name. (e.g. 'pf:DnaJ' means a Pfam
      database entry 'DnaJ').
    * **ko_id**: identifier consisting of 'ko' and a ko number used in KEGG/KO.
      KO (KEGG Orthology) is an classification of orthologous genes defined by
      KEGG (e.g. 'ko:K02598' means a KO group for nitrite transporter NirC
      genes).
    * **ko_class_id**: identifier which is used to classify 'ko_id' hierarchically 
      (e.g. '01110' means a 'Carbohydrate Metabolism' class).
      `URL:http://www.genome.jp/dbget-bin/get_htext?KO`   
* **offset** and 'limit' are both an integer and used to control the number of
  the results returned at once. Methods having these arguments will return
  first 'limit' results starting from 'offset'th.
* **fg_color_list** is a list of colors for the foreground (corresponding to the
  texts and borders of the objects on the KEGG pathway map).
* **bg_color_list** is a list of colors for the background (corresponding to the
  inside of the objects on the KEGG pathway map).




"""

"""


Database    Name    Abbrev  kid     Remark
KEGG PATHWAY    pathway     path    map number  
KEGG BRITE  brite   br  br number   
KEGG MODULE     module  md  M number    
KEGG DISEASE    disease     ds  H number    Japanese version: disease_ja ds_ja
KEGG DRUG   drug    dr  D number    Japanese version: drug_ja dr_ja
KEGG ENVIRON    environ     ev  E number    Japanese version: environ_ja ev_ja
KEGG ORTHOLOGY  orthology   ko  K number    
KEGG GENOME     genome  genome  T number    
KEGG GENOMES    genomes     gn  T number    Composite database: genome + egenome
+ mgenome
KEGG GENES  genes   -   -   Composite database: consisting of KEGG organisms
KEGG LIGAND     ligand  ligand  -   Composite database: compound + glycan +
reaction + rpair + rclass + enzyme
KEGG COMPOUND   compound    cpd     C number    Japanese version: compound_ja
cpd_ja
KEGG GLYCAN     glycan  gl  G number    
KEGG REACTION   reaction    rn  R number    
KEGG RPAIR  rpair   rp  RP number   
KEGG RCLASS     rclass  rc  RC number   
KEGG ENZYME     enzyme  ec  -   


Database entry

<dbentries> = <dbentry>1[+<dbentry>2...]
<dbentry> = <db:entry> | <kid> | <org:gene>

Each database entry is identified by:
db:entry
where
"db" is the database name or its abbreviation shown above and
"entry" is the entry name or the accession number that is uniquely assigned
within the database.
In reality "db" may be omitted, for the entry name called the KEGG object
identifier (kid) is unique across KEGG.
kid = database-dependent prefix + five-digit number
In the KEGG GENES database the db:entry combination must be specified. This is
more specifically written as:
org:gene
where
"org" is the three- or four-letter KEGG organism code or the T number genome
identifier and
"gene" is the gene identifier, usually locus_tag or ncbi GeneID, or the primary
gene name.


"""

from services import RESTService
import webbrowser
import copy


class Kegg(RESTService):
    """Interface to the `KEGG <http://www.genome.jp/kegg/pathway.html>`_ database

    ::

        import kegg
        k = kegg.Kegg()
        k.methods
        k.bget("hsa:7535")

        print len(k.pathways)

        k.organisms 


    """

    #: valida database 
    _valid_databases_base = ["module", "disease", "drug",
        "environ", "ko", "genome", "compound", "glycan", "reaction", "rpair",
        "rclass", "enzyme"]
    _valid_databases_info = _valid_databases_base + ["pathway", "brite", "genes", "ligand",
        "genomes", "kegg"]
    _valid_databases_list = _valid_databases_base + ["brite", "pathway", "organism"]


    _valid_databases_find = _valid_databases_base + ["pathway", "genes", "ligand"] 

    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(Kegg, self).__init__(name="Kegg", url="http://rest.kegg.jp", verbose=verbose)
        self.easyXMLConversion = False
        self._organisms = None
        self._organism = None
        self._pathways = None

    def _checkDB(self, database=None, mode=None):
        self.logging.info("checking database %s (mode=%s)" % (database, mode))
        if mode == "info":
            if database not in Kegg._valid_databases_info and\
                database not in self.organisms:
                self.logging.error("database or organism provided is not correct (mode=info)")
                raise
        elif mode == "list":
            if database not in Kegg._valid_databases_list and\
                database not in self.organisms:
                self.logging.error("database provided is not correct (mode=list)")
                raise 
        elif mode == "find":
            if database not in Kegg._valid_databases_find and\
                database not in self.organisms:
                self.logging.error("database provided is not correct (mode=find)")
                raise 
        else:
            raise ValueError("mode can be only info, list, ")

    def info(self, database="kegg"):
        """Displays the current statistics of a given database

        :param str database: can be one of: kegg (default), brite, module,
            disease, drug, environ, ko, genome, compound, glycan, reaction,
            rpair, rclass, enzyme, genomes, genes, ligand or any 
            :attr:`organisms`. Right now T number for organism are not accepted.

        ::

            from bioservices import Kegg
            k = Kegg()
            k.info("hsa") # human organism
            k.info("pathway")

        """
        url = self.url+"/"+"info"
        self._checkDB(database, mode="info")

        url = url + "/" + database
        res = self.request(url)
        return res

    def list(self, query, organism=None):
        """returns a list of entry identifiers and associated definition for a given database or a given set of database entries 

        :param str query: can be one of pathway, brite, module,
            disease, drug, environ, ko, genome, compound,
            glycan, reaction, rpair, rclass, enzyme, organism
            **or** an organism from the :attr:`organisms` attribute **or** a valid
            dbentry (see below). If a dbentry query is provided, organism
            should not be used!
        :param str organism: a valid organism identifier that can be 
            provided. If so, database can be only "pathway" or "module"

        There are convenient aliases to some of the databases. For instance,
        organism database can also be retrieved as a list from the
        :attr:`organisms` attribute. 


        Here is an example that shows how to extract the pathways IDs related to
        the hsa organism::

            >>> k = Kegg()
            >>> res = k.list("pathway", organism="hsa")
            >>> pathways = [x.split()[0] for x in res.strip().split("\\n")]
            >>> len(pathways)  # as of Dec 2012
            261


        .. note:: If you set the query to a valid organism, then the second
               argument (organism is irrelevant and ignored.

        .. note:: If the query is not a database or an organism, it is supposed
            to be a valid dbentries string and the maximum number of entries is 100.

        Other examples::

            k.list("pathway")             # returns the list of reference pathways
            k.list("pathway", "hsa")      # returns the list of human pathways
            k.list("organism")            # returns the list of KEGG organisms with taxonomic classification
            k.list("hsa")                 # returns the entire list of human genes
            k.list("T01001")    # same as above
            k.list("hsa:10458+ece:Z5100") # returns the list of a human gene and an E.coli O157 gene
            k.list("cpd:C01290+gl:G00092")# returns the list of a compound entry and a glycan entry
            k.list("C01290+G00092")       # same as above 
        """
        url = self.url+"/"+"list"
        if query:
            #can be something else than a database so we can not use checkDB
            #self._checkDB(database, mode="list")
            url = url + "/" + query

        if organism:
            if organism not in self.organisms:
                self.logging.error("""Invalid organism provided (%s). See the organisms attribute""" % organism)
                raise 
            if query not in ["pathway", "module"]:
                self.logging.error("""
    If organism is set, then the first argument
    (database) must be either 'pathway' or 'module'. You provided %s""" % query)
                raise
            url = url + "/" + organism


        res = self.request(url)
        return res

    def find(self, database, query, option=None):
        """finds entries with matching query keywords or other query data in a given database 

        :param str database: can be one of pathway, module, disease, drug,
            environ, ko, genome, compound, glycan, reaction, rpair, rclass, 
            enzyme, genes, ligand or an organism (code see :attr:`organism`
            attributes or T number)
        :param str query:
        :param str option: If option provided, database can be only 'compound' 
            or 'drug'. Option can be 'formula', 'exact_mass' or 'mol_weight'




        .. note:: Keyword search against brite is not supported. Use /list/brite to retrieve a short list.

        ::

            k.find("pathway", "Viral")    # search for pathways that contain Viral in the definition
            k.find("genes", "shiga+toxin")             # for keywords "shiga" and "toxin"
            k.find("genes", ""shiga toxin")            # for keywords "shiga toxin"
            k.find("compound", "C7H10O5", "formula")   # for chemical formula "C7H10O5"
            k.find("compound", "O5C7","formula")       # for chemical formula containing "O5" and "C7"
            k.find("compound", "174.05","exact_mass")  # for 174.045 =< exact mass < 174.055
            k.find("compound", "300-310","mol_weight") # for 300 =< molecular weight =< 310 

        """
        _valid_options = ["formula", "exact_mass", "mol_weight"]
        _valid_db_options = ["compound", "drug"]

        self._checkDB(database, mode="find") 
        url = self.url + "/find/"+ database + "/" +  query

        if option:
            if database not in _valid_db_options:
                raise ValueError("invalid database. Since option was provided, database must be in %s" % _valid_db_options)
            if option not in _valid_options:
                raise ValueError("invalid option. Must be in %s " % _valid_options)
            url +=  "/" + option

        res = self.request(url)
        return res


    def get(self, dbentries, option=None):
        """retrieves given database entries 

        :param str dbentries: KEGG database entries involving the following 
            database: pathway, brite, module, disease, drug, environ, ko, genome
            compound, glycan,  reaction, rpair, rclass, enzyme **or** any organism 
            using the KEGG organism code (see :attr:`organisms`) or T number.
        :param str option: one of: aaseq, ntseq, mol, kcf, image


        ::

            self.get("cpd:C01290+gl:G00092") # retrieves a compound entry and a glycan entry
            self.get("C01290+G00092")        # same as above
            self.get("hsa:10458+ece:Z5100")  # retrieves a human gene entry and an E.coli O157 gene entry
            self.get("hsa:10458+ece:Z5100/aaseq") #retrieves amino acid sequences of a human 
                                              #gene and an E.coli O157 gene
            self.get("hsa05130/image")        # retrieves the image file of a pathway map 


        Another is example here below show how to save the image of a given pathway::

            res =  k.get("hsa05130/image")
            f = open("test.png", "w")
            f.write(res)
            f.close()

        .. note::  The input is limited up to 10 entries. 
        """
        _valid_options = ["aaseq", "ntseq", "mol", "kcf", "image"]
        _valid_db_options = ["compound", "drug"]

        #self._checkDB(database, mode="find") 
        url = self.url + "/get/"+ dbentries

        if option:
            if option not in _valid_options:
                raise ValueError("invalid option. Must be in %s " % _valid_options)
            url +=  "/" + option

        res = self.request(url)
        return res


    def conv(self, target, source):
        """convert KEGG identifiers to/from outside identifiers 

        :param str target: the target database.
        :param str source: the source database. 

        :return: Tries to return 2 objects (2 lists) with the 2 identifiers. Otherwise it 
            returns the returned object itself

        Here are the rules to set the target and source parameters.

        First, the target and source are symmetric, therefore the following 
        rules can be inversed. 

        For gene identifiers, the source should be a kegg organism (or T 
        number) and the target can be 'ncbi-gi', 'ncbi-geneid' or 
        'uniprot' only.

        For chemical substance identifiers, the source must be one of the 
        following kegg database: drug, compound, glycan. If so, the source 
        must be either 'drug' or 'chebi'.

        Here are some examples::

            conv("eco","ncbi-geneid") # conversion from NCBI GeneID to KEGG ID for E. coli genes
            conv("ncbi-geneid","eco") #	opposite direction
            conv("ncbi-gi","hsa:10458+ece:Z5100") #conversion from KEGG ID to NCBI GI 


        You can also convert from uniprot to Kegg Id all human gene IDs:: 

            kegg_ids, uniprot_ids = k.conv("hsa", "uniprot")


        .. todo:: the dbentries case. 
        """

        if target in self.organisms:
            if source not in ['ncbi-gi', 'ncbi-geneid', 'uniprot']:
                raise ValueError
        if target in ['ncbi-gi', 'ncbi-geneid', 'uniprot']:
            if source not in self.organisms:
                raise ValueError
        if target in ['drug', 'compound', 'glycan']:
            if source not in ['chebi', 'pubchem']:
                raise ValueError
        if target in ['chebi', 'pubchem']:
            if source not in ['drug', 'compound', 'glycan']:
                raise ValueError




        url = self.url + "/conv/"+ target + '/' + source

        res = self.request(url)

        try:
            t = [x.split("\t")[0] for x in res.strip().split("\n")]
            s = [x.split("\t")[1] for x in res.strip().split("\n")]
            return (t, s)
        except:
            return res

    def link(self, target, source):
        """find related entries by using database cross-references 


	<target_db> = <database>
	<source_db> = <database>

	<database> = pathway | brite | module | disease | drug | environ | ko | genome |
             <org> | compound | glycan | reaction | rpair | rclass | enzyme
            res = k.link("hsa","pathway")

	/link/pathway/hsa 	  	KEGG pathways linked from each of the human genes
	/link/hsa/pathway 	  	human genes linked from each of the KEGG pathways
	/link/pathway/hsa:10458+ece:Z5100 	  	KEGG pathways linked from a human gene and an E. coli O157 gene 
        """
        url = self.url + "/link/"+ target + '/' + source
        res = self.request(url)
        return res


    def _get_organisms(self):
        if self._organisms == None:
            res = self.request(self.url + "/list/organism")
            orgs = [x.split()[1] for x in res.split("\n") if len(x)]
            self._organisms = orgs[:]
        return self._organisms
    organisms = property(_get_organisms, doc="returns list of organisms")

    def _get_glycans(self):
        if self._glycans == None:
            res = self.request(self.url + "/list/glycans")
            orgs = [x.split()[1] for x in res.split("\n") if len(x)]
            self._glycans = orgs[:]
        return self._glycans
    glycans = property(_get_glycans, doc="returns list of glycans")


    def _get_organism(self):
        return self._organism
    def _set_organism(self, organism):
        if organism in self.organisms:
            self._organism = organism
            self._pathways = None
        else:
            self.logging.error("Invalid organism. Check the list in :attr:`organisms` attribute")
            raise 
    organism = property(_get_organism, _set_organism, doc="returns the current default organism ")

    def _get_pathways(self):

        if self._organism == None:
            self.logging.warning("You must set the organism first (e.g., self.organism = 'hsa')")
            return

        if self._pathways == None:
            res = self.request(self.url + "/list/pathway/%s" % self.organism)
            orgs = [x.split()[0] for x in res.split("\n") if len(x)]
            self._pathways = orgs[:]
        return self._pathways
    pathwayIDs = property(_get_pathways, doc="""returns list of pathway IDs for the default organism. 
        
    :attr:`organism` must be set.
    ::

        k = Kegg()
        k.organism = "hsa"
        k.pathwayIDs

    """)
