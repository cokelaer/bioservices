from bioservices.quickgo_old import QuickGO_old
import pytest

on_success = pytest.mark.skipif(isinstance(QuickGO_old().Term('GO:0003824', frmt="obo"), int) is True,
                                reason="Got instance of int from QuickGO_old")


@pytest.fixture
def quickgo():
    return QuickGO_old(verbose=False, cache=False)


@on_success
def test_annotation_wrong_format(quickgo):
    try:
        res = quickgo.Annotation(tax='9606', frmt='tsddddddv')
        assert False
    except:
        assert True


@on_success
def test_annotation_format_col_compatibility(quickgo):
    # if col provided, format can be only tsv
    try:
        res = quickgo.Annotation(tax='9606', frmt='fasta', col="evidence")
        assert False
    except:
        assert True


@on_success
def test_annotation_no_protein_and_goid(quickgo):
    try:
        quickgo.Annotation(frmt='tsv', col="ref,evidence", ref='PMID:*')
        assert False
    except ValueError:
        assert True


@on_success
def test_annotation_evidence(quickgo):
    quickgo.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", evidence="IDA")
    quickgo.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", evidence=["IDA"])
    try:
        quickgo.Annotation(protein='P12345', frmt='tsv',
                           col="ref,evidence", evidence=1)
        assert False
    except:
        assert True


@on_success
def test_annotation_aspect(quickgo):
    quickgo.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", aspect='F')
    quickgo.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", aspect='C')
    quickgo.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", aspect='P')
    try:
        quickgo.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", aspect='dummy')
        assert False
    except:
        assert True


@on_success
def test_annotation_source(quickgo):
    quickgo.Annotation(protein='P12345', frmt='tsv',
                       col="ref,evidence", ref='PMID:*', source="UniProtKB")
    quickgo.Annotation(protein='P12345', frmt='tsv',
                       col="ref,evidence", ref='PMID:*', source=["UniProtKB"])
    try:
        quickgo.Annotation(protein='P12345', frmt='tsv',
                           col="ref,evidence", ref='PMID:*', source=111)
        assert False
    except:
        assert True


@on_success
def test_annotation_protein(quickgo):
    print(quickgo.Annotation(protein='P12345', frmt='tsv',
                             col="ref,evidence", ref='PMID:*'))


@on_success
def test_annotation_goid(quickgo):
    print(quickgo.Annotation(goid='GO:0003824', frmt='tsv',
                             col="ref,evidence"))


@on_success
def test_annotation_ref_PMID(quickgo):
    res = quickgo.Annotation(tax='9606', frmt='tsv', col="ref", ref="PMID:*")


@on_success
def test_annotation_qualifier(quickgo):
    res = quickgo.Annotation(tax='9606', frmt='tsv',
                             col="ref,evidence,proteinID,goID,proteinTaxon,qualifier", ref="PMID:*",
                             qualifier="NOT")
    res = quickgo.Annotation(tax='9606', frmt='tsv',
                             col="ref,evidence,proteinID,goID,proteinTaxon,qualifier", ref="PMID:*",
                             qualifier=["NOT"])
    try:
        res = quickgo.Annotation(tax='9606', frmt='tsv',
                                 col="ref,evidence,proteinID,goID,proteinTaxon,qualifier", ref="PMID:*",
                                 qualifier=1)
        assert False
    except:
        assert True


@on_success
def test_annotation_qualifier2(quickgo):
    res = set([x for x in quickgo.Annotation(tax='9606', frmt='tsv', col="qualifier", ref="PMID:*").split()])
    assert 'NOT' in res


@on_success
def test_annotation_termUse(quickgo):
    try:
        res = quickgo.Annotation(tax='9606', frmt='tsv',
                                 col="qualifier", ref="PMID:*", termUse="slimdummy")
        assert False
    except:
        assert True


@on_success
def test_Term(quickgo):
    quickgo.Term("GO:0003824", frmt="obo")
    quickgo.Term("GO:0003824", frmt="mini")
    quickgo.Term("GO:0003824")
    try:
        quickgo.Term("GO:0003824", frmt="dummy")
        assert False
    except:
        assert True

    try:
        quickgo.Term("G:0003824")
        assert False
    except:
        assert True


@on_success
def test_annotations_from_goid(quickgo):
    quickgo.Annotation_from_goid("GO:0003824")


@on_success
def test_annotations_from_protein(quickgo):
    quickgo.Annotation_from_protein("P43403")
