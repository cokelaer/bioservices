from bioservices import PDB


def test_pdb():
    s = PDB()
    res = s.getFile("1FBV", "pdb")
    res = s.getFile("1FBV", "xml")
    ids = s.getCurrentIDs()

