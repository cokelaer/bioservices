from bioservices.uniprot import *



class test_UniProt(UniProt):
    def __init__(self):
        super(test_UniProt, self).__init__(self)

    def test_mapping(self):
        res = self.mapping(fr="ACC", to="KEGG_ID", query='P43403')
        assert res == ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535']


