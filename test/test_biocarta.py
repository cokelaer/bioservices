import pytest
from bioservices import BioCarta

@skiptravis
# @pytest.mark.skip(reason="The NCI CBIIT instance of the CGAP and Mitelman data is no longer supported.")
def test_biocarta():

    b = BioCarta()
    res = b.get_pathway_protein_names('h_RELAPathway')
    assert len(res) == 13

    b.organism = 'Homo sapiens'
    b.all_pathways
