from bioservices import BioModels
from easydev import TempFile
import pytest
import os

#pytestmark = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
#     reason="On travis")


modelId = 'BIOMD0000000256'
uniprotId = 'P10113'
pubId = '18308339'
GOId = 'GO:0001756'
reacID = "REACT_1590"
personName = "LeNovere"

modelID = "BIOMD0000000100"





@pytest.fixture
def biomodels():
    return BioModels(verbose=False)


def test_get_model(biomodels):
    res = biomodels.get_model("BIOMD0000000100")
    assert res['submissionId'] == "MODEL4589754842"
    

    try:
        res = biomodels.get_model("BIOMD0000000100", frmt="dummy")
        assert False
    except:
        assert True


def test_get_model_files(biomodels):
    res = biomodels.get_model_files(modelID)
    assert "main" in res.keys()


def test_get_model_download(biomodels):
    with TempFile(suffix=".zip") as fout:
        biomodels.get_model_download(modelID, output_filename=fout.name)

    with TempFile(suffix=".png") as fout:
        # we download only the PNG file and save it in a new filename
        biomodels.get_model_download(modelID, filename="BIOMD0000000100.png", 
            output_filename=fout.name)


def test_get_p2m_representative(biomodels):
    models = biomodels.get_p2m_missing()
    modelID = models[0]
    res = biomodels.get_p2m_representative(modelID)
    assert res["requestedModelId"] == modelID

def test_search(biomodels):

    res = biomodels.search("XXXXXXXXXXXXX")
    assert res["matches"] == 0

    res = biomodels.search(modelID, sort="id-asc", offset=1, numResults=5)
    assert res['queryParameters']['offset'] == 1
    assert res['queryParameters']['sortBy'] == "id"
    assert res['queryParameters']['sortDirection'] == "asc"

    try:
        biomodels.search(modelID, sort="id-asffc")
        assert False
    except ValueError:
        assert True
    except:
        assert True


def test_search_download(biomodels):

    with TempFile(suffix=".zip") as fout:
        biomodels.search_download("BIOMD0000000100,BIOMD0000000654,",
            output_filename=fout.name, force=True)
        biomodels.search_download(["BIOMD0000000100","BIOMD0000000654"],
            output_filename=fout.name, force=True)

    biomodels.search_download("XXXXXXXXXXXXXX")

def test_search_parameters(biomodels):
    res = biomodels.search_parameter("MAPK", size=100, sort="entity")
    


def test_get_p2m_representatives(biomodels):
    models = "BMID000000112902,BMID000000009880,BMID000000027397"
    res = biomodels.get_p2m_representatives(models)
    assert sorted(models.split(",")) == sorted(res.keys())

    models = ["BMID000000112902","BMID000000009880","BMID000000027397"]
    res = biomodels.get_p2m_representatives(models)
    assert sorted(models) == sorted(res.keys())


def test_get_pdgsmm_representative(biomodels):
    models = biomodels.get_pdgsmm_missing()
    modelID = models[0]
    res = biomodels.get_pdgsmm_representative(modelID)
    assert res["requestedModelId"] == modelID

def test_get_pdgsmm_representatives(biomodels):
    models = "MODEL1707110145,MODEL1707112456,MODEL1707115900"
    res = biomodels.get_pdgsmm_representatives(models)
    assert sorted(models.split(",")) == sorted(res.keys())

"""
def test_size(biomodels):
    L1 = len(biomodels.getAllCuratedModelsId())
    L2 = len(biomodels.getAllNonCuratedModelsId())
    L = len(biomodels)
    assert L == L1+L2

def test_getAllModelsId(biomodels):
    assert len(biomodels.getAllModelsId()) > 800

def test_getAllCuratedModelsId(biomodels):
    assert len(biomodels.getAllCuratedModelsId()) > 100

def test_getAllNonCuratedModelsId(biomodels):
    assert len(biomodels.getAllNonCuratedModelsId()) > 100

def test_getModelById(biomodels):
    biomodels.getModelById('MODEL1006230101')

def test_getModelSBMLById(biomodels):
    biomodels.getModelSBMLById(modelId)
    biomodels.getModelSBMLById('MODEL1006230101')

def test_getAuthorsByModelId(biomodels):
    res = biomodels.getAuthorsByModelId(modelId)
    assert res == ['Rehm M', 'Huber HJ', 'Dussmann H', 'Prehn JH']

def test_getDateLastModifByModelId(biomodels):
    res = biomodels.getDateLastModifByModelId(modelId)
    # This changes with time so no need to check 
    #assert res == '2012-05-16T14:44:17+00:00'

def test_getEncodersByModelId(biomodels):
    res = biomodels.getEncodersByModelId("BIOMD0000000256")
    assert res == ['Lukas Endler']

def test_getLastModifiedDateByModelId(biomodels):
    res = biomodels.getLastModifiedDateByModelId("BIOMD0000000256")
    # This changes with time so no need to check 
    #assert res == '2012-05-16T14:44:17+00:00'

def test_getModelNameById(biomodels):
    res = biomodels.getModelNameById("BIOMD0000000256")
    assert res == 'Rehm2006_Caspase'

    try:
        biomodels.getModelNameById("dummy")
        assert False
    except:
        assert True

def test_getModelsIdByChEBI(biomodels):
    res = biomodels.getModelsIdByChEBI('CHEBI:4978')
    res == ['BIOMD0000000217', 'BIOMD0000000404']

def test_getModelsIdByChEBIId(biomodels):
    res = biomodels.getModelsIdByChEBIId('CHEBI:4978')
    assert res == ['BIOMD0000000404']

def test_getSimpleModelsByChEBIIds(biomodels):
    biomodels.getSimpleModelsByChEBIIds('CHEBI:4978')

# FIXME
def _test_getSimpleModelsRelatedWithChEBI(biomodels):
    res = biomodels.getSimpleModelsRelatedWithChEBI()
    from bioservices import xmltools
    res = xmltools.easyXML(res.encode('utf-8'))
    modelIDs = set([x.findall('modelId')[0].text for x in res.getchildren()])
    assert len(modelIDs) > 1

def test_getPublicationByModelId(biomodels):
    res = biomodels.getPublicationByModelId("BIOMD0000000256")
    assert res == '16932741'

def test_getSimpleModelByIds(biomodels):
    biomodels.getSimpleModelsByIds(modelId)

def test_getModelsIdByPerson(biomodels):
    biomodels.getModelsIdByPerson(personName)

# FIXME
def _test_getSimpleModelsByReactomeIds(biomodels):
    return biomodels.getSimpleModelsByReactomeIds(reacID)

def test_getModelsIdByUniprotId(biomodels):
    return biomodels.getModelsIdByUniprotId(uniprotId)

def test_getModelsIdByUniprotIds(biomodels):
    biomodels.getModelsIdByUniprotIds(["P10113", "P10415"])

def test_getModelsIdByName(biomodels):
    return biomodels.getModelsIdByName('2009')

def test_getModelsIdByPublication(biomodels):
    res = biomodels.getModelsIdByPublication(pubId)
    assert res == ['BIOMD0000000201']

def test_getModelsIdByGO(biomodels):
    return biomodels.getModelsIdByGO(GOId)

def test_getModelsIdByTaxonomy(biomodels):
    return biomodels.getModelsIdByTaxonomy("EGF")

def test_getModelsIdByTaxonomyId(biomodels, taxonomyId='9606'):
    return biomodels.getModelsIdByTaxonomyId(taxonomyId)

def test_getSubModelSBML(biomodels):
    biomodels.getSubModelSBML("BIOMD0000000242", "cyclinEdegradation_1")

def test_getModelsIdByGOId(biomodels):
    biomodels.getModelsIdByGOId(GOId)

def test_extra_getChEBIIds(biomodels):
    biomodels.extra_getChEBIIds(99, 101)
    try:
        biomodels.extra_getChEBIIds(1000, 101)
        assert False
    except:
        assert True

# FIXME
def _test_extra_getReactomeIds(biomodels):
    biomodels.extra_getReactomeIds(99, 101)  # just to cross the 100 Ids
    biomodels.extra_getReactomeIds(89, 90)  # just to get one output REACT_89
    try:
        biomodels.extra_getReactomeIds(1000, 101)
        assert False
    except:
        assert True

# FIXME
def _test_extra_getUniprotIds(biomodels):
    biomodels.extra_getUniprotIds(11099, 11101)
    biomodels.extra_getUniprotIds(10113, 10114)

    try:
        biomodels.extra_getUniprotIds(1000, 101)
        assert False
    except ValueError:
        assert True

def test_getModelsIdByUniprot(biomodels):
    biomodels.getModelsIdByUniprot("P10113")
"""

