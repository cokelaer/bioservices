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


# ---------------------------------------------------------------------------
# gene subcommand tests (help / option validation only, no network calls)
# ---------------------------------------------------------------------------


def test_gene_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "--help"])
    assert result.exit_code == 0
    assert "gene" in result.output.lower()


def test_gene_info_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "info", "--help"])
    assert result.exit_code == 0
    assert "--gene-id" in result.output


def test_gene_name_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "name", "--help"])
    assert result.exit_code == 0
    assert "--symbol" in result.output


def test_gene_ontology_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "ontology", "--help"])
    assert result.exit_code == 0
    assert "--query" in result.output


def test_gene_expression_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "expression", "--help"])
    assert result.exit_code == 0
    assert "--query" in result.output


def test_gene_pathway_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "pathway", "--help"])
    assert result.exit_code == 0
    assert "--query" in result.output
    assert "--source" in result.output


def test_gene_ortholog_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "ortholog", "--help"])
    assert result.exit_code == 0
    assert "--gene" in result.output
    assert "--taxid" in result.output


def test_gene_map_id_help():
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "map-id", "--help"])
    assert result.exit_code == 0
    assert "--from" in result.output
    assert "--to" in result.output
    assert "--id" in result.output


def test_gene_info_missing_gene_id():
    """info requires --gene-id; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "info"])
    assert result.exit_code != 0


def test_gene_name_missing_symbol():
    """name requires --symbol; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "name"])
    assert result.exit_code != 0


def test_gene_ontology_missing_query():
    """ontology requires --query; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "ontology"])
    assert result.exit_code != 0


def test_gene_expression_missing_query():
    """expression requires --query; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "expression"])
    assert result.exit_code != 0


def test_gene_pathway_missing_query():
    """pathway requires --query; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "pathway"])
    assert result.exit_code != 0


def test_gene_pathway_source_choices():
    """pathway --source only accepts reactome or kegg."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "pathway", "--query", "TP53", "--source", "invalid"])
    assert result.exit_code != 0


def test_gene_ortholog_missing_gene():
    """ortholog requires --gene; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "ortholog"])
    assert result.exit_code != 0


def test_gene_map_id_missing_options():
    """map-id requires --from, --to and --id; missing any should be an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["gene", "map-id", "--from", "uniprot", "--to", "kegg"])
    assert result.exit_code != 0
