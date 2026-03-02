from unittest.mock import patch
from urllib.error import HTTPError, URLError

import pytest
import requests

from bioservices.services import REST, Service, WSDLService


class test_Service(Service):
    def __init__(self):
        super(test_Service, self).__init__("test", "http://www.uniprot.org", verbose=False)
        self.url
        self.easyXMLConversion

    def test_easyXML(self):
        self.easyXML("<xml><id></id></xml>")

    def test_pubmed(self):
        self.pubmed("24064416")


def test_service():
    this = test_Service()
    this.test_easyXML()
    # this.test_pubmed()


class test_REST(REST):
    def __init__(self):
        super(test_REST, self).__init__("test", "http://www.uniprot.org", verbose=False)

    def test_request(self):
        try:
            self.request("dummy")
            assert False
        except:
            assert True


def test_rest():
    this = test_REST()
    this.test_request()


def test_service_http_error_no_warning(caplog):
    """HTTPError (4xx/5xx) should not trigger an 'unreachable' warning (issue #285)."""
    with patch("bioservices.services.urlopen", side_effect=HTTPError(None, 404, "Not Found", {}, None)):
        svc = Service("test", "http://example.com/api", verbose=True)
    assert "cannot be reached" not in caplog.text


def test_service_url_error_warns(caplog):
    """URLError (connection failure) should trigger an 'unreachable' warning."""
    with patch("bioservices.services.urlopen", side_effect=URLError("connection refused")):
        svc = Service("test", "http://example.com/api", verbose=True)
    assert "cannot be reached" in caplog.text


def test_cache_session_fallback_on_error(caplog):
    """When CachedSession creation fails, fall back to a regular session with a warning."""
    import requests_cache

    with patch("bioservices.services.urlopen", side_effect=URLError("connection refused")):
        with patch.object(requests_cache, "CachedSession", side_effect=Exception("You must install the python package: sqlite3")):
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
