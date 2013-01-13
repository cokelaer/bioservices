from bioservices.wsdbfetch import * 



class test_WSDbfetch(WSDbfetch):
    def __init__(self):
        super(test_WSDbfetch, self).__init__(verbose=False)

    def test_getSupportedDBs(self):
        res = self.getSupportedDBs()
        res = self.getSupportedDBs()
        assert len(res) >10

    def test_getSupportedFormats(self):
        res = self.getSupportedFormats()
        res = self.getSupportedFormats()
        assert len(res) >10

    def test_getSupportedStyles(self):
        res = self.getSupportedStyles()
        res = self.getSupportedStyles()
        assert len(res) >10

    def test_fetchBatch(self):
        self.fetchBatch("uniprot" ,"wap_mouse", "xml") 

    def test_fetchData(self):
        self.fetchData('uniprot:zap70_human')

    def test_getDatabaseInfo(self):
        res = self.getDatabaseInfo("uniprotkb")
        assert res.displayName == 'UniProtKB'

    def test_getDatabaseInfoList(self):
        assert len(self.getDatabaseInfoList())>10

    def test_getDatavaseInfoList(self):
        self.getDatabaseInfoList()

    def test_getDbFormats(self):
        self.getDbFormats("uniprotkb")

    def test_getFormat(self):
        assert self.getFormatStyles("uniprotkb", "fasta") >= 3
        #['default', 'raw', 'html']

    def test_wrong_db(self):
        try:
            self.getDbFormats("uniprot")
            assert False
        except:
            assert True
        
