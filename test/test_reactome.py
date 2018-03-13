from bioservices import Reactome
import pytest
from easydev import TempFile


@pytest.fixture
def reactome():
    return Reactome(verbose=True)

def test_data_discover(reactome):
    res = reactome.data_discover("R-HSA-446203")
    assert "name" in res

def test_data_diseases(reactome):
    res = reactome.data_diseases()
    assert len(res)

def test_data_diseases_doid(reactome):
    res = reactome.data_diseases_doid()
    assert len(res)

def test_exporter_diagram(reactome):
    res = reactome.exporter_diagram(109581, ext="png")
    res = reactome.exporter_diagram(109581, ext="jpg")
    res = reactome.exporter_diagram(109581, ext="jpg", quality=1)
    res = reactome.exporter_diagram(109581, ext="jpg", quality=1,
            diagramProfile="Standard")

    with TempFile(suffix=".png") as fout:
        res = reactome.exporter_diagram(109581, ext="png", filename=fout.name)

def test_data_complex_subunits(reactome):
    assert len(reactome.data_complex_subunits("R-HSA-5674003"))


def test_data_complexes(reactome):

    assert len(reactome.data_complexes("UniProt", "P43403"))
    assert reactome.data_complexes("UniProt", "P434") == 404


def test_data_entity_componentOf(reactome):
    assert len(reactome.data_entity_componentOf("R-HSA-199420"))


def test_data_entity_otherForms(reactome):
    assert len(reactome.data_entity_otherForms("R-HSA-199420"))


def test_data_event_ancestors(reactome):
    assert len(reactome.data_event_ancestors("R-HSA-5673001"))

def test_data_events_hierarchy(reactome):
    assert len(reactome.data_eventsHierarchy(9606))


def test_exporter_sbml(reactome):
    assert len(reactome.exporter_sbml("R-HSA-68616"))


def test_data_pathway_containedEvents(reactome):
    res =  reactome.data_pathway_containedEvents("R-HSA-5673001")
    assert len(res)


def test_data_pathway_containedEvents_by_attribute(reactome):
    res = reactome.data_pathway_containedEvents_by_attribute("R-HSA-5673001", "stId")
    assert len(res)


def test_data_pathways_low_diagram_entity(reactome):
    res =  reactome.data_pathways_low_diagram_entity("R-HSA-199420")
    assert len(res)


def test_data_pathways_low_diagram_entity_allForms(reactome):
    res =  reactome.data_pathways_low_diagram_entity_allForms("R-HSA-199420")
    assert len(res)


def test_data_pathways_low_diagram_identifier_allForms(reactome):
    res =  reactome.data_pathways_low_diagram_identifier_allForms("PTEN")
    assert len(res)


def test_data_pathways_low_entity(reactome):
    res =  reactome.data_pathways_low_entity("R-HSA-199420")
    assert len(res)


def test_data_pathways_low_entity_allForms(reactome):
    res =  reactome.data_pathways_low_entity_allForms("R-HSA-199420")
    assert len(res)


def test_data_pathways_top(reactome):
    res =  reactome.data_pathways_top(9606)
    assert len(res)


def test_references(reactome):
    res = reactome.references(15377)
    assert len(res)


def test_search_facet(reactome):
    res = reactome.search_facet()
    assert len(res)


def test_search_facet_query(reactome):
    res = reactome.search_facet_query("R-HSA-199420")
    assert len(res)


def test_search_query(reactome):
    res = reactome.search_query("R-HSA-199420")
    assert len(res)


def test_search_spellcheck(reactome):
    res = reactome.search_spellcheck("appostosis")
    assert len(res)


def test_search_suggest(reactome):
    res = reactome.search_spellcheck("apost")
    assert len(res)


def test_data_species_all(reactome):
    res = reactome.data_species_all()
    assert len(res)

def test_data_species_main(reactome):
    res = reactome.data_species_main()
    assert len(res)


"""

@pytest.fixture
def reactome():
    return ReactomeOld(verbose=True)


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


"""
