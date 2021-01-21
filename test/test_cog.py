from bioservices.cog import COG
import pytest

def test_cog():
    c = COG()
    c.get_cogs()
    c.get_cogs_by_gene("MK0280")
    c.get_cogs_by_id("COG0003")
    c.get_cogs_by_assembly_id("GCA_000007185.1")
    c.get_cogs_by_orgnanism("Nitrosopumilus_maritimus_SCM1")
    c.get_cogs_by_taxon_id("1229908")
    c.get_cogs_by_category("ACTINOBACTERIA")
    c.get_cogs_by_category_id("651137")
    c.get_cogs_by_category_("AJP49128.1")
    c.get_cogs_by_id_and_category("COG0004", "CYANOBACTERIA")
    c.get_cogs_by_id_and_organism("COG0004", "Escherichia_coli_K-12_sub_MG1655")
    c.get_all_cogs_definition()
    c.get_cog_definition_by_cog_id("COG0003")
    c.get_cog_definition_by_name("Thiamin-binding stress-response protein YqgV, UPF0045 family")
    c.get_taxonomic_categories()
    c.get_taxonomic_category_by_name("ALPHAPROTEOBACTERIA")

