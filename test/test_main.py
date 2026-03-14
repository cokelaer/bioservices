from click.testing import CliRunner

from bioservices.main import main


def test_main_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "BioServices" in result.output


def test_main_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0


def test_download_accession_help():
    runner = CliRunner()
    result = runner.invoke(main, ["download-accession", "--help"])
    assert result.exit_code == 0
    assert "accession" in result.output


def test_taxonomy_help():
    runner = CliRunner()
    result = runner.invoke(main, ["taxonomy", "--help"])
    assert result.exit_code == 0
    assert "taxon" in result.output.lower() or "id" in result.output.lower()


# ---------------------------------------------------------------------------
# protein subcommand tests (help / option validation only, no network calls)
# ---------------------------------------------------------------------------


def test_protein_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "--help"])
    assert result.exit_code == 0
    assert "protein" in result.output.lower()


def test_protein_search_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "search", "--help"])
    assert result.exit_code == 0
    assert "--query" in result.output


def test_protein_sequence_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "sequence", "--help"])
    assert result.exit_code == 0
    assert "--uniprot-id" in result.output


def test_protein_structure_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "structure", "--help"])
    assert result.exit_code == 0
    assert "--uniprot-id" in result.output


def test_protein_annotation_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "annotation", "--help"])
    assert result.exit_code == 0
    assert "--uniprot-id" in result.output


def test_protein_interaction_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "interaction", "--help"])
    assert result.exit_code == 0
    assert "--gene" in result.output
    assert "--taxid" in result.output


def test_protein_map_id_help():
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "map-id", "--help"])
    assert result.exit_code == 0
    assert "--from" in result.output
    assert "--to" in result.output
    assert "--id" in result.output


def test_protein_search_missing_query():
    """search requires --query; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "search"])
    assert result.exit_code != 0


def test_protein_sequence_missing_id():
    """sequence requires --uniprot-id; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "sequence"])
    assert result.exit_code != 0


def test_protein_map_id_missing_options():
    """map-id requires --from, --to and --id; missing any should be an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["protein", "map-id", "--from", "uniprot", "--to", "kegg"])
    assert result.exit_code != 0
