from bioservices.wikipathway import  Wikipath
import unittest


class TestRepGen(unittest.TestCase, Wikipath):
    @classmethod
    def setUpClass(self):
        self.s = Wikipath()




class test_wiki(TestRepGen):
    @classmethod
    def setUpClass(self):
        super(test_wiki, self).setUpClass()


    def test_organism(self):
        assert len(self.s.organisms)
        self.s.organism = 'Homo sapiens'
        assert self.s.organism == 'Homo sapiens'

        try:
            self.s.organism = 'Homo sapi'
            assert False
        except ValueError:
            assert True

    #@unittest.skip("test")
    def test_listPathways(self): 
        l = self.s.listPathways()
        len(l) > 40
        l = self.s.listPathways("Homo sapiens")
        len(l) > 40

    def test_getPathway(self):
        self.s.getPathway("WP2320")
    def test_getPathwayInfo(self):
        self.s.getPathwayInfo("WP2320")

    def _test_getPathwayAs(self):
        res = self.s.getPathwayAs("WP4", "txt")
        assert len(res)>0


    def test_findPathwaysByText(self):
        res = self.s.findPathwaysByText(query="p53",species='Homo sapiens')
        len([x.score for x in res]) == len(res)
        assert len(self.s.findPathwaysByText(query="p53 OR mapk",species='Homo sapiens'))>0

    def test_getOntologyTersmByPathway(self):
        res = self.s.getOntologyTermsByPathway("WP4")
        res[0].ontology

    def test_getOntologyTermsByOntology(self):
        self.s.getOntologyTermsByOntology("Disease")

    def test_getPathwaysByOntologyTerm(self):
        self.s.getPathwaysByOntologyTerm('DOID:344')


    def test_getPathwaysByParentOntologyTerm(self):
        self.s.getPathwaysByParentOntologyTerm("DOID:344")


    def test_getCurationTags(self):
        self.s.getCurationTags("WP4")

    def test_getcurationTagByNames(self):
        self.s.getCurationTagsByName("Curation:Tutorial")

    def test_findInteractions(self):
        self.s.findInteractions("P53")

    def test_getRecentChanges(self):
        self.s.getRecentChanges(20120101000000)

    def test_findPathwayByXref(self):
        self.s.findPathwaysByXref('P45985')


    def test_findPathwaysByLitterature(self):
        self.s.findPathwaysByLiterature(18651794)

    def test_savePathwayAs(self):
        self.s.savePathwayAs("WP4", "test.pdf", display=False)
        import os
        try:os.remove("test.pdf")
        except:pass
    def test_getPathwaysByParentOntologyTerm(self):
        self.s.getPathwaysByParentOntologyTerm("DOID:344")


    def test_remoceCurationTag(self):
        try:
            self.s.removeCurationTag("dummy", "dummy", "dummy")
            assert False
        except NotImplementedError:
            assert True

    def test_getPathwayHistory(self):
        res = self.s.getPathwayHistory("WP455", "20100101000000")

    def test_coloredPathway(self):
        res = self.getColoredPathway("WP4",revision=0)


