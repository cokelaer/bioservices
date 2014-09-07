from bioservices.rhea import Rhea
from nose.plugins.attrib import attr


@attr('skip_travis')
class test_rhea(Rhea):
    def __init__(self):
        super(test_rhea, self).__init__(verbose=False)

    def test_search(self):
        r1 = self.search("caffeine")
        r1 = self.search("caffeine", frmt="cmlreact")
        r2 = self.search("caffeine", frmt="biopax2")
        try:
            self.search("caffeine", frmt="biopaxddddddd2")
            assert False
        except:
            assert True

    def test_entry_cmlreact(self):
        self.entry(10280, "cmlreact")

    def test_entry_biopax2(self):
        self.entry(10280, "biopax2")

    def test_entry_rxn(self):
        self.entry(10090, "rxn")

    def test_entry_badformat(self):
        try:
            self.entry(10090, "ggg")
            assert False
        except:
            assert True





