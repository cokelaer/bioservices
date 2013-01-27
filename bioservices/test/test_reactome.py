from bioservices.reactome import Reactome
import unittest


class test_reactome(Reactome):
    def __init__(self):
        super(test_reactome, self).__init__(verbose=False)

    @unittest.skip
    def test_queryPathwaysForReferenceIdentifiers(self):
        self.queryPathwaysForReferenceIdentifiers(["Q9Y266", "P17480", "P20248"])

    def _test_generatePathwayDiagramInSVG(self):
        return self.generatePathwayDiagramInSVG(Id)


    def test_listTopLevelPathways(self):
        self.listTopLevelPathways()




