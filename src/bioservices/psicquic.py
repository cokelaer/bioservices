#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EMBL-EBI
#
#  File author(s): 
#      
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id$
"""Interface to the PSICQUIC web service

.. topic:: What is PSICQUIC ?

    :URL: http://code.google.com/p/psicquic/
    :REST: http://code.google.com/p/psicquic/wiki/PsicquicSpec_1_3_Rest

    .. highlights::

        "PSICQUIC is an effort from the HUPO Proteomics Standard Initiative
        (HUPO-PSI) to standardise the access to molecular interaction databases
        programmatically. The PSICQUIC View web interface shows that PSICQUIC
        provides access to 25 active service "

        -- Dec 2012


.. _about_queries:

About queries
================

.. rubric:: source: PSICQUIC View web page

The idea behind PSICQUIC is to retrieve information related to protein
interactions from various databases. Note that protein interactions does not
necesseraly mean protein-protein interactions. In order to be effective, the
query format has been standarised. 

To do a search you can use the Molecular Interaction Query Language which is
based on Lucene's syntax. Here are some rules 

* Use OR or space ' ' to search for ANY of the terms in a field
* Use AND if you want to search for those interactions where ALL of your terms are found
* Use quotes (") if you look for a specific phrase (group of terms that must
  be searched together) or terms containing special characters that may otherwise
  be interpreted by our query engine (eg. ':' in a GO term)
* Use parenthesis for complex queries (e.g. '(XXX OR YYY) AND ZZZ')
* Wildcards (`*`,?) can be used between letters in a term or at the end of terms to do fuzzy queries,
   but never at the beginning of a term. 
* Optionally, you can prepend a symbol in front of your term.
    *  + (plus): include this term. Equivalent to AND. e.g. +P12345
    *  - (minus): do not include this term. Equivalent to NOT. e.g. -P12345
    *    Nothing in front of the term. Equivalent to OR. e.g. P12345
* Implicit fields are used when no field is specified (simple search). For
  instance, if you put 'P12345' in the simple query box, this will mean the same
  as identifier:P12345 OR pubid:P12345 OR pubauth:P12345 OR species:P12345 OR
  type:P12345 OR detmethod:P12345 OR interaction_id:P12345

About the MITAB output
=========================

The output returned by a query contains a list of entries. Each entry is
formatted following the MITAB output. 

Here below are listed the name of the field returned ordered as they would
appear in one entry. The first item is always idA whatever version of MITAB is
used. The version 25 of MITAB contains the first 15 fields in the table below.
Newer version may incude more fields but always include the 15 from MITAB 25 in
the same order.  See the link from **irefindex** 
`about mitab <http://irefindex.uio.no/wiki/README_MITAB2.6_for_iRefIndex_8.0#What_each_line_represents>`_
for more information.

=============== =========================================== =============== ======================
Field Name      Searches on                                 Implicit*       Example
=============== =========================================== =============== ======================
idA             Identifier A                                No              idA:P74565
idB             Identifier B                                No              idB:P74565
id              Identifiers (A or B)                        No              id:P74565
alias           Aliases (A or B)                            No              alias:(KHDRBS1 HCK)
identifiers     Identifiers and Aliases undistinctively     Yes             identifier:P74565
pubauth         Publication 1st author(s)                   Yes             pubauth:scott
pubid           Publication Identifier(s) OR                Yes             pubid:(10837477 12029088)
taxidA          Tax ID interactor A: the tax ID or 
                the species name                            No              taxidA:mouse
taxidB          Tax ID interactor B: the tax ID or 
                species name                                No              taxidB:9606
species         Species. Tax ID A or Tax ID B               Yes             species:human
type            Interaction type(s)                         Yes             type:"physical interaction"
detmethod       Interaction Detection method(s)             Yes             detmethod:"two hybrid*"
interaction_id  Interaction identifier(s)                   Yes             interaction_id:EBI-761050
pbioroleA       Biological role A                           Yes             pbioroleA:ancillary
pbioroleB       Biological role B                           Yes             pbioroleB:"MI:0684"
pbiorole        Biological roles (A or B)                   Yes             pbiorole:enzyme
ptypeA          Interactor type A                           Yes             ptypeA:protein
ptypeB          Interactor type B                           Yes             ptypeB:"gene"
ptype           Interactor types (A or B)                   Yes             pbiorole:"small molecule"
pxrefA          Interactor xref A (or Identifier A)         Yes             pxrefA:"GO:0003824"
pxrefB          Interactor xref B (or Identifier B)                         Yes pxrefB:"GO:0003824"
pxref           Interactor xrefs (A or B or Identifier 
                A or Identifier B)                          Yes             pxref:"catalytic activity"
xref            Interaction xrefs (or Interaction 
                identifiers)                                Yes             xref:"nuclear pore"
annot           Interaction annotations and tags            Yes             annot:"internally curated"
udate           Update date                                 Yes             udate:[20100101 TO 20120101]
negative        Negative interaction boolean                Yes             negative:true
complex         Complex expansion                           Yes             complex:"spoke expanded"
ftypeA          Feature type of participant A               Yes             ftypeA:"sufficient to bind"
ftypeB          Feature type of participant B               Yes             ftypeB:mutation
ftype           Feature type of participant A or B          Yes             ftype:"binding site"
pmethodA        Participant identification method A         Yes             pmethodA:"western blot"
pmethodB        Participant identification method B         Yes             pmethodB:"sequence tag identification"
pmethod         Participant identification methods
                 (A or B)                                   Yes             pmethod:immunostaining 
stc             Stoichiometry (A or B). Only true or 
                false, just to be able to filter 
                interaction having stoichiometry available  Yes             stc:true
param           Interaction parameters. Only true or 
                false, just to be able to filter 
                interaction having parameters available     Yes             param:true
=============== =========================================== =============== ======================



"""

from bioservices import REST, UniProt


#http://code.google.com/p/psicquic/wiki/PsicquicSpec_1_3_Rest

#http://www.biocatalogue.org/services/2078#operations

__all__ = ["PSICQUIC"]


class PSICQUIC(REST):
    """Interface to the `PSICQUIC <http://code.google.com/p/psicquic/>`_ service

    There are 2 interfaces to the PSICQUIC service (REST and WSDL) but we used
    the REST only.


    This service provides a common interface to more than 25 other services
    related to protein. So, we won't detail all the possiblity of this service.
    Here is an example that consists of looking for interactors of the
    protein ZAP70 within the IntAct database::

        >>> from bioservices import *
        >>> s = PSICQUIC()
        >>> res = s.query("intact", "zap70")
        >>> len(res) # there are 11 interactions found
        11
        >>> for x in res[1]: 
        ...     print(x)
        uniprotkb:O95169
        uniprotkb:P43403
        intact:EBI-716238
        intact:EBI-1211276
        psi-mi:ndub8_human(display_long)|uniprotkb:NADH-ubiquinone oxidoreductase ASHI
        .
        .

    Here we have a list of entries. There are 15 of them (depending on
    the *output* parameter). The meaning of the entries is described on PSICQUIC
    website: https://code.google.com/p/psicquic/wiki/MITAB25Format . In short:

    
    #. Unique identifier for interactor A
    #. Unique identifier for interactor B.
    #. Alternative identifier for interactor A, for example the official gene
    #. Alternative identifier for interactor B.
    #. Aliases for A, separated by "|
    #. Aliases for B.
    #. Interaction detection methods, taken from the corresponding PSI-MI
    #. First author surname(s) of the publication(s) 
    #. Identifier of the publication 
    #. NCBI Taxonomy identifier for interactor A. 
    #. NCBI Taxonomy identifier for interactor B.
    #. Interaction types, 
    #. Source databases and identifiers, 
    #. Interaction identifier(s) i
    #. Confidence score. Denoted as scoreType:value. 



    Another example with reactome database::

        res = s.query("reactome", "Q9Y266")


    .. warning:: PSICQUIC gives access to 25 other services. We cannot create
        a dedicated parsing for all of them. So, the ::`query` method returns
        the raw data. Addition class may provide dedicated parsing in the
        future.

    .. seealso:: :class:`bioservices.biogrid.BioGRID`
    """

    _formats = ["tab25", "tab26", "tab27", "xml25", "count", "biopax", "xgmml",
        "rdf-xml", "rdf-xml-abbrev", "rdf-n3", "rdf-turtle"]


    # note the typo in "genbank indentifier from bind DB
    _mapping_uniprot = {"genbank indentifier": "P_GI",
        'entrezgene/locuslink':"P_ENTREZGENEID",
        'uniprotkb': "ACC+ID",
        'rcsb pdb':"PDB_ID",
        'ensembl':"ENSEMBL_ID",
        'refseq':"P_REFSEQ_AC",
        'hgnc':'HGNC_ID',
        "kegg": "KEGG_ID",
        "entrez gene/locuslink": "P_ENTREZGENEID",
        "chembl": "CHEMBL_ID",
        "ddbj/embl/genbank": "EMBL_ID",
        "dip": "DIP_ID",
        "ensemblgenomes": "ENSEMBLGENOME_ID",
        "omim":"MIM_ID",
        "chebi": None,
        "chembl": None,
        #        "intact": None
        }

    # unknown: hprd, omim, bind, bind complexid, mdl, 

    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages

        .. doctest:: 

            >>> from bioservices import PSICQUIC
            >>> s = PSICQUIC()

        """
        urlStr = 'http://www.ebi.ac.uk/Tools/webservices/psicquic'
        super(PSICQUIC, self).__init__("PSICQUIC", verbose=verbose, url=urlStr)
        self._registry = None

        try:
            self.uniprot = UniProt(verbose=False)
        except:
            self.logging.warning("UniProt service could be be initialised")
        self.buffer = {}

    def _get_formats(self):
        return PSICQUIC._formats
    formats = property(_get_formats, doc="Returns the possible output formats")

    def _get_active_db(self):
        names = self.registry_names[:]
        actives = self.registry_actives[:]
        names = [x.lower() for x,y in zip(names, actives) if y=="true"]
        return names
    activeDBs = property(_get_active_db, doc="returns the active DBs only")

    def read_registry(self):
        """Reads and returns the active registry 

        """
        url = 'registry/registry?action=ACTIVE&format=txt'
        res = self.http_get(url, frmt='txt')
        return res.split()

    def print_status(self):
        """Prints the services that are available

        :return: Nothing

        The output is tabulated. The columns are:

        * names
        * active
        * count
        * version
        * rest URL
        * soap URL
        * rest example
        * restricted

        .. seealso:: If you want the data into lists, see all attributes
            starting with registry such as :meth:`registry_names`
        """
        url = 'registry/registry?action=STATUS&format=xml'
        res = self.http_get(url, frmt="txt")

        names = self.registry_names
        counts = self.registry_counts
        versions = self.registry_versions
        actives = self.registry_actives
        resturls = self.registry_resturls
        soapurls = self.registry_soapurls
        restexs = self.registry_restexamples
        restricted = self.registry_restricted
        N = len(names)

        indices = sorted(range(0,N), key=lambda k: names[k])

        for i in range(0,N):
            print("%s\t %s\t %s\t %s\t %s %s %s %s\n" % (names[i], actives[i], 
                counts[i], versions[i], resturls[i], soapurls[i], restexs[i], restricted[i]))


    # todo a property for the version of PISCQUIC

    def _get_registry(self):
        if self._registry is None:
            url = 'registry/registry?action=STATUS&format=xml'
            res = self.http_get(url, frmt="xml")
            res = self.easyXML(res)
            self._registry = res
        return self._registry
    registry = property(_get_registry, doc="returns the registry of psicquic")

    def _get_registry_names(self):
        res = self.registry
        return [x.findAll('name')[0].text for x in res.findAll("service")]
    registry_names = property(_get_registry_names, 
            doc="returns all services available (names)")

    def _get_registry_restricted(self):
        res = self.registry
        return [x.findAll('restricted')[0].text for x in res.findAll("service")]
    registry_restricted = property(_get_registry_restricted, 
            doc="returns restricted status of services")

    def _get_registry_resturl(self):
        res = self.registry
        data = [x.findAll('resturl')[0].text for x in res.findAll("service")]
        return data
    registry_resturls = property(_get_registry_resturl, 
            doc="returns URL of REST services")

    def _get_registry_restex(self):
        res = self.registry
        data = [x.findAll('restexample')[0].text for x in res.findAll("service")]
        return data
    registry_restexamples = property(_get_registry_restex, 
            doc="retuns REST example for each service")

    def _get_registry_soapurl(self):
        res = self.registry
        return  [x.findAll('soapurl')[0].text for x in res.findAll("service")]
    registry_soapurls = property(_get_registry_soapurl, 
            doc="returns URL of WSDL service")

    def _get_registry_active(self):
        res = self.registry
        return  [x.findAll('active')[0].text for x in res.findAll("service")]
    registry_actives = property(_get_registry_active, 
            doc="returns active state of each service")

    def _get_registry_count(self):
        res = self.registry
        return  [x.findAll('count')[0].text for x in res.findAll("service")]
    registry_counts = property(_get_registry_count, 
            doc="returns number of entries in each service")

    def _get_registry_version(self):
        res = self.registry
        names = [x.findAll('name')[0].text for x in res.findAll("service")]
        N = len(names)
        version = [0] * N
        for i in range(0,N):
            x = res.findAll("service")[i]
            if x.findAll("version"):
                version[i] = x.findAll("version")[0].text
            else:
                version[i] = None 
        return  version
    registry_versions = property(_get_registry_version, 
            doc="returns version of each service")

    def query(self, service, query, output="tab25", version="current", firstResult=None, maxResults=None):
        """Send a query to a specific database 

        :param str service: a registered service. See :attr:`registry_names`.
        :param str query: a valid query. Can be `*` or a protein name.
        :param str output: a valid format. See s._formats

        ::

            s.query("intact", "brca2", "tab27")
            s.query("intact", "zap70", "xml25")
            s.query("matrixdb", "*", "xml25")

        This is the programmatic approach to this website:

        http://www.ebi.ac.uk/Tools/webservices/psicquic/view/main.xhtml


        Another example consist in accessing the *string* database for fetching 
        protein-protein interaction data of a particular model organism. Here we
        restrict the query to 100 results::

            s.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25")

        # spaces are automatically converted

            s.query("biogrid", "ZAP70 AND species:9606")

        .. warning:: AND must be in big caps. Some database are ore permissive
            than other (e.g., intact accepts "and"). species must be a valid ID number. Again, some DB are more
            permissive and may accept the name (e.g., human)

        To obtain the number of interactions in intact for the human specy:: 

            >>> len(p.query("intact", "species:9606"))


        """
        if service not in self.activeDBs:
            raise ValueError("database %s not in active databases" % service)

        params = {}
        if output is not None:
            self.devtools.check_param_in_list(output, self.formats)
            params['format'] = output
        else: output="none"

        names = [x.lower() for x in self.registry_names]
        try:
            index = names.index(service)
        except ValueError:
            print("The service you gave (%s) is not registered. See self.registery_names" % service)
            raise ValueError

        # get the base url according to the service requested
        resturl = self.registry_resturls[index]

        if firstResult is not None:
            params['firstResult'] = firstResult
        if maxResults is not None:
            params['maxResults'] = maxResults

        url = resturl  + 'query/' + query

        if "xml" in output:
            res = self.http_get(url, frmt="xml", params=params)
        else:
            res = self.http_get(url, frmt="txt", params=params)
            print(res)
            res = res.strip().split("\n")

        if output.startswith("tab"):
            res = self._convert_tab2dict(res)

        return res


    def _convert_tab2dict(self, data):
        """

        https://code.google.com/p/psicquic/wiki/MITAB26Format
        """
        results = []
        for line in data:
            results.append(line.split("\t"))

        return results


    def queryAll(self, query, databases=None, output="tab25", version="current", firstResult=None, maxResults=None):
        """Same as query but runs on all active database

        :param list databases: database to query. Queries all active DB if not provided
        :return: dictionary where keys correspond to databases and values to the output of the query.

        ::

            res = s.queryAll("ZAP70 AND species:9606")
        """

        results = {}
        if databases is None:
            databases = [x.lower() for x in self.activeDBs]

        for x in databases:
            if x not in self.activeDBs:
                raise ValueError("database %s not in active databases" % x)


        for name in databases:
            self.logging.warning("Querying %s" % name),
            res = self.query(name, query, output=output, version=version, firstResult=firstResult, maxResults=maxResults)
            if output.startswith("tab25"):
                results[name] = [x for x in res if x!=[""]]
            else:
                import copy
                results[name] = copy.copy(res)
        for name in databases:
            self.logging.info("Found %s in %s" % (len(results[name]), name))
        return results



    def getInteractionCounter(self, query):
        """Returns a dictionary with database as key and results as values

        :param str query: a valid query
        :return: a dictionary which key as database and value as number of entries 

        Consider only the active database.

        """
        # get the active names only
        activeDBs = self.activeDBs[:] 
        res = [(str(name), int(self.query(name, query, output="count")[0])) for name in activeDBs]
        return dict(res)

    def getName(self, data):
        idsA = [x[0] for x in data]
        idsB = [x[1] for x in data]
        return idsA, idsB

    def knownName(self, data):
        """Scan all entries (MITAB) and returns simplified version


        Each item in the input list of mitab entry
        The output is made of 2 lists corresponding to 
        interactor A and B found in the mitab entries.

        elements in the input list takes the following forms::

            DB1:ID1|DB2:ID2
            DB3:ID3

        The | sign separates equivalent IDs from different databases. 

        We want to keep only one. The first known databae is kept. If in the list of DB:ID pairs no known
        database is found, then we keep the first one whatsover.

        known databases are those available in the uniprot mapping tools. 

        chembl and chebi IDs are kept unchanged.


        """


        self.logging.info("converting data into known names")
        idsA = [x[0].replace("\"","") for x in data]
        idsB = [x[1].replace("\"", "") for x in data]
        # extract the first and second ID but let us check if it is part of a
        # known uniprot mapping.Otherwise no conversion will be possible.
        # If so, we set the ID to "unknown"
        # remove the " character that can be found in a few cases (e.g,
        # chebi:"CHEBI:29036")
        #idsA = [x.replace("chebi:CHEBI:","chebi:") for x in idsA]
        #idsB = [x.replace("chebi:CHEBI:", "chebi:") for x in idsB]

        # special case:
        # in mint, there is an entry that ends with a | uniprotkb:P17844|
        idsA = [x.strip("|") for x in idsA]
        idsB = [x.strip("|") for x in idsB]


        # the first ID
        for i, entry in enumerate(idsA):
            try:
                dbs = [x.split(":")[0] for x in entry.split("|")]
                IDs = [x.split(":")[1] for x in entry.split("|")]
                valid_dbs = [(db,ID) for db,ID in zip(dbs,IDs) if db in self._mapping_uniprot.keys()]
                # search for an existing DB
                if len(valid_dbs)>=1:
                    idsA[i] = valid_dbs[0][0] + ":" + valid_dbs[0][1]
                else:
                    self.logging.debug("none of the DB for this entry (%s) are available" % (entry))
                    idsA[i] = "?" + dbs[0] + ":" + IDs[0]
            except:
                self.logging.info("Could not extract name from %s" % entry)
                idsA[i] = "??:" + entry  # we add a : so that we are sure that a split(":") will work
        # the second ID
        for i, entry in enumerate(idsB):
            try:
                dbs = [x.split(":")[0] for x in entry.split("|")]
                IDs = [x.split(":")[1] for x in entry.split("|")]
                valid_dbs = [(db,ID) for db,ID in zip(dbs,IDs) if db in self._mapping_uniprot.keys()]
                # search for an existing DB
                if len(valid_dbs)>=1:
                    idsB[i] = valid_dbs[0][0] + ":" + valid_dbs[0][1]
                else:
                    self.logging.debug("none of the DB (%s) for this entry are available" % (entry))
                    idsB[i] = "?" + dbs[0] + ":" + IDs[0]
            except:
                self.logging.info("Could not extract name from %s" % entry)
                idsB[i] = "??:" + entry

        countA = len([x for x in idsA if x.startswith("?")])
        countB = len([x for x in idsB if x.startswith("?")])
        if countA+countB > 0:
            self.logging.warning("%s ids out of %s were not identified" % (countA+countB, len(idsA)*2))
            print(set([x.split(":")[0] for x in idsA if x.startswith("?")]))
            print(set([x.split(":")[0] for x in idsB if x.startswith("?")]))
        self.logging.info("knownName done")
        return idsA, idsB

    def preCleaning(self, data):
        """remove entries ehre IdA or IdB is set to "-"

        """
        ret = [x for x in data if x[0] !="-" and x[1]!="-"]
        return ret

    def postCleaningAll(self,data, keep_only="HUMAN", flatten=True, verbose=True):
        """
    
        even more cleaing by ignoring score, db and interaction
        len(set([(x[0],x[1]) for x in retnew]))
        """
        results = {}
        for k in data.keys():
            self.logging.info("Post cleaning %s" % k)
            ret = self.postCleaning(data[k], keep_only="HUMAN", verbose=verbose)
            if len(ret):
                results[k] = ret
        if flatten:
            results = [x for k in results.keys() for x in results[k]]
        return results

    def postCleaning(self, data, keep_only="HUMAN", remove_db=["chebi","chembl"], 
        keep_self_loop=False, verbose=True):
        """Remove entries with a None and keep only those with the keep pattern

        """
        if verbose:print("Before removing anything: ", len(data))

        data = [x for x in data if x[0] is not None and x[1] is not None]
        if verbose:print("After removing the None: ", len(data))
    
        data = [x for x in data if x[0].startswith("!")is False and x[1].startswith("!")is False]
        if verbose:print("After removing the !: ", len(data))

    
        for db in remove_db:
            data = [x for x in data if x[0].startswith(db)is False]
            data = [x for x in data if x[1].startswith(db)is False]
            if verbose:print("After removing entries that match %s : " % db, len(data))

        data = [x for x in data if keep_only in x[0] and keep_only in x[1]]
        if verbose:print("After removing entries that don't match %s : " % keep_only, len(data))
    
        if keep_self_loop is False:
            data = [x for x in data if x[0]!=x[1]]
            if verbose:print("After removing self loop : ", len(data))

        data = list(set(data))
        if verbose:print("After removing identical entries", len(data))



        return data


    def convertAll(self, data):
        results = {}
        for k in data.keys():
            self.logging.info("Analysing %s" % k)
            results[k] = self.convert(data[k], db=k)
        return results

    def convert(self, data, db=None):
        self.logging.debug("converting the database %s" % db)
        idsA, idsB = self.knownName(data)
        mapping = self.mappingOneDB(data)
        results = []
        for i, entry in enumerate(data):
            x = idsA[i].split(":",1)[1]
            y = idsB[i].split(":",1)[1]
            xp = mapping[x]
            yp = mapping[y]
            try:ref = entry[8]
            except:ref="?"
            try:score = entry[14]
            except:score = "?"
            try:interaction = entry[11]
            except:interaction="?"
            results.append((xp, yp, score, interaction, ref, db))
        return results


    def mappingOneDB(self, data):
        query = {}
        self.logging.debug("converting IDs with proper DB name (knownName function)")
        entriesA, entriesB = self.knownName(data) # idsA and B contains list of a single identifier of the form db:id
        # the db is known from _mapping.uniprot otherwise it is called "unknown"

        # get unique DBs to build the query dictionary
        dbsA = [x.split(":")[0] for x in entriesA]
        dbsB = [x.split(":")[0] for x in entriesB]
        for x in set(dbsA):
            query[x] = set()
        for x in set(dbsB):
            query[x] = set()
        for k in query.keys():
            if k.startswith("?"):
                del query[k]

        # the data to store
        mapping = {}
        N = len(data)

        # scan all entries
        counter = 0
        for entryA, entryB in zip(entriesA, entriesB):
            counter += 1
            dbA, idA = entryA.split(":")
            try:
                dbB, idB = entryB.split(":")
            except:
                print(entryB)
            if idA not in mapping.keys():
                if dbA.startswith("?"):
                    mapping[idA] = entryA
                else:
                    query[dbA].add(idA)
            if idB not in mapping.keys():
                if dbB.startswith("?"):
                    mapping[idB] = entryB
                else:
                    query[dbB].add(idB)

            for k in query.keys():
                if len(query[k])>2000 or counter == N:
                    this_query = list(query[k])
                    DBname = self._mapping_uniprot[k]

                    if DBname is not None:
                        self.logging.warning("Request sent to uniprot for %s database (%s/%s)" % (DBname, counter, N))
                        res = self.uniprot.mapping(fr=DBname, to="ID", query=" ".join(this_query))
                        for x in this_query:
                            if x not in res: #was not found
                                mapping[x] = "!" + k+":"+x
                            else:
                                # we should be here since the queries are populated
                                # if not already in the mapping dictionary
                                if x not in res.keys():
                                    raise ValueError(x)
                                if len(res[x])==1:
                                    mapping[x] = res[x][0]
                                else:
                                    self.logging.warning("psicquic mapping found more than 1 id. keep first one")
                                    mapping[x] = res[x][0]
                    else:
                        for x in this_query:
                            mapping[x] = k + ":" + x
                    query[k] = set()

        for k in query.keys():
            assert len(query[k])==0
        return mapping




class AppsPPI(object):
    """This is an application based on PPI that search for relevant interactions

    Interctions between proteins may have a score provided by each database.
    However, scores are sometimes ommited. Besides, they may have different
    meaning for different databases. Another way to score an interaction is to
    count in how many database it is found.

    This class works as follows. First, you query a protein:


        p = AppsPPI()
        p.query("ZAP70 AND species:9606")

    This, is going to call the PSICQUIC queryAll method to send this query to
    all active databases. Then, it calls the convertAll functions to convert all
    interactors names into uniprot name if possible. If not, interactions are
    not taken into account. Finally, it removes duplicated and performs some
    cleaning inside the postCleaningall method.

    Then, you can call the summary method that counts the interactions. The
    count is stored in the attrbiute relevant_interactions.

        p.summary()

    Let us see how many intercations where found with. THe number of databases
    that contains at least one interactions is 

        >>> p.N
        >>> p.relevant_interactions[N]
        [['ZAP70_HUMAN', 'DBNL_HUMAN']]

    So, there was 1 interaction found in all databases.

    """
    def __init__(self, verbose=False):
        """.. rubric:: constructor"""
        self.psicquic = PSICQUIC(verbose=False)
        self.verbose = verbose

    def queryAll(self, query, databases=None):
        """

        :param str query: a valid query. See :class:`~bioservices.psicquic.PSICQUIC` 
            and :mod:`bioservices.psicquic` documentation.
        :param str databases: by default, queries are sent to each active database.
            you can overwrite this behavious by providing your own list of
            databses
        :return: nothing but the interactions attributes is populated with a
            dictionary where keys correspond to each database that returned a non empty list
            of interactions. The item for each key is a list of interactions containing the
            interactors A and B, the score, the type of intercations and the score.


        """
        #self.results_query = self.psicquic.queryAll("ZAP70 AND species:9606")
        print("Requests sent to psicquic. Can take a while, please be patient...")
        self.results_query = self.psicquic.queryAll(query, databases)
        self.interactions = self.psicquic.convertAll(self.results_query)
        self.interactions = self.psicquic.postCleaningAll(self.interactions,
            flatten=False, verbose=self.verbose)
        self.N = len(self.interactions.keys())
        self.counter = {}
        self.relevant_interactions = {}

    def summary(self):
        """Build some summary related to the found interactions from queryAll

        :return: nothing but the relevant_interactions and counter attribute

            p = AppsPPI()
            p.queryAll("ZAP70 AND species:9606")
            p.summary()

        """
        for k,v in self.interactions.items():
            print("Found %s interactions within %s database" % (len(v), k))

        counter = {}
        for k in self.interactions.keys():
            # scan each dabase
            for v in self.interactions[k]:
                interaction = v[0] + "++" + v[1]
                db = v[5]
                if interaction in counter.keys():
                    counter[interaction].append(db)
                else:
                    counter[interaction] = [db]
        for k in counter.keys():
            counter[k] = list(set(counter[k]))

        N = len(self.interactions.keys())

        print("-------------")
        summ = {}
        for i in range(1, N+1):
            res = [(x.split("++"),counter[x]) for x in counter.keys() if len(counter[x]) == i]
            print("Found %s interactions in %s common databases" % (len(res), i))
            res = [x.split("++") for x in counter.keys() if len(counter[x]) == i]
            if len(res):
                summ[i] = [x for x in res]
            else:
                summ[i] = []

        self.counter = counter.copy()
        self.relevant_interactions = summ.copy() 



    def get_reference(self, idA, idB):
        key = idA+"++"+idB
        uniq = len(self.counter[key])
        ret = [x for k in self.interactions.keys() for x in self.interactions[k] if x[0]==idA and x[1]==idB]
        N = len(ret)
        print("Interactions %s -- %s has %s entries in %s databases (%s):" %
                (idA, idB, N, uniq, self.counter[key]))
        for r in ret:
            print(r[5], " reference", r[4])


    def show_pie(self):
        """a simple example to demonstrate how to visualise number of
        interactions found in various databases

        """
        try:
            from pylab import pie, clf, title, show, legend
        except ImportError:
            from bioservices import BioServicesError
            raise BioServicesError("You must install pylab/matplotlib to use this functionality")
        labels = range(1, self.N + 1)
        print(labels)
        counting = [len(self.relevant_interactions[i]) for i in labels]


        clf()
        #pie(counting, labels=[str(int(x)) for x in labels], shadow=True)
        pie(counting, labels=[str(x) for x in counting], shadow=True)
        title("Number of interactions found in N databases")
        legend([str(x) + " database(s)" for x in labels])
        show()
