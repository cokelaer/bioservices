from bioservices.chembl import ChEMBL
import pytest
import os

skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
     reason="On travis")


SMILE = "CC(=O)Oc1ccccc1C(=O)O"
INCHIKEY = "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"


@pytest.fixture
def chembl():
    c = ChEMBL(verbose=False, cache=False)
    c.TIMEOUT = 60
    c.default_extension = "xml"
    try:
        c.default_extension = "xmlf"
        assert False
    except:
        assert True
    return c

@pytest.mark.xfail
def test_filters(chembl):
    # test without filters
    res = chembl.get_molecule(limit=20)
    assert len(res) == 20

    # test with one string
    res1 = chembl.get_molecule(limit=20,
        filters='molecule_properties__mw_freebase__lte=300')
    assert len(res1) == 20

    # test with one filter in a list
    res2 = chembl.get_molecule(limit=20,
        filters=['molecule_properties__mw_freebase__lte=300'])
    assert len(res2) == 20

    assert res1 == res2

    # test with several filters in a list

    res = chembl.get_molecule(limit=20,
        filters=[
            'molecule_properties__mw_freebase__lte=300',
            'pref_name__iendswith=nib'])
    assert len(res)
    for this in res:
        assert 'nib' in this['pref_name'].lower()
        assert float(this['molecule_properties']['mw_freebase'])< 300


@pytest.mark.xfail
def test_assay_filter(chembl):
    # test get_assay using a filter:
    res = chembl.get_assay(filters=['assay_type__in=F'])
    assert set([this['assay_type'] for this in res]) == set(['F'])



# ACTIVITIES

@pytest.mark.xfail
def test_activity(chembl):
    res = chembl.get_activity()
    res = chembl.get_activity(['31863','31864'])
    res = chembl.get_activity(['31863',31864])
    assert len(res) == 2

    # here one will not be found (-1)
    res = chembl.get_activity(['31863','-1'])
    assert len(res) == 1
    assert chembl.not_found == ['-1']


# Test ALL resources get_<RESOURCE>

@pytest.mark.parametrize('name', [
    'assay', 'chembl_id_lookup', 'cell_line', 'compound_record', 'biotherapeutic',
    'chembl_id_lookup', 'binding_site', 'organism', 'compound_structural_alert',
    'document', 'document_similarity', 'drug',
    'drug_indication', 'go_slim', 'mechanism', 'metabolism', 'molecule_form',
    'protein_class', 'source', 'target', 'target_component',
    'tissue', 'target_relation', 'xref_source']
    )
def test_resource(chembl, name):
    res = getattr(chembl, "get_" + name)()
    assert len(res)

# This one has no S at the end ? error in the API or assuming it is an acronym
# therefore without S
def test_ATC(chembl):
    res = chembl.get_ATC()
    assert res[0]['who_name']


# SEARCHES ------------------

@skiptravis
def test_search_protein_class(chembl):
    res1715 = chembl.get_protein_class(1715)
    # no good example. This returns noting but at least calls the method
    chembl.search_protein_class('CAMK')

@pytest.mark.xfail
def test_search_target(chembl):
     res = chembl.search_target('cyclin')
     assert len(res['targets'])

@pytest.mark.xfail
def test_search_molecule(chembl):
    res = chembl.search_molecule('aspirin')
    assert len(res['molecules'])

@pytest.mark.xfail
def test_search_assay(chembl):
    res = chembl.search_assay("aspirin")
    assert len(res['assays'])

@pytest.mark.xfail
def test_search_activity(chembl):
    res = chembl.search_activity("GATES")
    assert len(res['activities'])

@pytest.mark.xfail
def test_search_document(chembl):
    res =  chembl.search_document("cytokine")['documents']
    assert len(res)

@pytest.mark.xfail
def test_search_chembl_id(chembl):
    res = chembl.search_chembl_id_lookup('morphine')['chembl_id_lookups']
    assert 'chembl_id' in res[0]


# Test different ways of using the get_<method>
@pytest.mark.xfail
def test_molecule(chembl):

    res = chembl.get_molecule('CHEMBL25')
    assert res['molecule_chembl_id'] == 'CHEMBL25'

    # list
    res = chembl.get_molecule(['CHEMBL25', 'CHEMBL100'])
    assert len(res) == 2

    # list with a wrong ID
    res = chembl.get_molecule(['CHEMBL25', 'CHEMBL00'])
    assert len(res) == 1
    assert chembl.not_found == ['CHEMBL00']


@pytest.mark.xfail
def test_substructure(chembl):

    res = chembl.get_substructure(SMILE)
    assert res[0]['molecule_structures']['canonical_smiles'] == SMILE

    # search by chembl I
    res = chembl.get_similarity("CHEMBL25")
    assert len(res) 

    # search by chembl I
    res = chembl.get_similarity(INCHIKEY)
    assert res


@pytest.mark.xfail
def test_similarity(chembl):

    # search by smiles
    res = chembl.get_similarity(SMILE)
    assert res

    # search by chembl I
    res = chembl.get_similarity("CHEMBL25")
    assert res

    # search by chembl I
    res = chembl.get_similarity(INCHIKEY)
    assert res


# others ---------------------------------------------

def test_get_approved_drugs(chembl):
    res = chembl.get_approved_drugs(maxdrugs=20)


# FIXME: this was failing on march 2020 . still failing june 2020
@pytest.mark.xfail
def test_image(chembl):
    res = chembl.get_image("CHEMBL25", view=False)
    os.remove("CHEMBL25.png")
    res = chembl.get_image("CHEMBL25", view=False, format='svg')
    os.remove("CHEMBL25.svg")


def test_get_status(chembl):
    res = chembl.get_status()
    assert 'activities' in res


def test_get_status_resources(chembl):
    res = chembl.get_status_resources()
    assert 'activity' in res


def test_int_str_request(chembl):
     assert chembl.get_mechanism(13) == chembl.get_mechanism('13')


def test_ordering(chembl):

    res = chembl.get_molecule(limit=100)

    # simple key
    chembl.order_by(res,'molecule_chembl_id')

    # double key
    data1 = [x['molecule_properties']['alogp'] for x in chembl.order_by(res, 'molecule_properties__alogp', ascending=True)]
    assert data1[0] < data1[1]

    data2 = [x['molecule_properties']['alogp'] for x in chembl.order_by(res, 'molecule_properties__alogp', ascending=False)]
    assert data2[0] > data2[1]

    # triple key: FIXME no exqample

    # more:
    try:
        chembl.order_by(res, 'test__test__test__test')
        assert False
    except:
        assert True


# very slow and probably useless now. 
# the test was written to check an unclear behaviou
def __test_limit(chembl):
    # Check that the limi
    # See notes in _get_data in ChEMBL.
    # if limit > 1000 and offset >0 ChEMBL REST API reset the limit to 1000-10,
    # which is not expected. 
    offset = 10
    res = chembl.get_mechanism(limit=6000, offset=offset)
    assert len(res) == chembl.page_meta['total_count'] - offset

# very very slow 
def __test_compounds2accession(chembl):
    res = chembl.compounds2accession('CHEMBL4')
