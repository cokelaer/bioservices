from bioservices.chembl import ChEMBL
from nose.plugins.attrib import attr

class test_Chembl(ChEMBL):

    def __init__(self):
        super(test_Chembl, self).__init__(verbose=False, 
                cache=False)
        self.default_extension = "xml"
        try:
            self.default_extension = "xmlf"
            assert False
        except:
            assert True

    def test_status(self):
        self.status()

    # COMPOUNDS RELATED ---------------------------------------------------------------

    def test_get_compounds_by_chemblId_form(self):
        res = self.get_compounds_by_chemblId_form("CHEMBL3")
        res[0]['parent']
        res = self.get_compounds_by_chemblId_form(["CHEMBL3"])
        assert len(res)

    def test_get_compounds_by_chemblId_drug_mechanism(self):
        res = self.get_compounds_by_chemblId_drug_mechanism("CHEMBL3")

    def test_get_individual_compounds_by_inChiKey(self):
        res = self.get_individual_compounds_by_inChiKey(self._inChiKey_example)
        assert res['molecularFormula'] == 'C19H21ClFN3O3'

    def test_get_compounds_by_chemblId(self):
        assert self.get_compounds_by_chemblId("CHEMBL1")
        # FIXME
        #assert self.get_compounds_by_chemblId("WRONG") in self._error_codes
        self.get_compounds_by_chemblId(self._chemblId_example)
        assert len(self.get_compounds_by_chemblId(["CHEMBL1", "CHEMBL2"]))==2

    def test_get_compounds_activities(self):
        self.get_compounds_activities("CHEMBL1")

    def test_get_compounds_by_SMILES(self):
        res = self.get_compounds_by_SMILES(self._smiles_example)

    def test_get_compounds_containing_SMILES(self):
        #res = self.get_compounds_containing_SMILES(self._smiles_struct_example)
        res = self.get_compounds_substructure(self._smiles_struct_example)

    def test_get_compounds_similar_to_SMILES(self):
        # at the time of the test, the length was 9
        res = self.get_compounds_similar_to_SMILES(self._smiles_example, similarity=90)
        assert len(res)>=9

    # TARGETS -----------------------------------------------------------------

    def test_get_target_uniprotId(self):
        res = self.get_target_by_uniprotId(self._target_uniprotId_example)
        assert res['proteinAccession'] == self._target_uniprotId_example

    def test_get_target_bioactivities(self):
        res = self.get_target_bioactivities(self._target_bioactivities_example)
        assert len(res)>1000

    def test_get_target_by_chemblId(self):
        resjson = self.get_target_by_chemblId(self._target_chemblId_example)

    def test_get_all_targets(self):
        assert len(self.get_all_targets())>1000

    def test_get_target_by_refseq(self):
        self.get_target_by_refseq(self._target_refseq_example)

    # ASSAYS ----------------------------------------------------------

    def test_get_assays_bioactivities(self):
        res = self.get_assays_bioactivities(self._assays_example)

    def test_get_assays(self):
        self.get_assays_bioactivities("CHEMBL1217643")
        self.get_assays_by_chemblId("CHEMBL1217643")

    @attr('skip')
    def test_inspect(self): 
        self.inspect(self._assays_example,'assay')

    def test_image(self):
        res = self.get_image_of_compounds_by_chemblId(
            self._image_chemblId_example
            , view=False)
        import os
        os.remove(self._image_chemblId_example + ".png")

    def test_version(self):
        self.version()

    def _test(self):

        """


    def get_target_by_refseq(self, query):

def get_assays_by_chemblId(self, query, frmt="json"):
    def get_assays_bioactivities(self, query, frmt="json"):
    def inspect(self, query, item_type):

    """
