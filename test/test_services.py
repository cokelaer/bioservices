from bioservices.services import Service, WSDLService, RESTService, REST
from nose.plugins.attrib import attr

class test_Service(Service):
    def __init__(self):
        super(test_Service, self).__init__("test", "http://www.uniprot.org", verbose=False)
        self.url
        self.easyXMLConversion

    def test_easyXML(self):
        self.easyXML("<xml><id></id></xml>")

    @attr('skip')
    def test_pubmed(self):
        self.pubmed("24064416")


class test_WSDLService(WSDLService):
    def __init__(self):
        super(test_WSDLService, self).__init__("test",
            "http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl", 
            verbose=False)

    def test_methods(self):
        self.wsdl_methods



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
