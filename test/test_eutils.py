from bioservices import eutils




class test_EUtils(object):

    @classmethod
    def setup_class(klass):
        klass.e = eutils.EUtils(verbose=False)

    def test_taxonomy(self):
        ret = self.e.taxonomy("9606")
        assert ret.Taxon[0].TaxId == '9606'
        ret.Taxon[0].ScientificName

    def test_snp(self):
        self.e.snp("123")

    def test_databases(self):
        assert "proteinclusters" in self.e.databases

    def test_summary(self):
        ret = self.e.ESummary("taxonomy", "9606,9913")
        assert ret.DocSum[0].Id == '9606'
        assert ret.DocSum[1].Id == '9913'

        # test another database 
        assert self.e.ESummary("structure", "10000").DocSum[0].Id

    def _test_espell(self):
        ret = self.e.ESpell(db="omim", term="aasthma+OR+alergy")
        print(ret.Query)
        assert ret.Query == 'aasthma OR alergy'
        assert ret.CorrectedQuery == 'asthma or allergy'

    def test_elink(self):
        ret = self.e.ELink("pubmed", "pubmed", Ids="20210808", cmd="neighbor_score")


        ret = self.e.ELink("pubmed", "24064416")
        assert len(ret.LinkSet[0].LinkSetDb[0].Link) > 10

        self.e.ELink("nucleotide", "48819,7140345", db="protein")

    def test_einfo(self):
        dbinfo = self.e.EInfo("gtr")
        assert dbinfo.DbName ==  'gtr'
        assert dbinfo.MenuName == 'GTR'
        assert dbinfo.Description == 'GTR database'
        assert dbinfo.FieldList[0].Name == 'ALL'

        ret = self.e.EInfo("taxonomy")
        ret.Count

        alldbs = self.e.EInfo()
        for db in ['pubmed', 'genome', 'dbvar', 'gene']:
            assert db in alldbs
        assert len(alldbs) > 40 # 52 Aug 2014 but let us be on the safe side
    def test_einfo_pubmed(self):
        ret = self.e.EInfo('pubmed')
        assert ret.DbName == 'pubmed'
        assert ret.MenuName == 'PubMed'
        assert ret.Description == 'PubMed bibliographic record'
        assert int(ret.Count) >  17905967
        assert ret.LastUpdate
        assert len(ret.FieldList)>=40
        assert ret.FieldList[0]['Name']
        assert ret.FieldList[0]['FullName'], 'All Fields'
 
    def test_gquery(self):
        ret = self.e.EGQuery("asthma")
        [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem if x.Count!='0']

    def test_efetch(self):
        #ret = self.e.EFetch("omim", "269840")
        #ret1 = self.e.EFetch("sequences", "34577063", retmode="text", rettype="fasta", stand=1)
        #ret2 = self.e.EFetch("sequences", "34577063", retmode="text", rettype="fasta", stand=2)
        #self.e.EFetch("sequences", "34577063", retmode="text", rettype="fasta",strand=2,seq_start=10, seq_stop=20)


        ret = self.e.EFetch('pubmed', '12091962,9997',  retmode='xml', rettype='abstract')
        # sequences
        res1 = self.e.EFetch("sequences", "352, 234", retmode="text", rettype="fasta")
        res2 = self.e.EFetch("sequences", ["352", "234"], retmode="text", rettype="fasta")
        res3 = self.e.EFetch("sequences", [352, 234], retmode="text", rettype="fasta")
        assert res1 == res2
        assert res2 == res3
        assert res1 == res3

    def test_efetch_gene(self):
        res = self.e.EFetch('gene', 4747, retmode="text")
        assert 'neurofilament' in res
        res = self.e.EFetch('gene', 4747, retmode="xml")



    def test_epost(self):
        ret = self.e.EPost("pubmed", "20210808")
        assert ret.QueryKey
        print(ret)
        assert "ERROR" not in dict(ret).keys()

        ret = self.e.EPost("pubmed", "-1")
        assert ret.QueryKey
        assert "ERROR" in dict(ret).keys()


