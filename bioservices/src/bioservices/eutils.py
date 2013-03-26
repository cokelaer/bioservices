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

"""
    Help

This chapter first describes the general function and use of the eight E-utilities, followed by basic usage guidelines and requirements, and concludes with a discussion of how the E-utilities function within the Entrez system.
Go to:
Usage Guidelines and Requirements
Use the E-utility URL

All E-utility requests should be made to URLs beginning with the following string:

http://eutils.ncbi.nlm.nih.gov/entrez/eutils/

These URLs direct requests to servers that are used only by the E-utilities and that are optimized to give users the best performance.

When constructing URLs for the E-utilities, please use lowercase characters for all parameters except &WebEnv. There is no required order for the URL parameters in an E-utility URL, and null values or inappropriate parameters are generally ignored. Avoid placing spaces in the URLs, particularly in queries. If a space is required, use a plus sign (+) instead of a space:

Incorrect: &id=352, 25125, 234
Correct:   &id=352,25125,234

Incorrect: &term=biomol mrna[properties] AND mouse[organism]
Correct:   &term=biomol+mrna[properties]+AND+mouse[organism]

Other special characters, such as quotation marks (") or the # symbol used in referring to a query key on the History server, should be represented by their URL encodings (%22 for "; %23 for #).

Incorrect: &term=#2+AND+"gene in genomic"[properties]
Correct:   &term=%232+AND+%22gene+in+genomic%22[properties]

Go to:
The Eight E-utilities in Brief
EInfo (database statistics)

eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi

Provides the number of records indexed in each field of a given database, the date of the last update of the database, and the available links from the database to other Entrez databases.
ESearch (text searches)

eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi

Responds to a text query with the list of matching UIDs in a given database (for later use in ESummary, EFetch or ELink), along with the term translations of the query.
EPost (UID uploads)

eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi

Accepts a list of UIDs from a given database, stores the set on the History Server, and responds with a query key and web environment for the uploaded dataset.
ESummary (document summary downloads)

eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi

Responds to a list of UIDs from a given database with the corresponding document summaries.
EFetch (data record downloads)

eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi

Responds to a list of UIDs in a given database with the corresponding data records in a specified format.
ELink (Entrez links)

eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi

Responds to a list of UIDs in a given database with either a list of related UIDs (and relevancy scores) in the same database or a list of linked UIDs in another Entrez database; checks for the existence of a specified link from a list of one or more UIDs; creates a hyperlink to the primary LinkOut provider for a specific UID and database, or lists LinkOut URLs and attributes for multiple UIDs.
EGQuery (global query)

eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi

Responds to a text query with the number of records matching the query in each Entrez database.
ESpell (spelling suggestions)

eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi

Retrieves spelling suggestions for a text query in a given database."""



# Although the wsdl are different, the efetch address can be used indiferently
# so efetch_taxon can be used to request any sql
class EFetch(WSDLService):
    def __init__(self,verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_taxon.wsdl"
        super(EFetch, self).__init__(name="EUtilsTaxon", verbose=verbose, url=url)

    def efetch(self, db, Id):
        ret = self.serv.run_eFetch(db=db, id=Id)
        return ret

class EUtilsPubmed(WSDLService):
    def __init__(self,verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_taxon.wsdl"
        super(EUtilsPubmed, self).__init__(name="EUtilsTaxon", verbose=verbose, url=url)

    def run_eFetch(self, db, Id):
        ret = self.serv.run_eFetch(db=db, id=Id)
        return ret


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



    """



    def __init__(self, verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/eutils.wsdl?"
        super(EUtils, self).__init__(name="EUtils", verbose=verbose, url=url)


        self._databases = None
        # some extra links
        self._efetch_taxonomy = EUtilsTaxon(verbose=verbose)
        self._efetch_snp = EUtilsSNP(verbose=verbose)
        self._efetch = EFetch(verbose=verbose)

    def _get_databases(self):
        """alias to run_eInfo"""
        if self._databases == None:
            self._databases = self.serv.run_eInfo().DbName
        return self._databases
    databases = property(_get_databases, doc="alias to run_eInfo()")

    def taxonomy(self, Id):
        """

            >>> ret = e.taxonomy("9606")
            >>> ret.Taxon.TaxId
            '9606'
            >>> ret.Taxon.ScientificName
            'Homo sapiens'
        """
        ret = self._efetch_taxonomy.serv.run_eFetch(db="taxonomy", id=Id)
        return ret 

    def snp(self, Id):
        """
            s.snp("123")
        """
        ret = self._efetch_snp.run_eFetch(Id)
        return ret

    def efetch(self, db, Id):
        """ret = e.efetch("omim", "269840")  --> ZAP70


        """
        ret = self._efetch.efetch(db,Id)
        return ret

    def run_eInfo(self, db=None):
        """Provides the number of records indexed in each field of a given
        database, the date of the last update of the database, and the available links
        from the database to other Entrez databases.

            >>> s.run_eInfo("taxonomy")
            >>> s.Count

        """
        if db == None or db not in self.databases:
            print("You must provide a valid databases from : ", self.databases)
            return
        return self.serv.run_eInfo(db=db) 

    def run_eSummary(self, db, Id):
        """eSummary functionalities

        Returns document summaries (DocSums) for a list of input UIDs
        OR returns DocSums for a set of UIDs stored on the Entrez History server


            >>> ret = s.serv.run_eSummary("snp","7535")
            >>> ret = s.serv.run_eSummary("snp","7535,7530")
            >>> ret = s.run_eSummary("taxonomy", "9606,9913")
            
        """

        # assert db in ??
        ret = self.serv.run_eSummary(db=db, id=Id)
        return ret

    def run_eGQuery(self, term):
        """Provides the number of records retrieved in all Entrez databases by a single text query. 

        :param str term: Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the PubMed or Entrez help for information about search field descriptions and tags. Search fields and tags are database specific.

        [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem if x.Count!='0']

        """
        ret = self.serv.run_eGQuery(term)


    def run_eSpell(self, db, term):
        """Provides spelling suggestions for terms within a single text query in a given database.


        :param str db: Database to search. Value must be a valid Entrez database name (default = pubmed).
        :param str term: Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the PubMed or Entrez help for information about search field descriptions and tags. Search fields and tags are database specific.


        >>> ret = e.serv.run_eSpell(db="omim", term="aasthma+OR+alergy")
        >>> ret.CorrectedQuery
        'asthma or allergy'
        """
        ret = self.serv.run_eSpell(db=db, term=term)
        return ret

"""
 u'run_eLink',  a complicated function
 u'run_ePost',
rFetch : in progress
 u'run_eSearch',
 u'run_eSummary']   in progress

"""

