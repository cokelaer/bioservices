from bioservices import UniChem
from nose.plugins.attrib import attr


@attr('skip_travis')
class test_UniChem(UniChem):
    def __init__(self):
        super(test_UniChem, self).__init__(verbose=False, cache=False)

    def test_get_compound_ids_from_src_id(self):
        res1 = self.get_compound_ids_from_src_id("CHEMBL2", "chembl", "chebi")
        res2 = self.get_compound_ids_from_src_id(["CHEMBL2"], "chembl", "chebi")
        assert res1 == res2[0]
        assert res1 == [{u'src_compound_id': u'8364'}]
        assert res2[0] == [{u'src_compound_id': u'8364'}]

    def test_get_all_src_ids(self):
        assert len(self.get_all_src_ids())>=23

    def test_get_source_id(self):
        assert self._get_source_id("chembl") == 1
        assert self._get_source_id("1") == 1
        assert self._get_source_id(1) == 1

        try:
            self._get_source_id("wrong")
            assert False
        except:
            assert True

        try:
            self._get_source_id("20000")
            assert False
        except:
            assert True

    def test_get_src_information(self):
        assert self.get_source_information("chebi")['name'] == "chebi"

        assert self.get_source_information(['chembl', 'drugbank'])[0]['name']=="chembl"

    def test_get_all_compound_ids_from_src_id(self):
        res = self.get_all_compound_ids_from_all_src_id("CHEMBL12", "chembl")
        res = self.get_all_compound_ids_from_all_src_id("CHEMBL12", "chembl", "chebi")


    def test_mapping(self):
        res = self.get_mapping("kegg_ligand", "chembl")
        assert len(res)>0

    def test_get_src_compound_ids_from_inchikey(self):
        self.get_src_compound_ids_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
        self.get_src_compound_ids_from_inchikey(["AAOVKJBEBIDNHE-UHFFFAOYSA-N"])
        #self.get_src_compound_ids_all_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
        #self.get_src_compound_ids_all_from_inchikey(["AAOVKJBEBIDNHE-UHFFFAOYSA-N"])

    def test_structure(self):
        self.get_structure("CHEMBL12", "chembl")
        self.get_structure(["CHEMBL12"], "chembl")
        self.get_structure_all("CHEMBL12", "chembl")


    def test_get_src_compound_id_url(self):
        self.get_src_compound_id_url("CHEMBL12", "chembl", "drugbank")
        self.get_src_compound_id_url(["CHEMBL12"], "chembl", "drugbank")


    def test_get_src_compound_ids_all_from_obsolete(self):
        self.get_src_compound_ids_all_from_obsolete("DB07699", "2")[0]
        self.get_src_compound_ids_all_from_obsolete("DB07699", "2", "2")[0]

    def test_get_verbose_src_compound_ids_from_inchikey(self):
        assert self.get_verbose_src_compound_ids_from_inchikey("GZUITABIAKMVPG-UHFFFAOYSA-N") != 400
        assert self.get_verbose_src_compound_ids_from_inchikey("QFFGVLORLPOAEC-SNVBAGLBSA-N") != 400 

    @attr('slow')
    def test_get_auxiliary_mapping(self):
        self.settings.TIMEOUT = 100
        res = self.get_auxiliary_mappings(1)
        assert len(res)>0

