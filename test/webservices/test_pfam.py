from bioservices import Pfam



def test_pfam():

    p = Pfam()
    p.show("P00789")
    p.get_protein("P00789")
