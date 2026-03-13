from unittest.mock import patch

import pytest

from bioservices.stringdb import STRING

s = STRING()


def test_get_string_ids_post():
    """Verify get_string_ids uses POST with identifiers in the form data."""
    mock_response = [{"queryIndex": 0, "stringId": "9606.ENSP00000379990", "preferredName": "ZAP70"}]
    with patch.object(s.services, "http_post", return_value=mock_response) as mock_post:
        result = s.get_string_ids("ZAP70", species=9606)
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert "data" in kwargs
        assert kwargs["data"]["identifiers"] == "ZAP70"
        assert kwargs["data"]["species"] == 9606


def test_get_string_ids_list_input():
    """Verify that a list of identifiers is joined with %0d separator."""
    mock_response = []
    with patch.object(s.services, "http_post", return_value=mock_response) as mock_post:
        s.get_string_ids(["ZAP70", "LCK"], species=9606)
        _, kwargs = mock_post.call_args
        assert "%0d" in kwargs["data"]["identifiers"]


def test_get_interactions_post():
    """Verify get_interactions sends identifiers via POST."""
    mock_response = [{"stringId_A": "9606.ENSP00000379990", "stringId_B": "9606.ENSP00000281879", "score": 900}]
    with patch.object(s.services, "http_post", return_value=mock_response) as mock_post:
        result = s.get_interactions("ZAP70", species=9606, required_score=400)
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert kwargs["data"]["identifiers"] == "ZAP70"
        assert kwargs["data"]["species"] == 9606
        assert kwargs["data"]["required_score"] == 400


def test_get_interaction_partners_post():
    """Verify get_interaction_partners sends identifiers via POST."""
    mock_response = [{"stringId_A": "9606.ENSP00000379990", "stringId_B": "9606.ENSP00000281879", "score": 850}]
    with patch.object(s.services, "http_post", return_value=mock_response) as mock_post:
        result = s.get_interaction_partners("ZAP70", species=9606, limit=5)
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert kwargs["data"]["identifiers"] == "ZAP70"
        assert kwargs["data"]["limit"] == 5


def test_get_enrichment_post():
    """Verify get_enrichment sends identifiers via POST."""
    mock_response = [{"category": "Process", "term": "GO:0007166", "p_value": 0.001}]
    with patch.object(s.services, "http_post", return_value=mock_response) as mock_post:
        result = s.get_enrichment("ZAP70,LCK,CD3E,CD3D", species=9606)
        assert result == mock_response
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert kwargs["data"]["identifiers"] == "ZAP70,LCK,CD3E,CD3D"
        assert kwargs["data"]["species"] == 9606


def test_get_ppi_enrichment_post():
    """Verify get_ppi_enrichment sends identifiers via POST."""
    mock_response = [{"number_of_nodes": 3, "number_of_edges": 3, "p_value": 0.001}]
    with patch.object(s.services, "http_post", return_value=mock_response) as mock_post:
        result = s.get_ppi_enrichment("ZAP70,LCK,CD3E", species=9606)
        assert result == mock_response[0]
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert kwargs["data"]["identifiers"] == "ZAP70,LCK,CD3E"


def test_get_version_get():
    """Verify get_version calls the version endpoint with GET."""
    mock_response = [{"string_version": "12.0", "stable_address": "https://version-12-0.string-db.org"}]
    with patch.object(s.services, "http_get", return_value=mock_response) as mock_get:
        result = s.get_version()
        assert result == mock_response[0]
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert "version" in args[0]


def test_get_string_ids_live():
    """Live test: resolve ZAP70 human gene to a STRING ID."""
    res = s.get_string_ids("ZAP70", species=9606, limit=1)
    assert isinstance(res, list)
    assert len(res) >= 1
    assert "stringId" in res[0]
    assert "9606" in res[0]["stringId"]


def test_get_interactions_live():
    """Live test: retrieve interactions for ZAP70."""
    res = s.get_interactions("ZAP70", species=9606, required_score=700)
    assert isinstance(res, list)
    assert len(res) > 0
    first = res[0]
    assert "stringId_A" in first
    assert "stringId_B" in first
    assert "score" in first


def test_get_interaction_partners_live():
    """Live test: retrieve interaction partners for ZAP70."""
    res = s.get_interaction_partners("ZAP70", species=9606, limit=5, required_score=700)
    assert isinstance(res, list)
    assert 0 < len(res) <= 5


def test_get_enrichment_live():
    """Live test: functional enrichment for a set of T-cell signalling genes."""
    res = s.get_enrichment("ZAP70,LCK,CD3E,CD3D", species=9606)
    assert isinstance(res, list)
    assert len(res) > 0
    assert "category" in res[0]
    assert "p_value" in res[0]


def test_get_ppi_enrichment_live():
    """Live test: PPI enrichment for a small gene set."""
    res = s.get_ppi_enrichment("ZAP70,LCK,CD3E", species=9606)
    assert isinstance(res, dict)
    assert "p_value" in res
    assert "number_of_edges" in res


def test_get_version_live():
    """Live test: retrieve STRING API version."""
    res = s.get_version()
    assert isinstance(res, dict)
    assert "string_version" in res
