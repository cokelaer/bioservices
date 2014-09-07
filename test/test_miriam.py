from bioservices import Miriam
from nose.plugins.attrib import attr


@attr('skip_travis')
class test_miriam(Miriam):

    def __init__(self):
        super(test_miriam, self).__init__(verbose=False)

    def test_checkRegExp(self):
        assert self.checkRegExp("1P43403", "uniprot") == False
        assert self.checkRegExp("P43403", "uniprot") == True

    def test_convertURL(self):
        assert self.convertURL("http://identifiers.org/ec-code/1.1.1.1") == 'urn:miriam:ec-code:1.1.1.1'

    def test_convertURLs(self):
        self.convertURLs(['http://identifiers.org/pubmed/16333295', 'http://identifiers.org/ec-code/1.1.1.1'])

    def test_convertURN(self):
        res = self.convertURN('urn:miriam:ec-code:1.1.1.1')
        assert res == 'http://identifiers.org/ec-code/1.1.1.1'

    def test_convertURNs(self):
        res = self.convertURNs(['urn:miriam:ec-code:1.1.1.1'])
        assert res == ['http://identifiers.org/ec-code/1.1.1.1']

    def test_getDataResources(self):
        self.getDataResources("uniprot")

    def test_getDataTypeDef(self):
        self.getDataTypeDef("uniprot")

    def test_getDataTypePattern(self):
        self.getDataTypePattern("uniprot")

    def test_getDataTypeSynonyms(self):
        assert len(self.getDataTypeSynonyms("uniprot"))>0

    def test_getDataTypeURI(self):
        assert self.getDataTypeURI("uniprot") == 'urn:miriam:uniprot'

    def test_getDataTypeURIs(self):
        self.getDataTypeURIs("uniprot")
        ['urn:miriam:uniprot', 'urn:lsid:uniprot.org:uniprot', 'urn:lsid:uniprot.org', 'http://www.uniprot.org/']

    def test_getDataTypesId(self):
        self.getDataTypesId()

    def test_getDataTypesName(self):
        self.getDataTypesName()

    def test_getJavaLibraryVersion(self):
        self.getJavaLibraryVersion()

    def test_getLocation(self):
        self.getLocation("UniProt", "MIR:00100005")
        self.getLocations("urn:miriam:obo.go:GO%3A0045202")


    def test_getLocations(self ):
        self.getLocations("UniProt","P62158")
        #>>> m.serv.getLocations("urn:miriam:obo.go:GO%3A0045202")

    def test_getLocationsWithToken(self):
        self.getLocationsWithToken("uniprot", "P43403")

    def test_getMiriamURI(self):
        res = self.getMiriamURI("http://www.ebi.ac.uk/chebi/#CHEBI:17891")
        assert res == 'urn:miriam:chebi:CHEBI%3A17891'

    def test_getName(self):
        self.getName('uniprot')

    def test_getNames(self):
        self.getNames('uniprot')
    
    def test_getOfficialDataTypeURI(self):
        self.getOfficialDataTypeURI("chEBI")
        #'urn:miriam:chebi'

    def test_getResourceInfo(self):
        res = self.getResourceInfo("MIR:00100005")
        assert res == 'MIRIAM Resources (data collection)'

    def test_getResourceInstitution(self):
        res = self.getResourceInstitution("MIR:00100005")
        assert res == "European Bioinformatics Institute"

    def test_getResourceLocation(self):
        res = self.getResourceLocation("MIR:00100005")
        assert res == "United Kingdom"

    def test_getServicesInfo(self):
        self.getServicesInfo()

    def test_getServicesVersion(self):
        self.getServicesVersion()

    def test_getURI(self):
        res = self.getURI("UniProt", "P62158")
        assert res == 'urn:miriam:uniprot:P62158'

    def test_getURIs(self):
        res = self.getURIs("UniProt", "P62158")

    def test_isDeprecated(self):
        self.isDeprecated("urn:miriam:uniprot")

