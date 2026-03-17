import pytest

from bioservices import HGNC


@pytest.fixture(scope="module")
def hgnc():
    return HGNC(verbose=False)


def test_hgnc(hgnc):
    hgnc.get_info()
    hgnc.fetch("symbol", "ZNF3")
    hgnc.fetch("alias_name", "A-kinase anchor protein, 350kDa")
    hgnc.search("BRAF")
    hgnc.search("symbol", "ZNF*")
    hgnc.search("symbol", "ZNF?")
    hgnc.search("symbol", "ZNF*+AND+status:Approved")
    hgnc.search("symbol", "ZNF3+OR+ZNF12")
    hgnc.search("symbol", "ZNF*+NOT+status:Approved")


def test_hgnc_search_no_args(hgnc):
    with pytest.raises(ValueError):
        hgnc.search()
