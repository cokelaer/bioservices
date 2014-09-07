from bioservices import ArrayExpress
from nose.plugins.attrib import attr


@attr('skip_travis')
class test_AE(object):

    @classmethod
    def setup_class(klass):
        klass.s = ArrayExpress(verbose=False)

    def test_retrieveFiles(self):
        #res = self.retrieveFiles(keywords="cancer+breast", species="Home+Sapiens")
        res = self.s.queryFiles(array="A-AFFY-33")

    def test_retrieveExperiments(self):
        #res = self.retrieveExperiments(keywords="cancer+breast", species="Home+Sapiens")

        #res = self.queryExperiments(array="A-AFFY-33")
        #assert len(res.getchildren())>0
        res = self.s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens",expdesign="dose+response")
        assert len(res.getchildren())>0
        res = self.s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens",expdesign="dosestupid")
        assert len(res.getchildren())==0
        res = self.s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens", expdesign="dose+response", 
            sortby="releasedate", sortorder="ascending")

    def test_retrieveFile(self):
        res = self.s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")
        self.s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt", save=True) 
        import os
        os.remove("E-MEXP-31.idf.txt")

        try:
            res == self.s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txtdddd")
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
        self.s.retrieveExperiment("E-MEXP-31")

    @attr('slow')
    def test_extra(self):
        # works. just takes 15 seconds so let us skip it.
        res = self.s.queryFiles(keywords="cancer+breast", wholewords=True)
        res = self.s.queryFiles(keywords="cancer+breast", wholewords=True, gxa="true")
        res = self.s.queryFiles(keywords="cancer+breast", wholewords=True, directsub="false")
