import pytest
from bioservices import InterPro


@pytest.fixture
def interpro():
    return InterPro(verbose=False)


def test_get_entry(interpro):
    entry = interpro.get_entry("IPR000001")
    assert entry is not None
    assert "metadata" in entry
    assert entry["metadata"]["accession"] == "IPR000001"


def test_get_entries(interpro):
    results = interpro.get_entries(page_size=5)
    assert results is not None
    assert "results" in results
    assert len(results["results"]) > 0


def test_get_member_database_entry(interpro):
    entry = interpro.get_member_database_entry("pfam", "PF00001")
    assert entry is not None
    assert "metadata" in entry


def test_get_member_database_entry_invalid(interpro):
    with pytest.raises(ValueError):
        interpro.get_member_database_entry("invalid_db", "PF00001")


def test_get_entries_by_member_database(interpro):
    results = interpro.get_entries_by_member_database("pfam", page_size=5)
    assert results is not None
    assert "results" in results


def test_get_entries_by_member_database_invalid(interpro):
    with pytest.raises(ValueError):
        interpro.get_entries_by_member_database("invalid_db")


def test_search_entries(interpro):
    results = interpro.search_entries("kinase", page_size=5)
    assert results is not None
    assert "results" in results
    assert len(results["results"]) > 0


def test_get_entries_by_type(interpro):
    results = interpro.get_entries_by_type("domain", page_size=5)
    assert results is not None
    assert "results" in results


def test_get_entries_by_type_invalid(interpro):
    with pytest.raises(ValueError):
        interpro.get_entries_by_type("invalid_type")


def test_get_protein(interpro):
    protein = interpro.get_protein("P00734")
    assert protein is not None
    assert "metadata" in protein


def test_get_protein_entries(interpro):
    entries = interpro.get_protein_entries("P00734")
    assert entries is not None
    assert "results" in entries


def test_get_proteins_by_entry(interpro):
    proteins = interpro.get_proteins_by_entry("IPR000001", page_size=5)
    assert proteins is not None
    assert "results" in proteins


def test_get_structure(interpro):
    structure = interpro.get_structure("1t2v")
    assert structure is not None
    assert "metadata" in structure


def test_get_entry_structures(interpro):
    structures = interpro.get_entry_structures("IPR000001", page_size=5)
    assert structures is not None
    assert "results" in structures


def test_get_taxonomy(interpro):
    taxon = interpro.get_taxonomy("9606")
    assert taxon is not None
    assert "metadata" in taxon


def test_get_entry_taxonomy(interpro):
    taxons = interpro.get_entry_taxonomy("IPR000001", page_size=5)
    assert taxons is not None
    assert "results" in taxons


def test_get_proteome(interpro):
    proteome = interpro.get_proteome("UP000005640")
    assert proteome is not None
    assert "metadata" in proteome


def test_get_entry_proteomes(interpro):
    proteomes = interpro.get_entry_proteomes("IPR000001", page_size=5)
    assert proteomes is not None
    assert "results" in proteomes


def test_get_set(interpro):
    pfam_clan = interpro.get_set("pfam", "CL0001")
    assert pfam_clan is not None
    assert "metadata" in pfam_clan
