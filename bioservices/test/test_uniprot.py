from bioservices.uniprot import *


class test_UniProt(UniProt):
    def __init__(self):
        super(test_UniProt, self).__init__(verbose=False)
        self.debugLevel = "ERROR"

    def test_mapping(self):
        res = self.mapping(fr="ACC+ID", to="KEGG_ID", query='P43403')
        print res
        assert res == {'P43403':['hsa:7535']}
        try: 
            res = self.mapping(fr="AC", to="KEID", query='P434')
            assert False
        except:
            assert True

    def test_searchUniProtId(self):
        self.searchUniProtId("P09958", format="rdf")
        self.searchUniProtId("P09958", format="xml")
        self.searchUniProtId("P09958", format="txt")
        self.searchUniProtId("P09958", format="fasta")
        self.searchUniProtId("P09958", format="gff")

        try:
            self.searchUniProtId("P09958", format="dummy")
            assert False
        except:
            assert True

    def test_search(self):
        self.search('zap70+AND+organism:9606', format='list')
        self.search("zap70+and+taxonomy:9606", format="tab", limit=3, columns="entry name,length,id, genes")
        self.search("zap70+and+taxonomy:9606", format="tab", limit=3, columns="entry name")

        self.search("ZAP70_HUMAN", format="tab", columns="sequence", limit=1)

        self.quick_search("ZAP70")


    def test_uniref(self):
        df = self.uniref("member:Q03063")
        df.Size

    def test_get_df(self):
        df = self.get_df(["P43403"])


