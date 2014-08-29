from bioservices.services import *


class test_Service(Service):
    def __init__(self):
        super(test_Service, self).__init__("test", "http://www.uniprot.org", verbose=False)
        self.url
        self.easyXMLConversion

    def test_easyXML(self):
        self.easyXML("<xml><id></id></xml>")

    def test_urlencode(self):
        res = self.urlencode({'a':1, 'b':2})
        assert res in ["a=1&b=2", "b=2&a=1"]

    def test_pubmed(self):
        self.pubmed("http://www.ncbi.nlm.nih.gov/pubmed/19693079")


class test_WSDLService(WSDLService):
    def __init__(self):
        super(test_WSDLService, self).__init__("test",
            "http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl", 
            verbose=False)

    def test_methods(self):
        self.methods
    def test_dump(self):
        self.dumpOut
        self.dumpIn
        self.dumpOut = 1
        self.dumpIn = 1



class test_RESTService(RESTService):
    def __init__(self):
        super(test_RESTService, self).__init__("test",
            "http://www.uniprot.org", 
            verbose=False)

    def test_request(self):
        try:
            self.request("dummy")
            assert False
        except:
            assert True
