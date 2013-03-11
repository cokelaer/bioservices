from bioservices import Miriam




class test_miriam(Miriam):

    def __init__(self):
        super(test_miriam, self).__init__()


    def test_checkRegExp(self):
        assert self.checkRegExp("uniprot", "P62158") == "true"

    def test_convertURL(self):
        assert self.convertURL("http://identifiers.org/ec-code/1.1.1.1") == 'urn:miriam:ec-code:1.1.1.1'


    def test_convertURLs(self):
        self.convertURLs(['http://identifiers.org/pubmed/16333295', 'http://identifiers.org/ec-code/1.1.1.1'])

    def test_convertURN(self):
        self.convertURN('urn:miriam:ec-code:1.1.1.1')
        #'http://identifiers.org/ec-code/1.1.1.1'

    def test_convertURNs(self):

        self.convertURNs(['urn:miriam:ec-code:1.1.1.1'])
        #    ['http://identifiers.org/ec-code/1.1.1.1']

    def test_getDataResources(self):
        self.getDataResources("uniprot")
        #['http://www.ebi.uniprot.org/', 'http://www.pir.uniprot.org/', 'http://www.expasy.uniprot.org/', 'http://www.uniprot.org/', 'http://purl.uniprot.org/', 'http://www.ncbi.nlm.nih.gov/protein/']
 

    def test_getDataTypeDef(self):
        self.getDataTypeDef("uniprot")
        'The UniProt Knowledgebase (UniProtKB) is a comprehensive resource for protein sequence and functional information with extensive cross-references to more than 120 external databases. Besides amino acid sequence and a description, it also provides taxonomic data and citation information.'

    #def test_getDataTypePattern(self, nickname):
    #    m.getDataTypePattern()
    def test_getDataTypeSynonyms(self):
        self.getDataTypeSynonyms("uniprot")
        ['UniProt Knowledgebase', 'UniProtKB', 'UniProt']

    def test_getDataTypeURI(self):

        self.getDataTypeURI("uniprot")
        'urn:miriam:uniprot'

    def test_getDataTypeURIs(self):
        self.getDataTypeURIs("uniprot")
        ['urn:miriam:uniprot', 'urn:lsid:uniprot.org:uniprot', 'urn:lsid:uniprot.org', 'http://www.uniprot.org/']


    def test_getDataTypesId(self):
        self.getDataTypesId()

    def test_getDataTypesName(self):
        self.getDataTypesName()

    def test_getJavaLibraryVersion(self):
        self.getJavaLibraryVersion()

    #def test_getLocation(self, uri, resource):

    def test_getLocations(self ):
        self.getLocations("UniProt","P62158")
        #>>> m.serv.getLocations("urn:miriam:obo.go:GO%3A0045202")

    #def getLocationsWithToken(self):
    #    raise NotImplementedError

    def test_getMiriamURI(self):
        self.getMiriamURI("http://www.ebi.ac.uk/chebi/#CHEBI:17891")
        #'urn:miriam:chebi:CHEBI%3A17891'
    """
    def getName(self, uri):
        raise NotImplementedError
    def getNames(self, uri):
        raise NotImplementedError
    """
    def test_getOfficialDataTypeURI(self):
        self.getOfficialDataTypeURI("chEBI")
        #'urn:miriam:chebi'

    #def test_getResourceInfo(self, Id):
    #    res = self.serv.getResourceInfo(Id)

    #def test_getResourceInstitution(self, Id):
    #    res = self.serv.getResourceInstitution(Id)

    #def test_getResourceLocation(self, Id):
    #    self.self.getResourceLocation(Id)

    def test_getServicesInfo(self):
        self.getServicesInfo()

    def test_getServicesVersion(self):
        self.getServicesVersion()

"""
    def getURI(self, name, Id):
        raise NotImplementedError

    def getURIs(self, name, Id):
        raise NotImplementedError

    def isDeprecated(self):
        raise NotImplementedError
    
"""


