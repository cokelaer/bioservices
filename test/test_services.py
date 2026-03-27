import binascii
import os
import tempfile
import time
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest
import requests
from requests.models import Response

from bioservices.services import (
    REST,
    BioServicesError,
    HTTPResponseError,
    RESTbase,
    Service,
)


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


# ---------------------------------------------------------------------------
# REST.http_get — single-query and async paths
# ---------------------------------------------------------------------------


def test_rest_http_get_single_query(rest, mocker):
    """Single string query should build headers and delegate to get_one."""
    mock_get_one = mocker.patch.object(rest, "get_one", return_value={"result": "ok"})
    result = rest.http_get("proteins/P12345", frmt="json")
    assert result == {"result": "ok"}
    mock_get_one.assert_called_once()


def test_rest_http_get_large_list_uses_async(rest, mocker):
    """Lists larger than ASYNC_THRESHOLD (10) should use the async path."""
    queries = [f"q{i}" for i in range(11)]
    mock_async = mocker.patch.object(rest, "get_async", return_value=[{}] * 11)
    rest.http_get(queries, frmt="json")
    mock_async.assert_called_once()


# ---------------------------------------------------------------------------
# REST.get_headers — parametrize over content types
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "content,expected_mime",
    [
        ("json", "application/json"),
        ("xml", "application/xml"),
        ("txt", "text/plain"),
        ("text", "text/plain"),
        ("fasta", "text/x-fasta"),
        ("bed", "text/x-bed"),
        ("png", "image/png"),
        ("gff3", "text/x-gff3"),
        ("yaml", "text/x-yaml"),
        ("default", "application/x-www-form-urlencoded"),
    ],
)
def test_rest_get_headers_content_types(rest, content, expected_mime):
    headers = rest.get_headers(content=content)
    assert headers["Accept"] == expected_mime
    assert headers["Content-Type"] == expected_mime
    assert "User-Agent" in headers


# ---------------------------------------------------------------------------
# REST._build_url — parametrize over URL patterns
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "query,expected",
    [
        (None, "http://example.com/api"),
        ("proteins/P12345", "http://example.com/api/proteins/P12345"),
        ("http://other.com/resource", "http://other.com/resource"),
        ("https://secure.com/data", "https://secure.com/data"),
    ],
)
def test_rest_build_url_parametrized(rest, query, expected):
    assert rest._build_url(query) == expected


# ---------------------------------------------------------------------------
# HTTPResponseError — parametrize hint messages for all known status codes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "status_code,hint_fragment",
    [
        (400, "query parameters"),
        (401, "Authentication"),
        (403, "Access denied"),
        (404, "resource was not found"),
        (408, "timed out"),
        (429, "Slow down"),
        (500, "Internal server error"),
        (503, "Service unavailable"),
        (418, "Check the input"),  # unknown code → fallback hint
    ],
)
def test_http_response_error_hint_messages(status_code, hint_fragment):
    e = HTTPResponseError(status_code, reason="test", url="http://x.com")
    with pytest.raises(BioServicesError, match=hint_fragment):
        e["key"]


# ---------------------------------------------------------------------------
# REST._calls — rate-limiting behaviour
# ---------------------------------------------------------------------------


def test_calls_first_call_no_sleep(rest, mocker):
    """The very first call (last_call == 0) should never sleep."""
    rest._last_call = 0
    mock_sleep = mocker.patch("bioservices.services.time.sleep")
    rest._calls()
    mock_sleep.assert_not_called()
    assert rest._last_call > 0


def test_calls_rate_limiting_sleeps(rest, mocker):
    """A call made immediately after another should trigger a sleep."""
    rest.requests_per_sec = 1  # time_lapse = 1.0 s
    rest._last_call = time.time()  # pretend last call was just now
    mock_sleep = mocker.patch("bioservices.services.time.sleep")
    rest._calls()
    mock_sleep.assert_called_once()


def test_calls_no_sleep_when_sufficient_gap(rest, mocker):
    """A call made long after the previous one should not sleep."""
    rest.requests_per_sec = 10  # time_lapse = 0.1 s
    rest._last_call = time.time() - 2.0  # 2 seconds ago — well past the limit
    mock_sleep = mocker.patch("bioservices.services.time.sleep")
    rest._calls()
    mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# REST.clear_cache
# ---------------------------------------------------------------------------


def test_rest_clear_cache(rest, mocker):
    mock_clear = mocker.patch("requests_cache.clear")
    rest.clear_cache()
    mock_clear.assert_called_once()


# ---------------------------------------------------------------------------
# REST._get_all_urls
# ---------------------------------------------------------------------------


def test_rest_get_all_urls(rest):
    keys = ["proteins/P12345", "proteins/P67890"]
    urls = list(rest._get_all_urls(keys))
    assert urls == [
        "http://example.com/api/proteins/P12345",
        "http://example.com/api/proteins/P67890",
    ]


# ---------------------------------------------------------------------------
# REST.post_one / http_post
# ---------------------------------------------------------------------------


def test_rest_http_post_delegates_to_post_one(rest, mocker):
    mock_post_one = mocker.patch.object(rest, "post_one", return_value={"ok": True})
    rest.http_post("submit", data={"seq": "ATGC"}, frmt="json")
    mock_post_one.assert_called_once()


def test_rest_http_post_custom_headers_preserved(rest, mocker):
    mock_post_one = mocker.patch.object(rest, "post_one", return_value={"ok": True})
    custom = {"X-Custom": "val"}
    rest.http_post("submit", headers=custom, frmt="json")
    call_kwargs = mock_post_one.call_args[1]
    assert call_kwargs["headers"] == custom


def test_rest_post_one_bytes_result_decoded(rest, mocker):
    mocker.patch.object(rest, "_calls")
    mock_resp = MagicMock(spec=Response)
    mocker.patch.object(rest.session, "post", return_value=mock_resp)
    mocker.patch.object(rest, "_interpret_returned_request", return_value=b"hello")
    result = rest.post_one(query="submit", frmt="xml")
    assert result == "hello"


def test_rest_post_one_non_bytes_result_returned_as_is(rest, mocker):
    mocker.patch.object(rest, "_calls")
    mock_resp = MagicMock(spec=Response)
    mocker.patch.object(rest.session, "post", return_value=mock_resp)
    mocker.patch.object(rest, "_interpret_returned_request", return_value={"key": "val"})
    result = rest.post_one(query="submit", frmt="json")
    assert result == {"key": "val"}


def test_rest_post_one_exception_returns_none(rest, mocker):
    mocker.patch.object(rest, "_calls")
    mocker.patch.object(rest.session, "post", side_effect=Exception("network error"))
    result = rest.post_one(query="submit", frmt="json")
    assert result is None


# ---------------------------------------------------------------------------
# REST.delete_one / http_delete
# ---------------------------------------------------------------------------


def test_rest_delete_one_bytes_result_decoded(rest, mocker):
    mocker.patch.object(rest, "_calls")
    mock_resp = MagicMock(spec=Response)
    mocker.patch.object(rest.session, "delete", return_value=mock_resp)
    mocker.patch.object(rest, "_interpret_returned_request", return_value=b"deleted")
    result = rest.delete_one(query="resource/123", frmt="json")
    assert result == "deleted"


def test_rest_delete_one_exception_returns_none(rest, mocker):
    mocker.patch.object(rest, "_calls")
    mocker.patch.object(rest.session, "delete", side_effect=Exception("network error"))
    result = rest.delete_one(query="resource/123", frmt="json")
    assert result is None


def test_rest_http_delete_delegates_to_delete_one(rest, mocker):
    mock_delete_one = mocker.patch.object(rest, "delete_one", return_value="ok")
    rest.http_delete("resource/123", frmt="json")
    mock_delete_one.assert_called_once()


# ---------------------------------------------------------------------------
# RESTbase — abstract HTTP methods raise NotImplementedError
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("method", ["http_get", "http_post", "http_put", "http_delete"])
def test_restbase_abstract_methods_raise(restbase, method):
    with pytest.raises(NotImplementedError):
        getattr(restbase, method)()
