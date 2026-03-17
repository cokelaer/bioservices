import pytest

from bioservices.rhea import Rhea


@pytest.fixture(scope="module")
def rhea():
    return Rhea(verbose=False)


def test_rhea(rhea):
    r1 = rhea.search("caffeine", limit=2)
    df = rhea.query("rhea:10660")
