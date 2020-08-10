from bioservices import UniChem
import pytest

@pytest.fixture
def unichem():
    u = UniChem(verbose=False)
    return u


def test_get_compound_ids_from_src_id(unichem):
    res1 = unichem.get_compound_ids_from_src_id("CHEMBL2", "chembl", "chebi")
    res2 = unichem.get_compound_ids_from_src_id(["CHEMBL2"], "chembl", "chebi")
    assert res1 == res2[0]
    assert res1 == [{u'src_compound_id': u'8364'}]
    assert res2[0] == [{u'src_compound_id': u'8364'}]

def test_get_all_src_ids(unichem):
    assert len(unichem.get_all_src_ids())>=23

def test_get_source_id(unichem):
    assert unichem._get_source_id("chembl") == 1
    assert unichem._get_source_id("1") == 1
    assert unichem._get_source_id(1) == 1

    try:
        unichem._get_source_id("wrong")
        assert False
    except:
        assert True

    try:
        unichem._get_source_id("20000")
        assert False
    except:
        assert True

def test_get_src_information(unichem):
    assert unichem.get_source_information("chebi")['name'] == "chebi"

    assert unichem.get_source_information(['chembl', 'drugbank'])[0]['name']=="chembl"

def test_get_all_compound_ids_from_src_id(unichem):
    res = unichem.get_all_compound_ids_from_all_src_id("CHEMBL12", "chembl")
    res = unichem.get_all_compound_ids_from_all_src_id("CHEMBL12", "chembl", "chebi")

def test_mapping(unichem):
    res = unichem.get_mapping("kegg_ligand", "chembl")
    assert len(res)>0

def test_get_src_compound_ids_from_inchikey(unichem):
    unichem.get_src_compound_ids_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
    unichem.get_src_compound_ids_from_inchikey(["AAOVKJBEBIDNHE-UHFFFAOYSA-N"])
    #unichem.get_src_compound_ids_all_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
    #unichem.get_src_compound_ids_all_from_inchikey(["AAOVKJBEBIDNHE-UHFFFAOYSA-N"])

def test_structure(unichem):
    unichem.get_structure("CHEMBL12", "chembl")
    unichem.get_structure(["CHEMBL12"], "chembl")
    unichem.get_structure_all("CHEMBL12", "chembl")

def test_get_src_compound_id_url(unichem):
    unichem.get_src_compound_id_url("CHEMBL12", "chembl", "drugbank")
    unichem.get_src_compound_id_url(["CHEMBL12"], "chembl", "drugbank")

def test_get_src_compound_ids_all_from_obsolete(unichem):
    unichem.get_src_compound_ids_all_from_obsolete("DB07699", "2")[0]
    unichem.get_src_compound_ids_all_from_obsolete("DB07699", "2", "2")[0]

#SLOW one
def test_get_verbose_src_compound_ids_from_inchikey(unichem):
    assert unichem.get_verbose_src_compound_ids_from_inchikey("GZUITABIAKMVPG-UHFFFAOYSA-N") != 400
    assert unichem.get_verbose_src_compound_ids_from_inchikey("QFFGVLORLPOAEC-SNVBAGLBSA-N") != 400 


@pytest.mark.xfail
def test_get_auxiliary_mapping(unichem):
    # useless since we have a global timeout for pytest of 10 o r30 seconds
    unichem.settings.TIMEOUT = 100
    res = unichem.get_auxiliary_mappings(1)
    if isinstance(res, int):
        pass
    else:
        assert len(res)>0

