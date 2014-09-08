from bioservices.wikipathway import  WikiPathways
from nose.plugins.attrib import attr

@attr('skip')
@attr('skip_travis')
class test_wiki(object):
    @classmethod
    def setup_class(klass):
        klass.s = WikiPathways(verbose=False)

    def test_organism(self):
        assert len(self.s.organisms)
        self.s.organism = 'Homo sapiens'
        assert self.s.organism == 'Homo sapiens'

        try:
            self.s.organism = 'Homo sapi'
            assert False
        except ValueError:
            assert True

    @attr('slow')
    def test_showPathwayInBrowser(self):
        self.s.showPathwayInBrowser("WP2320")

    @attr('slow')
    def test_listPathways(self):
        l = self.s.listPathways()
        assert len(l) > 40
        l = self.s.listPathways("Homo sapiens")
        assert len(l) > 40

    def test_getPathway(self):
        self.s.getPathway("WP2320")
    @attr('slow')
    def test_getPathwayInfo(self):
        self.s.getPathwayInfo("WP2320")

    @attr('slow')
    def test_getPathwayAs(self):
        res = self.s.getPathwayAs("WP4", filetype="txt")

    @attr('slow')
    def test_findPathwaysByText(self):
        res = self.s.findPathwaysByText(query="p53")
        res = self.s.findPathwaysByText(query="p53",species='Homo sapiens')
        len([x.score for x in res]) == len(res)
        assert len(self.s.findPathwaysByText(query="p53 OR mapk",species='Homo sapiens'))>0

    @attr('slow')
    def test_getOntologyTersmByPathway(self):
        res = self.s.getOntologyTermsByPathway("WP4")
        res[0].ontology

    @attr('slow')
    def test_getOntologyTermsByOntology(self):
        self.s.getOntologyTermsByOntology("Disease")

    @attr('slow')
    def test_getCurationTags(self):
        self.s.getCurationTags("WP4")

    @attr('slow')
    def test_getcurationTagByNames(self):
        self.s.getCurationTagsByName("Curation:Tutorial")

    @attr('slow')
    def test_findInteractions(self):
        self.s.findInteractions("P53")
        self.s.findInteractions("P53", interactionOnly=False)
        self.s.findInteractions("P53", raw=True)

    @attr('slow')
    def test_getRecentChanges(self):
        self.s.getRecentChanges(20120101000000)

    # does not seem to work
    @attr('slow')
    def test_findPathwayByXref(self):
        self.s.findPathwaysByXref('P45985')


    @attr('slow')
    def test_findPathwaysByLitterature(self):
        self.s.findPathwaysByLiterature(18651794)

    @attr('slow')
    def test_savePathwayAs(self):
        self.s.savePathwayAs("WP4", "test.pdf", display=False)
        import os
        try:os.remove("test.pdf")
        except:pass
    def test_getPathwaysByParentOntologyTerm(self):
        self.s.getPathwaysByParentOntologyTerm("DOID:344")


    def test_createPathway(self):
        try:
            self.s.createPathway("","")
            assert False
        except NotImplementedError:
            assert True


    def test_updatePathwa(self):
        try:
            self.s.updatePathway("","","")
            assert False
        except NotImplementedError:
            assert True

    def test_saveCurationTag(self):
        try:
            self.s.saveCurationTag("","","")
            assert False
        except NotImplementedError:
            assert True

    def test_login(self):
        try:
            self.s.login("dummy", "dummy")
            assert False
        except NotImplementedError:
            assert True
    def test_remoceCurationTag(self):
        try:
            self.s.removeCurationTag("dummy", "dummy")
            assert False
        except NotImplementedError:
            assert True

    def test_getPathwayHistory(self):
        _ = self.s.getPathwayHistory("WP455", "20100101000000")

    @attr('slow')
    def test_coloredPathway(self):
        _ = self.s.getColoredPathway("WP4",revision=0)



