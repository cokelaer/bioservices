from bioservices import Miriam
import pytest
import os

pytestmark = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
         reason="On travis")



@pytest.fixture
def miriam():
    return Miriam(verbose=False)


def test_checkRegExp(miriam):
    assert miriam.checkRegExp("1P43403", "uniprot") == False
    assert miriam.checkRegExp("P43403", "uniprot") == True

def test_convertURL(miriam):
    assert miriam.convertURL("http://identifiers.org/ec-code/1.1.1.1") == 'urn:miriam:ec-code:1.1.1.1'

def test_convertURLs(miriam):
    miriam.convertURLs(['http://identifiers.org/pubmed/16333295', 'http://identifiers.org/ec-code/1.1.1.1'])

def test_convertURN(miriam):
    res = miriam.convertURN('urn:miriam:ec-code:1.1.1.1')
    assert res == 'http://identifiers.org/ec-code/1.1.1.1'

def test_convertURNs(miriam):
    res = miriam.convertURNs(['urn:miriam:ec-code:1.1.1.1'])
    assert res == ['http://identifiers.org/ec-code/1.1.1.1']

def test_getDataResources(miriam):
    miriam.getDataResources("uniprot")

def test_getDataTypeDef(miriam):
    miriam.getDataTypeDef("uniprot")

def test_getDataTypePattern(miriam):
    miriam.getDataTypePattern("uniprot")

def test_getDataTypeSynonyms(miriam):
    assert len(miriam.getDataTypeSynonyms("uniprot"))>0

def test_getDataTypeURI(miriam):
    assert miriam.getDataTypeURI("uniprot") == 'urn:miriam:uniprot'

def test_getDataTypeURIs(miriam):
    miriam.getDataTypeURIs("uniprot")
    ['urn:miriam:uniprot', 'urn:lsid:uniprot.org:uniprot', 'urn:lsid:uniprot.org', 'http://www.uniprot.org/']

def test_getDataTypesId(miriam):
    miriam.getDataTypesId()

def test_getDataTypesName(miriam):
    miriam.getDataTypesName()

def test_getJavaLibraryVersion(miriam):
    miriam.getJavaLibraryVersion()

def test_getLocation(miriam):
    miriam.getLocation("UniProt", "MIR:00100005")
    miriam.getLocations("urn:miriam:obo.go:GO%3A0045202")


def test_getLocations(miriam ):
    miriam.getLocations("UniProt","P62158")
    #>>> m.serv.getLocations("urn:miriam:obo.go:GO%3A0045202")

def test_getLocationsWithToken(miriam):
    miriam.getLocationsWithToken("uniprot", "P43403")

def test_getMiriamURI(miriam):
    res = miriam.getMiriamURI("http://www.ebi.ac.uk/chebi/#CHEBI:17891")
    assert res == 'urn:miriam:chebi:CHEBI%3A17891'

def test_getName(miriam):
    miriam.getName('uniprot')

def test_getNames(miriam):
    miriam.getNames('uniprot')

def test_getOfficialDataTypeURI(miriam):
    miriam.getOfficialDataTypeURI("chEBI")
    #'urn:miriam:chebi'

def test_getResourceInfo(miriam):
    res = miriam.getResourceInfo("MIR:00100005")
    assert res == 'MIRIAM Resources (data collection)'

def test_getResourceInstitution(miriam):
    res = miriam.getResourceInstitution("MIR:00100005")
    assert res == "European Bioinformatics Institute, Hinxton, Cambridge"

def test_getResourceLocation(miriam):
    res = miriam.getResourceLocation("MIR:00100005")
    assert res == "UK"

def test_getServicesInfo(miriam):
    miriam.getServicesInfo()

def test_getServicesVersion(miriam):
    miriam.getServicesVersion()

def test_getURI(miriam):
    res = miriam.getURI("UniProt", "P62158")
    assert res == 'urn:miriam:uniprot:P62158'

def test_getURIs(miriam):
    res = miriam.getURIs("UniProt", "P62158")

def test_isDeprecated(miriam):
    miriam.isDeprecated("urn:miriam:uniprot")

