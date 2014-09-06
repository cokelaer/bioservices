from bioservices.quickgo import QuickGO
from nose.plugins.attrib import attr

class test_quickGO(QuickGO):

    def __init__(self):
        super(test_quickGO, self).__init__(verbose=False, 
                cache=False)

    def test_annotation_wrong_format(self):
        try:
            res = self.Annotation(tax='9606', frmt='tsddddddv')
            assert False
        except:
            assert True

    def test_annotation_format_col_compatibility(self):
        # if col provided, format can be only tsv
        try:
            res = self.Annotation(tax='9606', frmt='fasta', col="evidence")
            assert False
        except:
            assert True

    @attr('slow')
    def test_annotation_wrong_limit(self):
        try:
            res = self.Annotation(tax='9606', frmt='tsv', limit=-1)
            assert False
        except:
            assert True

        try:
            res = self.Annotation(tax='9606', frmt='tsv', limit="dummy")
            assert False
        except TypeError:
            assert True
        except:
            assert False

    def test_annotation_no_protein_and_goid(self):
        try:
            self.Annotation(frmt='tsv', col="ref,evidence",ref='PMID:*')
            assert False
        except ValueError:
            assert True

    def test_annotation_evidence(self):
        self.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", evidence="IDA")
        self.Annotation(protein='P12345', frmt='tsv', col="ref,evidence", evidence=["IDA"])
        try:
            self.Annotation(protein='P12345', frmt='tsv',
                col="ref,evidence",evidence=1)
            assert False
        except:assert True

    def test_annotation_aspect(self):
        self.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",aspect='F')
        self.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",aspect='C')
        self.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",aspect='P')
        try:
            self.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",aspect='dummy')
            assert False
        except:
            assert True


    def test_annotation_source(self):
        self.Annotation(protein='P12345', frmt='tsv',
            col="ref,evidence",ref='PMID:*', source="UniProtKB")
        self.Annotation(protein='P12345', frmt='tsv',
            col="ref,evidence",ref='PMID:*', source=["UniProtKB"])
        try:
            self.Annotation(protein='P12345', frmt='tsv',
                col="ref,evidence",ref='PMID:*', source=111)
            assert False    
        except:
            assert True

    def test_annotation_protein(self):
        print(self.Annotation(protein='P12345', frmt='tsv',
            col="ref,evidence",ref='PMID:*'))

    def test_annotation_goid(self):
        print(self.Annotation(goid='GO:0003824', frmt='tsv',
                col="ref,evidence"))

    def test_annotation_ref_PMID(self):
        res = self.Annotation(tax='9606', frmt='tsv', col="ref",ref="PMID:*")

    def test_annotation_qualifier(self):
        res = self.Annotation(tax='9606', frmt='tsv', 
            col="ref,evidence,proteinID,goID,proteinTaxon,qualifier",ref="PMID:*", 
            qualifier="NOT")
        res = self.Annotation(tax='9606', frmt='tsv', 
            col="ref,evidence,proteinID,goID,proteinTaxon,qualifier",ref="PMID:*", 
            qualifier=["NOT"])
        try:
            res = self.Annotation(tax='9606', frmt='tsv', 
                col="ref,evidence,proteinID,goID,proteinTaxon,qualifier",ref="PMID:*", 
                qualifier=1)
            assert False
        except:assert True

    def test_annotation_qualifier2(self):
        res = set([ x for x in self.Annotation(tax='9606', frmt='tsv', col="qualifier",ref="PMID:*").split()])
        assert 'NOT' in res

    def test_annotation_termUse(self):
        try:
            res = self.Annotation(tax='9606', frmt='tsv',
                col="qualifier",ref="PMID:*", termUse="slimdummy")
            assert False
        except:
            assert True

    def test_Term(self):
        self.Term("GO:0003824", frmt="obo")
        self.Term("GO:0003824", frmt="mini")
        self.Term("GO:0003824")
        try:
            self.Term("GO:0003824", frmt="dummy")
            assert False
        except:
            assert True

        try:
            self.Term("G:0003824")
            assert False
        except:
            assert True


    def test_annotations_from_goid(self):
        self.Annotation_from_goid("GO:0003824")

    def test_annotations_from_protein(self):
        self.Annotation_from_protein("P43403")
