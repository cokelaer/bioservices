"""Root pytest configuration shared across all bioservices tests."""
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def svc():
    """A Service instance that never makes real network calls."""
    from bioservices.services import Service

    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        s = Service("testsvc", "http://example.com/api", verbose=False)
    return s


@pytest.fixture
def rest():
    """A REST instance that never makes real network calls."""
    from bioservices.services import REST

    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        r = REST("testrest", "http://example.com/api", verbose=False)
    return r


@pytest.fixture
def restbase():
    """A RESTbase instance that never makes real network calls."""
    from bioservices.services import RESTbase

    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        rb = RESTbase("testbase", "http://example.com/api", verbose=False)
    return rb
