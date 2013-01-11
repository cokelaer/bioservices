from bioservices import biomodels


modelId = 'BIOMD0000000256'
uniprotId = 'P10113'
pubId = '18308339'
GOId = 'GO:0001756'
reacID = "REACT_1590" 
personName = "LeNovere"

class test_biomodels():


    def __init__(self):
        self.serv = biomodels.BioModels()

    def test_size(self):

        L1 = len(self.serv.getAllCuratedModelsId())
        L2 = len(self.serv.getAllNonCuratedModelsId())
        L = len(self.serv)
        assert L == L1+L2


    def _test_getAllModelsId(self):
        assert len(self.serv.getAllModelsId())>800

    def _test_getAllCuratedModelsId(self):
        assert len(self.serv.getAllCuratedModelsId())>100

    def _test_getAllNonCuratedModelsId(self):
        assert len(self.serv.getAllNonCuratedModelsId())>100

    def _test_getModelSBMLById(self):
        self.serv.getModelSBMLById(modelId)
        self.serv.getModelSBMLById('MODEL1006230101')

    def _test_getAuthorsByModelId(self):
        self.serv.getAuthorsByModelId(modelId)

    def _test_getDateLastModifByModelId(self):
        self.serv.getDateLastModifByModelId(modelId)

    def _test_getEncodersByModelId(self):
        return self.serv.getEncodersByModelId(modelId)

    def _test_getLastModifiedDateByModelId(self):
        return self.serv.getLastModifiedDateByModelId(modelId)

    def _test_getModelNameById(self):
        return self.serv.getModelNameById(modelId)

    def _test_getModelsIdByChEBI(self):
        return self.serv.getModelsIdByChEBI('CHEBI:4978')

    def _test_getModelsIdByChEBIId(self):
        res = self.serv.getModelsIdByChEBIId('CHEBI:4978')
        assert res == ['BIOMD0000000404']

    def _test_getSimpleModelsByChEBIIds(self):
        self.serv.getSimpleModelsByChEBIIds('CHEBI:4978')

    def _test_getSimpleModelsRelatedWithChEBI(self):
        res = self.serv.getSimpleModelsRelatedWithChEBI()
    
    def _test_getPublicationByModelId(self):
        self.serv.getPublicationByModelId(modelId)

    def _test_getSimpleModelByIds(self):
        self.serv.getSimpleModelsByIds(modelId)

    def _test_getModelsIdByPerson(self):
        self.serv.getModelsIdByPerson(personName)

    def _test_getSimpleModelsByReactomeIds(self):
        return self.serv.getSimpleModelsByReactomeIds(reacID)

    def _test_getModelsIdByUniprotId(self):
        return self.serv.getModelsIdByUniprotId(uniprotId)

    def _test_getModelsIdByName(self):
        return self.serv.getModelsIdByName('2009')

    def _test_getModelsIdByPublication(self):
        res = self.serv.getModelsIdByPublication(pubId)
        assert res == ['BIOMD0000000201']

    def _test_getModelsIdByGO(self):
        return self.serv.getModelsIdByGO(GOId)

    def _test_getModelsIdByTaxonomy(self):
        return self.serv.getModelsIdByTaxonomy("EGF")

    def _test_getModelsIdByTaxonomyId(self, taxonomyId='9606'):
        return self.serv.getModelsIdByTaxonomyId(taxonomyId)

    def _test_getSubModelSBML(self):
        #self.serv.getSubModelSBML(modelId, elementsIDs)
        pass

    def test_getModelsIdByGOId(self):
        self.serv.getModelsIdByGOId(GOId)


    def test_extra_getReactomeIds(self):
        self.serv.extra_getReactomeIds(0,100)

    def test_extra_getUniprotIds(self):
        self.serv.extra_getUniprotIds(11000,11100)


