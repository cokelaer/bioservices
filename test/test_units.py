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
        with pytest.raises((AssertionError, TypeError)):
            c.get_similarity("CHEMBL25", similarity=80.5)

    def test_similarity_below_70_raises(self):
        c = _make_chembl()
        with pytest.raises((AssertionError, ValueError)):
            c.get_similarity("CHEMBL25", similarity=69)

    def test_similarity_above_100_raises(self):
        c = _make_chembl()
        with pytest.raises((AssertionError, ValueError)):
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
        with pytest.raises((AssertionError, ValueError)):
            c._search("molecule", "x", params={"limit": 0, "offset": 0})

    def test_limit_too_high_raises(self):
        c = _make_chembl()
        with pytest.raises((AssertionError, ValueError)):
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


# ---------------------------------------------------------------------------
# ConfigReadOnly additional branches
# ---------------------------------------------------------------------------


class TestConfigReadOnlyBranches:
    def test_no_name_raises(self):
        with pytest.raises(Exception):
            ConfigReadOnly(name=None)

    def test_ioerror_creates_default_config(self):
        cfg = BioServicesConfig()
        with patch.object(cfg.config_parser, "read", side_effect=IOError("no file")):
            with patch.object(cfg, "create_default_config_file") as mock_create:
                cfg.read_user_config_file_and_update_params()
        mock_create.assert_called_once()

    def test_type_mismatch_casts_value(self):
        cfg = BioServicesConfig()
        # "5" is str, but general.max_retries expects int → cast int("5") = 5
        with patch.object(cfg.config_parser, "read"), patch.object(
            cfg.config_parser, "sections", return_value=["general"]
        ), patch.object(cfg.config_parser, "section2dict", return_value={"max_retries": "5"}):
            cfg.read_user_config_file_and_update_params()
        assert cfg.params["general.max_retries"][0] == 5

    def test_invalid_key_is_skipped(self):
        cfg = BioServicesConfig()
        with patch.object(cfg.config_parser, "read"), patch.object(
            cfg.config_parser, "sections", return_value=["general"]
        ), patch.object(cfg.config_parser, "section2dict", return_value={"no_such_option": "value"}):
            cfg.read_user_config_file_and_update_params()  # must not raise

    def test_get_home_import_error_falls_back_to_env(self, monkeypatch):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setenv("HOME", tmpdir)
            with patch("os.path.expanduser", side_effect=ImportError):
                result = cfg._get_home()
        assert result == tmpdir

    def test_get_home_returns_none_when_no_env(self):
        cfg = BioServicesConfig()
        with patch("os.path.expanduser", side_effect=ImportError), patch("os.environ.get", return_value=None):
            result = cfg._get_home()
        assert result is None

    def test_mkdirs_reraises_non_eexist_oserror(self):
        cfg = BioServicesConfig()
        err = OSError()
        err.errno = errno.EACCES
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "a", "b")
            with patch("os.makedirs", side_effect=err):
                with pytest.raises(OSError):
                    cfg._mkdirs(new_dir)

    def test_get_and_create_failure_returns_none(self):
        cfg = BioServicesConfig()
        with patch("os.path.exists", return_value=False), patch.object(
            cfg, "_mkdirs", side_effect=Exception("permission denied")
        ):
            result = cfg._get_and_create("/nonexistent/path")
        assert result is None

    def test_init_handles_config_dir_exception(self):
        cfg = BioServicesConfig()
        with patch.object(type(cfg), "user_config_dir", new_callable=PropertyMock, side_effect=Exception("fail")):
            with patch.object(cfg, "read_user_config_file_and_update_params"):
                cfg.init()  # must not raise

    def test_init_handles_cache_dir_exception(self):
        cfg = BioServicesConfig()
        with patch.object(type(cfg), "user_cache_dir", new_callable=PropertyMock, side_effect=Exception("fail")):
            with patch.object(cfg, "read_user_config_file_and_update_params"):
                cfg.init()  # must not raise

    def test_create_default_config_file_new(self):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = os.path.join(tmpdir, "bioservices.cfg")
            with patch.object(type(cfg), "user_config_file_path", new_callable=PropertyMock, return_value=fake_path):
                cfg.create_default_config_file()
            assert os.path.exists(fake_path)
            with open(fake_path) as f:
                content = f.read()
            assert "[general]" in content

    def test_create_default_config_file_backs_up_existing(self):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = os.path.join(tmpdir, "bioservices.cfg")
            with open(fake_path, "w") as f:
                f.write("[existing]\nkey = value\n")
            with patch.object(type(cfg), "user_config_file_path", new_callable=PropertyMock, return_value=fake_path):
                cfg.create_default_config_file()
            assert os.path.exists(fake_path + ".bk")

    def test_create_default_config_file_no_overwrite_backup_when_not_forced(self):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = os.path.join(tmpdir, "bioservices.cfg")
            with open(fake_path, "w") as f:
                f.write("[existing]\n")
            with open(fake_path + ".bk", "w") as f:
                f.write("[original_backup]\n")
            with patch.object(type(cfg), "user_config_file_path", new_callable=PropertyMock, return_value=fake_path):
                cfg.create_default_config_file(force=False)
            with open(fake_path + ".bk") as f:
                assert "[original_backup]" in f.read()

    def test_create_default_config_file_force_overwrites_backup(self):
        cfg = BioServicesConfig()
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = os.path.join(tmpdir, "bioservices.cfg")
            with open(fake_path, "w") as f:
                f.write("[existing]\n")
            with open(fake_path + ".bk", "w") as f:
                f.write("[old_backup]\n")
            with patch.object(type(cfg), "user_config_file_path", new_callable=PropertyMock, return_value=fake_path):
                cfg.create_default_config_file(force=True)
            assert os.path.exists(fake_path)

    def test_set_caching(self):
        cfg = BioServicesConfig()
        cfg._set_caching(True)
        assert cfg.params["cache.on"][0] is True
        cfg._set_caching(False)
        assert cfg.params["cache.on"][0] is False


# ---------------------------------------------------------------------------
# Service._calls rate-limiter
# ---------------------------------------------------------------------------


def _make_svc():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        return Service("testsvc", "http://example.com", verbose=False)


def _make_rest():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        return REST("testrest", "http://example.com/api", verbose=False)


def _make_string():
    with patch("bioservices.services.urlopen", return_value=MagicMock()):
        return STRING(verbose=False)


class TestServiceCalls:
    def test_first_call_sets_last_call(self):
        svc = _make_svc()
        assert svc._last_call == 0
        svc._calls()
        assert svc._last_call != 0

    def test_fast_enough_no_sleep(self):
        svc = _make_svc()
        svc._last_call = 1.0  # long ago (Unix epoch second 1)
        with patch("time.sleep") as mock_sleep:
            svc._calls()
        mock_sleep.assert_not_called()

    def test_too_fast_sleeps(self):
        svc = _make_svc()
        svc._last_call = time.time()  # just now → dt ≈ 0 < 1/requests_per_sec
        with patch("time.sleep") as mock_sleep:
            svc._calls()
        mock_sleep.assert_called_once()


# ---------------------------------------------------------------------------
# RESTbase abstract interface
# ---------------------------------------------------------------------------


class TestRESTbase:
    def test_init_sets_last_response(self):
        with patch("bioservices.services.urlopen", return_value=MagicMock()):
            base = RESTbase("test", "http://example.com", verbose=False)
        assert base.last_response is None

    def test_abstract_methods_raise(self):
        with patch("bioservices.services.urlopen", return_value=MagicMock()):
            base = RESTbase("test", "http://example.com", verbose=False)
        with pytest.raises(NotImplementedError):
            base.http_get()
        with pytest.raises(NotImplementedError):
            base.http_post()
        with pytest.raises(NotImplementedError):
            base.http_put()
        with pytest.raises(NotImplementedError):
            base.http_delete()


# ---------------------------------------------------------------------------
# REST session / cache management
# ---------------------------------------------------------------------------


class TestRESTSession:
    def test_get_session_uses_cache_when_caching_on(self):
        r = _make_rest()
        r.settings.params["cache.on"][0] = True
        r._session = None
        with patch.object(r, "_create_cache_session", return_value=MagicMock()) as mock_cache:
            _ = r.session
        mock_cache.assert_called_once()

    def test_delete_cache_no_file(self):
        r = _make_rest()
        with patch("os.path.exists", return_value=False), patch("builtins.input") as mock_input:
            r.delete_cache()
        mock_input.assert_not_called()

    def test_delete_cache_user_confirms(self):
        r = _make_rest()
        with patch("os.path.exists", return_value=True), patch("builtins.input", return_value="y"), patch(
            "os.remove"
        ) as mock_remove:
            r.delete_cache()
        mock_remove.assert_called_once()

    def test_delete_cache_user_declines(self):
        r = _make_rest()
        with patch("os.path.exists", return_value=True), patch("builtins.input", return_value="n"), patch(
            "os.remove"
        ) as mock_remove:
            r.delete_cache()
        mock_remove.assert_not_called()

    def test_clear_cache(self):
        r = _make_rest()
        with patch("requests_cache.clear") as mock_clear:
            r.clear_cache()
        mock_clear.assert_called_once()


# ---------------------------------------------------------------------------
# REST request helpers
# ---------------------------------------------------------------------------


class TestRESTRequestHelpers:
    def test_process_get_request_success(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.json.return_value = {"key": "val"}
        mock_session.get.return_value = mock_resp
        result = r._process_get_request("http://example.com", mock_session, "json")
        assert result == {"key": "val"}

    def test_process_get_request_exception_returns_none(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("timeout")
        result = r._process_get_request("http://example.com", mock_session, "json")
        assert result is None

    def test_interpret_json_decode_error_returns_response(self):
        r = _make_rest()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.json.side_effect = ValueError("not json")
        result = r._interpret_returned_request(mock_resp, "json")
        assert result is mock_resp

    def test_apply_filters_none(self):
        r = _make_rest()
        result = r._apply([1, 2, None, 3], lambda x: x * 10)
        assert result == [10, 20, 30]

    def test_get_all_urls(self):
        r = _make_rest()
        urls = list(r._get_all_urls(["q1", "q2"]))
        assert urls == ["http://example.com/api/q1", "http://example.com/api/q2"]

    def test_get_async_success(self):
        r = _make_rest()
        r._session = MagicMock()
        mock_grequests = MagicMock()
        mock_resp = MagicMock()
        mock_grequests.map.return_value = [mock_resp]
        with patch.dict(sys.modules, {"grequests": mock_grequests}):
            result = r._get_async(["q1"], frmt="json")
        assert result == [mock_resp]

    def test_get_async_via_get_async_wrapper(self):
        r = _make_rest()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.content = b"data"
        with patch.object(r, "_get_async", return_value=[mock_resp]):
            result = r.get_async(["q1"], frmt="xml")
        assert len(result) == 1

    def test_http_get_async_branch(self):
        r = _make_rest()
        queries = [f"q{i}" for i in range(11)]  # > ASYNC_THRESHOLD (10)
        with patch.object(r, "get_async", return_value=[{}] * 11) as mock_async:
            r.http_get(queries, frmt="json")
        mock_async.assert_called_once()

    def test_http_get_single_builds_headers(self):
        r = _make_rest()
        with patch.object(r, "get_one", return_value={"id": "x"}) as mock_get:
            result = r.http_get("proteins/P12345", frmt="json")
        assert result == {"id": "x"}
        call_kwargs = mock_get.call_args[1]
        assert "User-Agent" in call_kwargs["headers"]

    def test_http_get_single_custom_content(self):
        r = _make_rest()
        with patch.object(r, "get_one", return_value="ok") as mock_get:
            r.http_get("path", frmt="json", content=None)
        call_kwargs = mock_get.call_args[1]
        assert "headers" in call_kwargs

    def test_get_one_success(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.content = b"result data"
        mock_session.get.return_value = mock_resp
        r._session = mock_session
        result = r.get_one("proteins/P12345", frmt="txt")
        assert result is not None

    def test_get_one_json(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.json.return_value = {"id": "P12345"}
        mock_session.get.return_value = mock_resp
        r._session = mock_session
        result = r.get_one("proteins/P12345", frmt="json")
        assert result == {"id": "P12345"}

    def test_get_one_double_slash_warning(self, caplog):
        r = _make_rest()
        r._url = "http://example.com/api/"  # trailing slash → double //
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.content = b"ok"
        mock_session.get.return_value = mock_resp
        r._session = mock_session
        r.get_one("resource", frmt="txt")
        assert "double //" in caplog.text

    def test_get_one_exception_returns_none(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("connection refused")
        r._session = mock_session
        result = r.get_one("path", frmt="json")
        assert result is None

    def test_http_post_calls_post_one(self):
        r = _make_rest()
        with patch.object(r, "post_one", return_value="result") as mock:
            result = r.http_post("query", data={"k": "v"}, frmt="json")
        mock.assert_called_once()
        assert result == "result"

    def test_http_post_with_custom_headers(self):
        r = _make_rest()
        custom = {"Authorization": "Bearer token"}
        with patch.object(r, "post_one", return_value="ok") as mock:
            r.http_post("query", headers=custom, data={}, frmt="json")
        assert mock.call_args[1]["headers"] == custom

    def test_post_one_success(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.content = b"<result/>"
        mock_session.post.return_value = mock_resp
        r._session = mock_session
        result = r.post_one("query", frmt="xml")
        assert result == "<result/>"

    def test_post_one_no_query_uses_base_url(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.content = b"ok"
        mock_session.post.return_value = mock_resp
        r._session = mock_session
        result = r.post_one(None, frmt="xml")
        assert result == "ok"

    def test_post_one_exception_returns_none(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_session.post.side_effect = Exception("refused")
        r._session = mock_session
        result = r.post_one("query", frmt="json")
        assert result is None

    def test_debug_message(self, capsys):
        r = _make_rest()
        mock_resp = MagicMock()
        mock_resp.content = b"<xml/>"
        mock_resp.reason = "OK"
        mock_resp.status_code = 200
        r.last_response = mock_resp
        r.debug_message()
        captured = capsys.readouterr()
        assert "200" in captured.out

    def test_http_delete_delegates_to_delete_one(self):
        r = _make_rest()
        with patch.object(r, "delete_one", return_value="deleted") as mock:
            r.http_delete("resource/1", frmt="json")
        mock.assert_called_once()

    def test_delete_one_success(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_resp = MagicMock(spec=Response)
        mock_resp.ok = True
        mock_resp.content = b"deleted"
        mock_session.delete.return_value = mock_resp
        r._session = mock_session
        result = r.delete_one("resource/1", frmt="xml")
        assert result == "deleted"

    def test_delete_one_exception_returns_none(self):
        r = _make_rest()
        mock_session = MagicMock()
        mock_session.delete.side_effect = Exception("error")
        r._session = mock_session
        result = r.delete_one("resource/1", frmt="json")
        assert result is None


# ---------------------------------------------------------------------------
# STRING mocked tests
# ---------------------------------------------------------------------------


class TestSTRING:
    def test_init(self):
        s = _make_string()
        assert s.services is not None

    def test_identifiers_to_str_list(self):
        s = _make_string()
        assert s._identifiers_to_str(["ZAP70", "LCK"]) == "ZAP70\rLCK"

    def test_identifiers_to_str_tuple(self):
        s = _make_string()
        assert s._identifiers_to_str(("ZAP70", "LCK")) == "ZAP70\rLCK"

    def test_identifiers_to_str_string(self):
        s = _make_string()
        assert s._identifiers_to_str("ZAP70") == "ZAP70"

    def test_get_calls_requests(self):
        s = _make_string()
        mock_resp = MagicMock()
        mock_resp.json.return_value = [{"string_version": "11.5"}]
        with patch("requests.get", return_value=mock_resp):
            result = s._get("json/version", params={})
        assert result == [{"string_version": "11.5"}]
        mock_resp.raise_for_status.assert_called_once()

    def test_get_version_unwraps_single_element_list(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[{"string_version": "11.5"}]):
            result = s.get_version()
        assert result == {"string_version": "11.5"}

    def test_get_version_returns_non_list_as_is(self):
        s = _make_string()
        with patch.object(s, "_get", return_value={"string_version": "11.5"}):
            result = s.get_version()
        assert result == {"string_version": "11.5"}

    def test_get_string_ids_basic(self):
        s = _make_string()
        expected = [{"stringId": "9606.ENSP00000379990"}]
        with patch.object(s, "_get", return_value=expected) as mock_get:
            result = s.get_string_ids("ZAP70", species=9606)
        assert result == expected
        assert mock_get.call_args[1]["params"]["species"] == 9606

    def test_get_string_ids_no_species(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_string_ids("ZAP70")
        assert "species" not in mock_get.call_args[1]["params"]

    def test_get_string_ids_caller_identity(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_string_ids("ZAP70", caller_identity="myapp")
        assert mock_get.call_args[1]["params"]["caller_identity"] == "myapp"

    def test_get_interactions_basic(self):
        s = _make_string()
        expected = [{"stringId_A": "ZAP70", "score": 900}]
        with patch.object(s, "_get", return_value=expected):
            result = s.get_interactions("ZAP70", species=9606)
        assert result == expected

    def test_get_interactions_required_score(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interactions("ZAP70", required_score=500)
        assert mock_get.call_args[1]["params"]["required_score"] == 500

    def test_get_interactions_add_nodes(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interactions("ZAP70", add_nodes=5)
        assert mock_get.call_args[1]["params"]["add_nodes"] == 5

    def test_get_interactions_show_query_node_labels(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interactions("ZAP70", show_query_node_labels=1)
        assert mock_get.call_args[1]["params"]["show_query_node_labels"] == 1

    def test_get_interactions_caller_identity(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interactions("ZAP70", caller_identity="test")
        assert "caller_identity" in mock_get.call_args[1]["params"]

    def test_get_interactions_list_identifiers(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interactions(["ZAP70", "LCK"])
        assert "\r" in mock_get.call_args[1]["params"]["identifiers"]

    def test_get_network_is_alias_for_get_interactions(self):
        s = _make_string()
        with patch.object(s, "get_interactions", return_value=[]) as mock:
            s.get_network("ZAP70", species=9606)
        mock.assert_called_once_with(
            "ZAP70",
            species=9606,
            required_score=None,
            network_type="functional",
            add_nodes=0,
            show_query_node_labels=0,
            caller_identity=None,
        )

    def test_get_interaction_partners_basic(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interaction_partners("ZAP70", species=9606, required_score=500, limit=10)
        params = mock_get.call_args[1]["params"]
        assert params["species"] == 9606
        assert params["required_score"] == 500
        assert params["limit"] == 10

    def test_get_interaction_partners_no_optional(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_interaction_partners("ZAP70")
        params = mock_get.call_args[1]["params"]
        assert "species" not in params
        assert "required_score" not in params
        assert "limit" not in params

    def test_get_homology_basic(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_homology("ZAP70", species=9606, species_b=10090, required_score=400)
        params = mock_get.call_args[1]["params"]
        assert params["species"] == 9606
        assert params["species_b"] == 10090
        assert params["required_score"] == 400

    def test_get_homology_no_optional(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_homology("ZAP70")
        params = mock_get.call_args[1]["params"]
        assert "species" not in params
        assert "species_b" not in params

    def test_get_enrichment_basic(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_enrichment("ZAP70,LCK", species=9606)
        assert mock_get.call_args[1]["params"]["species"] == 9606

    def test_get_enrichment_with_background(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_enrichment("ZAP70", background_string_identifiers="LCK")
        assert "background_string_identifiers" in mock_get.call_args[1]["params"]

    def test_get_enrichment_caller_identity(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_enrichment("ZAP70", caller_identity="test")
        assert "caller_identity" in mock_get.call_args[1]["params"]

    def test_get_functional_annotation_basic(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_functional_annotation("TP53", species=9606)
        assert mock_get.call_args[1]["params"]["species"] == 9606

    def test_get_functional_annotation_allow_pubmed(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_functional_annotation("TP53", allow_pubmed=1)
        assert mock_get.call_args[1]["params"]["allow_pubmed"] == 1

    def test_get_functional_annotation_caller_identity(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[]) as mock_get:
            s.get_functional_annotation("TP53", caller_identity="test")
        assert "caller_identity" in mock_get.call_args[1]["params"]

    def test_get_ppi_enrichment_unwraps_single_list(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[{"p_value": 0.001, "number_of_edges": 10}]):
            result = s.get_ppi_enrichment("ZAP70,LCK", species=9606)
        assert result["p_value"] == 0.001

    def test_get_ppi_enrichment_returns_non_list_as_is(self):
        s = _make_string()
        with patch.object(s, "_get", return_value={"p_value": 0.001}):
            result = s.get_ppi_enrichment("ZAP70")
        assert result == {"p_value": 0.001}

    def test_get_ppi_enrichment_optional_params(self):
        s = _make_string()
        with patch.object(s, "_get", return_value=[{"p_value": 0}]) as mock_get:
            s.get_ppi_enrichment(
                "ZAP70", species=9606, required_score=500, background_string_identifiers="LCK", caller_identity="t"
            )
        params = mock_get.call_args[1]["params"]
        assert params["required_score"] == 500
        assert "background_string_identifiers" in params
        assert "caller_identity" in params
