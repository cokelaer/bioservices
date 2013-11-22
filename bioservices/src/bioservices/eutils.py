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
#$Id: kegg.py 156 2013-02-17 22:45:39Z cokelaer $
"""Interface to the EUtils web Service.

.. topic:: What is EUtils ?

    :STATUS: in progress. Some functionalities are implemented but not completed yet.

    :URL: http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
    :URL: http://www.ncbi.nlm.nih.gov/books/NBK25500/#chapter1.Demonstration_Programs
    :WSDL: http://www.ncbi.nlm.nih.gov/entrez/query/static/esoap_help.html

    .. highlights::

        The Entrez Programming Utilities (E-utilities) are a set of eight server-side programs that provide a stable interface into the Entrez query and database system at the National Center for Biotechnology Information (NCBI). The E-utilities use a fixed URL syntax that translates a standard set of input parameters into the values necessary for various NCBI software components to search for and retrieve the requested data. The E-utilities are therefore the structured interface to the Entrez system, which currently includes 38 databases covering a variety of biomedical data, including nucleotide and protein sequences, gene records, three-dimensional molecular structures, and the biomedical literature. 

       -- from http://www.ncbi.nlm.nih.gov/books/NBK25497/, March 2013

"""

from bioservices import WSDLService
from bioservices import RESTService


__all__ = ["EUtils"]

# Although the wsdl are different, the efetch address can be used indiferently
# so efetch_taxon can be used to request any sql
class EFetch(WSDLService):
    def __init__(self,verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_taxon.wsdl"
        super(EFetch, self).__init__(name="EUtilsTaxon", verbose=verbose, url=url)

    def efetch(self, db, Id):
        ret = self.serv.run_eFetch(db=db, id=Id)
        return ret

#class EUtilsPubmed(WSDLService):
#    def __init__(self,verbose=False):
#        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_taxon.wsdl"
#        super(EUtilsPubmed, self).__init__(name="EUtilsTaxon", verbose=verbose, url=url)
#
#    def run_eFetch(self, db, Id):
#        ret = self.serv.run_eFetch(db=db, id=Id)
#        return ret


class EUtilsTaxon(WSDLService):
    def __init__(self,verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_taxon.wsdl"
        super(EUtilsTaxon, self).__init__(name="EUtilsTaxon", verbose=verbose, url=url)

    def run_eFetch(self, db, Id):
        """run_eFetch 

        :param str db:
        :param str Id:
        """
        ret = self.serv.run_eFetch(db=db, id=Id)
        return ret

class EUtilsSNP(WSDLService):
    """

    ret = e.serv.run_eSummary(db="snp",id="7535")
    """
    def __init__(self, verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_snp.wsdl"
        super(EUtilsSNP, self).__init__(name="EUtilsSNP", verbose=verbose, url=url)

    def run_eFetch(self, Id):
        ret = self.serv.run_eFetch(id=Id)
        return ret

 
class EUtils(WSDLService):
    """Interface to `NCBI Entrez Utilities <http://www.ncbi.nlm.nih.gov/entrez/query/static/esoap_help.html>`_ service


    This class is not completed. However, you can already access to most of the
    E-utilities. What may be missing is optional keywords to EFecth and some
    other functions. The EPost is not implemented.

    .. warning:: Read the `guidelines
        <http://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ before sending requests.
        No more than 3 requests per seconds otherwise your IP may be banned.

    Here is an example on how to use EFetch to retrieve the FASTA sequence of a
    given ID (34577063)::

        >>> from bioservices import EUtils
        >>> s = EUtils()
        >>> s.EFetch("sequences", "34577063", retmode="text", rettype="fasta")
        >gi|34577063|ref|NP_001117.2| adenylosuccinate synthetase isozyme 2 [Homo sapiens]
        MAFAETYPAASSLPNGDCGRPRARPGGNRVTVVLGAQWGDEGKGKVVDLLAQDADIVCRCQGGNNAGHTV
        VVDSVEYDFHLLPSGIINPNVTAFIGNGVVIHLPGLFEEAEKNVQKGKGLEGWEKRLIISDRAHIVFDFH
        QAADGIQEQQRQEQAGKNLGTTKKGIGPVYSSKAARSGLRMCDLVSDFDGFSERFKVLANQYKSIYPTLE
        IDIEGELQKLKGYMEKIKPMVRDGVYFLYEALHGPPKKILVEGANAALLDIDFGTYPFVTSSNCTVGGVC
        TGLGMPPQNVGEVYGVVKAYTTRVGIGAFPTEQDNEIGELLQTRGREFGVTTGRKRRCGWLDLVLLKYAH
        MINGFTALALTKLDILDMFTEIKVGVAYKLDGEIIPHIPANQEVLNKVEVQYKTLPGWNTDISNARAFKE
        LPVNAQNYVRFIEDELQIPVKWIGVGKSRESMIQLF

    Most of the functions takes a database name as input. You can obtain the
    valid list by checking the :attr:`databases` attribute.

    A few functions takes Identifier(s) as input. It must be a string of one Id
    or several Ids, in which case they must be comma sperated without spaces::

        Incorrect: id=352, 25125, 234
        Correct:   id=352,25125,234

    A few functions takes an argument called **term**. You can use the **AND**
    keyword but spaces must be replaced by + signs::

        Incorrect: term=biomol mrna[properties] AND mouse[organism]
        Correct:   term=biomol+mrna[properties]+AND+mouse[organism]

    Other special characters, such as quotation marks (") or the # symbol used
    in referring to a query key on the History server, should be represented by
    their URL encodings (%22 for "; %23 for #).::

        Incorrect: term=#2+AND+"gene in genomic"[properties]
        Correct:   term=%232+AND+%22gene+in+genomic%22[properties]

    """
    def __init__(self, verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/eutils.wsdl?"
        super(EUtils, self).__init__(name="EUtils", verbose=verbose, url=url)


        self._databases = None
        # some extra links
        self._efetch_taxonomy = EUtilsTaxon(verbose=verbose)
        self._efetch_snp = EUtilsSNP(verbose=verbose)
        self._efetch = EFetch(verbose=verbose)
        self.tool = "bioservices"   # not used but may be used later on 
        self.email = "unknown"      # not used but may be used later on

    def _get_databases(self):
        """alias to run_eInfo"""
        if self._databases == None:
            self._databases = self.serv.run_eInfo().DbName
        return self._databases
    databases = property(_get_databases, doc="Returns list of valid databases")

    def taxonomy(self, Id):
        """Alias to EFetch for ther taxonomy database using WSDL

        ::

            >>> s = EUtils()
            >>> ret = s.taxonomy("9606")
            >>> ret.Taxon.TaxId
            '9606'
            >>> ret.Taxon.ScientificName
            'Homo sapiens'
            >>> ret = s.taxonomy("9606,9605,111111111,9604")
            >>> ret.Taxon[2].TaxId
            '9604'


        """
        ret = self._efetch_taxonomy.serv.run_eFetch(db="taxonomy", id=Id)
        return ret 

    def snp(self, Id):
        """Alias to Efetch for the SNP database using WSDL

        ::

            >>> s.snp("123")

        """
        ret = self._efetch_snp.run_eFetch(Id)
        return ret

    def EFetch(self, db, Ids, retmode="xml", **kargs):
        """Access to the EFetch E-Utilities

        :param str db: Database from which to retrieve UIDs. The value must be a valid Entrez database
            name . This is the destination database for the link operation. 
        :param str Ids: UID list. Either a single UID or a comma-delimited list of UIDs may be provided.
            All of the UIDs must be from the database specified by db. Limited  to 200 Ids

        ::

            >>> ret = s.EFetch("omim", "269840")  --> ZAP70
            
            >>> ret = s.EFetch("taxonomy", "9606")
            >>> [x.text for x in ret.getchildren()[0].getchildren() if x.tag=="ScientificName"]
            ['Homo sapiens']

            >>> s = eutils.EUtils()
            >>> s.EFetch("sequences", "34577063", retmode="text", rettype="fasta")
            >gi|34577063|ref|NP_001117.2| adenylosuccinate synthetase isozyme 2 [Homo sapiens]
            MAFAETYPAASSLPNGDCGRPRARPGGNRVTVVLGAQWGDEGKGKVVDLLAQDADIVCRCQGGNNAGHTV
            VVDSVEYDFHLLPSGIINPNVTAFIGNGVVIHLPGLFEEAEKNVQKGKGLEGWEKRLIISDRAHIVFDFH
            QAADGIQEQQRQEQAGKNLGTTKKGIGPVYSSKAARSGLRMCDLVSDFDGFSERFKVLANQYKSIYPTLE
            IDIEGELQKLKGYMEKIKPMVRDGVYFLYEALHGPPKKILVEGANAALLDIDFGTYPFVTSSNCTVGGVC
            TGLGMPPQNVGEVYGVVKAYTTRVGIGAFPTEQDNEIGELLQTRGREFGVTTGRKRRCGWLDLVLLKYAH
            MINGFTALALTKLDILDMFTEIKVGVAYKLDGEIIPHIPANQEVLNKVEVQYKTLPGWNTDISNARAFKE
            LPVNAQNYVRFIEDELQIPVKWIGVGKSRESMIQLF

        The alias :meth:`taxonomy` uses the WSDL and provides an easier way to manipulate
        the ouptut.

        .. note:: uses the REST service only

        .. todo:: more documentation and optional arguments
        """
        #self._check_db(db)
        self._check_retmode(retmode)
        self._check_ids(Ids)
        s = RESTService("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        request = "efetch.fcgi?db=%s&id=%s&retmode=%s" % (db, Ids, retmode)

        if kargs.get("strand"):
            strand = kargs.get("strand")
            if strand in [1,2]:
                request += "&strand=%s" % strand
            else:
                raise ValueError("invalid strand. must be a number in 1,2")

        if kargs.get("complexity"):
            strand = kargs.get("complexity")
            if strand in [0,1,2,3,4]:
                request += "&complexity=%s" % strand
            else:
                raise ValueError("invalid complexity. must be a number in 0,1,2,3,4")

        if kargs.get("seq_start"):
            request += "&seq_start=%s" % kargs.get("seq_start")
        if kargs.get("seq_stop"):
            request += "&seq_stop=%s" % kargs.get("seq_stop")

        if kargs.get("rettype"):
            print kargs.get("rettype")
            request += "&rettype=%s" % kargs.get("rettype")

        ret = s.request(request)

        return ret


    def EInfo(self, db=None, method="wsdl"):
        """Provides the number of records indexed in each field of a given
        database, the date of the last update of the database, and the available links
        from the database to other Entrez databases.

        :param str db: target database about which to gather statistics. Value must be a
            valid Entrez database name. See :attr:`databases` or don't provide
            db to get the list
        :return: statistics with XML format if method is "rest") or SOAP format
            if method is wsdl (default).

        ::

            >>> ret = s.EInfo("taxonomy")
            >>> ret.Count

        If method is xml, the output is in BeautifulSoup format::

            >>> ret = s.EInfo("taxonomy", method="rest")

        """
        if db == None:
            return self.databases
        else:
            self._check_db(db)

        if method=="wsdl":
            ret = self._einfo_wsdl(db)
        elif method == "rest":
            ret = self._einfo_rest(db)
        else:
            raise ValueError("method must be either wsdl or rest")
        return ret

    def _einfo_rest(self, db=None):
        s = RESTService("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        ret = s.request("einfo.fcgi?db=%s" % db)
        return ret

    def _einfo_wsdl(self, db=None):
        return self.serv.run_eInfo(db=db) 

    def _check_ids(self, Ids):
        if len(Ids.split(","))>200:
            raise ValueError("Number of comma separated IDs must be less than 200")

    def _check_db(self, db):
        if db not in self.databases:
            raise ValueError("You must provide a valid databases from : ", self.databases)

    def _check_retmode(self, retmode):
        if retmode not in ["xml", "text"]:
            raise ValueError("You must provide a retmode in 'xml', 'test'")

    def ESummary(self, db, Ids, method="wsdl"):
        """document summary downloads 

        Returns document summaries (DocSums) for a list of input UIDs
        OR returns DocSums for a set of UIDs stored on the Entrez History server

        :param str Ids: UID list. Either a single UID or a comma-delimited list of UIDs may be provided.
            All of the UIDs must be from the database specified by db. Limited  to 200 Ids

        ::

            >>> from bioservices import *
            >>> s = EUtils()
            >>> ret = s.ESummary("snp","7535")
            >>> ret = s.ESummary("snp","7535,7530")
            >>> ret = s.ESummary("taxonomy", "9606,9913")

        .. warning:: the query_key, WebEnv, restart, retmax, and version options
            are not yet implemented.
        """
        self._check_ids(Ids)
        if db == None:
            return self.databases
        else:
            self._check_db(db)

        if method=="wsdl":
            ret = self._esummary_wsdl(db, Ids)
        elif method == "rest":
            ret = self._esummary_rest(db, Ids)
        else:
            raise ValueError("method must be either wsdl or rest")
        return ret

    def _esummary_rest(self, db, Ids):
        # [(x.attrib['Name'], x.text) for x in ret.getchildren()[0].getchildren()[1:]]
        s = RESTService("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        ret = s.request("esummary.fcgi?db=%s&id=%s" % (db, Ids))
        return ret

    def _esummary_wsdl(self, db, Ids):
        ret = self.serv.run_eSummary(db=db, id=Ids)
        return ret

    def EGquery(self, term, retmode="xml", method="wsdl"):
        """Provides the number of records retrieved in all Entrez databases by a single text query.

        :param str term: Entrez text query. All special characters must be URL
            encoded. Spaces may be replaced by '+' signs. For very long queries (more than
            several hundred characters long), consider using an HTTP POST call. See the
            PubMed or Entrez help for information about search field descriptions and tags.
            Search fields and tags are database specific.

        ::

            >>> ret = s.EGquery("asthma")
            >>> [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem if x.Count!='0']

        .. note:: WSDL (default) and REST protocol available
        .. todo:: documentation and optional arguments
        """
        self._check_retmode(retmode)
        if method == "wsdl":
            ret = self._egquery_wsdl(term, retmode)
        elif method == "rest":
            ret = self._egquery_rest(term, retmode)
        else:
            raise ValueError("method must be either wsdl or rest")
        return ret

    def _egquery_rest(self, term, retmode="xml"):
        self._check_retmode(retmode)
        s = RESTService("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        ret = s.request("egquery.fcgi?term=%s&retmode=%s" % (term, retmode))
        return ret

    def _egquery_wsdl(self, term, retmode="xml"):
        """retmode does not seem to work in the wsdl case"""
        self._check_retmode(retmode)
        if retmode == "xml":
            ret = self.serv.run_eGquery(term=term, retmode="xml")
        else:
            ret = self.serv.run_eGquery(term=term)
        return ret


    def ESpell(self, db, term):
        """Provides spelling suggestions for terms within a single text query in a given database.

        :param str db: database to search. Value must be a valid Entrez database name (default = pubmed).
        :param str term: Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the PubMed or Entrez help for information about search field descriptions and tags. Search fields and tags are database specific.


        ::

            >>> ret = e.ESpell(db="omim", term="aasthma+OR+alergy")
            >>> ret.Query
            'asthmaa OR alergies'
            >>> ret.CorrectedQuery
            'asthma or allergy'

        .. note:: only WSDL protocol available 
        """
        self._check_db(db)
        ret = self.serv.run_eSpell(db=db, term=term)
        return ret


    def ELink(self, db, dbfrom, Ids, cmd="neighbor"):
        """The Entrez links utility

        Responds to a list of UIDs in a given database with either a list of
        related UIDs (and relevancy scores) in the same database or a list of linked
        UIDs in another Entrez database; checks for the existence of a specified link
        from a list of one or more UIDs; creates a hyperlink to the primary LinkOut
        provider for a specific UID and database, or lists LinkOut URLs and attributes
        for multiple UIDs.

        :param str db: Database from which to retrieve UIDs. The value must be a valid Entrez database
            name. This is the destination database for the link operation.
        :param str dbfrom: Database containing the input UIDs. The value must be a
            valid Entrez database name (default = pubmed). This is the origin database of
            the link operation. If db and dbfrom are set to the same database value, then
            ELink will return computational neighbors within that database. Please see the
            full list of Entrez links for available computational neighbors. Computational
            neighbors have linknames that begin with dbname_dbname (examples:
            protein_protein, pcassay_pcassay_activityneighbor).
        :param str Ids: UID list. Either a single UID or a comma-delimited list of UIDs may be provided.
            All of the UIDs must be from the database specified by db. Limited  to 200 Ids
        :param str cmd: ELink command mode. The command mode specified which
            function ELink will perform. Some optional parameters only function for certain
            values of cmd (see http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink).
            Examples are neighbor, prlinks.

        :: 

            >>> # Example: Find related articles to PMID 20210808
            >>> ret = s.ELink("pubmed", "pubmed", Ids="20210808", cmd="neighbor_score")


        """
        self._check_ids(Ids)
        self._check_db(db)
        self._check_db(dbfrom)
        assert cmd in ["neighbor", "neighbor_score", "neighbor_history",
"acheck", "llinks", "lcheck", "ncheck", "llinkslib" ,"prlinks"]

        s = RESTService("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")

        request = "elink.fcgi?db=%s&dbfrom=%s" % (db, dbfrom)
        request += "&id=%s" % Ids
        request += "&cmd=%s" % cmd
        ret = s.request(request)
        return ret

    def EPost(self):
        """Not implemented.

        """
        raise NotImplementedError

