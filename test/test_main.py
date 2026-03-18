from unittest.mock import MagicMock, patch

import pytest
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


# ---------------------------------------------------------------------------
# compound subcommand tests (help / option validation only, no network calls)
# ---------------------------------------------------------------------------


def test_compound_help():
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "--help"])
    assert result.exit_code == 0
    assert "compound" in result.output.lower()


def test_compound_search_help():
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "search", "--help"])
    assert result.exit_code == 0
    assert "--query" in result.output
    assert "--source" in result.output
    assert "--limit" in result.output


def test_compound_structure_help():
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "structure", "--help"])
    assert result.exit_code == 0
    assert "--id" in result.output
    assert "--field" in result.output


def test_compound_activity_help():
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "activity", "--help"])
    assert result.exit_code == 0
    assert "--chembl-id" in result.output
    assert "--limit" in result.output
    assert "--type" in result.output


def test_compound_reaction_help():
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "reaction", "--help"])
    assert result.exit_code == 0
    assert "--query" in result.output
    assert "--limit" in result.output


def test_compound_search_missing_query():
    """search requires --query; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "search"])
    assert result.exit_code != 0


def test_compound_search_source_choices():
    """search --source only accepts chembl or chebi."""
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "search", "--query", "aspirin", "--source", "invalid"])
    assert result.exit_code != 0


def test_compound_structure_missing_id():
    """structure requires --id; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "structure"])
    assert result.exit_code != 0


def test_compound_structure_field_choices():
    """structure --field only accepts all, smiles, formula, inchikey."""
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "structure", "--id", "CHEBI:27732", "--field", "invalid"])
    assert result.exit_code != 0


def test_compound_activity_missing_chembl_id():
    """activity requires --chembl-id; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "activity"])
    assert result.exit_code != 0


def test_compound_reaction_missing_query():
    """reaction requires --query; missing it should produce an error."""
    runner = CliRunner()
    result = runner.invoke(main, ["compound", "reaction"])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# download-accession functional tests
# ---------------------------------------------------------------------------


def test_download_accession_runs():
    runner = CliRunner()
    with patch("bioservices.apps.download_fasta.download_fasta") as mock_dl:
        result = runner.invoke(main, ["download-accession", "--accession", "FN433596.1"])
    assert result.exit_code == 0
    mock_dl.assert_called_once()


def test_download_accession_with_gff3():
    runner = CliRunner()
    with patch("bioservices.apps.download_fasta.download_fasta"), patch(
        "bioservices.apps.download_gff3.download_gff3"
    ) as mock_gff:
        result = runner.invoke(main, ["download-accession", "--accession", "FN433596.1", "--with-gff3"])
    assert result.exit_code == 0
    mock_gff.assert_called_once()


def test_download_accession_with_gbk():
    runner = CliRunner()
    with patch("bioservices.apps.download_fasta.download_fasta"), patch(
        "bioservices.apps.download_gbk.download_gbk"
    ) as mock_gbk:
        result = runner.invoke(main, ["download-accession", "--accession", "FN433596.1", "--with-gbk"])
    assert result.exit_code == 0
    mock_gbk.assert_called_once()


def test_download_accession_with_prefix():
    runner = CliRunner()
    with patch("bioservices.apps.download_fasta.download_fasta") as mock_dl:
        result = runner.invoke(main, ["download-accession", "--accession", "FN433596.1", "--prefix", "myfile"])
    assert result.exit_code == 0
    call_kwargs = mock_dl.call_args
    assert call_kwargs[1]["output_filename"] == "myfile.fa"


# ---------------------------------------------------------------------------
# taxonomy functional tests
# ---------------------------------------------------------------------------


def test_taxonomy_eutils():
    mock_eu = MagicMock()
    mock_eu.ESummary.return_value = {"uids": ["9606"], "9606": {"ScientificName": "Homo sapiens"}}
    with patch("bioservices.EUtils", return_value=mock_eu):
        runner = CliRunner()
        result = runner.invoke(main, ["taxonomy", "--id", "9606"])
    assert result.exit_code == 0
    mock_eu.ESummary.assert_called_once_with("taxonomy", "9606")


# ---------------------------------------------------------------------------
# protein functional tests
# ---------------------------------------------------------------------------


def test_protein_search_with_result():
    mock_u = MagicMock()
    mock_u.search.return_value = "accession\tZAP70_HUMAN\n"
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "search", "--query", "ZAP70"])
    assert result.exit_code == 0
    assert "ZAP70_HUMAN" in result.output


def test_protein_search_no_result():
    mock_u = MagicMock()
    mock_u.search.return_value = None
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "search", "--query", "NOTFOUND"])
    assert result.exit_code == 0
    assert result.output == ""


def test_protein_search_with_organism_name():
    mock_u = MagicMock()
    mock_u.search.return_value = "result"
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "search", "--query", "ZAP70", "--organism", "human"])
    assert result.exit_code == 0
    call_args = mock_u.search.call_args[0][0]
    assert "9606" in call_args


def test_protein_search_with_organism_taxid():
    mock_u = MagicMock()
    mock_u.search.return_value = "result"
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "search", "--query", "ZAP70", "--organism", "9606"])
    assert result.exit_code == 0
    call_args = mock_u.search.call_args[0][0]
    assert "9606" in call_args


def test_protein_search_format_fasta():
    mock_u = MagicMock()
    mock_u.search.return_value = ">P43403\nMSEQ"
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "search", "--query", "ZAP70", "--format", "fasta"])
    assert result.exit_code == 0
    mock_u.search.assert_called_once()
    assert mock_u.search.call_args[1]["frmt"] == "fasta"


def test_protein_sequence_with_result():
    mock_u = MagicMock()
    mock_u.get_fasta.return_value = ">P43403\nMSEQ"
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "sequence", "--uniprot-id", "P43403"])
    assert result.exit_code == 0
    assert "P43403" in result.output


def test_protein_sequence_no_result():
    mock_u = MagicMock()
    mock_u.get_fasta.return_value = None
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "sequence", "--uniprot-id", "NOTFOUND"])
    assert result.exit_code == 0
    assert result.output == ""


def test_protein_structure_with_result():
    mock_p = MagicMock()
    mock_p.search.return_value = {"result_set": [{"identifier": "1ATP"}]}
    with patch("bioservices.PDB", return_value=mock_p):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "structure", "--uniprot-id", "P43403"])
    assert result.exit_code == 0
    assert "1ATP" in result.output


def test_protein_structure_no_result():
    mock_p = MagicMock()
    mock_p.search.return_value = {}
    with patch("bioservices.PDB", return_value=mock_p):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "structure", "--uniprot-id", "NOTFOUND"])
    assert result.exit_code == 0


def test_protein_annotation_json():
    mock_u = MagicMock()
    mock_u.retrieve.return_value = {"id": "P43403", "gene": "ZAP70"}
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "annotation", "--uniprot-id", "P43403"])
    assert result.exit_code == 0
    assert "P43403" in result.output


def test_protein_annotation_txt():
    mock_u = MagicMock()
    mock_u.retrieve.return_value = "ID   ZAP70_HUMAN"
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "annotation", "--uniprot-id", "P43403", "--format", "txt"])
    assert result.exit_code == 0
    assert "ZAP70_HUMAN" in result.output


def test_protein_annotation_no_result():
    mock_u = MagicMock()
    mock_u.retrieve.return_value = None
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "annotation", "--uniprot-id", "NOTFOUND"])
    assert result.exit_code == 0
    assert result.output == ""


def test_protein_interaction_with_result():
    mock_s = MagicMock()
    mock_s.get_interactions.return_value = [{"preferredName_A": "ZAP70"}]
    with patch("bioservices.STRING", return_value=mock_s):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "interaction", "--gene", "ZAP70"])
    assert result.exit_code == 0
    assert "ZAP70" in result.output


def test_protein_interaction_no_result():
    mock_s = MagicMock()
    mock_s.get_interactions.return_value = None
    with patch("bioservices.STRING", return_value=mock_s):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "interaction", "--gene", "NOTFOUND"])
    assert result.exit_code == 0


def test_protein_map_id_with_result():
    mock_u = MagicMock()
    mock_u.mapping.return_value = {"results": [{"from": "P43403", "to": "hsa:7535"}], "failedIds": []}
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "map-id", "--from", "uniprot", "--to", "kegg", "--id", "P43403"])
    assert result.exit_code == 0
    assert "P43403" in result.output


def test_protein_map_id_no_result():
    mock_u = MagicMock()
    mock_u.mapping.return_value = None
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["protein", "map-id", "--from", "uniprot", "--to", "kegg", "--id", "NOTFOUND"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# gene functional tests
# ---------------------------------------------------------------------------


def test_gene_info_with_result():
    mock_mgi = MagicMock()
    mock_mgi.get_one_gene.return_value = {"symbol": "CDK2", "name": "cyclin dependent kinase 2"}
    with patch("bioservices.MyGeneInfo", return_value=mock_mgi):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "info", "--gene-id", "1017"])
    assert result.exit_code == 0
    assert "CDK2" in result.output


def test_gene_info_no_result():
    mock_mgi = MagicMock()
    mock_mgi.get_one_gene.return_value = None
    with patch("bioservices.MyGeneInfo", return_value=mock_mgi):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "info", "--gene-id", "9999999"])
    assert result.exit_code == 0


def test_gene_info_custom_fields():
    mock_mgi = MagicMock()
    mock_mgi.get_one_gene.return_value = {"symbol": "CDK2"}
    with patch("bioservices.MyGeneInfo", return_value=mock_mgi):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "info", "--gene-id", "1017", "--fields", "symbol,name"])
    assert result.exit_code == 0
    mock_mgi.get_one_gene.assert_called_once_with("1017", fields="symbol,name")


def test_gene_name_with_result():
    mock_h = MagicMock()
    mock_h.fetch.return_value = {"response": {"docs": [{"symbol": "BRAF"}]}}
    with patch("bioservices.HGNC", return_value=mock_h):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "name", "--symbol", "BRAF"])
    assert result.exit_code == 0
    assert "BRAF" in result.output


def test_gene_name_no_result():
    mock_h = MagicMock()
    mock_h.fetch.return_value = None
    with patch("bioservices.HGNC", return_value=mock_h):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "name", "--symbol", "NOTFOUND"])
    assert result.exit_code == 0


def test_gene_ontology_go_term():
    mock_go = MagicMock()
    mock_go.get_go_terms.return_value = {"results": [{"id": "GO:0003824", "name": "catalytic activity"}]}
    with patch("bioservices.QuickGO", return_value=mock_go):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "ontology", "--query", "GO:0003824"])
    assert result.exit_code == 0
    mock_go.get_go_terms.assert_called_once_with("GO:0003824")
    assert "GO:0003824" in result.output


def test_gene_ontology_free_text():
    mock_go = MagicMock()
    mock_go.go_search.return_value = {"results": [{"id": "GO:0016301"}]}
    with patch("bioservices.QuickGO", return_value=mock_go):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "ontology", "--query", "kinase"])
    assert result.exit_code == 0
    mock_go.go_search.assert_called_once_with("kinase")


def test_gene_ontology_no_result():
    mock_go = MagicMock()
    mock_go.go_search.return_value = None
    with patch("bioservices.QuickGO", return_value=mock_go):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "ontology", "--query", "notareal"])
    assert result.exit_code == 0


def test_gene_expression_with_result():
    mock_ae = MagicMock()
    mock_ae.queryAE.return_value = {"experiments": [{"accession": "E-MTAB-1"}]}
    with patch("bioservices.ArrayExpress", return_value=mock_ae):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "expression", "--query", "cancer"])
    assert result.exit_code == 0
    assert "E-MTAB-1" in result.output


def test_gene_expression_with_species():
    mock_ae = MagicMock()
    mock_ae.queryAE.return_value = {"experiments": []}
    with patch("bioservices.ArrayExpress", return_value=mock_ae):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "expression", "--query", "cancer", "--species", "homo sapiens"])
    assert result.exit_code == 0
    mock_ae.queryAE.assert_called_once_with(keywords="cancer", species="homo sapiens")


def test_gene_expression_no_result():
    mock_ae = MagicMock()
    mock_ae.queryAE.return_value = None
    with patch("bioservices.ArrayExpress", return_value=mock_ae):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "expression", "--query", "NOTFOUND"])
    assert result.exit_code == 0


def test_gene_pathway_reactome_with_result():
    mock_r = MagicMock()
    mock_r.search_query.return_value = {"results": [{"displayName": "TP53 Regulates Transcription"}]}
    with patch("bioservices.Reactome", return_value=mock_r):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "pathway", "--query", "TP53"])
    assert result.exit_code == 0
    assert "TP53" in result.output


def test_gene_pathway_reactome_no_result():
    mock_r = MagicMock()
    mock_r.search_query.return_value = None
    with patch("bioservices.Reactome", return_value=mock_r):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "pathway", "--query", "NOTFOUND"])
    assert result.exit_code == 0


def test_gene_pathway_kegg_with_result():
    mock_k = MagicMock()
    mock_k.find.return_value = "path:hsa04115\tp53 signaling pathway"
    with patch("bioservices.KEGG", return_value=mock_k):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "pathway", "--query", "TP53", "--source", "kegg"])
    assert result.exit_code == 0
    assert "p53" in result.output


def test_gene_pathway_kegg_no_result():
    mock_k = MagicMock()
    mock_k.find.return_value = None
    with patch("bioservices.KEGG", return_value=mock_k):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "pathway", "--query", "NOTFOUND", "--source", "kegg"])
    assert result.exit_code == 0


def test_gene_ortholog_with_result():
    mock_p = MagicMock()
    mock_p.get_mapping.return_value = {"mapped": [{"taxon_id": 10090}]}
    with patch("bioservices.Panther", return_value=mock_p):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "ortholog", "--gene", "zap70"])
    assert result.exit_code == 0
    assert "10090" in result.output


def test_gene_ortholog_no_result():
    mock_p = MagicMock()
    mock_p.get_mapping.return_value = None
    with patch("bioservices.Panther", return_value=mock_p):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "ortholog", "--gene", "NOTFOUND"])
    assert result.exit_code == 0


def test_gene_map_id_with_result():
    mock_u = MagicMock()
    mock_u.mapping.return_value = {"results": [{"from": "P43403", "to": "hsa:7535"}], "failedIds": []}
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "map-id", "--from", "uniprot", "--to", "kegg", "--id", "P43403"])
    assert result.exit_code == 0
    assert "P43403" in result.output


def test_gene_map_id_ncbi_geneid():
    mock_u = MagicMock()
    mock_u.mapping.return_value = {"results": [], "failedIds": ["7535"]}
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "map-id", "--from", "ncbi-geneid", "--to", "uniprot", "--id", "7535"])
    assert result.exit_code == 0
    # ncbi-geneid maps to GeneID
    mock_u.mapping.assert_called_once_with(fr="GeneID", to="UniProtKB_AC-ID", query="7535")


def test_gene_map_id_no_result():
    mock_u = MagicMock()
    mock_u.mapping.return_value = None
    with patch("bioservices.UniProt", return_value=mock_u):
        runner = CliRunner()
        result = runner.invoke(main, ["gene", "map-id", "--from", "uniprot", "--to", "kegg", "--id", "NOTFOUND"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# compound functional tests
# ---------------------------------------------------------------------------


def test_compound_search_chembl_with_result():
    mock_c = MagicMock()
    mock_c.search_molecule.return_value = {"molecules": [{"molecule_chembl_id": "CHEMBL25"}]}
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "search", "--query", "aspirin"])
    assert result.exit_code == 0
    assert "CHEMBL25" in result.output


def test_compound_search_chembl_no_result():
    mock_c = MagicMock()
    mock_c.search_molecule.return_value = None
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "search", "--query", "NOTFOUND"])
    assert result.exit_code == 0


def test_compound_search_chebi_with_result():
    mock_c = MagicMock()
    mock_c.getLiteEntity.return_value = [{"chebiId": "CHEBI:27732", "chebiAsciiName": "caffeine"}]
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "search", "--query", "caffeine", "--source", "chebi"])
    assert result.exit_code == 0
    assert "caffeine" in result.output


def test_compound_search_chebi_no_result():
    mock_c = MagicMock()
    mock_c.getLiteEntity.return_value = None
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "search", "--query", "NOTFOUND", "--source", "chebi"])
    assert result.exit_code == 0


def test_compound_search_limit_passed():
    mock_c = MagicMock()
    mock_c.search_molecule.return_value = {"molecules": []}
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "search", "--query", "aspirin", "--limit", "5"])
    assert result.exit_code == 0
    mock_c.search_molecule.assert_called_once_with("aspirin", limit=5)


def test_compound_structure_field_all():
    mock_entity = MagicMock()
    mock_entity.__bool__ = lambda self: True
    mock_entity.__iter__ = lambda self: iter([("smiles", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C")])
    mock_c = MagicMock()
    mock_c.getCompleteEntity.return_value = mock_entity
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "structure", "--id", "CHEBI:27732"])
    assert result.exit_code == 0


def test_compound_structure_field_smiles():
    mock_entity = MagicMock()
    mock_entity.__bool__ = lambda self: True
    mock_entity.smiles = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
    mock_c = MagicMock()
    mock_c.getCompleteEntity.return_value = mock_entity
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "structure", "--id", "CHEBI:27732", "--field", "smiles"])
    assert result.exit_code == 0
    assert "CN1C" in result.output


def test_compound_structure_field_formula():
    mock_entity = MagicMock()
    mock_entity.__bool__ = lambda self: True
    mock_entity.formula = "C8H10N4O2"
    mock_c = MagicMock()
    mock_c.getCompleteEntity.return_value = mock_entity
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "structure", "--id", "CHEBI:27732", "--field", "formula"])
    assert result.exit_code == 0
    assert "C8H10N4O2" in result.output


def test_compound_structure_field_inchikey():
    mock_entity = MagicMock()
    mock_entity.__bool__ = lambda self: True
    mock_entity.inchiKey = "RYYVLZVUVIJVGH-UHFFFAOYSA-N"
    mock_c = MagicMock()
    mock_c.getCompleteEntity.return_value = mock_entity
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "structure", "--id", "CHEBI:27732", "--field", "inchikey"])
    assert result.exit_code == 0
    assert "RYYVLZVUVIJVGH" in result.output


def test_compound_structure_no_result():
    mock_c = MagicMock()
    mock_c.getCompleteEntity.return_value = None
    with patch("bioservices.ChEBI", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "structure", "--id", "CHEBI:00000"])
    assert result.exit_code == 0


def test_compound_activity_with_result():
    mock_c = MagicMock()
    mock_c.get_activity.return_value = {"activities": [{"standard_value": "100", "standard_type": "IC50"}]}
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "activity", "--chembl-id", "CHEMBL25"])
    assert result.exit_code == 0
    assert "IC50" in result.output


def test_compound_activity_with_type_filter():
    mock_c = MagicMock()
    mock_c.get_activity.return_value = {"activities": []}
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "activity", "--chembl-id", "CHEMBL25", "--type", "IC50"])
    assert result.exit_code == 0
    call_kwargs = mock_c.get_activity.call_args[1]
    assert "standard_type=IC50" in call_kwargs["filters"]


def test_compound_activity_no_result():
    mock_c = MagicMock()
    mock_c.get_activity.return_value = None
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "activity", "--chembl-id", "CHEMBL00000"])
    assert result.exit_code == 0


def test_compound_activity_chembl_id_uppercased():
    mock_c = MagicMock()
    mock_c.get_activity.return_value = {"activities": []}
    with patch("bioservices.ChEMBL", return_value=mock_c):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "activity", "--chembl-id", "chembl25"])
    assert result.exit_code == 0
    call_kwargs = mock_c.get_activity.call_args[1]
    assert "molecule_chembl_id=CHEMBL25" in call_kwargs["filters"]


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_compound_reaction_with_result():
    import pandas as pd

    mock_r = MagicMock()
    mock_r.search.return_value = pd.DataFrame({"rhea_id": ["10660"], "equation": ["ATP + ADP"]})
    with patch("bioservices.Rhea", return_value=mock_r):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "reaction", "--query", "caffeine"])
    assert result.exit_code == 0
    mock_r.search.assert_called_once_with("caffeine", limit=10)


def test_compound_reaction_with_limit():
    mock_r = MagicMock()
    mock_r.search.return_value = "rhea:10660"
    with patch("bioservices.Rhea", return_value=mock_r):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "reaction", "--query", "caffeine", "--limit", "5"])
    assert result.exit_code == 0
    mock_r.search.assert_called_once_with("caffeine", limit=5)


def test_compound_reaction_no_result():
    mock_r = MagicMock()
    mock_r.search.return_value = None
    with patch("bioservices.Rhea", return_value=mock_r):
        runner = CliRunner()
        result = runner.invoke(main, ["compound", "reaction", "--query", "NOTFOUND"])
    assert result.exit_code == 0
