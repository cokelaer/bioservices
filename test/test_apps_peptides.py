import pytest

from bioservices.apps.peptides import Peptides


@pytest.mark.network
def test_peptides():
    p = Peptides()
    pos = p.get_phosphosite_position("Q8IYB3", "VPKPEPIPEPKEPSPE")
    assert pos == [740, 901]
