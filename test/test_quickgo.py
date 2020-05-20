from bioservices.quickgo import QuickGO
import pytest

@pytest.fixture
def quickgo():
    return QuickGO(verbose=False, cache=False)

def test_annotation_taxonid(quickgo):
    res = quickgo.Annotation(taxonId='9606')

def test_annotation_aspect(quickgo):
    res = quickgo.Annotation(taxonId="9606", limit=100, aspect="F")

def test_annotation_geneProductType(quickgo):
    res = quickgo.Annotation(taxonId="9606", limit=100, geneProductType="protein")

def test_annotations_from_goid(quickgo):
    df = quickgo.Annotation_from_goid(goId="GO:0003824,GO:0003677", taxonId="9606" )
    assert len(df)

def test_Term(quickgo):
    res = quickgo.goterms("GO:0003824,GO:0003677")
    assert len(res) == 2
