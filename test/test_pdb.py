from bioservices import PDB

def test_pdb():
    s = PDB()
    res = s.get_file("1FBV", "pdb")
    res = s.get_file("1FBV", "xml", compression=True)
    res = s.get_file("1FBV", "cif")

    ids = s.get_current_ids()

