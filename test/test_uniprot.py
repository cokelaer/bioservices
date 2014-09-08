from bioservices.uniprot import UniProt
from nose.plugins.attrib import attr


class test_UniProt(UniProt):
    def __init__(self):
        super(test_UniProt, self).__init__(verbose=False, cache=False)
        self.debugLevel = "ERROR"

    def test_mapping(self):
        res = self.mapping(fr="ACC+ID", to="KEGG_ID", query='P43403')
        assert res['P43403'] == ['hsa:7535']
        try:
            res = self.mapping(fr="AC", to="KEID", query='P434')
            assert False
        except:
            assert True

    @attr('slow')
    def test_searchUniProtId(self):
        self.searchUniProtId("P09958", frmt="rdf")
        self.searchUniProtId("P09958", frmt="xml")
        self.searchUniProtId("P09958", frmt="txt")
        self.searchUniProtId("P09958", frmt="fasta")
        self.searchUniProtId("P09958", frmt="gff")

        try:
            self.searchUniProtId("P09958", frmt="dummy")
            assert False
        except:
            assert True

    @attr('slow')
    def test_search(self):
        self.search('zap70+AND+organism:9606', frmt='list')
        self.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name,length,id, genes")
        self.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name")

        self.search("ZAP70_HUMAN", frmt="tab", columns="sequence", limit=1)

        self.quick_search("ZAP70")

    @attr('skip')
    def test_uniref(self):
        df = self.uniref("member:Q03063")
        df.Size

    @attr('skip')
    def test_get_df(self):
        df = self.get_df(["P43403"])

