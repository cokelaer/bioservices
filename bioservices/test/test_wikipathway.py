from bioservices.wikipathway import  Wikipath


class test_wiki(Wikipath):
    def __init__(self):
        super(test_wiki, self).__init__()
        assert len(self.organisms)

    def test_init(self):
        self.serv = Wikipath()


    def test_listPathways(self): 
        l = self.listPathways()
        len(l) > 400


    def test_findPathwaysByText(self):
        res = self.findPathwaysByText('MTOR')
        len([x.score for x in res]) == len(res)

    def test_getPathwayInfo(self):
        self.getPathwayInfo("WP2320")

    def test_getPathwayAs(self):
        res = self.getPathwayAs("WP4", "txt")
        assert len(res)>0

    def test_findPathwaysByText(self):
        assert len(self.serv.findPathwaysByText(query="p53",species='Homo sapiens'))>0
        assert len(self.findPathwaysByText(query="p53 OR mapk",species='Homo sapiens'))>0
