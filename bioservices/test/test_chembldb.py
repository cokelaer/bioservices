from bioservices.chembldb import *



class test_Chembl(Chembl):

    def __init__(self):
        super(test_Chembl, self).__init__()


    def test_api_status(self):
        self.api_status()

    def test_get_compound_by_ChemblId(self):
        self.get_compound_by_ChemblId("CHEMBL1")

