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

    :URL: http://www.ncbi.nlm.nih.gov/books/NBK25499/
    :URL: http://www.ncbi.nlm.nih.gov/books/NBK25500/#chapter1.Demonstration_Programs

    .. highlights::

        The Entrez Programming Utilities (E-utilities) are a set of eight server-side programs that provide a stable interface into the Entrez query and database system at the National Center for Biotechnology Information (NCBI). The E-utilities use a fixed URL syntax that translates a standard set of input parameters into the values necessary for various NCBI software components to search for and retrieve the requested data. The E-utilities are therefore the structured interface to the Entrez system, which currently includes 38 databases covering a variety of biomedical data, including nucleotide and protein sequences, gene records, three-dimensional molecular structures, and the biomedical literature.

       -- from http://www.ncbi.nlm.nih.gov/books/NBK25497/, March 2013

"""
import json
from bioservices import REST
from bioservices import __version__

__all__ = ["EUtils", "EUtilsParser"]

# source:
# http://www.dalkescientific.com/writings/diary/archive/2005/09/30/using_eutils.html




class EUtils(REST):
    """Interface to `NCBI Entrez Utilities <http://www.ncbi.nlm.nih.gov/entrez>`_ service

    .. note:: Technical note: the WSDL interface was dropped in july 2015 
        so we now use the REST service.

    .. warning:: Read the `guidelines
        <http://www.ncbi.nlm.nih.gov/books/NBK25497/>`_ before sending requests.
        No more than 3 requests per seconds otherwise your IP may be banned.
        You should provide your email by filling the :attr:`email` so that
        before being banned, you may be contacted.

    There are a few methods such as :meth:`ELink`, :meth:`EFetch`.
    Here is an example on how to use :meth:`EFetch` method to retrieve the
    FASTA sequence of a given identifier (34577063)::

        >>> from bioservices import EUtils
        >>> s = EUtils()
        >>> print(s.EFetch("protein", "34577063", rettype="fasta"))
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

    A few functions takes Identifier(s) as input. It could be a list of 
    strings, list of numbers, or a string where identifiers are separated 
    either by comma or spaces.

    A few functions take an argument called **term**. You can use the **AND**
    keyword with spaces or + signs as separators::

        Correct:   term=biomol mrna[properties] AND mouse[organism]
        Correct:   term=biomol+mrna[properties]+AND+mouse[organism]

    Other special characters, such as quotation marks (") or the # symbol used
    in referring to a query key on the History server, could be represented by
    their URL encodings (%22 for "; %23 for #) or verbatim .::

        Correct: term=#2+AND+"gene in genomic"[properties]
        Correct: term=%232+AND+%22gene+in+genomic%22[properties]

    """
    def __init__(self, verbose=False, email="unknown"):
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        super(EUtils, self).__init__(name="EUtils", verbose=verbose, url=url)


        warning = """

        NCBI recommends that users post no more than three URL requests per 
        second. Failure to comply with this policy may result in an IP address
        being blocked from accessing NCBI. If NCBI blocks an IP address, 
        service will not be restored unless the developers of the software 
        accessing the E-utilities register values of the tool and email 
        parameters with NCBI. The value of email will be used only to contact 
        developers if NCBI observes requests that violate our policies, and we
        will attempt such contact prior to blocking access.  For more details 
        see http://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.chapter2_table1
        BioServices does not check if you send more than 3 requests per 
        seconds. This is considered to be the user responsability. Within 
        BioServices, we fill the parameter **tool** and **email**, however, 
        to fill the latter you should provide your email either globablly
        when instanciating EUtils, or locally when calling a method.

        This message will not appear if you set the email as a parameter::

            e = EUtils(email="name@adress")

        or in you bioservices configuration file 
        (.config/bioservices/bioservices.cfg) under linux with a user section::

            [user]
            email = yourname@somewhere


        """
        self._databases = None
        self.tool = "BioServices, " + __version__

        #: fill this with your email address
        self.email = email
        if self.email == "unknown":
            # trying the bioservices config file
            if self.settings.params['user.email'][0] != "unknown":
                self.email = self.settings.params['user.email'][0]
            else:
                self.logging.warning(warning)

    def help(self):
        """Open EUtils help page"""
        self.on_web('http://www.ncbi.nlm.nih.gov/books/NBK25497')

    def _get_databases(self):
        """alias to run_eInfo"""
        # Let us use the REST services instead of WSDL, which fails sometimes
        # and for sure since version Sept 2015
        if self._databases is None:
            res = self.http_get('einfo.fcgi', params={'retmode':'json'})
            databases = res['einforesult']['dblist']

            self._databases = sorted(databases)
        return self._databases
    databases = property(_get_databases, doc="Returns list of valid databases")

    def _check_db(self, db=None):
        msg = "You must provide a valid databases from : "
        if db is None or db not in self.databases:
            raise ValueError(msg, self.databases)

    def _check_retmode(self, retmode, valids=['xml', 'text']):
        if retmode not in valids:
            raise ValueError("You must provide a retmode in %s" % valids)

    def _get_params(self, keys=[], **kargs):
        # could use a defaultdict from collections.
        params = {'tool': self.tool, 'email': self.email}
        # fill the structure with None
        for this in keys:
            params[this] = None
        # update structure with user's items if any

        for k, v in kargs.items():
            if k in keys:
                params[k] = v
            else:
                # unknown so let use it but raise a warning
                params[k] = v
                self.warning("%s does not seem to be a known parameter. " % k+
                        "Use it anyway but may be ignored")
        return params

    def _get_einfo_params(self, **kargs):
        params = self._get_params(['db', 'version', 'retmode'], **kargs)
        return params

    def _get_esummary_params(self, **kargs):
        keys = ['WebEnv', 'query_key', 'retstart', 'retmax',
            'retmode', 'version']
        params = self._get_params(keys, **kargs)
        return params

    def _get_esearch_params(self, **kargs):
        keys = ['retmax', 'retstart', 'WebEnv', 'query_key',
                'datetype', 'retmode',
                'field', 'maxdate', 'mindate', 'reldate', 'rettype',
                'sort',  'usehistory']
        params = self._get_params(keys, **kargs)
        return params

    def _get_egquery_params(self, **kargs):
        params = self._get_params([], **kargs)
        return params

    def _get_espell_params(self, **kargs):
        params = self._get_params([], **kargs)
        return params

    def _get_efetch_params(self, **kargs):
        keys = ['WebEnv', 'query_key', 'retmode', 'rettype', 'retstart',
                'retmax', 'strand', 'seq_start', 'seq_stop', 'complexity']
        params = self._get_params(keys, **kargs)
        return params

    def _get_elink_params(self, **kargs):
        # Note that id could be id[] ?
        keys = ['reldate', 'mindate', 'maxdate', 'datetype',
                'term', 'holding', 'linkname', 'WebEnv', 'query_key', 'cmd']
        params = self._get_params(keys, **kargs)
        return params

    def _get_epost_params(self, **kargs):
        params = self._get_params(['WebEnv'], **kargs)
        return params

    def _check_ids(self, sid):
        if sid is None:
            return sid
        elif isinstance(sid, int):
            sid = str(sid)
        elif isinstance(sid, list):
            sid = ",".join([str(x) for x in sid])

        # If there are commas, let us split, strip spaces and join back the ids
        sid = ",".join([x.strip() for x in sid.split(',') if x.strip()!=""])

        if len(sid.split(",")) > 200:
            raise ValueError("Number of comma separated IDs must be less than 200")
        return sid

    def taxonomy_summary(self, id):
        """Alias to EFetch for the taxonomy database

        ::

            >>> s = EUtils()
            >>> ret = s.taxonomy("9606")
            >>> ret['9606']['species']
            'sapiens'
            >>> ret = s.taxonomy("9606,9605,111111111,9604")
            >>> ret['9604']['taxid']
            9604

        """
        sid = self._check_ids(id)
        ret = self.ESummary('taxonomy', sid, retmode='json')
        return ret

    def snp_summary(self, id):
        """Alias to Efetch for the SNP database 


        :Return: a json data structure.

        ::

            >>> ret = s.snp("123")


        """
        ret = self.ESummary("snp", id)
        return ret

    def EFetch(self, db, id, retmode="text", **kargs):
        """Access to the EFetch E-Utilities

        :param str db: database from which to retrieve UIDs. 
        :param str id: list of identifiers.
        :param retmode: default to text (could be xml but not recommended).
        :param rettype: could be fasta, summary, ...
        :return: depends on retmode parameter.

        ::

            >>> ret = s.EFetch("omim", "269840")  --> ZAP70
            >>> ret = s.EFetch("taxonomy", "9606", retmode="xml")
            >>> [x.text for x in ret.getchildren()[0].getchildren() if x.tag=="ScientificName"]
            ['Homo sapiens']

            >>> s = eutils.EUtils()
            >>> s.EFetch("protein", "34577063", retmode="text", rettype="fasta")
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

            >>> e.EFetch("protein", "352, 234", retmode="text", rettype="fasta")
            >>> e.EFetch("protein", 352, retmode="text", rettype="fasta")
            >>> e.EFetch("protein", [352], retmode="text", rettype="fasta")
            >>> e.EFetch("protein", [352, 234], retmode="text", rettype="fasta")


        **retmode** should be xml or text depending on the database. 
        For instance, xml for pubmed::

            >>> e.EFetch("pubmed", "20210808", retmode="xml")
            >>> e.EFetch('nucleotide', id=15, retmode='xml')
            >>> e.EFetch('nucleotide', id=15, retmode='text', rettype='fasta')
            >>> e.EFetch('nucleotide', 'NT_019265', rettype='gb')

        Other special characters, such as quotation marks (") or the # symbol
        used in referring to a query key on the History server, should be
        represented by their URL encodings (%22 for "; %23 for #).
        """
        self._check_db(db)
        #self._check_retmode(retmode, valids=['text', 'xml'])
        sid = self._check_ids(id)

        params = self._get_efetch_params(**kargs)
        if 'strand' in params.keys() and params['strand'] != None:
            self.devtools.check_param_in_list(params['strand'], [1, 2])
        if 'complexity' in params.keys() and params['complexity'] != None:
            self.devtools.check_param_in_list(params['complexity'],
                    [0, 1, 2, 3, 4])

        query = "efetch.fcgi?db=%s&id=%s" % (db, sid)

        ret = self.http_get(query, params=params)
        try: ret = ret.content
        except: pass

        return ret

    def EInfo(self, db=None, retmode='json', **kargs):
        """Provides information about a database (e.g., number of records)

        :param str db: target database about which to gather statistics.
            Value must be a valid Entrez database name. See :attr:`databases`
            or don't provide any value to obtain the entire list
        :return: an XML or json data structure that depends on the
           value of :param:`databases` (default to json)

        ::

            >>> all_database_names = s.EInfo()
            >>> # specific info about one database:
            >>> ret = s.EInfo("taxonomy")
            >>> ret['count']
            u'1445358'
            >>> ret = s.EInfo('pubmed')
            >>> ret['fieldlist'][2]['fullname']
            'Filter'

        You can use the *retmode* parameter to 'xml' as well. In that
        case, you will need a XML parser. 

        ::

            >>> ret = s.EInfo("taxonomy", retmode='xml')
            >>> ret = s.parse_xml('objectify')
            >>> ret.root.DbInfo.FieldList.getchildren()[2].FullName
            'Filter'

        .. note:: Note that the name in the XML or json outputs 
            differ (some have lower cases, some have upper cases). This
            is inherent to the output of EUtils.

        """
        if db is not None:
            self._check_db(db)
        else:
            return self.databases

        self._check_retmode(retmode, valids=['xml', 'json'])
        kargs['retmode'] = retmode

        # let us create the query now
        query = 'einfo.fcgi'
        if db is not None:
            query += '?db=%s' % db

        # with parameters
        params = self._get_einfo_params(**kargs)

        # the real call using GET method
        ret = self.http_get(query,  params=params)
        try: ret = ret.content
        except: pass

        if retmode == 'json':
            ret = ret['einforesult']['dbinfo']
        return ret

    def parse_xml(self, ret, method='easyxml'):
        if method == 'EUtilsParser':
            ret = self.easyXML(ret)
            return EUtilsParser(ret)
        elif method == 'objectify':
            from bioservices.xmltools import XMLObjectify
            return XMLObjectify(ret)
        elif method == 'easyxml':
            return self.easyXML(ret)

    def ESummary(self, db, id=None,  retmode='json', **kargs):
        """Returns document summaries for a list of input UIDs


        :param db: a valid database
        :param str id: list of identifiers (or string comma separated).
            all of the UIDs must be from the database specified by db. Limited
            to 200 identifiers

        ::

            >>> from bioservices import *
            >>> s = EUtils()
            >>> ret = s.ESummary("snp","7535")
            >>> ret = s.ESummary("snp","7535,7530")
            >>> ret = s.ESummary("taxonomy", "9606,9913")

        ::

            >>> proteins = e.ESearch("protein", "bacteriorhodopsin", 
                    retmax=20)
            >>> ret = e.ESummary("protein", 449301857)
            >>> ret['result']['449301857']['extra']
            'gi|449301857|gb|EMC97866.1||gnl|WGS:AEIF|BAUCODRAFT_31870'


        """
        sid = self._check_ids(id)
        self._check_db(db)
        self._check_retmode(retmode, valids=['xml', 'json'])
        kargs['retmode'] = retmode

        params = self._get_esummary_params(**kargs)
        # the real call using GET method
        query = "esummary.fcgi?db=%s&id=%s" % (db, sid)
        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass

        # if XMl, we can parse it using dedicated parser
        if retmode == 'json':
            ret = json.loads(ret)
            ret = ret['result']
        return ret

    def EGQuery(self, term, **kargs):
        """Provides the number of records retrieved in all Entrez databases by a text query.

        :param str term: Entrez text query. 
            Spaces may be replaced by '+' signs. For very long queries 
            (more than  several hundred characters long), consider using 
            an HTTP POST call. See the
            PubMed or Entrez help for information about search field 
            descriptions and tags.
            Search fields and tags are database specific.
        :return: returns a XML data structure parsed with :class:`EUtilsParser`

        ::

            >>> ret = s.EGQuery("asthma")
            >>> [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem if x.Count!='0']

            >>> ret = s.EGQuery("asthma")
            >>> ret.eGQueryResult.ResultItem[0]
            {'Count': '115241',
             'DbName': 'pmc',
             'MenuName': 'PubMed Central',
             'Status': 'Ok'}


        """
        params = self._get_egquery_params(**kargs)

        query = "egquery.fcgi?term=%s" % (term)
        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass

        ret = self.parse_xml(ret, 'EUtilsParser').Result

        return ret

    def ESearch(self, db, term, retmode='json', **kargs):
        """Responds to a query in a given database

        The response can be used later in ESummary, EFetch or ELink, 
        along with the term translations of the query.

        :param db: a valid database
        :param term: an Entrez text query

        .. note:: see :meth:`_get_esearch_params` for the list of valid parameters.

        ::

            >>> ret = e.ESearch('protein', 'human', RetMax=5)
            >>> ret = e.ESearch('taxonomy', 'Staphylococcus aureus[all names]')
            >>> ret = e.ESearch('pubmed', "cokelaer AND BioServices")

            >>> ret = e.ESearch('protein', '15718680', retmode='json')
            >>> # Let us show the first pubmed identifier in a browser
            >>> identifiers = e.pubmed(ret['idlist'][0])

        More complex requests can be used. We will not cover all the
        possiblities (see the NCBI website). Here is an example to tune
        the search term to look into PubMed for the journal PNAS
        Volume 16, and retrieve.::

            >>> e.ESearch("pubmed", "PNAS[ta] AND 16[vi]")

        You can then look more closely at a specific identifier using EFetch::

            >>> e = EFetch("pubmed")
            >>> e.Efetch(identifiers)

        .. note:: valid parameters can be found by calling 
            :meth:`_get_esearch_params`
        """
        self._check_db(db)
        self._check_retmode(retmode, valids=['xml', 'json'])
        kargs['retmode'] = retmode

        params = self._get_esearch_params(**kargs)

        query = "esearch.fcgi?db=%s&term=%s" % (db, term)
        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass
        if retmode == 'json':
            ret = json.loads(ret)
            ret = ret['esearchresult']
        return ret

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
        self._check_db(db)

        params = self._get_esearch_params(**kargs)

        query = "espell.fcgi?db=%s&term=%s" % (db, term)
        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass

        ret = self.parse_xml(ret, 'EUtilsParser')
        return ret

    def ECitMatch(self,bdata, **kargs):
        """


        :param bdata: Citation strings. Each input citation must
            be represented by a citation string in the following format::

                journal_title|year|volume|first_page|author_name|your_key|

            Multiple citation strings may be provided by separating the
            strings with a carriage return character (%0D).

            The your_key value is an arbitrary label provided by the user
            that may serve as a local identifier for the citation,
            and it will be included in the output.

            all spaces must be replaced by + symbols and that citation
            strings should end with a final vertical bar |.


        Only xml supported at the time of this implementation.
        """
        params = {'bdata': bdata}

        # note here, we use .cgi not .fcgi
        query = "ecitmatch.cgi?db=pubmed&retmode=xml"
        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass

        return ret

    def ELink(self, db=None, dbfrom=None, id=None, **kargs):
        """The Entrez links utility

        Responds to a list of UIDs in a given database with either a list of
        related UIDs (and relevancy scores) in the same database or a list 
        of linked UIDs in another Entrez database; 

        :param str db: valid database from which to retrieve UIDs. 
        :param str dbfrom: Database containing the input UIDs. The 
            value must be a valid database name (default = pubmed). 
            This is the origin database of
            the link operation. If db and dbfrom are set to the same database 
            value, then  ELink will return computational neighbors within 
            that database. Computational neighbors have linknames that begin 
            with dbname_dbname (examples: protein_protein, 
            pcassay_pcassay_activityneighbor).
        :param str id: UID list. Either a single UID or a comma-delimited list
            Limited  to 200 Ids
        :param str cmd: ELink command mode. The command mode specified which
            function ELink will perform. Some optional parameters only 
            function for certain values of cmd (see 
            http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink).
            Examples are neighbor, prlinks.

        ::

            >>> # Example: Find related articles to PMID 20210808
            >>> ret = s.ELink("pubmed", id="20210808", cmd="neighbor_score")

            >>> ret = s.parse_xml(ret, 'EUtilsParser')
            >>> ret.eLinkResult.LinkSet.LinkSetDb[0].Link[1]
            {'Id': '16539535'}


            >>> s.Elink(dbfrom="nucleotide", db="protein",
                              id="48819,7140345")
            >>> s.Elink(dbfrom="nucleotide", db="protein",
                              id="48819,7140345")
            >>> s.ELink(dbfrom='nuccore', id='21614549,219152114',
                    cmd='ncheck')

        """
        # unlike other EUtils, db and dbfrom are here optional
        sid = self._check_ids(id)
        if db is not None:
            self._check_db(db)
        if dbfrom is not None:
            self._check_db(dbfrom)
        if db is None and dbfrom is None:
            raise ValueError("One of db or dbfrom parameter must be provided")

        if 'cmd' in kargs.keys():
            assert kargs['cmd'] in ["neighbor", "neighbor_score",
                    "neighbor_history", "acheck", "llinks", "lcheck",
                    "ncheck", "llinkslib", "prlinks"]
            cmd = kargs['cmd']
        else:
            cmd = None

        if db is not None and dbfrom is not None:
            query = "elink.fcgi?db=%s&dbfrom=%s" % (db, dbfrom)
        elif dbfrom is not None:
            query = "elink.fcgi?dbfrom=%s" % dbfrom
        elif db is not None:
            query = "elink.fcgi?db=%s" % db

        if sid is not None:
            query += "&id=%s" % sid
        if cmd is not None:
            query += "&cmd=%s" % cmd

        params = self._get_elink_params(**kargs)

        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass

        return ret

    def EPost(self, db, id, **kargs):
        """Accepts a list of UIDs from a given database,

        stores the set on the History Server, and responds with a query
        key and web environment for the uploaded dataset.

        :param str db: a valid database
        :param id: list of strings of strings

        :return: a dictionary with a Web Environment string
            and a QueryKey to be re-used in another EUtils.
        """
        self._check_db(db)
        sid = self._check_ids(id)

        params = self._get_epost_params(**kargs)

        query = "epost.fcgi/?db=%s&id=%s" % (db, sid)

        ret = self.http_get(query, None,  params=params)
        try: ret = ret.content
        except: pass
        ret = self.easyXML(ret)
        for item in ret.getchildren():
            if item.tag == 'QueryKey':
                query_key = item.text
            elif item.tag == 'WebEnv':
                webenv = item.text
        return {'WebEnv':webenv, 'QueryKey':query_key}



class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class EUtilsParser(AttrDict):
    """Convert xml returned by EUtils into a structure easier to manipulate

    Used by :meth:`EGQuery` method in EUtils class. Also by ESpell.
    """
    def __init__(self, xml):
        super(EUtilsParser, self).__init__()

        try:
            name = xml.root.tag
            self[name] = EUtilsParser(xml.root)
            children = []
            #children = xml.root.getchildren()[0].getchildren()
            #self.__name = xml.root.getchildren()[0].tag
        except:
            children = xml.getchildren()
            if len(children) == 0:
                self[xml.tag] = xml.text

        for i, child in enumerate(children):
            if len(child.getchildren()) == 0:
                self[child.tag] = child.text
            else:
                # This is probably a list then
                e = EUtilsParser(child)
                if child.tag not in self.keys():
                    self[child.tag] = e
                else:
                    try:
                        self[child.tag].append(e)
                    except:
                        self[child.tag] = [self[child.tag]]
                        self[child.tag].append(e)

                #self[child.tag] = []
                #for subchild in child.getchildren():
                #    self[child.tag].append(EUtilsParser(subchild))

    def __str__(self):
        name = self._EUtilsParser__name
        if name == "DbInfo":
            txt = ""
            for this in self.FieldList:
                txt += "{0:10}:{1}\n".format(this.Name, this.Description)
            return txt
        else:
            print("Not implemented for {0}".format(name))



