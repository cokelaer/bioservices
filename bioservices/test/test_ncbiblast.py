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
        try:
            names = self.parametersDetails("matrixddddd") 
            assert False
        except:
            assert True

    def test_run(self):

        try:
            self.jobid = self.run(program="blastp", sequence=self._sequence_example,
                stype="protein", database="uniprotkb")
            assert False # missing argument
        except:
            assert True
        self.jobid = self.run(program="blastp", sequence=self._sequence_example,
            stype="protein", database="uniprotkb", email="name@test.org",
            matrix="BLOSUM45")
        res = self.getResult(self.jobid, "out")

        res = self.getResultTypes(self.jobid)

    def test_attributse(self):
        self.databases
