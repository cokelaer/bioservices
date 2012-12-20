from bioservices import biomodels


modelId = 'BIOMD0000000256'
uniprotId = 'P10113'
pubId = '18308339'
GOId = 'GO:0001756'
reacID = "REACT_1590" 
personName = "LeNovere"

class _test_biomodels():


    def __init__(self):
        self.serv = biomodels.BioModels()

    def test_size(self):

        L1 = len(self.serv.getAllCuratedModelsId())
        L2 = len(self.serv.getAllNonCuratedModelsId())
        L = len(self.serv)
        assert L == L1+L2


    def test_getAllModelsId(self):
        assert len(self.serv.getAllModelsId())>800

    def test_getAllCuratedModelsId(self):
        assert len(self.serv.getAllCuratedModelsId())>100

    def test_getAllNonCuratedModelsId(self):
        assert len(self.serv.getAllNonCuratedModelsId())>100

    def test_getModelSBMLById(self):
        self.serv.getModelSBMLById(modelId)
        self.serv.getModelSBMLById('MODEL1006230101')

    def test_getAuthorsByModelId(self):
        self.serv.getAuthorsByModelId(modelId)

    def test_getDateLastModifByModelId(self):
        self.serv.getDateLastModifByModelId(modelId)

    def test_getEncodersByModelId(self):
        return self.serv.getEncodersByModelId(modelId)

    def test_getLastModifiedDateByModelId(self):
        return self.serv.getLastModifiedDateByModelId(modelId)

    def test_getModelNameById(self):
        return self.serv.getModelNameById(modelId)

    def test_getModelsIdByChEBI(self):
        return self.serv.getModelsIdByChEBI('CHEBI:4978')

    def test_getModelsIdByChEBIId(self):
        res = self.serv.getModelsIdByChEBIId('CHEBI:4978')
        assert res == ['BIOMD0000000404']

    def test_getSimpleModelsByChEBIIds(self):
        self.serv.getSimpleModelsByChEBIIds('CHEBI:4978')

    def test_getSimpleModelsRelatedWithChEBI(self):
        res = self.serv.getSimpleModelsRelatedWithChEBI()
    
    def test_getPublicationByModelId(self):
        self.serv.getPublicationByModelId(modelId)

    def test_getSimpleModelByIds(self):
        self.serv.getSimpleModelsByIds(modelId)

    def test_getModelsIdByPerson(self):
        self.serv.getModelsIdByPerson(personName)

    def test_getSimpleModelsByReactomeIds(self):
        return self.serv.getSimpleModelsByReactomeIds(reacID)

    def test_getModelsIdByUniprotId(self):
        return self.serv.getModelsIdByUniprotId(uniprotId)

    def test_getModelsIdByName(self):
        return self.serv.getModelsIdByName('2009')

    def test_getModelsIdByPublication(self):
        res = self.serv.getModelsIdByPublication(pubId)
        assert res == ['BIOMD0000000201']

    def test_getModelsIdByGO(self):
        return self.serv.getModelsIdByGO(GOId)

    def test_getModelsIdByTaxonomy(self):
        return self.serv.getModelsIdByTaxonomy("EGF")

    def test_getModelsIdByTaxonomyId(self, taxonomyId='9606'):
        return self.serv.getModelsIdByTaxonomyId(taxonomyId)

    def test_getSubModelSBML(self):
        #self.serv.getSubModelSBML(modelId, elementsIDs)
        pass

    def test_getModelsIdByGOId(self):
        self.serv.getModelsIdByGOId(GOId)


    def test_extra_getReactomeIds(self):
        self.serv.extra_getReactomeIds(0,100)

    def test_extra_getUniprotIds(self):
        self.serv.extra_getUniprotIds(11000,11100)


