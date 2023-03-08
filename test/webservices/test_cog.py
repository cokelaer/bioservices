from bioservices.cog import COG


def test_cog():
    c = COG()
    c.get_cogs(page=2, organism=' Escherichia_coli_K-12_sub_MG1655')


def test_cogs_by_gene():
    c = COG()
    c.get_cogs_by_gene("MK0280", page=1)


def test_cogs_by_id():
    c = COG()
    c.get_cogs_by_id("COG0003", page=1)


def test_cogs_by_assembly_id():
    c = COG()
    c.get_cogs_by_assembly_id("GCA_000007185.1", page=1)


def test_cogs_by_orgamism():
    c = COG()
    c.get_cogs_by_organism("Nitrosopumilus_maritimus_SCM1", page=1)


def test_cogs_by_taxon_id():
    c = COG()
    c.get_cogs_by_taxon_id("1229908", page=1)


def test_cogs_by_category():
    c = COG()
    c.get_cogs_by_category("ACTINOBACTERIA", page=1)


def test_cogs_by_category_id():
    c = COG()
    c.get_cogs_by_category_id("651137", page=1)


def test_cogs_by_protein_name():
    c = COG()
    c.get_cogs_by_protein_name("AJP49128.1", page=1)


def test_cogs_by_id_and_category():
    c = COG()
    c.get_cogs_by_id_and_category("COG0004", "CYANOBACTERIA", page=1)


def test_cogs_by_id_and_organism():
    c = COG()
    c.get_cogs_by_id_and_organism("COG0004", "Escherichia_coli_K-12_sub_MG1655", page=1)


def test_get_all_cogs_definition():
    c = COG()
    c.get_all_cogs_definition(page=1)


def test_cogs_definition_by_cog_id():
    c = COG()
    c.get_cog_definition_by_cog_id("COG0003")


def test_cogs_definition_by_name():
    c = COG()
    c.get_cog_definition_by_name("Thiamin-binding stress-response protein YqgV, UPF0045 family", page=1)


def test_taxomomic_categories():
    c = COG()
    c.get_taxonomic_categories(page=1)


def test_taxonomic_category_by_name():
    c = COG()
    c.get_taxonomic_category_by_name("ALPHAPROTEOBACTERIA", page=1)


def test_search_organism():
    c = COG()
    _ = c.search_organism("coli")

