import pytest
from bioservices import BioCarta

def test_biocarta():

    b = BioCarta()
    res = b.get_pathway_protein_names('h_RELAPathway')
    assert len(res) == 13

    b.organism = 'Homo sapiens'
    b.all_pathways
