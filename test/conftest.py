"""Root pytest configuration shared across all bioservices tests."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

#: Everything under test/webservices/ calls a live remote API.
WEBSERVICES_DIR = Path(__file__).parent / "webservices"

#: Recorded payloads, see dev/record_fixtures.py.
FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Live-network tests are opt-in
# ---------------------------------------------------------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--network",
        action="store_true",
        default=False,
        help="also run the tests that call live web services (skipped by default)",
    )


def pytest_collection_modifyitems(config, items):
    """Mark and, unless --network was passed, skip the live-network tests.

    Marking and skipping happen in this one hook rather than in a
    test/webservices/conftest.py so that there is no dependency on the order in
    which pytest calls conftest hooks: the directory rule is applied before the
    skip decision reads the marker, always.
    """
    run_network = config.getoption("--network")
    skip_network = pytest.mark.skip(reason="calls a live web service; pass --network to run it")

    for item in items:
        if WEBSERVICES_DIR in Path(str(item.fspath)).parents:
            item.add_marker(pytest.mark.network)
        if not run_network and "network" in item.keywords:
            item.add_marker(skip_network)


# ---------------------------------------------------------------------------
# Recorded payloads
# ---------------------------------------------------------------------------


def load_fixture(name):
    """Load a recorded exchange by name, e.g. ``"uniprot/search_zap70"``.

    :param str name: path under ``test/fixtures``, without the ``.json``.
    :returns: the recorded ``{"request": ..., "response": ...}`` mapping.
    :raises FileNotFoundError: with a pointer to the recorder script.
    """
    path = FIXTURES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"No fixture {name!r} at {path}. Record it with: python dev/record_fixtures.py {name}")
    return json.loads(path.read_text())


@pytest.fixture
def fixture():
    """Return :func:`load_fixture`, for tests that need recorded payloads."""
    return load_fixture


@pytest.fixture
def fixture_body():
    """Return a helper giving just the response body of a recorded exchange."""

    def _body(name):
        return load_fixture(name)["response"]["body"]

    return _body


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
