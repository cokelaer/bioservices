from bioservices import Reactome, ReactomeOld
import pytest
from easydev import TempFile
import os
skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
     reason="On travis")


@pytest.fixture
def reactome():
    return Reactome(verbose=True)


def test_discover(reactome):
    res = reactome.get_discover("R-HSA-446203")
    assert "name" in res


def test_diseases(reactome):
    res = reactome.get_diseases()
    assert len(res)


def test_diseases_doid(reactome):
    res = reactome.get_diseases_doid()
    assert len(res)


@skiptravis
def test_exporter_diagram(reactome):
    res = reactome.get_exporter_diagram("R-HSA-5674003", ext="png")
    res = reactome.get_exporter_diagram("R-HSA-5674003", ext="jpg")
    res = reactome.get_exporter_diagram("R-HSA-5674003", ext="jpg", quality=1)
    res = reactome.get_exporter_diagram("R-HSA-5674003", ext="jpg", quality=1,
                                    diagramProfile="Standard")

    with TempFile(suffix=".png") as fout:
        res = reactome.get_exporter_diagram(109581, ext="png", filename=fout.name)


def test_complex_subunits(reactome):
    assert len(reactome.get_complex_subunits("R-HSA-5674003"))


def test_complexes(reactome):
    assert len(reactome.get_complexes("UniProt", "P43403"))
    assert reactome.get_complexes("UniProt", "P434") == 404


def test_entity_componentOf(reactome):
    assert len(reactome.get_entity_componentOf("R-HSA-199420"))


def test_entity_otherForms(reactome):
    assert len(reactome.get_entity_otherForms("R-HSA-199420"))


def test_event_ancestors(reactome):
    assert len(reactome.get_event_ancestors("R-HSA-5673001"))


def test_events_hierarchy(reactome):
    assert len(reactome.get_eventsHierarchy(9606))


def test_exporter_sbml(reactome):
    assert len(reactome.get_exporter_sbml("R-HSA-68616"))


def test_pathway_containedEvents(reactome):
    res = reactome.get_pathway_containedEvents("R-HSA-5673001")
    assert len(res)


def test_pathway_containedEvents_by_attribute(reactome):
    res = reactome.get_pathway_containedEvents_by_attribute("R-HSA-5673001", "stId")
    assert len(res)


def test_pathways_low_diagram_entity(reactome):
    res = reactome.get_pathways_low_diagram_entity("R-HSA-199420")
    assert len(res)


def test_pathways_low_diagram_entity_allForms(reactome):
    res = reactome.get_pathways_low_diagram_entity_allForms("R-HSA-199420")
    assert len(res)


def test_pathways_low_entity(reactome):
    res = reactome.get_pathways_low_entity("R-HSA-199420")
    assert len(res)


def test_pathways_low_entity_allForms(reactome):
    res = reactome.get_pathways_low_entity_allForms("R-HSA-199420")
    assert len(res)


def test_pathways_top(reactome):
    res = reactome.get_pathways_top(9606)
    assert len(res)


def test_references(reactome):
    res = reactome.get_references(15377)
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


def test_species_all(reactome):
    res = reactome.get_species_all()
    assert len(res)


def test_species_main(reactome):
    res = reactome.get_species_main()
    assert len(res)



# obsolet
def __test_species():
    r = ReactomeOld(verbose=True)
    assert len(r.get_species()) > 10
    res = r.query_by_ids("Pathway", 'TP53')
    assert len(res) >= 1

