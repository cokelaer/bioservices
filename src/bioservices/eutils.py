# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
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
# $Id$
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
from bioservices import REST


__all__ = ["EUtils"]


#DONE

"""
EINFO
ESEARCH
ESummary
EGQuery
EPost

"""
# source:
# http://www.dalkescientific.com/writings/diary/archive/2005/09/30/using_eutils.html

# http://blog.tremily.us/posts/entrez/



# Although the wsdl are different, the efetch address can be used indiferently
# so efetch_taxon can be used to request any sql
class EFetch(WSDLService):
    def __init__(self, database, verbose=False):
        """database could be e.g. taxon, snp

        ::

            >>> e = EFetch("taxon")
            >>> ret = e.efetch("9606")
            >>> ret.TaxaSet.Taxon[0].ScientificName


        """
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_%s.wsdl"
        #TODO: valid list of database
        # TODO dynamic service ?
        url = url % database
        super(EFetch, self).__init__(name="EFetch", verbose=verbose, url=url)
        self.db = database
        self.params = self.suds.factory.create("nsef:eFetchRequest")

    def efetch(self, sid, **kargs):
        """Check out the parameter list in the :attr:`params` attribute.

        """
        ret = self.serv.run_eFetch(sid, **kargs)
        return ret



class EUtils(WSDLService):
    """Interface to `NCBI Entrez Utilities <http://www.ncbi.nlm.nih.gov/entrez/query/static/esoap_help.html>`_ service

    The EUtils class has a method called EFetch so this is actually covering
    all Entrez functionalities.

    Note that we use the WSDL protocol for all EUtils but we had to use the REST
    service in a few cases.

    .. warning:: Read the `guidelines
        <http://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ before sending requests.
        No more than 3 requests per seconds otherwise your IP may be banned.
        You should provide your email by filling the :attr:`email` so that
        before being banned, you may be contacted.

    Here is an example on how to use :method:`EFetch` method to retrieve the
    FASTA sequence of a given identifier (34577063)::

        >>> from bioservices import EUtils
        >>> s = EUtils()
        >>> print(s.EFetch("sequences", "34577063", rettype="fasta"))
        >gi|34577063|ref|NP_001117.2| adenylosuccinate synthetase isozyme 2 [Homo sapiens]
        MAFAETYPAASSLPNGDCGRPRARPGGNRVTVVLGAQWGDEGKGKVVDLLAQDADIVCRCQGGNNAGHTV
        VVDSVEYDFHLLPSGIINPNVTAFIGNGVVIHLPGLFEEAEKNVQKGKGLEGWEKRLIISDRAHIVFDFH
        QAADGIQEQQRQEQAGKNLGTTKKGIGPVYSSKAARSGLRMCDLVSDFDGFSERFKVLANQYKSIYPTLE
        IDIEGELQKLKGYMEKIKPMVRDGVYFLYEALHGPPKKILVEGANAALLDIDFGTYPFVTSSNCTVGGVC
        TGLGMPPQNVGEVYGVVKAYTTRVGIGAFPTEQDNEIGELLQTRGREFGVTTGRKRRCGWLDLVLLKYAH
        MINGFTALALTKLDILDMFTEIKVGVAYKLDGEIIPHIPANQEVLNKVEVQYKTLPGWNTDISNARAFKE
        LPVNAQNYVRFIEDELQIPVKWIGVGKSRESMIQLF

    Most of the methods take a database name as input. You can obtain the
    valid list by checking the :attr:`databases` attribute.

    A few functions takes Identifier(s) as input. It could be a list of strings,
    list of numbers, or a string where identifiers are separated either by
    comma or spaces.

    A few functions takes an argument called **term**. You can use the **AND**
    keyword with spaces or + signs as separators::

        Correct:   term=biomol mrna[properties] AND mouse[organism]
        Correct:   term=biomol+mrna[properties]+AND+mouse[organism]

    Other special characters, such as quotation marks (") or the # symbol used
    in referring to a query key on the History server, could be represented by
    their URL encodings (%22 for "; %23 for #) or verbatim .::

        Correct: term=#2+AND+"gene in genomic"[properties]
        Correct: term=%232+AND+%22gene+in+genomic%22[properties]

    .. note:: most of the parameter names are identical to the expected names
        except for **id**, which has been replaced by **sid**.

    """
    def __init__(self, verbose=False, email="unknown"):
        #url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/eutils.wsdl?"

        # according to http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1
        # this url should be use
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/eutils.wsdl?"
        super(EUtils, self).__init__(name="EUtils", verbose=verbose, url=url)


        warning = """

        NCBI recommends that users post no more than three URL requests per second.
        Failure to comply with this policy may result in an IP address being blocked
        from accessing NCBI. If NCBI blocks an IP address, service will not be
        restored unless the developers of the software accessing the E-utilities
        register values of the tool and email parameters with NCBI. The value of
        email will be used only to contact developers if NCBI observes requests
        that violate our policies, and we will attempt such contact prior to blocking
        access.  For more details see http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1

        BioServices does not check if you send more than 3 requests per seconds.
        This is considered to be the user responsability. Within BioServices, we
        fill the parameter **tool** and **email**, however, to fill the later
        you should provide your email either globablly when instanciating EUtils,
        or locally when calling a method.

        This message will not appear if you set the email as a parameter::

            e = EUtils(email="name@adress")

        or in you bioservices configuration file (.config/bioservices/bioservices.cfg)
        under linux with a user section::

            [user]
            email = yourname@somewhere


        """
        # on top of the WSDL protocol we also need a REST for the EFetch method
        # Indeed, although we have a WSDL class for EFetch, it is (i) limited
        # because doc could not be found (ii) required sn instanciation for
        # each database whereas with REST, we ca do it just once
        self._efetch = REST("Efetch","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")

        self._databases = None
        self.tool = "bioservices"
        self.email = email
        if self.email == "unknown":
            # trying the bioservices config file
            if self.settings.params['user.email'][0]!="unknown":
                self.email = self.settings.params['user.email'][0]
            else:
                self.logging.warning(warning)

    def _get_databases(self):
        """alias to run_eInfo"""
        if self._databases is None:
            # DbData changed into DbList in rev 1.3.0
            self._databases = sorted(self.serv.run_eInfo().DbList.DbName)
        return self._databases
    databases = property(_get_databases, doc="Returns list of valid databases")

    def _check_db(self, db):
        if db not in self.databases:
            raise ValueError("You must provide a valid databases from : ", self.databases)

    def _check_retmode(self, retmode):
        if retmode not in ["xml", "text"]:
            raise ValueError("You must provide a retmode in 'xml', 'text'")

    def get_einfo_params(self, **kargs):
        return self.wsdl_create_factory("nsei:eInfoRequest", **kargs)

    def get_esummary_params(self, **kargs):
        return self.wsdl_create_factory("nsesu:eSummaryRequest", **kargs)

    def get_esearch_params(self, **kargs):
        return self.wsdl_create_factory("nsese:eSearchRequest", **kargs)

    def get_egquery_params(self, **kargs):
        return self.wsdl_create_factory("nseg:eGqueryRequest", **kargs)

    def get_espell_params(self, **kargs):
        return self.wsdl_create_factory("nsesp:eSpellRequest", **kargs)

    def get_elink_params(self, **kargs):
        return self.wsdl_create_factory("nsel:eLinkRequest", **kargs)

    def get_epost_params(self, **kargs):
        return self.wsdl_create_factory("nseps:ePostRequest", **kargs)

    def _check_ids(self, sid):
        if isinstance(sid, int):
            sid = [sid]
        if isinstance(sid, list):
            sid = ",".join([str(x) for x in sid])

        # If there are commas, let us split, strip spaces and join back the ids
        sid = ",".join([x.strip() for x in sid.split(',') if x.strip()!=""])

        if len(sid.split(","))>200:
            raise ValueError("Number of comma separated IDs must be less than 200")
        return sid

    def taxonomy(self, sid, raw=False):
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
        sid = self._check_ids(sid)
        serv = EFetch("taxon")
        ret = serv.efetch(sid)
        if raw:
            return ret
        else:
            return ret.TaxaSet

    def snp(self, sid):
        """Alias to Efetch for the SNP database using WSDL

        ::

            >>> s.snp("123")

        """
        serv = EFetch("snp")
        ret = serv.efetch(sid)
        return ret

    def EFetch(self, db, sid=None, retmode="text", **kargs):
        """Access to the EFetch E-Utilities

        :param str db: Database from which to retrieve UIDs. The value must be a valid Entrez database
            name . This is the destination database for the link operation.
        :param str sid: UID list. Either a single UID or a comma-delimited list of UIDs may be provided.
            All of the UIDs must be from the database specified by db. Limited
            to 200 sid

        :param retmode: default to text (could be xml but not recommended).
        :param rettype: could be fasta, summar      :param rettype: could be
        fasta, summaryy

        ::

            >>> ret = s.EFetch("omim", "269840")  --> ZAP70
            >>> ret = s.EFetch("taxonomy", "9606", retmode="xml")
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


        Identifiers could be provided as a single string with comma-separated
        values, or a list of strings, a list of integers, or just one
        string or one integer but no mixing of types in the list::

            >>> e.EFetch("sequences", "352, 234", retmode="text", rettype="fasta")
            >>> e.EFetch("sequences", 352, retmode="text", rettype="fasta")
            >>> e.EFetch("sequences", [352], retmode="text", rettype="fasta")
            >>> e.EFetch("sequences", [352, 234], retmode="text", rettype="fasta")


        **retmode** should be xml or text depending on the database. For instance, xml fo
        pubmed::

            >>> e.EFetch("pubmed", "20210808", retmode="xml")
            >>> e.EFetch('nucleotide', id=15, retmode='xml')
            >>> e.EFetch('nucleotide', id=15, retmode='xml', rettype='fasta')
            >>> e.EFetch('nucleotide', 'NT_019265', rettype='gb')

        eutils.EUtilsParser(e.EFetch("taxonomy", "9685", retmode="xml")
        .. todo:: more documentation and optional arguments

        Other special characters, such as quotation marks (") or the # symbol
        used in referring to a query key on the History server, should be
        represented by their URL encodings (%22 for "; %23 for #).
        """
        #self._check_db(db)
        self._check_retmode(retmode)
        if sid is not None:
            sid = self._check_ids(sid)

        params = {'db':db, 'id':sid, 'retmode':retmode, 'tool':self.tool,
                'email': self.email}
        if kargs.get("strand"):
            strand = kargs.get("strand")
            self.devtools.check_param_in_list(strand, [1,2])
            params['strand'] = strand

        if kargs.get("complexity"):
            complexity = kargs.get("complexity")
            if complexity in [0,1,2,3,4]:
                params['complexity'] = complexity
            else:
                raise ValueError("invalid complexity. must be a number in 0,1,2,3,4")

        for param in ['retmax', 'seq_start', "seq_stop", "rettype", "query_key", "WebEnv"]:
            if kargs.get(param):
                params[param] = kargs.get(param)

        #print(params)
        if retmode == "xml":
            ret = self._efetch.http_get("efetch.fcgi", 'xml', params=params)
            ret = self.easyXML(ret)
        else:
            ret = self._efetch.http_get("efetch.fcgi", 'txt', params=params)


        return ret

    def EInfo(self, db=None, **kargs):
        """Provides the number of records indexed in each field of a given
        database, the date of the last update of the database, and the available links
        from the database to other Entrez databases.

        :param str db: target database about which to gather statistics. Value must be a
            valid Entrez database name. See :attr:`databases` or don't provide
            any value to obtain the entire list
        :return: either a list of databases, or a dictionary with relevant information
            about the requested database

        ::

            >>> all_database_names = s.EInfo()
            >>> # specific info about one database:
            >>> ret = s.EInfo("taxonomy")
            >>> ret.Count
            >>> ret.Name
            >>> ret = s.EInfo('pubmed')
            >>> res.FieldList[2].FullName
            'Filter'

        """
        if db is None:
            return self.databases
        else:
            self._check_db(db)

        # WSDL does not work, let us use rest instead.
        ret = self._einfo_rest(db, **kargs)
        ret = EUtilsParser(ret)
        return ret

    def _einfo_rest(self, db=None, **kargs):
        s = REST("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        ret = s.http_get("einfo.fcgi?db=%s" % db, frmt="xml",
                         params={'tool':kargs.get('tool',self.tool),
                                 'email':kargs.get('email',self.email)
                                 })
        ret = self.easyXML(ret)
        return ret

    """Does not work...issue with DbBuil
    # ret = self._einfo_wsdl(db, **kargs)
    def _einfo_wsdl(self, db=None, **kargs):
        params = self.suds.factory.create("nsei:eInfoRequest", **kargs)
        params.db = db
        params.tool = self.tool[:]
        params.email = self.email[:]
        return self.serv.run_eInfo(db, params)
    """




    def ESummary(self, db, sid=None,  **kargs):
        """Returns document summaries for a list of input UIDs


        :param str sid: list of identifiers (or string comma separated).
            all of the UIDs must be from the database specified by db. Limited
            to 200 sid

        ::

            >>> from bioservices import *
            >>> s = EUtils()
            >>> ret = s.ESummary("snp","7535")
            >>> ret = s.ESummary("snp","7535,7530")
            >>> ret = s.ESummary("taxonomy", "9606,9913")

        ::

            >>> proteins = e.ESearch("protein", "bacteriorhodopsin", RetMax=20,)
            >>> ret = e.ESummary("protein", proteins.IdList.Id[0])
            >>> ret.DocSum[0].Item[2]
            (ItemType){
               _Type = "String"
               _Name = "Extra"
               ItemContent = "gi|6320236|ref|NP_010316.1|[6320236]"
            }


        """
        if sid is not None:
            sid = self._check_ids(sid)

        if db is None:
            return self.databases
        else:
            self._check_db(db)

        params = self.get_esummary_params(**kargs)
        params.db = db
        params.id = sid
        ret = self.serv.run_eSummary(**dict(params))
        return ret

    def _esummary_rest(self, db, sid):
        # [(x.attrib['Name'], x.text) for x in ret.getchildren()[0].getchildren()[1:]]
        s = REST("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        ret = s.http_get("esummary.fcgi?db=%s&id=%s" % (db, sid), None)
        ret = self.easyXML(ret)
        return ret



    def EGQuery(self, term, **kargs):
        """Provides the number of records retrieved in all Entrez databases by a text query.

        :param str term: Entrez text query. All special characters must be URL
            encoded. Spaces may be replaced by '+' signs. For very long queries (more than
            several hundred characters long), consider using an HTTP POST call. See the
            PubMed or Entrez help for information about search field descriptions and tags.
            Search fields and tags are database specific.

        ::

            >>> ret = s.EGQuery("asthma")
            >>> [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem if x.Count!='0']

            >>> ret = s.EGQuery("asthma")
            >>> ret.eGQueryResult.ResultItem[0]
            >>> ret.Term

        """
        params = self.get_egquery_params(**kargs)
        ret = self.serv.run_eGquery(term, params)
        return ret

    def ESearch(self, db, term, **kargs):
        """Responds to a query in a given  database


        The response can be used later in ESummary, EFetch or ELink, along with
        the term translations of the query.

        :param db:
        :param term:

        .. note:: see :meth:`get_esearch_params` for the list of valid parameters.

        ::

            >>> ret = e.ESearch('protein', 'human', RetMax=5)
            >>> ret = e.ESearch('taxonomy', 'Staphylococcus aureus[all names]')
            >>> ret = e.ESearch('pubmed', "cokelaer AND BioServices")
            >>> # There is on identifier in the IdList (therefore the first element)
            >>> identifiers = e.pubmed(ret.IdList.Id)


        More complex requests can be used. We will not cover all the possiblities (see the
        NCBI website). Here is an example to tune the search term to look into
        PubMed for the journal PNAS Volume 16, and retrieve.::

            >>> e.ESearch("pubmed", "PNAS[ta] AND 16[vi]")


        You can then look more closely at a specific identifier using EFetch::

            >>> e = EFetch("pubmed")
            >>> e.efetch(identifiers)


        .. note:: valid parameters can be found by calling :meth:`get_esearch_params`
        """
        params = self.get_esearch_params(**kargs)
        params['db'] = db
        params['term'] = term
        # the API requires the db and term paramters to be provided
        # as positional arguments. The db and term attribute in the
        # params structure are just ignored. Note, however, that
        # the db and term parameter must also be provided in the params
        # dict so that other argument are also used... wierd
        ret = self.serv.run_eSearch(db, term, params)
        return ret

    #def _egquery_rest(self, term, retmode="xml"):
    #    self._check_retmode(retmode)
    #    s = REST("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
    #    ret = s.request("egquery.fcgi?term=%s&retmode=%s" % (term, retmode))
    #    return ret



    def ESpell(self, db, term, **kargs):
        """Retrieve spelling suggestions for a text query in a given database.

        :param str db: database to search. Value must be a valid Entrez
            database name (default = pubmed).
        :param str term: Entrez text query. All special characters must be
            URL encoded.

        ::

            >>> ret = e.ESpell(db="omim", term="aasthma+OR+alergy")
            >>> ret.Query
            'asthmaa OR alergies'
            >>> ret.CorrectedQuery
            'asthma or allergy'
            >>> ret = e.ESpell(db="pubmed", term="biosservices")
            >>> ret.CorrectedQuery
            bioservices


        .. note:: only WSDL protocol available
        """
        params = self.get_espell_params(**kargs)
        self._check_db(db)
        ret = self.serv.run_eSpell(db, term, params)
        return ret

    def ELink(self, dbfrom, sid=None, **kargs):
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
        :param str sid: UID list. Either a single UID or a comma-delimited list of UIDs may be provided.
            All of the UIDs must be from the database specified by db. Limited  to 200 Ids
        :param str cmd: ELink command mode. The command mode specified which
            function ELink will perform. Some optional parameters only function for certain
            values of cmd (see http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink).
            Examples are neighbor, prlinks.

        ::

            >>> # Example: Find related articles to PMID 20210808
            >>> ret = s.ELink("pubmed", sid="20210808", cmd="neighbor_score")
            >>> ret.LinkSet[0].LinkSetDb[0].Link[0].Id


            # FIXME: change example values
            >>> s.Elink(dbfrom="nucleotide", db="protein",
                              id="48819,7140345")
            >>> s.Elink(dbfrom="nucleotide", db="protein",
                              id="48819,7140345")

            LinkSetDb, DbFrom , IdList

        .. todo:: remove LinkSet : there is only 1 set ?
        """
        if sid is not None:
            sid = self._check_ids(sid)
        self._check_db(dbfrom)
        if 'cmd' in kargs.keys():
            assert kargs['cmd'] in ["neighbor", "neighbor_score",
                    "neighbor_history", "acheck", "llinks", "lcheck",
                    "ncheck", "llinkslib", "prlinks"]

        #s = REST("test","http://eutils.ncbi.nlm.nih.gov/entrez/eutils/")
        #request = "elink.fcgi?db=%s&dbfrom=%s" % (db, dbfrom)
        #request += "&id=%s" % sid
        #request += "&cmd=%s" % cmd
        #ret = s.request(request)
        #return ret
        params = self.get_elink_params(**kargs)
        params.dbfrom = dbfrom
        params.id = sid

        ret = self.serv.run_eLink(**dict(params))
        return ret

    def EPost(self, db, sid, **kargs):
        """Accepts a list of UIDs from a given database,

        stores the set on the History Server, and responds with a query
        key and web environment for the uploaded dataset.

        :param str db: a valid database
        :param id: list of strings of strings


        """
        params = self.get_epost_params(**kargs)
        params.id = sid
        params.db = db
        ret = self.serv.run_ePost(**dict(params))
        return ret


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class EUtilsParser(AttrDict):
    """Convert xml returned by EUtils into a structure easier to manipulate

    Tested and used for EInfo,

    Does not work for Esummary
    """
    def __init__(self, xml):
        super(EUtilsParser, self).__init__()

        try:
            children = xml.root.getchildren()[0].getchildren()
            self.__name = xml.root.getchildren()[0].tag
        except:
            children = xml.getchildren()

        for i, child in enumerate(children):
            if len(child.getchildren()) == 0:
                self[child.tag] = child.text
            else:
                # This is probably a list then
                self[child.tag] = []
                for subchild in child.getchildren():
                    self[child.tag].append(EUtilsParser(subchild))

    def __str__(self):
        name = self._EUtilsParser__name
        if name == "DbInfo":
            txt = ""
            for this in self.FieldList:
                txt += "{0:10}:{1}\n".format(this.Name, this.Description)
            return txt
        else:
            print("Not implemented for {0}".format(name))



"""
(Part){
   root = <part element="nseps:ePostRequest" name="request"/>
   name = "request"
   qname[] =
      "request",
      "http://www.ncbi.nlm.nih.gov/soap/eutils/",
   element = "('ePostRequest', 'http://www.ncbi.nlm.nih.gov/soap/eutils/epost')"
   type = "None"
 }
"""
