from bioservices.uniprot import *



class test_UniProt(UniProt):
    def __init__(self):
        super(test_UniProt, self).__init__(self)

    def test_mapping(self):
        res = self.mapping(fr="ACC", to="KEGG_ID", query='P43403')
        assert res == ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535']

    def test_search(self):
        self.search("P09958", format="rdf")
        self.search("P09958", format="xml")
        self.search("P09958", format="txt")
        self.search("P09958", format="fasta")
        self.search("P09958", format="gff")

        try:
            self.search("P09958", format="dummy")
            assert False
        except:
            assert True


