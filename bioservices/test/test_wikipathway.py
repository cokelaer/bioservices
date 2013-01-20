from bioservices.wikipathway import  Wikipath


class test_wiki(Wikipath):
    def __init__(self):
        super(test_wiki, self).__init__()

    def test_organism(self):
        assert len(self.organisms)
        self.organism = 'Homo sapiens'
        assert self.organism == 'Homo sapiens'

        try:
            self.organism = 'Homo sapi'
            assert False
        except ValueError:
            assert True
            
    def test_listPathways(self): 
        l = self.listPathways()
        len(l) > 40
        l = self.listPathways("Homo sapiens")
        len(l) > 40

    def test_getPathwayInfo(self):
        self.getPathwayInfo("WP2320")

    def test_getPathwayAs(self):
        res = self.getPathwayAs("WP4", "txt")
        assert len(res)>0

    def test_findPathwaysByText(self):
        res = self.findPathwaysByText(query="p53",species='Homo sapiens')
        len([x.score for x in res]) == len(res)
        assert len(self.findPathwaysByText(query="p53 OR mapk",species='Homo sapiens'))>0

    def test_getOntologyTersmByPathway(self):
        res = self.getOntologyTermsByPathway("WP4")
        res[0].ontology

    def test_getOntologyTermsByOntology(self):
        self.getOntologyTermsByOntology("Disease")

    def test_getPathwaysByOntologyTerm(self):
        self.getPathwaysByOntologyTerm('DOID:344')


    def test_getPathwaysByParentOntologyTerm(self):
        self.getPathwaysByParentOntologyTerm("DOID:344")


    def test_getCurationTags(self):
        self.getCurationTags("WP4")

    def test_getcurationTagByNames(self):
        self.getCurationTagsByName("Curation:Tutorial")

    def test_findInteractions(self):
        self.findInteractions("P53")

    def test_getRecentChanges(self):
        self.getRecentChanges(20120101000000)

    def test_findPathwayByXref(self):
        self.findPathwaysByXref('P45985')


    def test_findPathwaysByLitterature(self):
        self.findPathwaysByLiterature(18651794)

    def test_savePathwayAs(self):
        self.savePathwayAs("WP4", "test.pdf", display=False)
        import os
        try:os.remove("test.pdf")
        except:pass
    def test_getPathwaysByParentOntologyTerm(self):
        self.getPathwaysByParentOntologyTerm("DOID:344")


    def test_remoceCurationTag(self):
        try:
            self.removeCurationTag("dummy", "dummy", "dummy")
            assert False
        except NotImplementedError:
            assert True
        
