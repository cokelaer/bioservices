from bioservices.mygeneinfo import MyGeneInfo

mgi = MyGeneInfo()


def test_get_all_genes():
    res = mgi.get_genes("301345,22637")
    assert len(res) == 2
    assert res[0]["_id"] == "301345"

    mgi.get_genes(("301345,22637"))
    # first one is rat, second is mouse. This will return a 'notfound'
    # entry and the second entry as expected.
    res = mgi.get_genes("301345,22637", species="mouse")
    assert "_id" not in res[0]
    assert res[1]["_id"] == "22637"
    assert res[1]["taxid"] == 10090


def test_get_one_gene():
    res = mgi.get_one_gene("301345")
    assert res["_id"] == "301345"
    assert res["taxid"] == 10116


def test_get_one_query():
    res = mgi.get_one_query("zap70", size=10, dotfield=True, sort="taxid")

    # sort by taxid to make sure we always test against the same object
    res["hits"] = sorted(res["hits"], key=lambda x: x.get("taxid", 0))
    hit = res["hits"][0]

    assert isinstance(res["took"], int)
    assert res["total"] == 401
    assert res["max_score"] is None
    assert hit["_id"] == "24590835"
    assert hit["_score"] is None
    assert hit["entrezgene"] == "24590835"
    assert hit["name"] == "Tyrosine-protein kinase ZAP-70"
    assert hit["symbol"] == "ZAP70"
    assert hit["taxid"] == 6185


def test_get_queries():
    res = mgi.get_queries("zap70,zap70", dotfield=True)

    # sort by taxid to make sure we always test against the same object
    res = sorted(res, key=lambda x: x["taxid"])
    assert len(res) == 20
    assert res[0]["query"] == "zap70"
    assert res[0]["_id"] == "ENSIPUG00015013332"
    assert 12 <= res[0]["_score"] <= 13
    assert res[0]["symbol"] == "ZAP70"
    assert res[0]["taxid"] == 7998


def test_get_metadata():
    res = mgi.get_metadata()
    assert res["biothing_type"] == "gene"
    assert "human" in res["genome_assembly"]


def test_get_taxonomy():
    res = mgi.get_taxonomy()
    assert res["human"] == 9606
    assert res["mouse"] == 10090
    assert res["rat"] == 10116
    assert res["fruitfly"] == 7227
    assert res["nematode"] == 6239
    assert res["zebrafish"] == 7955
    assert res["thale-cress"] == 3702
    assert res["frog"] == 8364
    assert res["pig"] == 9823
