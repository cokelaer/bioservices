from bioservices.apps.peptides import Peptides



def test_peptides():
    p = Peptides()
    pos = p.get_phosphosite_position("Q8IYB3", "VPKPEPIPEPKEPSPE")
    assert pos == [740, 901]

