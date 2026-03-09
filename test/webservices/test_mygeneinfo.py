from unittest.mock import patch

from bioservices.mygeneinfo import MyGeneInfo

mgi = MyGeneInfo()


def test_get_genes_uses_post_with_data():
    """Verify that get_genes sends ids in the POST body (data), not as URL params."""
    mock_response = [{"_id": "301345"}, {"_id": "22637"}]
    with patch.object(mgi.services, "http_post", return_value=mock_response) as mock_post:
        result = mgi.get_genes("301345,22637")
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert "data" in kwargs
        assert kwargs["data"]["ids"] == "301345,22637"
        # params should not be passed (ids should be in data, not URL params)
        assert kwargs.get("params") is None


def test_get_genes_uses_post_with_data_species():
    """Verify that species is also sent in the POST body when provided."""
    mock_response = [{"notfound": True}, {"_id": "22637"}]
    with patch.object(mgi.services, "http_post", return_value=mock_response) as mock_post:
        result = mgi.get_genes("301345,22637", species="mouse")
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert "data" in kwargs
        assert kwargs["data"]["species"] == "mouse"


def test_get_queries_uses_post_with_data():
    """Verify that get_queries sends the query in the POST body (data)."""
    mock_response = [{"_id": "1017", "query": "zap70"}]
    with patch.object(mgi.services, "http_post", return_value=mock_response) as mock_post:
        result = mgi.get_queries("zap70")
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert "data" in kwargs
        assert kwargs["data"] == {"q": "zap70"}


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
    assert res["total"] >= 0
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
