from bioservices import eutils




class test_EUtils(object):

    @classmethod
    def setup_class(klass):
        klass.e = eutils.EUtils(verbose=False)

    def test_taxonomy(self):
        ret = self.e.taxonomy_summary("9606")
        assert ret['9606']['taxid'] == 9606

    def test_snp(self):
        self.e.snp_summary("123")

    def test_databases(self):
        assert "proteinclusters" in self.e.databases

    def test_summary(self):
        ret = self.e.ESummary("taxonomy", "9606,9913")
        assert ret['9606']['taxid'] == 9606
        assert ret['9913']['taxid'] == 9913

        # test another database 
        ret = self.e.ESummary("structure", "10000")
        assert ret['10000']['pdbacc'] == '1CA4'

    def test_espell(self):
        ret = self.e.ESpell(db="omim", term="aasthma+OR+alergy")
        ret = ret.eSpellResult
        print(ret.Query)
        assert ret.Query == 'aasthma OR alergy'
        assert ret.CorrectedQuery == 'asthma or allergy'

    def test_elink(self):
        ret = self.e.ELink(db="pubmed", dbfrom="pubmed", id="20210808", 
                cmd="neighbor_score")

        ret = self.e.ELink(db="pubmed", id="24064416")

        #assert len(ret.LinkSet[0].LinkSetDb[0].Link) > 10

        self.e.ELink(dbfrom="nucleotide", id="48819,7140345", db="protein")

    def test_einfo(self):
        # Use XML
        dbinfo = self.e.EInfo("gtr", retmode='xml')
        dbinfo = self.e.parse_xml(dbinfo, 'EUtilsParser').eInfoResult
        dbinfo = dbinfo.DbInfo
        assert dbinfo.DbName ==  'gtr'
        assert dbinfo.MenuName == 'GTR'
        assert dbinfo.Description == 'GTR database'
        assert dbinfo.FieldList.Field[0].Name == 'ALL'

        # use JSON
        ret = self.e.EInfo("taxonomy")
        ret['count']

        alldbs = self.e.EInfo()
        for db in ['pubmed', 'genome', 'dbvar', 'gene']:
            assert db in alldbs
        assert len(alldbs) > 40 # 52 Aug 2014 but let us be on the safe side

    def test_einfo_pubmed(self):
        ret = self.e.EInfo('pubmed')
        assert ret['dbname'] == 'pubmed'
        assert ret['menuname'] == 'PubMed'
        assert ret['description'] == 'PubMed bibliographic record'
        assert int(ret['count']) > 17905967
        assert ret['lastupdate']
        assert len(ret['fieldlist']) >= 40
        assert ret['fieldlist'][0]['name'] == 'ALL'
        assert ret['fieldlist'][0]['fullname'], 'All Fields'
 
    def test_gquery(self):
        ret = self.e.EGQuery("asthma")
        [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem 
                if x.Count!='0']

    def test_efetch(self):
        ret = self.e.EFetch("omim", "269840")
        ret1 = self.e.EFetch("protein", "34577063", 
                retmode="text", rettype="fasta", stand=1)
        ret2 = self.e.EFetch("protein", "34577063", 
                retmode="text", rettype="fasta", stand=2)
        self.e.EFetch("protein", "34577063", 
                retmode="text", rettype="fasta",strand=2,
                seq_start=10, seq_stop=20)


        ret = self.e.EFetch('pubmed', '12091962,9997',  
                retmode='xml', rettype='abstract')
        # sequences
        res1 = self.e.EFetch("protein", "352, 234", 
                retmode="text", rettype="fasta")
        res2 = self.e.EFetch("protein", ["352", "234"], 
                retmode="text", rettype="fasta")
        res3 = self.e.EFetch("protein", [352, 234], 
                retmode="text", rettype="fasta")

        assert res1 == res2
        assert res2 == res3
        assert res1 == res3

    def test_efetch_gene(self):
        res = self.e.EFetch('gene', 4747, retmode="text")
        assert b'neurofilament' in res
        res = self.e.EFetch('gene', 4747, retmode="xml")

    def test_epost(self):
        ret = self.e.EPost("pubmed", "20210808")
        assert ret['QueryKey']
        assert ret['WebEnv']
        print(ret)



