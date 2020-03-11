import os.path as osp

import pytest
from easydev import TempFile

from bioservices.bigg import BiGG

@pytest.fixture
def bigg():
    return BiGG(verbose=True)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def test_version(bigg):
    version = bigg.version
    assert keys_exists(version,
        ("bigg_models_version", "api_version", "last_updated"))

    assert version["api_version"] == bigg._api_version

def test_length(bigg):
    assert len(bigg)

def test_models(bigg):
    models = bigg.models
    assert isinstance(models, list)

    assert keys_exists(models[0],
        ("bigg_id", "metabolite_count", "organism", "reaction_count",
        "gene_count"))

def test_metabolites(bigg):
    metabolites = bigg.metabolites("iND750")
    assert isinstance(metabolites, list)

    assert keys_exists(metabolites[0],
        ("bigg_id", "model_bigg_id", "organism", "name", "compartment_bigg_id"))

    metabolite = bigg.metabolites("iND750", "10fthf_c")
    assert keys_exists(metabolite,
        ("formula", "bigg_id", "compartment_bigg_id", "name", "model_bigg_id",
        "old_identifiers", "escher_maps", "other_models_with_metabolite",
        "database_links"))

    metabolites = bigg.metabolites("iND750", ids=["10fthf", "12dgr_SC"])
    assert isinstance(metabolites, list)
    assert len(metabolites)

def test_reactions(bigg):
    reactions = bigg.reactions("iND750")
    assert isinstance(reactions, list)

    assert keys_exists(reactions[0],
        ("bigg_id", "model_bigg_id", "organism", "name"))

    reaction = bigg.reactions("iND750", "GAPD")
    assert keys_exists(reaction,
        ("name", "pseudoreaction", "count", "model_bigg_id", "metabolites",
        "database_links", "escher_maps", "other_models_with_reaction",
        "count", "results"))

    reactions = bigg.reactions("iND750", ids=["13BGH", "13BGHe"])
    assert isinstance(reactions, list)
    assert len(reactions)

def test_genes(bigg):
    genes = bigg.genes("iMM904")
    assert isinstance(genes, list)

    assert keys_exists(genes[0],
        ("bigg_id", "model_bigg_id", "organism", "name"))

    gene = bigg.genes("iMM904", "Q0045")
    assert keys_exists(gene,
        ("bigg_id", "name", "strand", "leftpos", "genome_ref_string",
        "database_links", "rightpos", "protein_sequence", "model_bigg_id",
        "reactions", "old_identifiers", "mapped_to_genbank",
        "genome_name", "chromosome_ncbi_accession"))

    genes = bigg.genes("iMM904", ids=["Q0045", "Q0080"])
    assert isinstance(genes, list)
    assert len(genes)

def test_universal(bigg):
    for type_ in ("metabolites", "reactions"):
        results = getattr(bigg, type_)()
        assert isinstance(results, list)

        result = results[0]
        assert keys_exists(result,
            ("bigg_id", "model_bigg_id", "name"))

        assert result["model_bigg_id"] == "Universal"

def test_search(bigg):
    with pytest.raises(TypeError):
        bigg.search("foobar", "foobar")
    
    models = bigg.search("e coli", "models")
    assert keys_exists(models[0],
        ("bigg_id", "organism", "metabolite_count", "gene_count",
        "reaction_count"))

    required_keys = ("model_bigg_id", "bigg_id", "name", "organism")

    metabolites = bigg.search("g3p", "metabolites")
    assert keys_exists(metabolites[0], required_keys)

    genes = bigg.search("gap", "genes")
    assert keys_exists(genes[0], required_keys)

    reactions = bigg.search("phosphate", "reactions")
    assert keys_exists(reactions[0], required_keys)

def test_download(bigg):
    with pytest.raises(TypeError):
        bigg.download("iND750", format_="foobar")

    with TempFile() as f:
        bigg.download("iND750", target=f.name)

        assert osp.exists(f.name)

