from bioservices.geneprof import GeneProf
from nose.plugins.attrib import attr


def test_geneprof():
    g = GeneProf(verbose=False)
    #res = g.get_list_experiments(with_outputs=True)
    res = g.get_list_experiments(with_outputs=False)
    len(res)>0
    res = g.get_metadata_experiment("3")

    g.get_metadata_experiment(Id="385", with_workflow=True)
    g.get_metadata_dataset("11_12_122_1", with_ats=True)


@attr('slow')
def test_1():
    g = GeneProf(verbose=False)
    g.get_list_reference_datasets()

    g.get_list_experiment_samples("mouse")
    g.get_list_experiment_samples("human", frmt="txt")
    g.get_list_experiment_samples("human", frmt="rdata")

    g.search_genes("sox2")
    g.search_genes("sox2", taxons="9606")
    g.search_genes("sox2", taxons="9606, 10090")
    res = g.search_genes("brca2 AND cancer AND reference", taxons="mouse")

@attr('slow')
def test_2():
    g = GeneProf(verbose=False)
    g.search_experiments("sox2")
    g.search_experiments("citation:cancer")
    g.search_experiments("citation:'stem cell'")
    g.search_datasets('sox2')
    g.search_datasets('gene expression')
    g.search_datasets("datatype:GENOMIC_REGIONS AND sox2")
    g.search_samples("ChIP")
    g.search_samples("Gene:sox2")
    g.search_samples("human")

@attr('slow')
def test_3():
    g = GeneProf(verbose=False)
    g.get_gene_id("mouse", "C_ENSG", "ENSMUSG00000059552")
    g.get_gene_id("human", "C_RSEQ", "NM_005657")
    g.get_gene_id("human", "any", "NM_005657")
    g.get_external_gene_id("mouse","715", "C_ENSG")
    g.get_external_gene_id("mouse","2981", "C_RSEQ")
    g.get_external_gene_id("mouse","2981", "C_NAME")
    g.get_list_idtypes("mouse")
    g.get_list_idtypes("human")
    g.get_gene_expression("mouse", "715", with_sample_info=True)
    g.get_gene_expression("mouse", "715", output="RAW")
    g.get_gene_expression("mouse", "715", frmt="txt", with_sample_info=True)
    g.get_gene_expression("mouse", "715", frmt="rdata", with_sample_info=True)
   

@attr('slow')
def test_gettargets():
    g = GeneProf(verbose=False)
    g.get_targets_tf("mouse", "9885")
    g.get_targets_tf("human", "36958", include_unbound=True)
    g.get_targets_tf("mouse", "14899", ats="C_NAME,C_ENSG")
    g.get_targets_tf("human", "36958", frmt="rdata")
    g.get_targets_by_experiment_sample("mouse", "541")
    g.get_targets_by_experiment_sample("human", "784", include_unbound=True)
    g.get_targets_by_experiment_sample("mouse", "541", ats="C_NAME,C_ENSG")
    g.get_targets_by_experiment_sample("human", "784", frmt="rdata")


@attr('slow')
def test_get_tfas():
    g = GeneProf(verbose=False)
    g.get_tfas_by_gene("mouse", "9885")
    g.get_tfas_by_gene("human", "36958", frmt="xml",
                    include_unbound=True)
    g.get_tfas_by_gene("mouse", "14899", frmt="txt", 
                    ats="C_NAME,C_ENSG")
    g.get_tfas_by_gene("human", "36958", frmt="rdata")

    g.get_tfas_by_sample("mouse", 541)
    g.get_tfas_by_sample("human", "784", frmt="xml",
                    include_unbound=True)
    g.get_tfas_by_sample("mouse", "541", frmt="txt", 
                ats="C_NAME,C_ENSG")
    g.get_tfas_by_sample("human", "784")


@attr('slow')
def test_get_tf():
    g = GeneProf(verbose=False)
    g.get_tf_by_target_gene("mouse", "715", with_sample_info=True)
    g.get_tf_by_target_gene("mouse", "715", frmt="xml",
                    with_sample_info=True)
    g.get_tf_by_target_gene("mouse", "715", frmt="txt")
    g.get_tf_by_target_gene("mouse", "715", frmt="rdata", 
                    with_sample_info=True)

    g.get_tfas_scores_by_target("mouse", "715", with_sample_info=True)
    g.get_tfas_scores_by_target("mouse", 715, with_sample_info=True)
    g.get_tfas_scores_by_target("mouse", 715, frmt="txt")
    g.get_tfas_scores_by_target("mouse", "715", frmt="rdata",
                with_sample_info=True)

@attr('slow')
def test_data():
    g = GeneProf(verbose=False)
    g.get_data("11_119_18_1", frmt="txt", gz=True)
    g.get_data("11_119_18_1", frmt="txt", gz=True, 
         ats="C_ENSG,C_11_119_16_1_RPKM0,C_11_119_16_1_RPKM1,C_11_119_16_1_RPKM2,C_11_119_16_1_RPKM3")

    g.get_chromosome_names("pub_mm_ens58_ncbim37", frmt="txt")
    g.get_chromosome_names("pub_hs_ens59_grch37", frmt="json")
    g.get_chromosome_names("11_3_7_2", frmt="xml")

    g.get_bed_files("11_3_7_2")
    g.get_bed_files("11_3_7_2", chromosome="3-chr3")
    g.get_bed_files("zebrafish", with_track_description=False)
    g.get_bed_files("11_12_125_2", filter_column="C_11_12_125_2_14_TFBS")
    g.get_wig_files("11_58_16_2")
    g.get_wig_files("11_12_112_2", with_track_description=False,
                only_distinct=True, frag_length=200)
    
    g.get_fasta("11_385_6_1")
    g.get_fastq("11_385_6_1")

