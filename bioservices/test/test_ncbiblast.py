from bioservices import *


class test_nciblast(NCBIblast):
    def __init__(self):
        super(test_nciblast, self).__init__(verbose=False)

    def test_param(self):
        self.getParameters()
        assert(len(self.parameters)>0)
        assert(len(self.parameters)>0)

    def test_paramdetails(self):
        names = self.parametersDetails("matrix") 
