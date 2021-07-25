from bioservices import PubChem



def test_compound_by_smiles():

    p = PubChem()
    p.get_compound_by_smiles("CC(=O)Oc1ccccc1C(=O)O")

