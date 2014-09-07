from bioservices import chemspider

from nose.plugins.attrib import attr


# works only if you have a token
@attr('skip_travis')
def test_chemspider():
    s = chemspider.ChemSpider()
    assert s.find("Pyridine") == [1020]
    s.GetExtendedCompoundInfo(1020)
    s.mol(1020)
    s.mol3d(1020)
    s.image(1020)
    s.ImagesHandler(1020)
    s.databases
