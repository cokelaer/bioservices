from bioservices import GEO

g = GEO()


def test_search():
    res = g.search("breast cancer", db="gds", retmax=5)
    assert isinstance(res, dict)
    assert "count" in res
    assert "idlist" in res
    assert int(res["count"]) > 0


def test_search_with_organism():
    res = g.search("breast cancer AND Homo sapiens[organism]", db="gds", retmax=5)
    assert isinstance(res, dict)
    assert "count" in res
    assert int(res["count"]) > 0


def test_get_summary():
    # First search to get a UID
    search_res = g.search("GSE10[ACCN]", db="gds", retmax=1)
    assert search_res and search_res.get("idlist")
    uid = search_res["idlist"][0]
    res = g.get_summary(uid, db="gds")
    assert isinstance(res, dict)


def test_get_summary_list():
    search_res = g.search("GSE10[ACCN]", db="gds", retmax=1)
    if search_res and search_res.get("idlist"):
        uid = search_res["idlist"][0]
        res = g.get_summary([uid], db="gds")
        assert isinstance(res, dict)


def test_get_accession_info():
    res = g.get_accession_info("GSE10")
    assert res is not None
    assert isinstance(res, dict)


def test_get_geo_datasets():
    res = g.get_geo_datasets("cancer", organism="Homo sapiens", retmax=5)
    assert isinstance(res, dict)
    assert "count" in res


def test_get_geo_series():
    res = g.get_geo_series("BRCA1", organism="Homo sapiens", retmax=5)
    assert isinstance(res, dict)
    assert "count" in res


def test_get_geo_samples():
    res = g.get_geo_samples("cancer", organism="Homo sapiens", retmax=5)
    assert isinstance(res, dict)
    assert "count" in res


def test_get_geo_platforms():
    res = g.get_geo_platforms("Affymetrix", organism="Homo sapiens", retmax=5)
    assert isinstance(res, dict)
    assert "count" in res


def test_fetch():
    search_res = g.search("GSE10[ACCN]", db="gds", retmax=1)
    if search_res and search_res.get("idlist"):
        uid = search_res["idlist"][0]
        res = g.fetch(uid, db="gds")
        assert res is not None
