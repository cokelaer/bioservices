from bioservices.quickgo import QuickGO
import pytest

@pytest.fixture
def quickgo():
    return QuickGO(verbose=False, cache=False)

def test_annotation(quickgo):
    res = quickgo.Annotation(taxonId='9606')
    res = quickgo.Annotation(taxonId="9606", limit=100, aspect="F")
    res = quickgo.Annotation(taxonId="9606", limit=100, geneProductType="protein")
    res = quickgo.Annotation(taxonId="9606", limit=100, geneProductType="protein", assignedBy="UniProt")
    res = quickgo.Annotation(taxonId="9606", evidenceCode="ECO:0000501")






def test_annotations_from_goid(quickgo):
    df = quickgo.Annotation_from_goid(goId="GO:0003824,GO:0003677", taxonId="9606" )
    assert len(df)

def test_Term(quickgo):
    res = quickgo.get_go_terms("GO:0003824,GO:0003677")
    assert len(res) == 2

def test_gosearch(quickgo):
    res = quickgo.go_search("GO:0022804")
    assert len(res)

def test_go_ancestors(quickgo):
    res = quickgo.get_go_ancestors("GO:0022804")
    assert len(res)

def test_go_children(quickgo):
    res = quickgo.get_go_children("GO:0022804")
    assert len(res)

def test_go_chart(quickgo):
    res = quickgo.get_go_chart("GO:0022804")

def test_go_paths(quickgo):
    res = quickgo.get_go_paths("GO:0022804", "GO:0005215")
    assert len(res)

