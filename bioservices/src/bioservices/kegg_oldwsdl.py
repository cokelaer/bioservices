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
#$Id: kegg.py 55 2013-01-11 17:17:31Z cokelaer $
"""This module provides a class :class:`~Kegg` that allows an easy access to all the
WDSL Kegg interface as well as additional methods to obtain statistics about the
Kegg database. See below for details about the functionalities available and the
tutorial/quickstart :ref:`kegg_tutorial`.

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


Functions/methods
-------------------

In addition to all Kegg API methods (see :meth:`~bioservices.kegg.Kegg.methods`),
we provide additional functionalities:

.. autosummary::

    bioservices.kegg.Kegg.analyse
    bioservices.kegg.Kegg.lookfor_specy
    bioservices.kegg.Kegg.lookfor_pathway
    bioservices.kegg.Kegg.lookfor_organism
    bioservices.kegg.Kegg.extra_pathway_summary
    bioservices.kegg.Kegg.extra_get_all_relations
    bioservices.kegg.Kegg.extra_get_pathway_types
    bioservices.kegg.Kegg.extra_get_elements_by_pathway

"""


from services import WSDLService
import webbrowser
import copy


class Items(object):
    """Simple class to ease access to some data in the Kegg database


    Used to access to organisms and databases. Could be extended for the
    pathways

    ::

            k = Kegg()
            k.organisms
            k.organisms.items
            k.organisms.entry_id
            k.organisms.definition

    """

    def __init__(self, data, name="items", verbose=True):
        self.verbose = verbose
        self.name = name

        self._items = copy.deepcopy(data)

    def _get_definitions(self):
        ids = [x['definition'] for x in self.items]
        return ids
    definitions = property(_get_definitions, doc="return list of definition")

    def _get_entry_ids(self):
        ids = [x['entry_id'] for x in self.items]
        return ids
    entry_ids = property(_get_entry_ids, doc="return list of Ids")

    def _get_items(self):
        return self._items
    items = property(_get_items, doc=_get_items.__doc__)

    def lookfor(self, query):
        """Search for a pattern in the items

        :param str query: can be an id, a word

        case insensitive
        """
        matches = []
        for i, item in enumerate(self.definitions):
            if query.lower() in item.lower():
                matches.append(i)
        for i, item in enumerate(self.entry_ids):
            if query.lower() in item.lower():
                matches.append(i)
        return [(self.definitions[i], self.entry_ids[i]) for i in matches]

    def __str__(self):
        txt = ""
        txt += "%60s || %s\n" % ("Definition", "ID")
        txt += "="*80 + "\n"
        for x,y in zip(self.definitions, self.entry_ids):
            txt +=  "%60s || %s\n" % (x,y)
        return txt 



class Kegg(WSDLService):
    """Interface to the `KEGG <http://www.genome.jp/kegg/pathway.html>`_ database

    ::

        import kegg
        k = kegg.Kegg()
        k.methods
        k.bget("hsa:7535")

        print len(k.pathways)

        k.organism #hsa (homo sapiens by default)

        .. warning:: unfortunately, the WSDL sevices is closed since 31st Dec 2012

    """
    _url = "http://soap.genome.jp/KEGG.wsdl"
    def __init__(self, verbose=True):
        """Constructor

        :param bool verbose:

        """
        import logging
        logging.warning("unfortunately, the WSDL sevices is closed since 31st Dec 2012")
        """super(Kegg, self).__init__(name="Kegg", url=Kegg._url, verbose=verbose)
        self._pathways = {}
        self._buffer = {}
        self._relations = {}

        self._mapping = None
        self._organism = 'hsa'
        self.debug = debug
        if self.debug: 
            self.info()

        if self.verbose:
            print "Fetching databases and organisms..."
        self.databases = Items(self.serv.list_databases(), "databases", self.verbose)
        self.organisms = Items(self.serv.list_organisms(), "organisms", self.verbose)
        """

    def _check_pathway_id(self, pathway_id):
        pids = [x.entry_id for x in self.pathways]
        if pathway_id not in pids:
            if len(self.bget(pathway_id))==0:
                print "%s pathway if cannot be found" % pathway_id
                raise Exception



    def info(self):
        """For debugging. 

        prints the WSDL service methods not yet wrapped."""
        methods = self.methods[:]
        for m in methods:
            if m not in Kegg.__dict__.keys():
                print "%s not part of the methods but can be access through server attribute" % m
                # self.__setattr__(m, self.serv.__getattr__(m)) # this code
                # makes it available, but we must first call the
                # self.server.method to allow self.method to work...

    def _set_organism(self, organism):
        if organism in self.organisms.entry_ids:
            self._organism = organism
        else:
            raise Exception("%s organism not valid. See organisms attribute" % organism)
    def _get_organism(self):
        return self._organism
    organism = property(_get_organism, _set_organism, 
        doc="read/write attribute for the organism")


    def get_pathways_by_genes(self, gene_id):
        """Returns pathways that contains the gene_id

        :param str gene_id: a valid **gene_id**

        call WSDL
        """
        if isinstance(gene_id, str):
            res = self.serv.get_pathways_by_genes([gene_id])
        else:
            res = self.serv.get_pathways_by_genes(list(gene_id))
        return res

    def get_pathways_by_reactions(self, reactions_list):
        """

        """
        if isinstance(reactions_list, str):
            res = self.serv.get_pathways_by_reactions([reactions])
        else:
            res = self.serv.get_pathways_by_reactions(list(reactions))
        return res

    def get_pathways_by_compounds(self, compounds_list):
        """Search all pathways which include all the given compounds.

        ::

            >>> k.serv.get_pathways_by_compounds(['cpd:C00076', 'cpd:C00165', 'cpd:C01245'])
        """
        return k.serv.get_pathways_by_compounds(compounds_list)

    def get_pathways_by_enzymes(self, enzymes_list):
        """Search all pathways which include all the given enzymes.

        :param list enzymes_list:

        """
        if isinstance(enzymes_list, str):
            res = self.serv.get_pathways_by_enzynes([enzymes_list])
        else:
            res = self.serv.get_pathways_by_enzymes(list(enzymes_list))
        return res

    def get_pathways_by_drugs(self, drugs_list):
        """Search all pathways which include all the given drugs.

        :param list enzymes_list:

        """
        if isinstance(drugs_list, str):
            res = self.serv.get_pathways_by_drugs([drugs_list])
        else:
            res = self.serv.get_pathways_by_drugs(list(drugs_list))
        return res

    def get_pathways_by_glycans(self, glycans_list):
        """Search all pathways which include all the given glycans.

        """
        if isinstance(glycans_list, str):
            res = self.serv.get_pathways_by_glycans([glycans_list])
        else:
            res = self.serv.get_pathways_by_glycans(list(glycans_list))
        return res

    def get_pathways_by_kos(self, kos_list):
        """Retrieve all pathways of the organisms which include all the given KO IDs.

        """
        if isinstance(kos_list, str):
            res = self.serv.get_pathways_by_kos([kos_list])
        else:
            res = self.serv.get_pathways_by_kos(list(kos_list))
        return res


    def get_compounds_by_pathway(self, pathway_id):
        """Search all compounds on the specified pathway.

        :param str pathway_id: a valid pathway id

        ::

            >>>        k.get_compounds_by_pathway(pathway_id)
            ['cpd:C00076', 'cpd:C00165', 'cpd:C01245']
        """
        self._check_pathway_id(pathway_id)
        res = self.serv.get_compounds_by_pathway(pathway_id)
        return res


    def get_drugs_by_pathway(self, pathway_id):
        """Search all drugs on the specified pathway.

        :param str pathway_id: a valid pathway id

        """
        self._check_pathway_id(pathway_id)
        res = self.serv.get_drugs_by_pathway(pathway_id)
        return res

    def get_glycans_by_pathway(self, pathway_id):
        """Search all glycans on the specified pathway.

        :param str pathway_id: a valid pathway id
        """
        self._check_pathway_id(pathway_id)
        return self.serv.get_glycans_by_pathway(pathway_id)

    def get_enzymes_by_pathway(self, pathway_id):
        """Retrieve all enzymes on the specified pathway.

        :param str pathway_id: a valid pathway id
        """
        self._check_pathway_id(pathway_id)
        return self.serv.get_enzymes_by_pathway(pathway_id)

    def get_linked_by_pathway(self, linked):
        """

        :param str pathway_id: a valid pathway id
        """
        self._check_pathway_id(pathway_id)
        return self.serv.get_linked_by_pathway(pathway_id)



    def binfo(self, db=None, verbose=True):
        """show information of the latest GenBank database

        :param str db: name of a specific database. default is None (fetch all DBs)
        :param bool verbose: print the results

        ::

            results = k.binfo("gb", verbose=True)
        """
        if db==None:
            res = self.serv.binfo()
            print res
        else:
            res = self.serv.binfo(db)
            print res
        return res

    def bget(self, entry_id):
        """returns complete information about an entry_id

        ::
            
            # Retrieve the human gene with 7535
            res = k.bget("hsa:7535")
            # retrieve two KEGG/GENES entries
            bget("eco:b0002 hin:tRNA-Cys-1")
            # retrieve nucleic acid sequences in a FASTA format
            bget("-f -n n eco:b0002 hin:tRNA-Cys-1")
            # retrieve amino acid sequence in a FASTA format
            bget("-f -n a eco:b0002")

        """
        assert type(entry_id)==str or type(entry_id)==list
        if type(entry_id) != list:
            return self.serv.bget(entry_id)
        else:
            results = []
            for e in entry_id:
                res = self.serv.bget(e)
                results.append(res)
            return results

    def bfind(self, request):
        """Searches entries by keywords. 

        User need to specify a database from those which are supported by
        DBGET system before keywords. Number of keywords given at a time is restricted
        up to 100.
    
        :param str request: a string that specifies a database. Number of 
            keywords must be less than 100
        :return: string

        ::

            # Returns the IDs and definitions of entries which have definition
            # including the word 'E-cadherin' and 'human' from GenBank.
            k = Kegg()
            k.bfind("gb E-cadherin human")

        """
        return self.serv.bfind(request)


    def btit(self, request):
        """btit is used for retrieving the definitions by given database entries. 

        Number of entries given at a time is restricted up to 100.

        :param str request: a string contains valid DB entries
        :return: string

        ::

            # Returns the ids and definitions of four GENES entries "hsa:1798",
            # "mmu:13478", "dme:CG5287-PA" and cel:Y60A3A.14".
            k.btit("hsa:1798")

        """
        return self.serv.btit(request)



    def get_number_of_genes_by_organism(self, organism=None):
        if organism == None:
            organism = self.organism
        if organism not in self.organisms.entry_ids:
            raise Exception("invalid organism id. See organism_ids attribute.")

        if organism in self._buffer.keys():
            return self._buffer[organism]['N']
        else:
            N = self.serv.get_number_of_genes_by_organism(organism)
            self._buffer[organism] = {'N': N}
            return N

    def list_pathways(self, organism=None):

        if organism == None:
            return self.serv.list_pathways(self.organism)
        else:
            return self.serv.list_pathways(organism)

    def _get_pathways(self):
        """Returns names of the organisms supported by KEGG databases

        ::

            k = Kegg()
            k.pathways()
            k.list_pathways()
        """
        if self.organism not in self._pathways.keys():
            if self.verbose:
                print "fetching pathways...",
            res = self.serv.list_pathways(self.organism)
            self._pathways[self.organism] = res
            if self.verbose:
                print "ok"
        return self._pathways[self.organism]
    pathways = property(_get_pathways)




    def bconv(self, entry_ids):
        """Given a gene identifier, the functions queries KEGG to retrieve the appropriate KEGG ID.

        The bconv command converts external IDs to KEGG IDs. Currently, following
        external databases are available.

        :param list entry_ids: ids can be a list of strings or a single string where ids are separated by spaces

        ::

            >>> print k.bconv("ncbi-gi:10047086 uniprot:P43403")
            ncbi-gi:10047086    hsa:54206   equivalent
            up:P43403   hsa:7535    equivalent
            >>> print k.bconv(["ncbi-gi:10047086", "uniprot:P43403"])
            ncbi-gi:10047086    hsa:54206   equivalent
            up:P43403   hsa:7535    equivalent


        Note that the original Kegg API works with a unique string. However, we
        also implemented a way to provide a list of strings.


        """
        if isinstance(entry_ids, list)==True:
            request = " ".join([x for x in entry_ids])
        else:
            request = entry_ids[:]
        return self.serv.bconv(request)



    def retrieveKGML(self, pathway_id="05210", organism="hsa", filename="test.xml", 
            format=None):
        """Return URL of a pathway


        :param str pathway_id: just the id, not the organism !
        :param str organism: 
        :param str filename: 
        :param str format: e.g., kgml 
            

        http://www.genome.jp/dbget-bin/show_pathway?hsa05210


        """
        self._check_pathway_id(":".join(["path", organism+ pathway_id]))

        if format == None:
            url = "http://www.genome.jp/dbget-bin/show_pathway?%s%s" 
            url = url % (organism, pathway_id)
        elif format == "KGML" or format == "kgml":
            url = "http://www.genome.jp/kegg-bin/download?entry=%s%s&format=kgml"
            url = url % (organism, pathway_id)
        else:
            raise NotImplementedError("only kgml format implemented")
        return url


    def analyse(self, entry_id, type="gene"):
        """Analyse the contents returned by :meth:`bget`

        :param str entry_id: a valid **entry_id** identifier
        :param str type: default is "gene"
        :return: a dictionary with NAME/DESCRIPTION/PATHWAY keys found in the
            output of bget method.

        Example::

            >>> k = Kegg()
            >>> k.analyse("hsa:7535")
            {'DEFINITION': 'zeta-chain (TCR) associated protein kinase 70kDa (EC:2.7.10.2)',
             'NAME': ['ZAP70', 'SRK', 'STD', 'TZK', 'ZAP-70'],
             'PATHWAY': ['hsa04064  NF-kappa B signaling pathway',
              'hsa04650  Natural killer cell mediated cytotoxicity',
              'hsa04660  T cell receptor signaling pathway',
              'hsa05340  Primary immunodeficiency']}


        .. note:: only the type "gene" is implemented so far. The gene case
            analyse only a subset of the returned data string to extract the
            names or description and pathways.

        """
        if type=="gene": 
            data = self.bget_buffer(entry_id)
            return self._analyse_gene(data)
        else:
            raise NotImplementedError

    def bget_buffer(self, entry_id):
        """Same as bget but buffers the results.


        """
        if entry_id not in self._buffer:
            data = self.bget(entry_id)
            self._buffer[entry_id] = data
        return self._buffer[entry_id]

    def _analyse_gene(self, data):
        output = {}
        try:
            names = [x for x in data.split("\n") if x.startswith("NAME")][0]
            names = names.split("NAME")[1].strip()
            names = [x.strip() for x in names.split(",")]
            output['NAME'] = names
        except:
            pass

        try:
            # we can also use get_pathways_by_gene()
            output['PATHWAY'] = [x.strip() for x in data.split("PATHWAY")[1].split("\n") if x.strip().startswith("hsa")]
        except:
            pass

        try:
            defi = [x.strip() for x in data.split("\n") if x.startswith("DEFINITION")]
            defi = defi[0].split("DEFINITION")[1].strip()

            output['DEFINITION'] = defi
        except:
            pass

        return output


    def get_genes_by_motifs(self, genes, start, max_results):
        """Onbtain the names of genes that contain the motifs


        Given a set of motif ids, the function searches the databases implied by the motif ids for genes
        containing the motifs specified by the motif ids

        :param genes: list of character strings for the ids of the motifs that are conserved by genes across organisms
        :param int start: location of the entry in the query results from which the results will be extracted and returned
        :param int max_results: maximum number of entries that will be extracted from the query results and returned


        KEGG seems to have two ways of defining the ids for motifs. One is the motif ids obtained through
        get.motifs.by.gene, where pfam, tfam, pspt, pspf are used for the Pfam, TIGRFAM, PROSITE
        pattern, and PROSITE profile database, respectively and for the first part of a motif id (e. g.
        pfam:aakinase). Another is the motif ids used to query the databases for genes that contain the
        motif, where only the first two letters of the abbreviations for databases form the first part of a motif
        id (e. g. pf:aakinase)



        :return: The function returns a named vector with the names of the vector being the
            textual definition of genes and values of the vector being the ids used by KEGG 
            to represent genes.

        ::

            k = Kegg():
            k.serv.get_genes_by_motifs(["pf:DnaJ", "ps:DNAJ_2"], 1, 10)


        :source: KEGGSOAP for the doc

        """

        return self.serv.get_genes_by_motifs(genes, start, max_results)

    def get_genes_by_organism(self, organism="hsa", start=1, max_results=1e9):
        """Obtain list of genes for a given organism


        :param str organism: id used by KEGG for organisms. The organism
            ids are normally three-letter codes with the first letter being the first letter
            of the genus name and the rest being the first two letters of the species name of the
            scientic name of the organism of concern
        :param int start: location of the entry in the query results from which the results will be extracted and returned
        :param int max_results: maximum number of entries that will be extracted from the query results and returned


        :return: list of ids used by KEGG ro represent genes

        """
        if organism in self._buffer.keys():
            if "genes" in self._buffer[organism].keys():
                return self._buffer[organism]['genes']
            else:
                res = self.serv.get_genes_by_organism(organism, start, max_results)
                self._buffer[organism] = {'genes':res, 'N': len(res)}
        else:
            res = self.serv.get_genes_by_organism(organism, start, max_results)
            self._buffer[organism] = {'genes':res, 'N': len(res)}
        return res


    def get_genes_by_pathway(self, pathway):
        self._check_pathway_id(pathway)
        if pathway.startswith("path:")==False:
            raise Exception("pathway must start with 'path:'")
        return self.serv.get_genes_by_pathway(pathway)



    def _get_Npathways(self):
        if self._pathways == None:
            org = self.pathways
        N = len([x['entry_id'] for x in self.pathways])
        return N
    Npathways = property(_get_Npathways, doc="nmber of pathways in the current orgamism (read-only)")


    def __str__(self):
        verbose = self.verbose
        self.verbose = False
        self.get_number_of_genes_by_organism(self.organism)
        txt = "Kegg database summary:\n"
        txt+= "  Number of organisms: %s\n"  % len(self.organisms.items)
        txt+= "  Number of pathways(%s): %s\n"  % (self.organism, self.Npathways)
        txt+= "  Number of genes(%s): %s\n"  % (self.organism, self._buffer[self.organism]['N'])

        for o in self._genes.keys():
            txt += " Number of genes (%s): %s" %(o, self._buffer[o]['N'])
        self.verbose = verbose
        return txt



    def get_reactions_by_pathway(self, pathway_id):
        """

        k.get_reactions_by_pathway('path:eco00260')
        k.get_reactions_by_pathway("path:hsa00010")

        """
        self._check_pathway_id(pathway_id)
        return self.serv.get_reactions_by_pathway(pathway_id)

    def get_kos_by_pathway(self, pathway_id):
        self._check_pathway_id(pathway_id)
        # Returns all ko_ids on the pathway map 'path:hsa00010'
        return self.serv.get_kos_by_pathway(pathway_id)



    def color_pathway_by_elements(self, pathway, element_id_list=[],
            fg_color_list=[], bg_color_list=[], show=True):
        """Show the pathway image in a browser with colored elements


        Color the elements (rectangles and circles on a pathway map)
        corresponding to the given **element_id_list** with the specified colors and
        return the URL of the colored image. 

        :param list element_id_list: list of elements ids to color (ids can be
            found from :meth:`get_elements_by_pathway`.
        :param list fg_color_list: the color of text and border of the elements
        :param list bg_color_list: the background color of the elements. 
        :param bool show: show the result in a browser

        This method is useful to specify which graphical object on the pathway to be
        colored as there are some cases that multiple genes are assigned to one
        rectangle or a gene is assigned to more than one rectangle on the pathway map.


        For more details on KGML, see: `<http://www.kegg.jp/kegg/soap/doc/keggapi_manual.html#label:33>`_
    
        ::

            # Returns the URL of the colored image of given pathway 'path:bsu00010' with
            # * gene bsu:BG11350 (element_id 78, ec:3.2.1.86) colored in red on yellow
            # * gene bsu:BG11203 (element_id 79, ec:3.2.1.86) colored in blue on yellow
            # * gene bsu:BG11685 (element_id 51, ec:2.7.1.2)  colored in red on orange
            # * gene bsu:BG11685 (element_id 47, ec:2.7.1.2)  colored in blue on orange
            element_id_list = [ 78, 79, 51, 47 ]
            fg_list  = [ '#ff0000', '#0000ff', '#ff0000', '#0000ff' ]
            bg_list  = [ '#ffff00', '#ffff00', '#ffcc00', '#ffcc00' ]
            k.color_pathway_by_elements('path:bsu00010', element_id_list, fg_list, bg_list)

        """
        assert len(fg_color_list)==len(element_id_list)
        assert len(bg_color_list)==len(element_id_list)

        res = self.serv.color_pathway_by_elements(pathway, element_id_list, fg_color_list, bg_color_list)
        print res
        if res and show==True:
            webbrowser.open(res)

    def color_pathway_by_objects(self, pathway, objects_id_list=[],
            fg_color_list=[], bg_color_list=[], show=True):
        """Show the pathway image in a browser with colored elements

        Same as :meth:`color_pathway_by_elements` but working with names
        instead of element_ids.

        """
        assert len(fg_color_list)==len(objects_id_list)
        assert len(bg_color_list)==len(objects_id_list)

        res = self.serv.color_pathway_by_objects(pathway,objects_id_list, fg_color_list, bg_color_list)
        print res
        if res and show==True:
            webbrowser.open(res)

    def mark_pathway_by_objects(self, pathway, objects_id_list=[], show=True):
        """Mark the given objects on the given pathway map and return the URL of the generated image."""
        res = self.serv.mark_pathway_by_objects(pathway,objects_id_list)
        print res
        if res and show==True:
            webbrowser.open(res)

    def get_html_of_marked_pathway_by_objects(self, pathway, objects_id_list=[],
            show=True):
        """HTML version of the :meth:`~pathways.kegg.Kegg.mark_pathway_by_objects` method. """
        res = self.serv.get_html_of_marked_pathway_by_objects(pathway,objects_id_list)
        print res
        if res and show==True:
            webbrowser.open(res)


    def get_html_of_colored_pathway_by_elements(self, pathway,
            element_id_list=[], fg_color_list=[], bg_color_list=[], show=True):
        """HTML version of the :meth:`~pathways.kegg.Kegg.color_pathway_by_elements` method. """
        assert len(fg_color_list)==len(element_id_list)
        assert len(bg_color_list)==len(element_id_list)

        res = self.serv.get_html_of_colored_pathway_by_elements(pathway, element_id_list, fg_color_list, bg_color_list)
        print res
        if res and show==True:
            webbrowser.open(res)

    def get_html_of_colored_pathway_by_objects(self, pathway,
            objects_id_list=[], fg_color_list=[], bg_color_list=[], show=True):
        """HTML version of the :meth:`~pathways.kegg.Kegg.color_pathway_by_objects` method. """
        assert len(fg_color_list)==len(objects_id_list)
        assert len(bg_color_list)==len(objects_id_list)

        res = self.serv.get_html_of_colored_pathway_by_objects(pathway, objects_id_list, fg_color_list, bg_color_list)
        if res and show==True:
            webbrowser.open(res)




    def get_references_by_pathway(self, pathway_id):
        """todo"""
        return self.serv.get_references_by_pathway(pathway_id)

    def view_reference(self, pathway_id):
        from browse.browser import browse
        browse("http://www.ncbi.nlm.nih.gov/pubmed/" + str(pathway_id))

    def view_all_references_by_pathway(self, pathway_id, maxtabs=10):
        """open all pubmed reference for a given pathway

        not in Kegg WSDL
        """
        refs = self.get_references_by_pathway(pathway_id)
        if len(refs)>maxtabs:
            print("%s references found. Openning only the first 10 tabs. change maxtabs if needed" % len(refs))
        for r in refs[0:min(maxtabs, len(refs))]:
            print r
            self.view_reference(r)


    def get_elements_by_pathway(self, pathway_id):
        elements = self.serv.get_elements_by_pathway(pathway_id)
        return elements

    def get_element_relations_by_pathway(self, pathway_id):
        """

        buffering
        """
        if self.organism in self._relations.keys():
            if pathway_id in self._relations[self.organism]:
                return self._relations[self.organism][pathway_id]
            else:
                relations = self.serv.get_element_relations_by_pathway(pathway_id)
                self._relations[self.organism][pathway_id] = relations
        else:
            self._relations[self.organism] = {}
            relations = self.serv.get_element_relations_by_pathway(pathway_id)
            self._relations[self.organism][pathway_id] = relations
        return self._relations[self.organism][pathway_id]




    def get_pathways_by_specy(self, specy):
        print "This will take a while since we are analysing all entries"
        results = self.lookfor(specy)
        print results

        pws = self.get_pathways_by_genes(gene)
        return pws
        

    def build_specy_ids_mapping(self, rebuild=False):
        """Build Mapping between genes IDs and thei description.

        :param bool rebuild: force the rebuild of the mapping. (default is False)

        Take a while. Saved in :attr:`_mapping` attribute.

        """
        print("Retrieving all genes for organism %s" % self.organism)
        genes = self.get_genes_by_organism()
        maxRequests = 100
        d = {}
        N = len(genes)
        calls = N/maxRequests

        entry = 0
        print("Building dictionary mapping Kegg id to description (names). Takes about 5 minutes depeding on organism")
        for i in range(0, calls):
            print("Analysing pathways %s/%s" % (i, calls))
            subgenes = genes[i*maxRequests:(i+1)*maxRequests]
            data = self.btit(" ".join([x for x in subgenes])).split("\n")
            for this in data:
                print this
                if len(this)>0:
                    keggid, description = this.split(" ", 1)
                    d[entry] = {'keggid':keggid, 'description': description}
                    entry+=1

        subgenes = genes[calls*maxRequests:]
        data = self.btit(" ".join([x for x in subgenes])).split("\n")
        for this in data:
            if len(this)>0:
                keggid, description = this.split(" ", 1)
                d[entry] = {'keggid':keggid, 'description': description}
                entry+=1

        self._mapping = d.copy()
        return self._mapping 

    def get_linked_pathways(self, pathway):
        return self.serv.get_linked_pathways(pathway)


    # SDDB related
    # =========================================
    def get_best_best_neighbors_by_gene(self, genes_id, offset=0, limit=10):
        """Search best-best neighbor of the gene in all organisms."""
        return self.serv.get_best_best_neighbors_by_gene(genes_id, offset, limit)

    def get_best_neighbors_by_gene(self, genes_id, offset=0, limit=10):
        """Search best neighbors in all organism."""
        return self.serv.get_best_neighbors_by_gene(genes_id, offset, limit)

    def get_reverse_best_neighbors_by_gene(self, genes_id, offset=0, limit=10):
        """Search reverse best neighbors in all organisms.

        ::

            >>> k.get_reverse_best_neighbors_by_gene('eco:b0002', 1, 10)

        """
        return self.serv.get_reverse_best_neighbors_by_gene(genes_id, offset, limit)

    def get_paralogs_by_gene(self, genes_id, offset=0, limit=10):
        """"Search paralogous genes of the given gene in the same organism."""
        return self.serv.get_paralogs_by_gene(genes_id, offset, limit)

    # KO related
    # =========================================
    def get_genes_by_ko(self, kid, org=None):
        """Returns all genes corresponding to this ko id (all organism)"""
        if org ==None:
            org = self.organism
            return self.serv.get_genes_by_ko(kid, org)
        else:
            return self.serv.get_genes_by_ko(kid)
    def get_ko_by_gene(self, gid):
        return self.serv.get_ko_by_gene(gid)
    def get_genes_by_ko_class(self, classid, org, offset, limit):
        return self.serv.get_genes_by_ko_class(classid)
    def get_ko_by_ko_class(self, classid, org, offset, limit):
        return self.serv.get_ko_by_ko_class(self, classid)


    # LIGAND related
    def search_drugs_by_name(self, drug):
        """Returns a list of drugs having the specified name.

        :param str drug: drug name
        :return: drug_id

        :: 

            k.search_drugs_by_name("tetracyclin")
        """
        return self.serv.search_drugs_by_name(drug)
    def search_drugs_by_mass(self, mass, error):
        return self.serv.search_drugs_by_mass(mass, error)

    # HERE BELOW ARE IMPROVED FUNCTIONS NEW TO KEGG WSDL INTERFACE


    
    def extra_get_elements_by_pathway_and_type(self, pathway_id, type="gene"):
        """Same as :meth:`~pathways.kegg.Kegg.get_elements_by_pathway` with type selection.

        :param pathway_id: valid pathway id
        :param str type: (Default gene)


        """
        self._check_pathway_id(pathway_id)
        elts_ids = self.get_elements_by_pathway(pathway_id)
        return [e for e in elts_ids if e['type']==type]

    def view_pathways(self, pathways=[], genes_ids=[], requires_all=False):
        """show a pathway in your browser.

        pattern can be a valid pathway id or a list of genes that must be
        contained in the pathway


        """

        # pathways must be a list but if only one pathway, users may provide a
        # string, so we need to convert it:
        if len(pathways) != 0:
            if isinstance(pathways, list) == False and isinstance(pathways, str):
                pathways = [pathways]

        if isinstance(genes_ids, list)==False:
            raise Exception("genes_ids must be a list")
        # look for pathways that contains genes_ids
        if len(pathways) == 0:
            for g in genes_ids:
                newpws = self.get_pathways_by_genes(g)

                if requires_all==False:
                    pathways.extend(newpws)
                else:
                    if len(pathways) == 0:
                        pathways = newpws
                    else:
                        newpws = set(newpws)
                        pathways = set(pathways).intersection(newpws)
            pathways = list(set(pathways))
            print "Found %s pathways" %len(pathways)
        else:
            pass


        print pathways

        for p in pathways:
            print "showin pathway", p
            element_ids = []
            for g in genes_ids:
                print " -- fetching id", p, g
                element = self._get_element_id_by_pathway(p, g)
                if element:
                    element_ids.append(element)
            print element_ids
            bg =["red"] * len(element_ids)
            fg =["white"] * len(element_ids)
            self.color_pathway_by_elements(p, element_ids, bg, fg)
            import time
            time.sleep(1)

    def _get_element_id_by_pathway(self, pathway_id, gene=None):
        elements = self.get_elements_by_pathway(pathway_id)
        if gene == None:
            return elements
        else:
            for e in elements:
                if gene in e['names']:
                    return e['element_id']

    def get_sif(self, pathway_id):
        """Export a pathway in SIF format

        .. note:: experimental, not to be used.


        """
        elements = self.extra_get_elements_by_pathway_and_type(pathway_id, type="gene")
        relations = self.get_element_relations_by_pathway(pathway_id)

        print "ok"
        for r in relations:
            print r
            link = r['subtypes'][0]
            print link
            (id1, id2) = r['element_id1'], r['element_id2']
            print("==========")
            #if id1 not in elements['element_id']:
            #    print "id1 %s not found" %id1
            #if id2 not in elements['element_id']:
            #    print "id2 %s not found" %id2

            print 'test'
            if link['relation'] == 'activation':
                print id1, 1, id2
            elif  link['relation'] == 'inibition':
                print id1, -1, id2
            else:
                print "#", id1, link['relation'], id2


    def load_mapping(self, filename=None):
        """Load a pickle of the buffered genes save by :meth:`~pathways.kegg.Kegg.save_kegg_names`

        :param str filename: a pickled file (can be zipped; see note below)

        Can be a zipped file but the zip archive must have been built as follows::

            zip archive.dat.zip archive.dat

        In other word, we expect to find a file inside the archive that has the
        name **archive.dat**

        """
        import pickle

        if filename.endswith("zip"):

            import zipfile, os
            # read the zip file given the full filename
            fh = zipfile.ZipFile(filename)
            # assuming the filename ending in zip is the same file that we want
            # to access to in the archive. First, get the filename without path
            filename = os.path.split(filename)[1]
            # second, get rid of extension
            filename = filename.split(".zip")[0]
            # Finally, extract the file
            data = fh.read(filename)
            # and since it should be a pickle, load it.
            self._mapping = pickle.loads(data)  # note use loads method NOT load 
        else:
            self._mapping = pickle.load(open(filename, "r"))

    def save_mapping(self, filename):
        """Save a pickle of the genes attribute in a file.

        """
        import pickle
        pickle.dump(self._mapping, open(filename, "w"))

    def lookfor_organism(self, query):
        return self.organisms.lookfor(query)

    def lookfor_specy(self, pattern):
        """Search for a specy in the gene database

        Specy are stored according to their Kegg id. In general, 
        one look for a specy given its usual name (e.g., LAT, ZAP70, ...)

        This function allows to search for a Kegg id given a name. 

        It takes a long time to search the database that way. So, we built a 
        dictionary that is stored within the package. 

        Otherwise, if you want to use the latests database, you can call::

            k.build_specy_ids_mapping()

        before hand.

        :return: list of tuples containing keggid and their corresponding
            description.
        """
        if self._mapping == None:
            import os
            filename = "kegg-hsa-gene_mapping_oct_2012.dat.zip"
            print "!! Reversed dictionary of names/genes is empty."
            print "\tLoading %s from the library" % filename
            print "\tYou can rebuild the dictionary (and save it) that way "
            print "\t >>> self.build_specy_ids_mapping()"
            print """\t >>> self.save_mapping("test.dat")"""
            print "\t and reload it before calling that function"
            print """\t >>> self.load_mapping("test.dat")"""
            from easydev import get_shared_directory_path
            db = get_shared_directory_path("pathways")
            self.load_mapping(db + os.sep + "data" +os.sep + filename)

        found = [v for k,v in self._mapping.iteritems() if pattern.lower() in v['description'].lower()]
        if self.verbose:
            print found
        return found


    def extra_get_all_relations(self, Nmax=None):
        """Returns all relations found in all pathways

        :param int Nmax: max number of pathways to look at.

        .. todo:: Takes a while to complete. Could save the results in a pickle.

        Output to be used by :meth:`~pathways.kegg.Kegg.extra_count_relations`

        """
        all_relations = []
        if Nmax == None:
            Nmax = len(self.pathways)
        pids = [p['entry_id'] for p in self.pathways[0:Nmax]]
        for i,pathway_id in enumerate(pids):
            print "processing %s/%s (%s)" % (i+1, Nmax, pathway_id)
            all_relations.append(self.get_element_relations_by_pathway(pathway_id))
        return all_relations


    def extra_count_relations(self, all_relations):
        """Returns number of relations in a dictionary 

        :param all_relations: output of :meth:`~pathways.kegg.Kegg.extra_get_all_relations`

        :return: dictionary of number of relations for each relation category.
        """
        counter = {}
        for relations in all_relations:
            these_relations = [r['subtypes'][0]['relation'] for r in relations if len(r['subtypes'])]
            for this in these_relations:
                if this not in counter.keys():
                    counter[this] = 1
                else:
                    counter[this] = counter[this] + 1
        return counter

    def info_database(self):
        """prints the databases definition and entry IDs

        .. seealso:: :meth:`list_databases`"""
        for x in self.list_databases:
            print("%50s: %s" %(  x['definition'], x['entry_id']))


    def extra_pathway_summary(self, pathway_id, show=True):
        """A tentative of pathway summary

        """
        assert pathway_id in [x['entry_id'] for x in self.pathways]
        # get genes of the pathway
        genes_ids = self.get_genes_by_pathway(pathway_id)
        # get information for each gene (e.g., name that appear in the image)
        names = []
        for i, gid in enumerate(genes_ids):
            print "analysing genes %s (%s out of %s)" % (gid, i, len(genes_ids))
            self.analyse(gid)
            #names.append(self.analyse(gid)['NAME']

        if show:
            self.view_pathways(pathway_id)

        # pathways contained in the pathway itself
        print "===========\nPathways contained in this pathway:\n\n"
        pids = [x for x in self.extra_get_elements_by_pathway_and_type(pathway_id, type="map")]
        for pathway_id in pids:
            results = self.lookfor_pathway(pathway_id['names'][0])
            for res in results:
                print(" *"+ res.definition+" "+ res.entry_id)

    def extra_get_pathway_types(self, pathway_id):
        """Return types found in a given pathway

        :param str pathway_id:


        """
        types = [x['type'] for x in self.get_elements_by_pathway(pathway_id)]
        return set(types)




    def extra_get_elements_by_pathway(self, pathway_id):
        """Returns elements id from a pathway (and more)

        :param str pathway_id:

        Given a pathway, this function returns a dictionary with the element_id,
        type, components and usual name of the elements found in the pathway.

        """
        elements = self.get_elements_by_pathway(pathway_id)
        d = {}
        for e in elements: 
            usual_names = []
            for name in e['names']:
                res = self.analyse(name)
                if 'NAME' in res.keys():
                    usual_names.append(res['NAME'])
            d[e['element_id']] = {'names': e['names'], 
                'type': e['type'],
                'components': e['components'],
                'usual_names': usual_names}
        return d


    def _extra_get_gene_element_id(self, pathway_id):
        """Given a pathway, returns elements type

        :param str pathway_id:
        """
        elements = self.get_elements_by_pathway(pathway_id)
        d = {}
        for e in elements: 
            if e['type'] == 'gene':
                for name in e['names']:
                    d[name] = e['element_id']
        return d



    def lookfor_pathway(self, query):
        """Search for a pathway in the databases

        :param str query: can be an id, a word

        case insensitive

        ::
    
            >>> k.lookfor_pathway("hsa:04604")

        """
        pathways = []
        for item in self.pathways:
            if query.lower() in item['definition'].lower():
                pathways.append(item)
            if query.lower() in item['entry_id'].lower():
                pathways.append(item)
        return pathways 



