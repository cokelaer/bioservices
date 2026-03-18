import binascii
import os
import tempfile
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest
import requests
from requests.models import Response

from bioservices.services import REST, BioServicesError, HTTPResponseError, Service


class test_Service(Service):
    def __init__(self):
        super(test_Service, self).__init__("test", "http://www.uniprot.org", verbose=False)
        self.url

    def test_pubmed(self):
        self.pubmed("24064416")


def test_service():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        test_Service()
    # this.test_pubmed()


class test_REST(REST):
    def __init__(self):
        super(test_REST, self).__init__("test", "http://www.uniprot.org", verbose=False)

    def test_request(self):
        with pytest.raises(Exception):
            self.request("dummy")


def test_rest():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        this = test_REST()
    this.test_request()


def test_service_http_error_no_warning(caplog):
    """HTTPError (4xx/5xx) should not trigger an 'unreachable' warning (issue #285)."""
    with patch("bioservices.services.urlopen", side_effect=HTTPError(None, 404, "Not Found", {}, None)):
        Service("test", "http://example.com/api", verbose=True)
    assert "cannot be reached" not in caplog.text


def test_service_url_error_warns(caplog):
    """URLError (connection failure) should trigger an 'unreachable' warning."""
    with patch("bioservices.services.urlopen", side_effect=URLError("connection refused")):
        Service("test", "http://example.com/api", verbose=True)
    assert "cannot be reached" in caplog.text


def test_cache_session_fallback_on_error(caplog):
    """When CachedSession creation fails, fall back to a regular session with a warning."""
    import requests_cache

    with patch("bioservices.services.urlopen", side_effect=URLError("connection refused")):
        with patch.object(
            requests_cache, "CachedSession", side_effect=Exception("You must install the python package: sqlite3")
        ):
            svc = REST("test", "http://example.com/api", verbose=True, cache=True)
            # Reset session so _create_cache_session creates a new one
            svc._session = None
            session = svc._create_cache_session()

    assert session is not None
    assert "Could not create a cached session" in caplog.text
    assert "Falling back to a regular session" in caplog.text


def test_install_cache_fallback_on_error(caplog):
    """When install_cache fails, caching is disabled gracefully with a warning."""
    import requests_cache

    with patch("bioservices.services.urlopen", side_effect=URLError("connection refused")):
        with patch.object(requests_cache, "install_cache", side_effect=Exception("sqlite3 not available")):
            svc = REST("test", "http://example.com/api", verbose=True, cache=True)

    assert "Could not install cache" in caplog.text
    assert svc.CACHING is False


# ---------------------------------------------------------------------------
# BioServicesError
# ---------------------------------------------------------------------------


def test_bioservices_error():
    err = BioServicesError("something went wrong")
    assert "something went wrong" in str(err)


# ---------------------------------------------------------------------------
# HTTPResponseError
# ---------------------------------------------------------------------------


def test_http_response_error_is_int():
    e = HTTPResponseError(404, reason="Not Found", url="http://example.com")
    assert isinstance(e, int)
    assert e == 404


def test_http_response_error_attributes():
    e = HTTPResponseError(403, reason="Forbidden", url="http://example.com/api")
    assert e.status_code == 403
    assert e.reason == "Forbidden"
    assert e.url == "http://example.com/api"


def test_http_response_error_repr():
    e = HTTPResponseError(404, reason="Not Found")
    assert "404" in repr(e)
    assert "Not Found" in repr(e)


def test_http_response_error_str():
    e = HTTPResponseError(404, reason="Not Found")
    assert "404" in str(e)
    assert "Not Found" in str(e)


def test_http_response_error_getitem_raises_friendly():
    e = HTTPResponseError(404, reason="Not Found", url="http://example.com")
    with pytest.raises(BioServicesError, match="404"):
        _ = e["key"]


def test_http_response_error_iter_raises_friendly():
    e = HTTPResponseError(500, reason="Internal Server Error")
    with pytest.raises(BioServicesError, match="500"):
        list(e)


def test_http_response_error_len_raises_friendly():
    e = HTTPResponseError(403, reason="Forbidden")
    with pytest.raises(BioServicesError):
        len(e)


def test_http_response_error_keys_raises_friendly():
    e = HTTPResponseError(400, reason="Bad Request")
    with pytest.raises(BioServicesError):
        e.keys()


def test_http_response_error_values_raises_friendly():
    e = HTTPResponseError(400, reason="Bad Request")
    with pytest.raises(BioServicesError):
        e.values()


def test_http_response_error_items_raises_friendly():
    e = HTTPResponseError(400, reason="Bad Request")
    with pytest.raises(BioServicesError):
        e.items()


def test_http_response_error_known_hint_in_message():
    e = HTTPResponseError(429, reason="Too Many Requests", url="http://x.com")
    with pytest.raises(BioServicesError, match="Slow down"):
        e["result"]


def test_http_response_error_unknown_status_fallback_hint():
    e = HTTPResponseError(418, reason="I'm a Teapot")
    with pytest.raises(BioServicesError, match="Check the input"):
        e["result"]


def test_interpret_bad_status_returns_http_response_error(rest):
    mock_resp = MagicMock(spec=Response)
    mock_resp.ok = False
    mock_resp.reason = "Not Found"
    mock_resp.status_code = 404
    mock_resp.url = "http://example.com/missing"
    result: HTTPResponseError = rest._interpret_returned_request(mock_resp, "json")
    assert isinstance(result, HTTPResponseError)
    assert result == 404
    assert result.reason == "Not Found"
    assert result.url == "http://example.com/missing"


# ---------------------------------------------------------------------------
# Service utility methods (no network required)
# ---------------------------------------------------------------------------


@pytest.fixture
def svc():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        s = Service("testsvc", "http://example.com/api", verbose=False)
    return s


@pytest.fixture
def rest():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        r = REST("testrest", "http://example.com/api", verbose=False)
    return r


def test_service_str(svc):
    assert "testsvc" in str(svc)


def test_service_url_strips_trailing_slash(svc):
    svc.url = "http://example.com/api/"
    assert not svc.url.endswith("/")


def test_service_url_none():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        s = Service("t", None, verbose=False)
    assert s.url is None


def test_service_pubmed_calls_browser(svc):
    with patch("webbrowser.open") as mock_open:
        svc.pubmed("12345678")
    mock_open.assert_called_once()
    assert "12345678" in mock_open.call_args[0][0]


def test_service_on_web_calls_browser(svc):
    with patch("webbrowser.open") as mock_open:
        svc.on_web("http://example.com")
    mock_open.assert_called_once_with("http://example.com")


def test_service_save_str_to_image(svc):
    raw = b"hello"
    encoded = binascii.b2a_base64(raw).decode("utf-8").strip()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        fname = f.name
    try:
        svc.save_str_to_image(encoded, fname)
        with open(fname, "rb") as f:
            assert f.read() == raw
    finally:
        os.unlink(fname)


# ---------------------------------------------------------------------------
# REST utility methods (no network required)
# ---------------------------------------------------------------------------


def test_rest_build_url_none(rest):
    assert rest._build_url(None) == rest.url


def test_rest_build_url_relative(rest):
    url = rest._build_url("proteins/P12345")
    assert url == "http://example.com/api/proteins/P12345"


def test_rest_build_url_absolute(rest):
    abs_url = "http://other.com/resource"
    assert rest._build_url(abs_url) == abs_url


def test_rest_get_user_agent(rest):
    ua = rest.getUserAgent()
    assert "BioServices" in ua
    assert "Python" in ua


def test_rest_get_headers_default(rest):
    headers = rest.get_headers()
    assert "User-Agent" in headers
    assert "Accept" in headers
    assert "Content-Type" in headers


def test_rest_get_headers_json(rest):
    headers = rest.get_headers(content="json")
    assert headers["Accept"] == "application/json"


def test_rest_timeout_property(rest):
    original = rest.TIMEOUT
    rest.TIMEOUT = 999
    assert rest.TIMEOUT == 999
    rest.TIMEOUT = original


def test_rest_caching_property(rest):
    rest.CACHING = False
    assert rest.CACHING is False


def test_rest_interpret_non_response(rest):
    result = rest._interpret_returned_request("raw_string", "json")
    assert result == "raw_string"


def test_rest_interpret_bad_status(rest):
    mock_resp = MagicMock(spec=Response)
    mock_resp.ok = False
    mock_resp.reason = "Not Found"
    mock_resp.status_code = 404
    result = rest._interpret_returned_request(mock_resp, "json")
    assert result == 404


def test_rest_interpret_json_response(rest):
    mock_resp = MagicMock(spec=Response)
    mock_resp.ok = True
    mock_resp.json.return_value = {"key": "value"}
    result = rest._interpret_returned_request(mock_resp, "json")
    assert result == {"key": "value"}


def test_rest_interpret_content_response(rest):
    mock_resp = MagicMock(spec=Response)
    mock_resp.ok = True
    mock_resp.content = b"<xml/>"
    result = rest._interpret_returned_request(mock_resp, "xml")
    assert result == b"<xml/>"


def test_rest_get_sync(rest):
    with patch.object(rest, "get_one", return_value={"id": "x"}) as mock_get:
        results = rest.get_sync(["q1", "q2"], frmt="json")
    assert len(results) == 2
    assert mock_get.call_count == 2


def test_rest_http_get_list_sync(rest):
    # ASYNC_THRESHOLD defaults to 10; a 2-item list uses the sync path
    with patch.object(rest, "get_one", return_value={}) as mock_get:
        results = rest.http_get(["q1", "q2"], frmt="json")
    assert len(results) == 2
