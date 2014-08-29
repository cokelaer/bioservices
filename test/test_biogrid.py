from bioservices import *


def test_biogrid():
    b = BioGRID(query=["map2k4","akt1"],taxId = "9606")
    b.biogrid.interactors
    b = BioGRID(query=["mtor","akt1"],taxId="9606",exP="two hybrid")
    b = BioGRID(query="mtor",taxId="9606")
    b.biogrid.interactors


