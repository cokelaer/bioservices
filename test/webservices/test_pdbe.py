import pytest
from bioservices import PDBe


@pytest.fixture(scope="module")
def pdbe():
    return PDBe(verbose=False)


class TestGetSummary:
    def test_single(self, pdbe):
        res = pdbe.get_summary("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_comma_separated(self, pdbe):
        res = pdbe.get_summary("1cbs,2kv8")
        assert isinstance(res, dict)
        assert len(res) >= 2

    def test_list(self, pdbe):
        res = pdbe.get_summary(["1cbs", "2kv8"])
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetMolecules:
    def test_single(self, pdbe):
        res = pdbe.get_molecules("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_molecules("1cbs,2kv8")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetEntities:
    def test_single(self, pdbe):
        res = pdbe.get_entities("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_entities("1cbs,2kv8")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetPublications:
    def test_single(self, pdbe):
        res = pdbe.get_publications("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_publications("1cbs,2kv8")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetRelatedPublications:
    def test_single(self, pdbe):
        res = pdbe.get_related_publications("1cbs")
        assert isinstance(res, dict)

    def test_multi(self, pdbe):
        res = pdbe.get_related_publications("1cbs,2kv8")
        assert isinstance(res, dict)


class TestGetExperiment:
    def test_single(self, pdbe):
        res = pdbe.get_experiment("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_experiment("1cbs,2kv8")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetLigandMonomers:
    def test_single(self, pdbe):
        res = pdbe.get_ligand_monomers("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_ligand_monomers("1cbs,2kv8")
        assert isinstance(res, dict)


class TestGetModifiedResidues:
    def test_single(self, pdbe):
        res = pdbe.get_modified_residues("4v5j")
        assert isinstance(res, dict)
        assert "4v5j" in res

    def test_multi(self, pdbe):
        res = pdbe.get_modified_residues("4v5j,1cbs")
        assert isinstance(res, dict)


class TestGetMutatedResidues:
    def test_single(self, pdbe):
        res = pdbe.get_mutated_residues("1bgj")
        assert isinstance(res, dict)
        assert "1bgj" in res

    def test_multi(self, pdbe):
        res = pdbe.get_mutated_residues("1bgj,4v5j")
        assert isinstance(res, dict)


class TestGetReleaseStatus:
    def test_single(self, pdbe):
        res = pdbe.get_release_status("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_release_status("1cbs,4v5j")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetObservedRanges:
    def test_single(self, pdbe):
        res = pdbe.get_observed_ranges("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_observed_ranges("1cbs,4v5j")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetObservedRangesInPdbChain:
    def test_single(self, pdbe):
        res = pdbe.get_observed_ranges_in_pdb_chain("1cbs", "A")
        assert isinstance(res, dict)
        assert "1cbs" in res


class TestGetSecondaryStructure:
    def test_single(self, pdbe):
        res = pdbe.get_secondary_structure("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_secondary_structure("1cbs,4v5j")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetResidueListing:
    def test_single(self, pdbe):
        res = pdbe.get_residue_listing("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res


class TestGetResidueListingInPdbChain:
    def test_single(self, pdbe):
        res = pdbe.get_residue_listing_in_pdb_chain("1cbs", "A")
        assert isinstance(res, dict)
        assert "1cbs" in res


class TestGetBindingSites:
    def test_single(self, pdbe):
        res = pdbe.get_binding_sites("1cbs", 1)
        assert isinstance(res, dict)
        assert "1cbs" in res


class TestGetFiles:
    def test_single(self, pdbe):
        res = pdbe.get_files("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_files("1cbs,4v5j")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetObservedResiduesRatio:
    def test_single(self, pdbe):
        res = pdbe.get_observed_residues_ratio("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_observed_residues_ratio("1cbs,4v5j")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetAssembly:
    def test_single(self, pdbe):
        res = pdbe.get_assembly("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_assembly("1cbs,4v5j")
        assert isinstance(res, dict)
        assert len(res) >= 2


class TestGetElectronDensityStatistics:
    def test_single(self, pdbe):
        res = pdbe.get_electron_density_statistics("1cbs")
        assert isinstance(res, dict)
        assert "1cbs" in res

    def test_multi(self, pdbe):
        res = pdbe.get_electron_density_statistics("1cbs,4v5j")
        assert isinstance(res, dict)


class TestGetFunctionalAnnotation:
    def test_single(self, pdbe):
        res = pdbe.get_functional_annotation("1cbs")
        assert isinstance(res, dict)


class TestGetDrugbankAnnotation:
    def test_single(self, pdbe):
        res = pdbe.get_drugbank_annotation("5hht")
        assert isinstance(res, dict)


class TestGetRelatedDataset:
    def test_single(self, pdbe):
        res = pdbe.get_related_dataset("5o8b")
        assert isinstance(res, dict)

    def test_multi(self, pdbe):
        res = pdbe.get_related_dataset("5o8b,5o8b")
        assert isinstance(res, dict)


class TestGetBranchedEntities:
    def test_single(self, pdbe):
        res = pdbe.get_branched_entities("3d12")
        assert isinstance(res, dict)

    def test_multi(self, pdbe):
        res = pdbe.get_branched_entities("3d12,7v7u")
        assert isinstance(res, dict)


class TestGetCarbohydratePolymer:
    def test_single(self, pdbe):
        res = pdbe.get_carbohydrate_polymer("3d12")
        assert isinstance(res, dict)

    def test_multi(self, pdbe):
        res = pdbe.get_carbohydrate_polymer("3d12,7v7u")
        assert isinstance(res, dict)


class TestInvalidInput:
    def test_id_too_long(self, pdbe):
        with pytest.raises(AssertionError):
            pdbe.get_summary("sdklfjslkdfj")

    def test_id_too_short(self, pdbe):
        with pytest.raises(AssertionError):
            pdbe.get_summary("1c")

    def test_wrong_type(self, pdbe):
        with pytest.raises(TypeError):
            pdbe.get_summary(12345)

    def test_invalid_id_in_list(self, pdbe):
        with pytest.raises(AssertionError):
            pdbe.get_summary(["1cbs", "bad"])

    def test_invalid_id_in_comma_separated(self, pdbe):
        with pytest.raises(AssertionError):
            pdbe.get_summary("1cbs,bad")
