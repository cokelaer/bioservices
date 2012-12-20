from bioservices.wikipathway import  Wikipath


class test_wiki(object):
    def __init__(self):
        self.test_init()

    def test_init(self):
        self.serv = Wikipath()


    def test_listPathways(self): 
        l = self.serv.listPathways()
        len(l) > 400


