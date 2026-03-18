import pytest

from bioservices.rhea import Rhea


@pytest.fixture(scope="module")
def rhea():
    return Rhea(verbose=False)


def test_rhea(rhea):
    rhea.search("caffeine", limit=2)
    rhea.query("rhea:10660")
