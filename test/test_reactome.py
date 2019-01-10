from bioservices import Reactome, ReactomeOld
import pytest
from easydev import TempFile
import os
skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
     reason="On travis")


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


@skiptravis
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
    res = reactome.data_pathway_containedEvents("R-HSA-5673001")
    assert len(res)


def test_data_pathway_containedEvents_by_attribute(reactome):
    res = reactome.data_pathway_containedEvents_by_attribute("R-HSA-5673001", "stId")
    assert len(res)


def test_data_pathways_low_diagram_entity(reactome):
    res = reactome.data_pathways_low_diagram_entity("R-HSA-199420")
    assert len(res)


def test_data_pathways_low_diagram_entity_allForms(reactome):
    res = reactome.data_pathways_low_diagram_entity_allForms("R-HSA-199420")
    assert len(res)


def test_data_pathways_low_diagram_identifier_allForms(reactome):
    res = reactome.data_pathways_low_diagram_identifier_allForms("PTEN")
    assert len(res)


def test_data_pathways_low_entity(reactome):
    res = reactome.data_pathways_low_entity("R-HSA-199420")
    assert len(res)


def test_data_pathways_low_entity_allForms(reactome):
    res = reactome.data_pathways_low_entity_allForms("R-HSA-199420")
    assert len(res)


def test_data_pathways_top(reactome):
    res = reactome.data_pathways_top(9606)
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


@pytest.fixture
def reactomeold():
    return ReactomeOld(verbose=True)


def test_species(reactomeold):
    assert len(reactomeold.get_species()) > 10


def test_query_by_ids(reactomeold):
    res = reactomeold.query_by_ids("Pathway", 'TP53')
    assert len(res) >= 1

