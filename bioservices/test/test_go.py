from bioservices.go import *



class test_quickGO(QuickGO):

    def __init__(self):
        super(test_quickGO, self).__init__()

    def test_annotation_ref_PMID(self):
        res = self.Annotation(tax='9606', format='tsv', col="ref",ref="PMID:*")

    def test_annotation_qualifier(self):
        res = self.Annotation(tax='9606', format='tsv', 
            col="ref,evidence,proteinID,goID,proteinTaxon,qualifier",ref="PMID:*", 
            qualifier="NOT")

    def test_annotation_qualifier(self):
        res = set([ x for x in g.Annotation(tax='9606', format='tsv', col="qualifier",ref="PMID:*").split()])

        assert 'NOT' in res

