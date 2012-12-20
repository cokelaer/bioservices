from bioservices.rhea import Rhea



class test_rhea():
    def __init__(self):

        self.s = Rhea()

    def test_search(self):
        r1 = self.s.search("caffeine", format="cmlreact")
        r2 = self.s.search("caffeine", format="biopax2")
        try:
            self.s.search("caffeine", format="biopaxddddddd2")
            assert False
        except:
            assert True

    def test_entry_cmlreact(self):
        self.s.entry(10280, "cmlreact")
    def test_entry_biopax2(self):
        self.s.entry(10280, "biopax2")
    def test_entry_rxn(self):
        self.s.entry(10090, "rxn")






