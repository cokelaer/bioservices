from bioservices.chembldb import *



class test_Chembl(Chembl):

    def __init__(self):
        super(test_Chembl, self).__init__(verbose=False)


    def test_api_status(self):
        self.api_status()

    def test_get_compound_by_ChemblId(self):
        self.get_compound_by_ChemblId("CHEMBL1")

    def test_get_target_uniprotId(self):
        self.get_target_by_uniprotId("Q00534")

    def _test_get_compound_activities(self):
        self.get_compound_activities("CHEMBL240")
