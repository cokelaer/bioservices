from bioservices.geneprof import GeneProf



def test_geneprof():
    g = GeneProf(verbose=False)
    res = g.list_experiments(with_outputs=True)
    len(res)>0
    res = g.metadata_experiment("3")

    g.metadata(Id="385", with_workflow=True)
    g.metadata_dataset("11_12_122_1", with_ats=True)

def test_1():
    g = GeneProf(verbose=False)
    g.list_datasets()

    g.list_samples("mouse")
    g.list_samples("human.txt")
    g.list_samples("human.rdata")

    g.search_genes("sox2")['total_results']
    g.search_genes("sox2", taxons="9606")['total_results']
    g.search_genes("sox2", taxons="9606, 10090")['total_results']
    res = g.search_genes("brca2 AND cancer AND reference", taxons="mouse")
def test_2():
    g = GeneProf(verbose=False)
    g.search_experiment("sox2")
    g.search_experiment("citation:cancer")
    g.search_experiment("citation:'stem cell'")
    g.search_datasets('sox2')
    g.search_datasets('gene expression')
    g.search_datasets("datatype:GENOMIC_REGIONS AND sox2")
    g.search_samples("ChIP")
    g.search_samples("Gene:sox2")
    g.search_samples("human")

def test_3():
    g = GeneProf(verbose=False)
    g.get_gene_id("mouse", "C_ENSG", "ENSMUSG00000059552")
    g.get_gene_id("human", "C_RSEQ", "NM_005657")
    g.get_gene_id("human", "any", "NM_005657")
    g.get_external_gene_id("mouse","715", "C_ENSG")
    g.get_external_gene_id("mouse","2981", "C_RSEQ")
    g.get_external_gene_id("mouse","2981", "C_NAME")
    g.get_idtypes("mouse")
    g.get_idtypes("human")
    g.get_expression("mouse", "715", with_sample_info=True)
    g.get_expression("mouse", "715", type="RAW")
    g.get_expression("mouse", "715", format="txt", with_sample_info=True)
    g.get_expression("mouse", "715", format="rdata", with_sample_info=True)
    
