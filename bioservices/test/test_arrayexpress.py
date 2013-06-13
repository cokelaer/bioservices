from bioservices import ArrayExpress
import unittest



"""class test_AE(object):
    @classmethod
    def setup_class(klass):
        klass.e = ArrayExpress(verbose=False)
"""

class test_AE(ArrayExpress):
    def __init__(self):
        super(test_AE, self).__init__()

    @unittest.skip
    def test_retrieveFiles(self):
        #res = self.retrieveFiles(keywords="cancer+breast", species="Home+Sapiens")
        res = self.queryFiles(array="A-AFFY-33")

    def test_retrieveExperiments(self):
        #res = self.retrieveExperiments(keywords="cancer+breast", species="Home+Sapiens")

        #res = self.queryExperiments(array="A-AFFY-33")
        #assert len(res.getchildren())>0
        res = self.queryExperiments(array="A-AFFY-33", species="Homo%20Sapiens",expdesign="dose+response")
        assert len(res.getchildren())>0
        res = self.queryExperiments(array="A-AFFY-33", species="Homo%20Sapiens",expdesign="dosestupid")
        assert len(res.getchildren())==0
        res = self.queryExperiments(array="A-AFFY-33", species="Homo%20Sapiens", expdesign="dose+response", 
            sortby="releasedate", sortorder="ascending")

    def test_retrieveFile(self):
        res = self.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")
        self.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt", save=True) 
        import os
        os.remove("E-MEXP-31.idf.txt")

        try:
            res = self.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txtdddd")
            assert False
        except:
            pass

    def test_format(self):
        self.format = "json"
        self.format = "xml"
        try:
            self.format = "dummy"
            assert False
        except:
            assert True

    def test_retrieveExperiment(self):
        self.retrieveExperiment("E-MEXP-31")

    @unittest.skip
    def test_extra(self):
        # works. just takes 15 seconds so let us skip it.
        res = self.e.queryFiles(keywords="cancer+breast", wholewords=True)
        res = self.e.queryFiles(keywords="cancer+breast", wholewords=True, gxa="true")
        res = self.e.queryFiles(keywords="cancer+breast", wholewords=True, directsub="false")
