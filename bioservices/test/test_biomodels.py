from bioservices import biomodels




class test_biomodels():


    def __init__(self):
        self.serv = biomodels.BioModels()

    def test_size(self):

        L1 = len(self.serv.getAllCuratedModelsId())
        L2 = len(self.serv.getAllNonCuratedModelsId())
        L = len(self.serv)
        assert L == L1+L2


