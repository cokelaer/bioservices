from bioservices.chembl import ChEMBL
import pytest


@pytest.fixture
def chembl():
    c = ChEMBL(verbose=False, cache=False)
    c.default_extension = "xml"
    try:
        c.default_extension = "xmlf"
        assert False
    except:
        assert True
    return c



def test_status(chembl):
    chembl.status()

# COMPOUNDS RELATED ---------------------------------------------------------------

def test_get_compounds_by_chemblId_form(chembl):
    res = chembl.get_compounds_by_chemblId_form("CHEMBL3")
    res[0]['parent']
    res = chembl.get_compounds_by_chemblId_form(["CHEMBL3"])
    assert len(res)

def test_get_compounds_by_chemblId_drug_mechanism(chembl):
    res = chembl.get_compounds_by_chemblId_drug_mechanism("CHEMBL3")

def test_get_individual_compounds_by_inChiKey(chembl):
    res = chembl.get_individual_compounds_by_inChiKey(chembl._inChiKey_example)
    assert res['molecularFormula'] == 'C19H21ClFN3O3'

def test_get_compounds_by_chemblId(chembl):
    assert chembl.get_compounds_by_chemblId("CHEMBL1")
    # FIXME
    #assert chembl.get_compounds_by_chemblId("WRONG") in chembl._error_codes
    chembl.get_compounds_by_chemblId(chembl._chemblId_example)
    assert len(chembl.get_compounds_by_chemblId(["CHEMBL1", "CHEMBL2"]))==2

def test_get_compounds_activities(chembl):
    chembl.get_compounds_activities("CHEMBL1")

def test_get_compounds_by_SMILES(chembl):
    res = chembl.get_compounds_by_SMILES(chembl._smiles_example)

def test_get_compounds_containing_SMILES(chembl):
    #res = chembl.get_compounds_containing_SMILES(chembl._smiles_struct_example)
    res = chembl.get_compounds_substructure(chembl._smiles_struct_example)

def test_get_compounds_similar_to_SMILES(chembl):
    # at the time of the test, the length was 9
    res = chembl.get_compounds_similar_to_SMILES(chembl._smiles_example, similarity=90)
    assert len(res)>=9

# TARGETS -----------------------------------------------------------------

def test_get_target_uniprotId(chembl):
    res = chembl.get_target_by_uniprotId(chembl._target_uniprotId_example)
    assert res['proteinAccession'] == chembl._target_uniprotId_example

def test_get_target_bioactivities(chembl):
    res = chembl.get_target_bioactivities(chembl._target_bioactivities_example)
    assert len(res)>1000

def test_get_target_by_chemblId(chembl):
    resjson = chembl.get_target_by_chemblId(chembl._target_chemblId_example)

def test_get_all_targets(chembl):
    assert len(chembl.get_all_targets())>1000

def test_get_target_by_refseq(chembl):
    chembl.get_target_by_refseq(chembl._target_refseq_example)

# ASSAYS ----------------------------------------------------------

def test_get_assays_bioactivities(chembl):
    res = chembl.get_assays_bioactivities(chembl._assays_example)

def test_get_assays(chembl):
    chembl.get_assays_bioactivities("CHEMBL1217643")
    chembl.get_assays_by_chemblId("CHEMBL1217643")

def test_inspect(chembl): 
    chembl.inspect(chembl._assays_example,'assay')

def test_image(chembl):
    res = chembl.get_image_of_compounds_by_chemblId(
        chembl._image_chemblId_example
        , view=False)
    import os
    os.remove(chembl._image_chemblId_example + ".png")

def test_version(chembl):
    chembl.version()


"""


    def get_target_by_refseq(chembl, query):

def get_assays_by_chemblId(chembl, query, frmt="json"):
    def get_assays_bioactivities(chembl, query, frmt="json"):
    def inspect(chembl, query, item_type):

"""
