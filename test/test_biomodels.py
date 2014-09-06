from bioservices import BioModels
from nose.plugins.attrib import attr

modelId = 'BIOMD0000000256'
uniprotId = 'P10113'
pubId = '18308339'
GOId = 'GO:0001756'
reacID = "REACT_1590"
personName = "LeNovere"


class test_biomodels(object):

    @classmethod
    def setup_class(klass):
        klass.s = BioModels(verbose=False)

    def test_size(self):
        L1 = len(self.s.getAllCuratedModelsId())
        L2 = len(self.s.getAllNonCuratedModelsId())
        L = len(self.s)
        assert L == L1+L2

    def test_getAllModelsId(self):
        assert len(self.s.getAllModelsId()) > 800

    def test_getAllCuratedModelsId(self):
        assert len(self.s.getAllCuratedModelsId()) > 100

    def test_getAllNonCuratedModelsId(self):
        assert len(self.s.getAllNonCuratedModelsId()) > 100

    def test_getModelById(self):
        self.s.getModelById('MODEL1006230101')

    def test_getModelSBMLById(self):
        self.s.getModelSBMLById(modelId)
        self.s.getModelSBMLById('MODEL1006230101')

    def test_getAuthorsByModelId(self):
        res = self.s.getAuthorsByModelId(modelId)
        assert res == ['Rehm M', 'Huber HJ', 'Dussmann H', 'Prehn JH']

    def test_getDateLastModifByModelId(self):
        res = self.s.getDateLastModifByModelId(modelId)
        assert res == '2012-05-16T14:44:17+00:00'

    def test_getEncodersByModelId(self):
        res = self.s.getEncodersByModelId("BIOMD0000000256")
        assert res == ['Lukas Endler']

    def test_getLastModifiedDateByModelId(self):
        res = self.s.getLastModifiedDateByModelId("BIOMD0000000256")
        assert res == '2012-05-16T14:44:17+00:00'

    def test_getModelNameById(self):
        res = self.s.getModelNameById("BIOMD0000000256")
        assert res == 'Rehm2006_Caspase'

        try:
            self.s.getModelNameById("dummy")
            assert False
        except:
            assert True

    def test_getModelsIdByChEBI(self):
        res = self.s.getModelsIdByChEBI('CHEBI:4978')
        res == ['BIOMD0000000217', 'BIOMD0000000404']

    def test_getModelsIdByChEBIId(self):
        res = self.s.getModelsIdByChEBIId('CHEBI:4978')
        assert res == ['BIOMD0000000404']

    def test_getSimpleModelsByChEBIIds(self):
        self.s.getSimpleModelsByChEBIIds('CHEBI:4978')

    @attr('slow')
    def test_getSimpleModelsRelatedWithChEBI(self):
        res = self.s.getSimpleModelsRelatedWithChEBI()
        from bioservices import xmltools
        res = xmltools.easyXML(res.encode('utf-8'))
        modelIDs = set([x.findall('modelId')[0].text for x in res.getchildren()])
        assert len(modelIDs) > 1

    def test_getPublicationByModelId(self):
        res = self.s.getPublicationByModelId("BIOMD0000000256")
        assert res == '16932741'

    def test_getSimpleModelByIds(self):
        self.s.getSimpleModelsByIds(modelId)

    def test_getModelsIdByPerson(self):
        self.s.getModelsIdByPerson(personName)

    def test_getSimpleModelsByReactomeIds(self):
        return self.s.getSimpleModelsByReactomeIds(reacID)

    def test_getModelsIdByUniprotId(self):
        return self.s.getModelsIdByUniprotId(uniprotId)

    def test_getModelsIdByUniprotIds(self):
        self.s.getModelsIdByUniprotIds(["P10113", "P10415"])

    def test_getModelsIdByName(self):
        return self.s.getModelsIdByName('2009')

    def test_getModelsIdByPublication(self):
        res = self.s.getModelsIdByPublication(pubId)
        assert res == ['BIOMD0000000201']

    def test_getModelsIdByGO(self):
        return self.s.getModelsIdByGO(GOId)

    def test_getModelsIdByTaxonomy(self):
        return self.s.getModelsIdByTaxonomy("EGF")

    def test_getModelsIdByTaxonomyId(self, taxonomyId='9606'):
        return self.s.getModelsIdByTaxonomyId(taxonomyId)

    def test_getSubModelSBML(self):
        self.s.getSubModelSBML("BIOMD0000000242", "cyclinEdegradation_1")

    def test_getModelsIdByGOId(self):
        self.s.getModelsIdByGOId(GOId)

    def test_extra_getChEBIIds(self):
        self.s.extra_getChEBIIds(99, 101)
        try:
            self.s.extra_getChEBIIds(1000, 101)
            assert False
        except:
            assert True

    def test_extra_getReactomeIds(self):
        self.s.extra_getReactomeIds(99, 101)  # just to cross the 100 Ids
        self.s.extra_getReactomeIds(89, 90)  # just to get one output REACT_89
        try:
            self.s.extra_getReactomeIds(1000, 101)
            assert False
        except:
            assert True

    def test_extra_getUniprotIds(self):
        self.s.extra_getUniprotIds(11099, 11101)
        self.s.extra_getUniprotIds(10113, 10114)

        try:
            self.s.extra_getUniprotIds(1000, 101)
            assert False
        except ValueError:
            assert True

    def test_getModelsIdByUniprot(self):
        self.s.getModelsIdByUniprot("P10113")
