from bioservices.wikipathway import  Wikipath


class test_wiki(Wikipath):
    def __init__(self):
        super(test_wiki, self).__init__()

    def test_init(self):
        self.serv = Wikipath()


    def test_listPathways(self): 
        l = self.serv.listPathways()
        len(l) > 400


