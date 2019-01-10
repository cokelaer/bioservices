from bioservices.services import Service, WSDLService,  REST
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

#version 1.6.0  the example service does not work anymore and WSDL services are
# closing down so let us remove this test
"""
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
"""

class test_REST(REST):
    def __init__(self):
        super(test_REST, self).__init__("test",
            "http://www.uniprot.org", 
            verbose=False)

    def test_request(self):
        try:
            self.request("dummy")
            assert False
        except:
            assert True


def test_rest():
    this = test_REST()
    this.test_request()
