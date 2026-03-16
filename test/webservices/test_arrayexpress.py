import os

import pytest

from bioservices import ArrayExpress


@pytest.fixture
def array():
    return ArrayExpress(verbose=False)


# -----------------------------------------------------------------------
# Tests for new-style methods
# -----------------------------------------------------------------------


def test_search_basic(array):
    res = array.search("breast cancer")
    assert "totalHits" in res
    assert res["totalHits"] > 0
    assert "hits" in res
    assert len(res["hits"]) > 0
    hit = res["hits"][0]
    assert "accession" in hit
    assert "title" in hit


def test_search_with_sort(array):
    res = array.search("Homo sapiens", sort_by="release_date", sort_order="ascending")
    assert res["sortBy"] == "release_date"
    assert res["sortOrder"] == "ascending"


def test_search_pagination(array):
    res = array.search("cancer", page=2, page_size=5)
    assert res["page"] == 2
    assert res["pageSize"] == 5
    assert len(res["hits"]) <= 5


def test_search_invalid_sort_by(array):
    with pytest.raises(ValueError):
        array.search("cancer", sort_by="invalid_field")


def test_search_invalid_sort_order(array):
    with pytest.raises(ValueError):
        array.search("cancer", sort_order="sideways")


def test_get_study(array):
    study = array.get_study("E-MEXP-31")
    assert study["accno"] == "E-MEXP-31"
    titles = [a["value"] for a in study["attributes"] if a["name"] == "Title"]
    assert len(titles) == 1
    assert "germ cell" in titles[0].lower()


def test_get_files(array):
    files = array.get_files("E-MEXP-31")
    assert isinstance(files, list)
    assert len(files) > 0
    assert "E-MEXP-31.idf.txt" in files


def test_retrieve_file(array):
    content = array.retrieve_file("E-MEXP-31", "E-MEXP-31.idf.txt")
    assert content is not None
    assert "E-MEXP-31" in content


def test_retrieve_file_save(array):
    array.retrieve_file("E-MEXP-31", "E-MEXP-31.idf.txt", save=True)
    assert os.path.exists("E-MEXP-31.idf.txt")
    os.remove("E-MEXP-31.idf.txt")


def test_retrieve_file_invalid(array):
    with pytest.raises(ValueError):
        array.retrieve_file("E-MEXP-31", "nonexistent_file.txt")


# -----------------------------------------------------------------------
# Tests for backward-compatible methods
# -----------------------------------------------------------------------


def test_queryExperiments_keywords(array):
    res = array.queryExperiments(keywords="breast cancer")
    assert "totalHits" in res
    assert res["totalHits"] > 0


def test_queryExperiments_array_species(array):
    res = array.queryExperiments(array="A-AFFY-33", species="Homo Sapiens")
    assert "totalHits" in res


def test_queryExperiments_sort(array):
    res = array.queryExperiments(keywords="cancer", sortby="releasedate", sortorder="ascending")
    assert "totalHits" in res


def test_queryExperiments_invalid_param(array):
    with pytest.raises(ValueError):
        array.queryExperiments(invalid_param="foo")


def test_queryFiles(array):
    res = array.queryFiles(keywords="breast cancer")
    assert "totalHits" in res
    assert "hits" in res
    assert res["hits"][0]["files"] > 0


def test_retrieveExperiment(array):
    study = array.retrieveExperiment("E-MEXP-31")
    assert study["accno"] == "E-MEXP-31"


def test_retrieveFilesFromExperiment(array):
    files = array.retrieveFilesFromExperiment("E-MEXP-31")
    assert "E-MEXP-31.idf.txt" in files


def test_retrieveFile_legacy(array):
    content = array.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")
    assert "E-MEXP-31" in content


def test_queryAE(array):
    accessions = array.queryAE("pneumonia homo sapiens")
    assert isinstance(accessions, list)
    assert len(accessions) > 0
    assert all(acc.startswith("E-") for acc in accessions)
