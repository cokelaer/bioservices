from bioservices import PDB
from .settings import DEBUG

def test_pdb():
    s = PDB()
    res = s.get_file("1FBV", "pdb")
    res = s.get_file("1FBV", "xml", compression=True)
    res = s.get_file("1FBV", "cif")

    if DEBUG:
        ids = s.get_current_ids()

