import pytest

from bioservices import PubChem

# Aspirin CID / SMILES / InChIKey used throughout
ASPIRIN_CID = 2244
ASPIRIN_SMILES = "CC(=O)Oc1ccccc1C(=O)O"
ASPIRIN_INCHIKEY = "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"
ASPIRIN_FORMULA = "C9H8O4"


@pytest.fixture(scope="module")
def pubchem():
    return PubChem()


# ------------------------------------------------------------------
# Backward-compatibility
# ------------------------------------------------------------------


def test_compound_by_smiles(pubchem):
    res = pubchem.get_compound_by_smiles(ASPIRIN_SMILES)
    assert res is not None


# ------------------------------------------------------------------
# CID lookup methods
# ------------------------------------------------------------------


def test_get_cids_by_name(pubchem):
    res = pubchem.get_cids_by_name("aspirin")
    assert isinstance(res, dict)
    assert "IdentifierList" in res
    assert ASPIRIN_CID in res["IdentifierList"]["CID"]


def test_get_cids_by_smiles(pubchem):
    res = pubchem.get_cids_by_smiles(ASPIRIN_SMILES)
    assert isinstance(res, dict)
    assert "IdentifierList" in res
    assert ASPIRIN_CID in res["IdentifierList"]["CID"]


def test_get_cids_by_inchikey(pubchem):
    res = pubchem.get_cids_by_inchikey(ASPIRIN_INCHIKEY)
    assert isinstance(res, dict)
    assert "IdentifierList" in res
    assert ASPIRIN_CID in res["IdentifierList"]["CID"]


def test_get_cids_by_formula(pubchem):
    res = pubchem.get_cids_by_formula(ASPIRIN_FORMULA)
    assert isinstance(res, dict)
    assert "IdentifierList" in res
    assert ASPIRIN_CID in res["IdentifierList"]["CID"]


# ------------------------------------------------------------------
# Compound record methods
# ------------------------------------------------------------------


def test_get_compound_by_cid(pubchem):
    res = pubchem.get_compound_by_cid(ASPIRIN_CID)
    assert isinstance(res, dict)
    assert "PC_Compounds" in res


def test_get_compound_by_name(pubchem):
    res = pubchem.get_compound_by_name("aspirin")
    assert isinstance(res, dict)
    assert "PC_Compounds" in res


# ------------------------------------------------------------------
# Properties / synonyms / description
# ------------------------------------------------------------------


def test_get_properties(pubchem):
    res = pubchem.get_properties(ASPIRIN_CID, properties=["MolecularFormula", "MolecularWeight"])
    assert isinstance(res, dict)
    assert "PropertyTable" in res
    props = res["PropertyTable"]["Properties"][0]
    assert props["MolecularFormula"] == ASPIRIN_FORMULA


def test_get_synonyms(pubchem):
    res = pubchem.get_synonyms(ASPIRIN_CID)
    assert isinstance(res, dict)
    assert "InformationList" in res
    synonyms = res["InformationList"]["Information"][0]["Synonym"]
    assert any("aspirin" in s.lower() for s in synonyms)


def test_get_description(pubchem):
    res = pubchem.get_description(ASPIRIN_CID)
    assert isinstance(res, dict)
    assert "InformationList" in res


def test_get_description_by_name(pubchem):
    res = pubchem.get_description("aspirin", namespace="name")
    assert isinstance(res, dict)
    assert "InformationList" in res


# ------------------------------------------------------------------
# Cross-domain links
# ------------------------------------------------------------------


def test_get_sids_by_cid(pubchem):
    res = pubchem.get_sids_by_cid(ASPIRIN_CID)
    assert isinstance(res, dict)
    assert "InformationList" in res
    assert len(res["InformationList"]["Information"]) > 0


def test_get_aids_by_cid(pubchem):
    res = pubchem.get_aids_by_cid(ASPIRIN_CID)
    assert isinstance(res, dict)
    assert "InformationList" in res


# ------------------------------------------------------------------
# Substance operations
# ------------------------------------------------------------------


def test_get_substance_by_sid(pubchem):
    # SID 10 is a well-known substance
    res = pubchem.get_substance_by_sid(10)
    assert isinstance(res, dict)


def test_get_cids_by_sid(pubchem):
    res = pubchem.get_cids_by_sid(10)
    assert isinstance(res, dict)
    assert "InformationList" in res


# ------------------------------------------------------------------
# Assay operations
# ------------------------------------------------------------------


def test_get_assay(pubchem):
    res = pubchem.get_assay(2244)
    assert isinstance(res, dict)


def test_get_assay_description(pubchem):
    res = pubchem.get_assay_description(1)
    assert isinstance(res, dict)


def test_get_cids_by_aid(pubchem):
    res = pubchem.get_cids_by_aid(1)
    assert isinstance(res, dict)
    assert "InformationList" in res


def test_get_sids_by_aid(pubchem):
    res = pubchem.get_sids_by_aid(1)
    assert isinstance(res, dict)
    assert "InformationList" in res
