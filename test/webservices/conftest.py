"""Shared pytest configuration for webservices tests.

Patches webbrowser.open (and the webbrowser module imported inside service
modules) so that tests never open a real browser window.
"""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def no_browser(monkeypatch):
    """Prevent any test from opening a browser window."""
    monkeypatch.setattr("webbrowser.open", lambda *a, **kw: None)
    monkeypatch.setattr("webbrowser.open_new", lambda *a, **kw: None)
    monkeypatch.setattr("webbrowser.open_new_tab", lambda *a, **kw: None)
