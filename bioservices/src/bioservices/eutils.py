"""

http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch

http://www.ncbi.nlm.nih.gov/books/NBK25500/#chapter1.Demonstration_Programs



"""

from bioservices import WSDLService


# Although the wsdl are different, the efetch address can be used indiferently
# so efetch_taxon can be used to request any sql
class EFetch(WSDLService):
    def __init__(self,verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/efetch_taxon.wsdl"
        super(EFetch, self).__init__(name="EUtilsTaxon", verbose=verbose, url=url)

    def efetch(self, db, Id):
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
    def __init__(self, verbose=False):
        url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/soap/v2.0/eutils.wsdl?"
        super(EUtils, self).__init__(name="EUtils", verbose=verbose, url=url)

        # some extra links
        self._efetch_taxonomy = EUtilsTaxon(verbose=verbose)
        self._efetch_snp = EUtilsSNP(verbose=verbose)
        self._efetch = EFetch(verbose=verbose)

    def info(self):
        """alias to run_einfo"""
        return self.serv.run_eInfo()

    def databases(self):
        """alias to run_einfo"""
        ret = self.serv.run_eInfo()
        return ret.DbName

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

    def run_einfo(self, db):
        return self.serv.run_eInfo()    

    def run_eSummary(self, db, Id):
        """eSummary functionalities

        Returns document summaries (DocSums) for a list of input UIDs
        OR returns DocSums for a set of UIDs stored on the Entrez History server


        ret = e.serv.run_eSummary(db="snp",id="7535")
        """

        # assert db in ??
        ret = e.serv.run_eSummary(db=db, id=Id)

        """if isinstance(idlist, list):
            idlist = ",".join([x for x in idlist])
        elif isinstance(idlist, str):
            pass
        else:
            raise NotImplementedError
        request = "db=%s&id=%s&version=%s" % (db, idlist,version)
        res = self.serv.run_eSummary(request)

        """

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

