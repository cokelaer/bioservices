from bioservices import UniChem
import pytest

@pytest.fixture
def unichem():
    u = UniChem(verbose=False)
    return u

# new API from v1.9 and unichem update in May 2022

def test_get_compounds(unichem):
    res = unichem.get_compounds('GZUITABIAKMVPG-UHFFFAOYSA-N', 'inchikey')
    res = res['compounds']
    assert 'sources' in res[0]

    res = unichem.get_compounds('CHEMBL12', 'chembl')
    res = res['compounds']
    assert 'sources' in res[0]

    res = unichem.get_compounds('CHEMBL12', 1)
    res = res['compounds']
    assert 'sources' in res[0]

    assert unichem.get_compounds('CHEMBL12', 'dummy') == {}

def test_get_sources_by_inchikey(unichem):

    inchikey = "AAOVKJBEBIDNHE-UHFFFAOYSA-N"
    res = unichem.get_sources_by_inchikey(inchikey)
    assert unichem.get_sources_by_inchikey("AAOV") == {}
    assert unichem.get_sources_by_inchikey(["AAOV"]) == {'AAOV': {}}

def test_connectivity(unichem):
    res = unichem.get_connectivity('GZUITABIAKMVPG-UHFFFAOYSA-N', 'inchikey')
    assert 'sources' in res

    res = unichem.get_connectivity('CHEMBL12', 'chembl')
    assert 'sources' in res

    res = unichem.get_connectivity('CHEMBL12', 1)
    assert 'sources' in res

    assert unichem.get_connectivity('CHEMBL12', 'dummy')  == {}

def test_images(unichem, tmpdir):

    res = unichem.get_images('304698')
    assert res

    res = unichem.get_images('dummy')
    assert res is None

    outfile = tmpdir.join('test.svg')
    res = unichem.get_images('304698', filename=outfile)


def test_get_id_from_name(unichem):
    res = unichem.get_id_from_name('chembl')
    assert res == 1

    assert unichem.get_id_from_name('dummmy') is None

def test_get_sources(unichem):
    unichem.get_sources()

def test_get_all_src_ids(unichem):
    unichem.get_all_src_ids()

def test_get_source_info_by_name(unichem):
    unichem.get_source_info_by_name('chembl')
    assert unichem.get_source_info_by_name('du,,y') is None

def test_get_source_info_by_id(unichem):
    unichem.get_source_info_by_id(1)
    assert unichem.get_source_info_by_id(-1) is None

def test_get_inchi_from_inchikey(unichem):
    res = unichem.get_inchi_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
    assert 'standardinchi' in res[0]

    inchikey1 = "AAOVKJBEBIDNHE-UHFFFAOYSA-N"
    inchikey2 = "GZUITABIAKMVPG-UHFFFAOYSA-N"
    res = unichem.get_inchi_from_inchikey([inchikey1,inchikey2])
    assert 'standardinchi' in res[inchikey1][0]
    assert 'standardinchi' in res[inchikey2][0]

def test_get_sources_by_inchikey(unichem):

    # assume everything is alright:
    inchikey1 = "AAOVKJBEBIDNHE-UHFFFAOYSA-N"
    inchikey2 = "GZUITABIAKMVPG-UHFFFAOYSA-N"

    # uses only one string as input
    res = unichem.get_sources_by_inchikey(inchikey1)
    assert 'src_compound_id' in res[0]

    # uses a list
    res = unichem.get_sources_by_inchikey([inchikey1, inchikey2])
    assert len(res) == 2
    assert 'src_compound_id' in res[inchikey2][0]
    assert 'src_compound_id' in res[inchikey1][0]

    # Now let us make a mistake:
    res = unichem.get_sources_by_inchikey("dummy")
    assert "error" in res
    res = unichem.get_sources_by_inchikey(["dummy1", 'dummy2'])
    assert "error" in res['dummy1']
    assert "error" in res['dummy2']

def test_get_sources_by_inchikey_verbose(unichem):

    # assume everything is alright:
    inchikey1 = "AAOVKJBEBIDNHE-UHFFFAOYSA-N"
    inchikey2 = "GZUITABIAKMVPG-UHFFFAOYSA-N"

    # uses only one string as input
    res = unichem.get_sources_by_inchikey_verbose(inchikey1)
    assert 'src_compound_id' in res[0]

    # uses a list
    res = unichem.get_sources_by_inchikey_verbose([inchikey1, inchikey2])
    assert len(res) == 2
    assert 'src_compound_id' in res[inchikey2][0]
    assert 'src_compound_id' in res[inchikey1][0]

    # Now let us make a mistake:
    res = unichem.get_sources_by_inchikey_verbose("dummy")
    assert "error" in res
    res = unichem.get_sources_by_inchikey_verbose(["dummy1", 'dummy2'])
    assert "error" in res['dummy1']
    assert "error" in res['dummy2']


def test_get_structure(unichem):
    assert unichem.get_structure("CHEMBL12", "chembl")
