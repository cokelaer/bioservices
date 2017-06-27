from bioservices.services import Service, WSDLService, RESTService, REST
import pytest


class test_Service(Service):
    def __init__(self):
        super(test_Service, self).__init__("test", "http://www.uniprot.org", verbose=False)
        self.url
        self.easyXMLConversion

    def test_easyXML(self):
        self.easyXML("<xml><id></id></xml>")

    def test_pubmed(self):
        self.pubmed("24064416")

def test_service():
    this = test_Service()
    this.test_easyXML()
    #this.test_pubmed()

class test_WSDLService(WSDLService):
    def __init__(self):
        super(test_WSDLService, self).__init__("test",
            "http://biomodels.caltech.edu/services/BioModelsWebServices?wsdl", 
            verbose=False)

    def test_methods(self):
        self.wsdl_methods

def test_wsdl():
    this = test_WSDLService()
    this.test_methods()


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


def test_rest():
    this = test_RESTService()
    this.test_request()
