from bioservices import eutils




class test_EUtils(object):

    @classmethod
    def setup_class(klass):
        klass.e = eutils.EUtils(verbose=True)

    def test_espell(self):
        ret = self.e.serv.run_eSpell(db="omim", term="aasthma+OR+alergy")
        assert ret.CorrectedQuery == 'asthma or allergy'

    def test_taxonomy(self):
        ret = self.e.taxonomy("9606")
        ret.Taxon.TaxId
        ret.Taxon.ScientificName

    def test_snp(self):
        self.e.snp("123")


    def test_databases(self):
        assert "protein" in self.e.databases


    def test_summary(self):
        ret = self.e.ESummary("taxonomy", "9606,9913")


    def test_espell(self):
        ret = self.e.ESpell(db="omim", term="aasthma+OR+alergy")
        print ret.Query
        assert ret.Query == 'aasthma OR alergy'
        assert ret.CorrectedQuery == 'asthma or allergy'

    def test_elink(self):
        ret = self.e.ELink("pubmed", "pubmed", Ids="20210808", cmd="neighbor_score")

    def test_einfo(self):
        ret = self.e.EInfo("taxonomy")
        ret.Count

    def test_gquery(self):
        ret = self.e.EGquery("asthma")
        [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem if x.Count!='0']

    def test_efetch(self):
        ret = self.e.EFetch("omim", "269840")


        ret1 = self.e.EFetch("sequences", "34577063", retmode="text", rettype="fasta", stand=1)
        ret2 = self.e.EFetch("sequences", "34577063", retmode="text", rettype="fasta", stand=2)
        self.e.EFetch("sequences", "34577063", retmode="text", rettype="fasta",strand=2,seq_start=10, seq_stop=20)
