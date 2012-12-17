from bioservices import uniprot



class test_UniProt(object):
    def __init__(self):
       self.u = uniprot.UniProt()

    def test_mapping(self):
        res = self.u.mapping(fro="ACC", to="KEGG_ID", query='P43403')
        assert res.split() == ['From', 'To', 'P43403', 'hsa:7535']

