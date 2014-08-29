from bioservices import BioModels


modelId = 'BIOMD0000000256'
uniprotId = 'P10113'
pubId = '18308339'
GOId = 'GO:0001756'
reacID = "REACT_1590" 
personName = "LeNovere"

class test_biomodels(BioModels):

    def __init__(self):
        super(test_biomodels, self).__init__(verbose=False)

    def test_size(self):

        L1 = len(self.getAllCuratedModelsId())
        L2 = len(self.getAllNonCuratedModelsId())
        L = len(self)
        assert L == L1+L2


    def test_getAllModelsId(self):
        assert len(self.getAllModelsId())>800

    def test_getAllCuratedModelsId(self):
        assert len(self.getAllCuratedModelsId())>100

    def test_getAllNonCuratedModelsId(self):
        assert len(self.getAllNonCuratedModelsId())>100

    def test_getModelById(self):
        self.getModelById('MODEL1006230101')

    def test_getModelSBMLById(self):
        self.getModelSBMLById(modelId)
        self.getModelSBMLById('MODEL1006230101')

    def test_getAuthorsByModelId(self):
        res = self.getAuthorsByModelId(modelId)
        assert res == ['Rehm M', 'Huber HJ', 'Dussmann H', 'Prehn JH']

    def test_getDateLastModifByModelId(self):
        res = self.getDateLastModifByModelId(modelId)
        assert res == '2012-05-16T14:44:17+00:00'

    def test_getEncodersByModelId(self):
        res = self.getEncodersByModelId("BIOMD0000000256")
        assert res == ['Lukas Endler']

    def test_getLastModifiedDateByModelId(self):
        res = self.getLastModifiedDateByModelId("BIOMD0000000256")
        assert res == '2012-05-16T14:44:17+00:00'

    def test_getModelNameById(self):
        res = self.getModelNameById("BIOMD0000000256")
        assert res == 'Rehm2006_Caspase'

        try:
            self.getModelNameById("dummy")
            assert False
        except:assert True

    def test_getModelsIdByChEBI(self):
        res =  self.getModelsIdByChEBI('CHEBI:4978')
        res == ['BIOMD0000000217', 'BIOMD0000000404']

    def test_getModelsIdByChEBIId(self):
        res = self.getModelsIdByChEBIId('CHEBI:4978')
        assert res == ['BIOMD0000000404']

    def test_getSimpleModelsByChEBIIds(self):
        self.getSimpleModelsByChEBIIds('CHEBI:4978')

    def test_getSimpleModelsRelatedWithChEBI(self):
        res = self.getSimpleModelsRelatedWithChEBI()
        from bioservices import xmltools
        res = xmltools.easyXML(res.encode('utf-8'))    
        modelIDs = set([x.findall('modelId')[0].text for x in res.getchildren()])
        assert len(modelIDs) > 1


    
    def test_getPublicationByModelId(self):
        res = self.getPublicationByModelId("BIOMD0000000256")
        assert res == '16932741'


    def test_getSimpleModelByIds(self):
        self.getSimpleModelsByIds(modelId)

    def test_getModelsIdByPerson(self):
        self.getModelsIdByPerson(personName)

    def test_getSimpleModelsByReactomeIds(self):
        return self.getSimpleModelsByReactomeIds(reacID)

    def test_getModelsIdByUniprotId(self):
        return self.getModelsIdByUniprotId(uniprotId)

    def test_getModelsIdByUniprotIds(self):
        self.getModelsIdByUniprotIds(["P10113", "P10415"])

    def test_getModelsIdByName(self):
        return self.getModelsIdByName('2009')

    def test_getModelsIdByPublication(self):
        res = self.getModelsIdByPublication(pubId)
        assert res == ['BIOMD0000000201']

    def test_getModelsIdByGO(self):
        return self.getModelsIdByGO(GOId)

    def test_getModelsIdByTaxonomy(self):
        return self.getModelsIdByTaxonomy("EGF")

    def test_getModelsIdByTaxonomyId(self, taxonomyId='9606'):
        return self.getModelsIdByTaxonomyId(taxonomyId)

    def test_getSubModelSBML(self):
        self.getSubModelSBML("BIOMD0000000242", "cyclinEdegradation_1")
        #self.getSubModelSBML(modelId, elementsIDs)
        pass

    def test_getModelsIdByGOId(self):
        self.getModelsIdByGOId(GOId)

    def test_extra_getChEBIIds(self):
        self.extra_getChEBIIds(99, 101)
        try:
            self.extra_getChEBIIds(1000,101)
            assert False
        except:
            assert True

    def test_extra_getReactomeIds(self):
        self.extra_getReactomeIds(99,101)  # just to cross the 100 Ids
        self.extra_getReactomeIds(89,90)  # just to get one output REACT_89
        try:
            self.extra_getReactomeIds(1000,101)
            assert False
        except:
            assert True

    def test_extra_getUniprotIds(self):
        self.extra_getUniprotIds(11099,11101)
        self.extra_getUniprotIds(10113,10114)

        try:
            self.extra_getUniprotIds(1000,101)
            assert False
        except ValueError:
            assert True



    def test_getModelsIdByUniprot(self):
        self.getModelsIdByUniprot("P10113")
