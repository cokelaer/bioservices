"""Pure unit tests (no network calls) for ChEBI, ChEMBL, Rhea, Settings, Services, and STRING."""
import errno
import os
import sys
import tempfile
import time
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from requests.models import Response

from bioservices.chebi import _RELATION_TYPE_MAP, ChEBI, ChebiEntity
from bioservices.chembl import ChEMBL
from bioservices.rhea import Rhea
from bioservices.services import REST, RESTbase, Service
from bioservices.settings import BioServicesConfig, ConfigReadOnly, defaultParams
from bioservices.string import STRING

# ---------------------------------------------------------------------------
# Helpers: create instances without network
# ---------------------------------------------------------------------------


def _make_chebi():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        return ChEBI(verbose=False)


def _make_chembl():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        return ChEMBL(verbose=False)


def _make_rhea():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        return Rhea(verbose=False)


# ---------------------------------------------------------------------------
# ChebiEntity properties
# ---------------------------------------------------------------------------


class TestChebiEntity:
    def test_mass(self):
        e = ChebiEntity({"chemical_data": {"mass": "194.19"}})
        assert e.mass == "194.19"

    def test_mass_missing(self):
        assert ChebiEntity({}).mass is None

    def test_mass_none_chemical_data(self):
        assert ChebiEntity({"chemical_data": None}).mass is None

    def test_smiles(self):
        e = ChebiEntity({"default_structure": {"smiles": "Cn1cnc2c1"}})
        assert e.smiles == "Cn1cnc2c1"

    def test_smiles_missing(self):
        assert ChebiEntity({}).smiles is None

    def test_inchikey(self):
        e = ChebiEntity({"default_structure": {"standard_inchi_key": "RYYVLZVUVIJVGH-UHFFFAOYSA-N"}})
        assert e.inchiKey == "RYYVLZVUVIJVGH-UHFFFAOYSA-N"

    def test_inchikey_missing(self):
        assert ChebiEntity({}).inchiKey is None

    def test_formula(self):
        e = ChebiEntity({"chemical_data": {"formula": "C8H10N4O2"}})
        assert e.formula == "C8H10N4O2"

    def test_formula_missing(self):
        assert ChebiEntity({}).formula is None

    def test_charge(self):
        e = ChebiEntity({"chemical_data": {"charge": "0"}})
        assert e.charge == "0"

    def test_charge_missing(self):
        assert ChebiEntity({}).charge is None

    def test_chebi_ascii_name_primary(self):
        e = ChebiEntity({"ascii_name": "caffeine"})
        assert e.chebiAsciiName == "caffeine"

    def test_chebi_ascii_name_fallback_to_name(self):
        e = ChebiEntity({"name": "caffeine"})
        assert e.chebiAsciiName == "caffeine"

    def test_chebi_ascii_name_missing(self):
        assert ChebiEntity({}).chebiAsciiName is None

    def test_chebi_id_accession(self):
        e = ChebiEntity({"chebi_accession": "CHEBI:27732"})
        assert e.chebiId == "CHEBI:27732"

    def test_chebi_id_int_fallback(self):
        e = ChebiEntity({"id": 27732})
        assert e.chebiId == "27732"

    def test_chebi_id_empty(self):
        assert ChebiEntity({}).chebiId == ""

    def test_database_links(self):
        e = ChebiEntity(
            {
                "database_accessions": {
                    "kegg": [{"accession_number": "C01873", "source_name": "KEGG COMPOUND accession"}],
                    "pdb": [{"accession_number": "CAF", "source_name": "PDB Chemical Component accession"}],
                }
            }
        )
        links = e.DatabaseLinks
        assert ("C01873", "KEGG COMPOUND accession") in links
        assert ("CAF", "PDB Chemical Component accession") in links
        assert len(links) == 2

    def test_database_links_empty(self):
        assert ChebiEntity({}).DatabaseLinks == []

    def test_database_links_empty_list(self):
        e = ChebiEntity({"database_accessions": {"kegg": []}})
        assert e.DatabaseLinks == []

    def test_database_links_skips_blank_entries(self):
        e = ChebiEntity({"database_accessions": {"x": [{"accession_number": "", "source_name": ""}]}})
        assert e.DatabaseLinks == []

    def test_database_links_non_list_value_skipped(self):
        e = ChebiEntity({"database_accessions": {"x": "not-a-list"}})
        assert e.DatabaseLinks == []


# ---------------------------------------------------------------------------
# ChEBI._chebi_num
# ---------------------------------------------------------------------------


class TestChebiNum:
    def test_prefixed_string(self):
        ch = _make_chebi()
        assert ch._chebi_num("CHEBI:27732") == "27732"

    def test_plain_string(self):
        ch = _make_chebi()
        assert ch._chebi_num("27732") == "27732"

    def test_integer(self):
        ch = _make_chebi()
        assert ch._chebi_num(27732) == "27732"

    def test_whitespace_stripped(self):
        ch = _make_chebi()
        assert ch._chebi_num("  CHEBI:27732  ") == "27732"

    def test_lowercase_prefix(self):
        ch = _make_chebi()
        assert ch._chebi_num("chebi:27732") == "27732"


# ---------------------------------------------------------------------------
# ChEBI mocked methods
# ---------------------------------------------------------------------------


class TestChEBIMocked:
    def test_get_complete_entity_returns_chebi_entity(self):
        ch = _make_chebi()
        payload = {"chebi_accession": "CHEBI:27732", "ascii_name": "caffeine"}
        with patch.object(ch, "http_get", return_value=payload):
            result = ch.getCompleteEntity("CHEBI:27732")
        assert isinstance(result, ChebiEntity)
        assert result.chebiAsciiName == "caffeine"

    def test_get_complete_entity_non_dict_passthrough(self):
        ch = _make_chebi()
        with patch.object(ch, "http_get", return_value=404):
            result = ch.getCompleteEntity("CHEBI:99999")
        assert result == 404

    def test_get_lite_entity_parses_results(self):
        ch = _make_chebi()
        payload = {
            "results": [
                {"_source": {"ascii_name": "caffeine", "chebi_accession": "CHEBI:27732"}},
                {"_source": {"ascii_name": "theobromine", "chebi_accession": "CHEBI:28946"}},
            ]
        }
        with patch.object(ch, "http_get", return_value=payload):
            results = ch.getLiteEntity("caffeine")
        assert len(results) == 2
        assert all(isinstance(r, ChebiEntity) for r in results)
        assert results[0].chebiAsciiName == "caffeine"
        assert results[1].chebiAsciiName == "theobromine"

    def test_get_lite_entity_no_results_key(self):
        ch = _make_chebi()
        with patch.object(ch, "http_get", return_value={"other": "data"}):
            assert ch.getLiteEntity("nothing") == []

    def test_get_lite_entity_non_dict_response(self):
        ch = _make_chebi()
        with patch.object(ch, "http_get", return_value=404):
            assert ch.getLiteEntity("nothing") == []

    def test_conv_invalid_target_raises(self):
        ch = _make_chebi()
        entity = ChebiEntity(
            {
                "database_accessions": {
                    "kegg": [{"accession_number": "C01873", "source_name": "KEGG COMPOUND accession"}]
                }
            }
        )
        with patch.object(ch, "getCompleteEntity", return_value=entity):
            with pytest.raises(ValueError, match="valid database target"):
                ch.conv("CHEBI:27732", "wrong db")

    def test_conv_non_dict_entity_raises(self):
        ch = _make_chebi()
        with patch.object(ch, "getCompleteEntity", return_value=404):
            with pytest.raises(ValueError, match="Could not retrieve entity"):
                ch.conv("CHEBI:27732", "KEGG COMPOUND accession")

    def test_get_all_ontology_children_filters_by_relation_type(self):
        ch = _make_chebi()
        mock_response = {
            "ontology_relations": {
                "incoming_relations": [
                    {"relation_type": "is_a", "chebi_id": "CHEBI:100"},
                    {"relation_type": "has_role", "chebi_id": "CHEBI:200"},
                ]
            }
        }
        with patch.object(ch, "http_get", return_value=mock_response):
            results = ch.getAllOntologyChildrenInPath("CHEBI:27732", "is a")
        assert len(results) == 1
        assert results[0]["chebi_id"] == "CHEBI:100"

    def test_get_all_ontology_children_empty_incoming(self):
        ch = _make_chebi()
        mock_response = {"ontology_relations": {"incoming_relations": []}}
        with patch.object(ch, "http_get", return_value=mock_response):
            results = ch.getAllOntologyChildrenInPath("CHEBI:27732", "has role")
        assert results == []

    def test_get_all_ontology_children_invalid_type_raises(self):
        ch = _make_chebi()
        with pytest.raises(Exception):
            ch.getAllOntologyChildrenInPath("CHEBI:27732", "invalid type")

    def test_get_structure_search_invalid_mode_raises(self):
        ch = _make_chebi()
        with pytest.raises(Exception):
            ch.getStructureSearch("structure", mode="INVALID")

    def test_get_structure_search_invalid_category_raises(self):
        ch = _make_chebi()
        with pytest.raises(Exception):
            ch.getStructureSearch("structure", structureSearchCategory="INVALID")

    def test_get_complete_entity_by_list_calls_get_complete_entity(self):
        ch = _make_chebi()
        e1 = ChebiEntity({"ascii_name": "caffeine"})
        e2 = ChebiEntity({"ascii_name": "theobromine"})
        with patch.object(ch, "getCompleteEntity", side_effect=[e1, e2]):
            results = ch.getCompleteEntityByList(["CHEBI:27732", "CHEBI:28946"])
        assert len(results) == 2

    def test_get_complete_entity_by_list_empty(self):
        ch = _make_chebi()
        assert ch.getCompleteEntityByList([]) == []

    def test_get_complete_entity_by_list_none_default(self):
        ch = _make_chebi()
        with patch.object(ch, "getCompleteEntity", return_value=None):
            results = ch.getCompleteEntityByList(["CHEBI:1"])
        assert results == []


# ---------------------------------------------------------------------------
# ChEMBL._check_request
# ---------------------------------------------------------------------------


class TestChEMBLCheckRequest:
    def test_int_raises_value_error(self):
        c = _make_chembl()
        with pytest.raises(ValueError):
            c._check_request(404)

    def test_zero_raises_value_error(self):
        c = _make_chembl()
        with pytest.raises(ValueError):
            c._check_request(0)

    def test_dict_passes(self):
        c = _make_chembl()
        c._check_request({"page_meta": {}})  # must not raise

    def test_none_passes(self):
        c = _make_chembl()
        c._check_request(None)  # non-int, must not raise

    def test_list_passes(self):
        c = _make_chembl()
        c._check_request([])  # non-int, must not raise


# ---------------------------------------------------------------------------
# ChEMBL.order_by
# ---------------------------------------------------------------------------


class TestChEMBLOrderBy:
    DATASET = [
        {"name": "b", "props": {"mw": 300, "logp": {"val": 2.0}}},
        {"name": "a", "props": {"mw": 100, "logp": {"val": 3.0}}},
        {"name": "c", "props": {"mw": 200, "logp": {"val": 1.0}}},
    ]

    def test_top_level_ascending(self):
        c = _make_chembl()
        result = c.order_by(list(self.DATASET), "name")
        assert [r["name"] for r in result] == ["a", "b", "c"]

    def test_top_level_descending(self):
        c = _make_chembl()
        result = c.order_by(list(self.DATASET), "name", ascending=False)
        assert [r["name"] for r in result] == ["c", "b", "a"]

    def test_one_underscore_level(self):
        c = _make_chembl()
        result = c.order_by(list(self.DATASET), "props__mw")
        assert [r["props"]["mw"] for r in result] == [100, 200, 300]

    def test_two_underscore_levels(self):
        c = _make_chembl()
        result = c.order_by(list(self.DATASET), "props__logp__val")
        assert [r["props"]["logp"]["val"] for r in result] == [1.0, 2.0, 3.0]

    def test_three_or_more_underscores_raises(self):
        c = _make_chembl()
        with pytest.raises(NotImplementedError):
            c.order_by(list(self.DATASET), "a__b__c__d")


# ---------------------------------------------------------------------------
# ChEMBL.get_similarity validation
# ---------------------------------------------------------------------------


class TestChEMBLGetSimilarity:
    def test_float_similarity_raises(self):
        c = _make_chembl()
        with pytest.raises(AssertionError):
            c.get_similarity("CHEMBL25", similarity=80.5)

    def test_similarity_below_70_raises(self):
        c = _make_chembl()
        with pytest.raises(AssertionError):
            c.get_similarity("CHEMBL25", similarity=69)

    def test_similarity_above_100_raises(self):
        c = _make_chembl()
        with pytest.raises(AssertionError):
            c.get_similarity("CHEMBL25", similarity=101)

    def test_boundary_70_accepted(self):
        c = _make_chembl()
        with patch.object(
            c.services, "http_get", return_value={"molecules": [], "page_meta": {"total_count": 0, "next": None}}
        ):
            c.get_similarity("CHEMBL25", similarity=70)  # must not raise

    def test_boundary_100_accepted(self):
        c = _make_chembl()
        with patch.object(
            c.services, "http_get", return_value={"molecules": [], "page_meta": {"total_count": 0, "next": None}}
        ):
            c.get_similarity("CHEMBL25", similarity=100)  # must not raise


# ---------------------------------------------------------------------------
# ChEMBL._search result parsing
# ---------------------------------------------------------------------------


class TestChEMBLSearch:
    def test_http_error_returns_empty_dict(self):
        c = _make_chembl()
        with patch.object(c.services, "http_get", return_value=404):
            result = c._search("molecule", "aspirin", params={"limit": 10, "offset": 0})
        assert result == {}

    def test_success_returns_result(self):
        c = _make_chembl()
        payload = {"molecules": [{"molecule_chembl_id": "CHEMBL25"}], "page_meta": {"next": None}}
        with patch.object(c.services, "http_get", return_value=payload):
            result = c._search("molecule", "aspirin", params={"limit": 10, "offset": 0})
        assert result == payload

    def test_limit_too_low_raises(self):
        c = _make_chembl()
        with pytest.raises(AssertionError):
            c._search("molecule", "x", params={"limit": 0, "offset": 0})

    def test_limit_too_high_raises(self):
        c = _make_chembl()
        with pytest.raises(AssertionError):
            c._search("molecule", "x", params={"limit": 1001, "offset": 0})


# ---------------------------------------------------------------------------
# Rhea parameter assembly
# ---------------------------------------------------------------------------


class TestRheaParams:
    def test_search_includes_default_columns(self):
        r = _make_rhea()
        captured = {}

        def mock_get(url, frmt=None, params=None):
            captured.update(params or {})
            return "RHEA-ID\tEquation\n"

        with patch.object(r.services, "http_get", side_effect=mock_get):
            r.search("caffeine")

        assert "columns" in captured
        assert "rhea-id" in captured["columns"]
        assert "equation" in captured["columns"]

    def test_search_with_explicit_columns(self):
        r = _make_rhea()
        captured = {}

        def mock_get(url, frmt=None, params=None):
            captured.update(params or {})
            return "RHEA-ID\n"

        with patch.object(r.services, "http_get", side_effect=mock_get):
            r.search("caffeine", columns="rhea-id")

        assert captured["columns"] == "rhea-id"

    def test_search_includes_limit_when_given(self):
        r = _make_rhea()
        captured = {}

        def mock_get(url, frmt=None, params=None):
            captured.update(params or {})
            return "RHEA-ID\n"

        with patch.object(r.services, "http_get", side_effect=mock_get):
            r.search("caffeine", limit=5)

        assert captured.get("limit") == 5

    def test_search_omits_limit_when_none(self):
        r = _make_rhea()
        captured = {}

        def mock_get(url, frmt=None, params=None):
            captured.update(params or {})
            return "RHEA-ID\n"

        with patch.object(r.services, "http_get", side_effect=mock_get):
            r.search("caffeine")

        assert "limit" not in captured

    def test_search_falls_back_to_string_when_pandas_parse_fails(self):
        r = _make_rhea()
        raw_tsv = "col1\tcol2\nval1\tval2\n"

        with patch.object(r.services, "http_get", return_value=raw_tsv):
            with patch("pandas.read_csv", side_effect=Exception("parse error")):
                result = r.search("caffeine")

        assert result == raw_tsv

    def test_query_includes_default_columns(self):
        r = _make_rhea()
        captured = {}

        def mock_get(url, frmt=None, params=None):
            captured.update(params or {})
            return "RHEA-ID\n"

        with patch.object(r.services, "http_get", side_effect=mock_get):
            r.query("uniprot:*")

        assert "columns" in captured
        assert "rhea-id" in captured["columns"]

    def test_query_includes_limit_when_given(self):
        r = _make_rhea()
        captured = {}

        def mock_get(url, frmt=None, params=None):
            captured.update(params or {})
            return "RHEA-ID\n"

        with patch.object(r.services, "http_get", side_effect=mock_get):
            r.query("uniprot:*", limit=3)

        assert captured.get("limit") == 3

    def test_query_falls_back_to_string_when_pandas_parse_fails(self):
        r = _make_rhea()
        raw_tsv = "col1\tcol2\nval1\tval2\n"

        with patch.object(r.services, "http_get", return_value=raw_tsv):
            with patch("pandas.read_csv", side_effect=Exception("parse error")):
                result = r.query("caffeine")

        assert result == raw_tsv


# ---------------------------------------------------------------------------
# BioServicesConfig / ConfigReadOnly
# ---------------------------------------------------------------------------


class TestBioServicesConfig:
    def test_config_file_property(self):
        cfg = BioServicesConfig()
        assert cfg.config_file == "bioservices.cfg"

    def test_reload_default_params_restores_modified_value(self):
        cfg = BioServicesConfig()
        original = cfg.params["general.timeout"][0]
        cfg.params["general.timeout"][0] = 9999
        cfg.reload_default_params()
        assert cfg.params["general.timeout"][0] == original

    def test_reload_default_params_does_not_mutate_defaults(self):
        cfg = BioServicesConfig()
        cfg.params["general.timeout"][0] = 9999
        cfg.reload_default_params()
        # Reloading again should still work
        cfg.params["general.timeout"][0] = 1111
        cfg.reload_default_params()
        assert cfg._default_params["general.timeout"][0] == cfg.params["general.timeout"][0]

    def test_get_home_returns_path(self):
        cfg = BioServicesConfig()
        home = cfg.home
        assert home is not None
        assert isinstance(home, str)
        assert os.path.isdir(home)

    def test_get_home_fallback_env(self, monkeypatch):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setenv("HOME", tmpdir)
            monkeypatch.setattr("os.path.expanduser", lambda _: "/nonexistent_xyz_12345")
            result = cfg._get_home()
        assert result == tmpdir

    def test_mkdirs_creates_nested_directories(self):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "a", "b", "c")
            cfg._mkdirs(new_dir)
            assert os.path.isdir(new_dir)

    def test_mkdirs_existing_directory_is_silent(self):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg._mkdirs(tmpdir)  # already exists — must not raise

    def test_timeout_default(self):
        cfg = BioServicesConfig()
        assert cfg.TIMEOUT == 30

    def test_timeout_setter(self):
        cfg = BioServicesConfig()
        cfg.TIMEOUT = 120
        assert cfg.TIMEOUT == 120

    def test_max_retries_default(self):
        cfg = BioServicesConfig()
        assert cfg.MAX_RETRIES == 3

    def test_max_retries_setter(self):
        cfg = BioServicesConfig()
        cfg.MAX_RETRIES = 5
        assert cfg.MAX_RETRIES == 5

    def test_async_threshold_default(self):
        cfg = BioServicesConfig()
        assert cfg.ASYNC_THRESHOLD == 10

    def test_concurrent_default(self):
        cfg = BioServicesConfig()
        assert cfg.CONCURRENT == 50

    def test_fast_save_default(self):
        cfg = BioServicesConfig()
        assert cfg.FAST_SAVE is True

    def test_caching_default_is_false(self):
        cfg = BioServicesConfig()
        assert cfg.CACHING is False
