import pytest

from bioservices import Proteins

p = Proteins()


def test_get_proteins():
    res = p.get_proteins(accession="P12345")
    assert isinstance(res, list)
    assert len(res) > 0
    assert res[0]["accession"] == "P12345"


def test_get_protein():
    res = p.get_protein("P12345")
    assert isinstance(res, dict)
    assert res["accession"] == "P12345"


def test_get_features():
    res = p.get_features("P12345")
    assert isinstance(res, dict)
    assert "accession" in res


def test_get_variation():
    res = p.get_variation("P12345")
    assert isinstance(res, dict)


def test_get_proteomics():
    res = p.get_proteomics("P12345")
    assert isinstance(res, (dict, list))


def test_get_antigen():
    res = p.get_antigen("P12345")
    assert isinstance(res, (dict, list))


def test_get_coordinates():
    res = p.get_coordinates("P12345")
    assert isinstance(res, (dict, list))


def test_get_taxonomy():
    res = p.get_taxonomy(9606)
    assert isinstance(res, dict)
    assert res["taxonomyId"] == 9606


def test_get_taxonomy_by_name():
    res = p.get_taxonomy_by_name("homo sapiens")
    assert isinstance(res, (dict, list))


def test_get_taxonomy_lineage():
    res = p.get_taxonomy_lineage(9606)
    assert isinstance(res, (dict, list))


def test_get_taxonomy_relationship():
    res = p.get_taxonomy_relationship(9606, 10090)
    assert isinstance(res, (dict, list))


def test_get_taxonomy_path():
    res = p.get_taxonomy_path(9606)
    assert isinstance(res, (dict, list))
