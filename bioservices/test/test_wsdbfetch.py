from bioservices.wsdbfetch import * 



class test_WSDbfetch(WSDbfetch):
    def __init__(self):
        super(test_WSDbfetch, self).__init__()

    def test_getSupportedDBs(self):
        res = self.getSupportedDBs()
        assert len(res) >10

