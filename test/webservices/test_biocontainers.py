from bioservices import Biocontainers
import pytest
import os

skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
    reason="too slow for travis")


@skiptravis
@pytest.mark.xfail
def test_biocontainers():

    b = Biocontainers()
    stats = b.get_stats()
    b.get_tools(limit=10)
    b.get_versions_one_tool("bioservices")

