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
