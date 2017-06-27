from bioservices import Reactome
import pytest


@pytest.fixture
def reactome():
    return Reactome(verbose=True)

def test_species(reactome):
    assert len( reactome.get_species()) > 10

def test_biopax_exporter(reactome):
    res = reactome.biopax_exporter(109581)

def test_front_page_items(reactome):
    res = reactome.front_page_items("homo sapiens")

def test_highlight_pathway_diagram(reactome):
    res = reactome.highlight_pathway_diagram(68875, frmt="PNG", genes="CDC2")

def test_list_by_query(reactome):
    assert len(reactome.list_by_query("Pathway", name="Apoptosis"))>1

def test_pathway_diagram(reactome):
    res = reactome.pathway_diagram(109581, 'XML')
    res = reactome.pathway_diagram(109581, 'PNG')
    res = reactome.pathway_diagram(109581, 'PDF')
    try:
        res = reactome.pathway_diagram(109581, 'XDF')
        assert False
    except:
        assert True

def test_pathway_hierarchy(reactome):
    res = reactome.pathway_hierarchy('homo sapiens')
    assert len(res)>10

def test_pathway_participants(reactome):
    res = reactome.pathway_participants(109581)
    assert len(res)>0

def test_pathway_complexes(reactome):
    res = reactome.pathway_complexes(109581)
    assert len(res)>1
    assert "dbId" in list(res[0].keys())

def test_query_by_id(reactome):
    res = reactome.query_by_id("Pathway", 109581)
    assert len(res)>1

def test_query_by_ids(reactome):
    res = reactome.query_by_ids("Pathway", 'TP53')
    assert len(res)>=1

def test_query_hit_pathways(reactome):
    assert len(reactome.query_hit_pathways("TP53"))>1

def test_pathway_for_entities(reactome):
    res = reactome.query_pathway_for_entities("TP53")

def test_species_list(reactome):
    res = reactome.species_list()

def test_sbml_exporter(reactome):
    res = reactome.SBML_exporter(109581)



