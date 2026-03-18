import pytest

from bioservices import ChEBI


@pytest.fixture(scope="module")
def chebi():
    return ChEBI(verbose=False)


@pytest.mark.timeout(120)
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_chebi(chebi):
    chebi.getCompleteEntity("CHEBI:10102")
    res = chebi.conv("CHEBI:10102", "KEGG COMPOUND")
    assert res == ["151319-34-5", "C07484"]

    with pytest.raises(Exception):
        chebi.conv("CHEBI:10102", "wrong db")

    chebi.getOntologyChildren("CHEBI:27732")
    chebi.getOntologyParents("CHEBI:27732")
    chebi.getUpdatedPolymer("CHEBI:27732")


def test_chebi_mass(chebi):
    res = chebi.getCompleteEntity("CHEBI:27732")
    assert float(res.mass) == 194.194


def test_polymer(chebi):
    x = chebi.getUpdatedPolymer("CHEBI:27732")
    assert x is not None
    assert x.chebiId is not None


def test_completelist(chebi):
    entities = chebi.getCompleteEntityByList(["CHEBI:27732", "CHEBI:36707"])
    names = [str(x.chebiAsciiName) for x in entities]
    assert names == ["caffeine", "2-acetyl-1-alkyl-sn-glycero-3-phosphocholine"]


def test_search(chebi):
    smiles = chebi.getCompleteEntity("CHEBI:27732").smiles
    assert smiles is not None
    chebi.getStructureSearch(smiles, "SMILES", "SIMILARITY", 3, 0.25)


def test_ontology(chebi):
    chebi.getAllOntologyChildrenInPath("CHEBI:27732", "has part")


def test_structure(chebi):
    smiles = chebi.getCompleteEntity("CHEBI:27732").smiles
    assert smiles is not None
    chebi.getStructureSearch(smiles, "SMILES", "SIMILARITY", 3, 0.25)
