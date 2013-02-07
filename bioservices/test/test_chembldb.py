from bioservices.chembldb import *
import unittest


class test_Chembl(ChEMBLdb):

    def __init__(self):
        super(test_Chembl, self).__init__(verbose=False)
        self.default_extension = "xml"
        try:
            self.default_extension = "xmlf"
            assert False
        except:
            assert True

    def test_api_status(self):
        self.api_status()

    def test_get_compounds_by_chemblId(self):
        self.get_compounds_by_chemblId("CHEMBL1")
        self.get_compounds_by_chemblId("CHEMBL1.json")
        self.get_compounds_by_chemblId(self._chemblId_example)

    def test_get_target_uniprotId(self):
        self.get_target_by_uniprotId("Q13936")

    def _test_get_compounds_activities(self):
        self.get_compounds_activities("CHEMBL1")

    def test_get_compounds_by_SMILES(self):
        self.get_compounds_by_SMILES(self._smiles_example + ".json")


    def test_get_compounds_containing_SMILES(self):
        self.get_compounds_containing_SMILES(self._smiles_example + ".json")

    def test_get_compounds_similar_to_SMILES(self):
        res = self.get_compounds_similar_to_SMILES(self._smiles_example + "/70.json")
        assert len(res['compounds'])>=1

    def test_get_target_by_chemblId(self):
        self.get_target_by_chemblId("CHEMBL2477")

    def test_get_compounds_activities(self):
        self.get_compounds_activities("CHEMBL2")
        self.get_compounds_activities("CHEMBL2.json")

    def test_get_target_bioactivities(self):
        self.get_target_bioactivities("CHEMBL240.json")

    def test_get_target_by_chemblId(self):
        resjson = self.get_target_by_chemblId(self._target_chemblId_example)

    def test_get_assay_bioactivities(self):
        res = self.get_assay_bioactivities(self._assay_example)

    def test_get_all_targets(self):
        self.get_all_targets()

    def test_get_assays(self):
        self.get_assay_bioactivities("CHEMBL1217643")
        self.get_assay_by_chemblId("CHEMBL1217643")

    @unittest.skip
    def test_inspect(self): 
        self.inspect("CHEMBL240")

    def test_image(self):
        self.get_image_of_compounds_by_chemblId(
            self._image_chemblId_example,
            self._image_dimension_example, view=False)

