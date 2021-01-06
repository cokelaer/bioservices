from bioservices import Ensembl
import pytest

@pytest.fixture
def ensembl():
    return Ensembl(verbose=False)


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_get_archive(ensembl):
    res = ensembl.get_archive("ENSG00000157764")
    assert 'id' in res.keys()


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_post_archive(ensembl):
    res = ensembl.post_archive(["ENSG00000157764"])
    assert "ENSG00000157764" in [x['id'] for x in res]


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_genetree_by_id(ensembl):
    res = ensembl.get_genetree_by_id("ENSGT00390000003602",
                                    frmt='phyloxml', aligned=False, sequence='cdna')[0:1000]
    assert "taxonomy" in res
    assert "117571" in res
    assert "Euteleos" in res

    ensembl.get_genetree_by_id('ENSGT00390000003602', frmt='nh',
                              nh_format='simple')
    ensembl.get_genetree_by_id('ENSGT00390000003602', frmt='phyloxml')
    ensembl.get_genetree_by_id('ENSGT00390000003602', frmt='phyloxml',
                              aligned=True, sequence='cdna')
    ensembl.get_genetree_by_id('ENSGT00390000003602', frmt='phyloxml',
                              sequence='none')


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_get_genetree_by_member_id(ensembl):
    res = ensembl.get_genetree_by_member_id('ENSG00000157764',
                                           frmt='json', nh_format='phylip')
    assert len(res) > 1000


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_get_genetree_by_member_symbol(ensembl):
    res = ensembl.get_genetree_by_member_symbol('human', 'BRCA2',
                                               nh_format='simple')
    # was working until dec 2014 then results changed. so not stable
    # assert res[0:200] == """((((((((ENSPFOP00000001575:0.046083,ENSXMAP00000006983:0.065551):0.43822,ENSONIP00000006940:0.359035):0.019582,((ENSTRUP00000015030:0.077336,ENSTNIP00000002435:0.099898):0.208834,ENSGACP00000015199:0."""


# FIXME
# feb 2020. does not work even on ensemble website
def __test_get_alignment_by_region(ensembl):
    region = '2:106040000-106040050'
    species = 'taeniopygia_guttata'
    res = ensembl.get_alignment_by_region(region, species,
                                         species_set_group='sauropsids')

    assert 'gallus_gallus' in res[0]['tree']


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_get_homology_by_id(ensembl):
    res = ensembl.get_homology_by_id('ENSG00000157764')
    assert res.keys()
    res = ensembl.get_homology_by_id('ENSG00000157764', frmt='xml')
    res = ensembl.get_homology_by_id('ENSG00000157764', format='condensed',
                                    type='orthologues', target_taxon='10090')
    assert 'homologies' in res['data'][0].keys()


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_references(ensembl):
    # does not work anymore Dev 2018 returns empty list
    #res = ensembl.get_xrefs_by_id('ENST00000288602', external_db='PDB',
    #                             all_levels=True)
    #assert res[0]['dbname'] == 'PDB'
    res = ensembl.get_xrefs_by_id('ENST00000288602')
    assert len(res)

    res = ensembl.get_xrefs_by_name('BRCA2', 'human')
    assert 'db_display_name' in res[0].keys()

    res = ensembl.get_xrefs_by_symbol('BRCA2', 'homo_sapiens',
                                     external_db='HGNC')
    assert 'id' in res[0]


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_info(ensembl):
    assert len(ensembl.get_info_analysis('human')) > 0
    assert len(ensembl.get_info_assembly('human')['karyotype']) == 25

    ensembl.get_info_assembly_by_region('homo_sapiens', 'X')

    assert len(ensembl.get_info_biotypes('human'))

    assert ensembl.get_info_compara_methods()

    assert ensembl.get_info_compara_by_method('EPO')[0]['method'] == 'EPO'

    assert ensembl.get_info_comparas()['comparas']

    assert ensembl.get_info_data()

    res = ensembl.get_info_external_dbs('human')
    assert 'HGNC' in [x['name'] for x in res if 'hgnc' in x['name'].lower()]

    assert ensembl.get_info_ping()
    assert ensembl.get_info_rest()
    assert ensembl.get_info_software()
    res = ensembl.get_info_species()
    assert 'ovis_aries' in [x['name'] for x in res['species'] if 'ovis' in x['name']]


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_lookup(ensembl):
    res = ensembl.get_lookup_by_id('ENSG00000157764', expand=True)


    res = ensembl.post_lookup_by_id(["ENSG00000157764", "ENSG00000248378"],
                                   expand=0)

    res = ensembl.get_lookup_by_symbol('homo_sapiens', 'BRCA2', expand=True)
    assert len(res['Transcript'])

    res = ensembl.post_lookup_by_symbol('human', ["BRCA2", "BRAF"], expand=True)
    assert len(res['BRCA2']['Transcript'])


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_mapping(ensembl):
    res = ensembl.get_map_assembly_one_to_two('GRCh37', 'GRCh38',
                                             region='X:1000000..1000100:1')

    res = ensembl.get_map_translation_to_region('ENSP00000288602', '100..300')
    assert res['mappings'][0]

    res = ensembl.get_map_cds_to_region('ENST00000288602', '1..1000')

    res = ensembl.get_map_cdna_to_region('ENST00000288602', '100..300')


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ontologies(ensembl):
    res = ensembl.get_ontology_ancestors_by_id('GO:0005667')
    res = ensembl.get_ontology_ancestors_chart_by_id('GO:0005667')
    res = ensembl.get_ontology_descendants_by_id('GO:0005667')
    res = ensembl.get_ontology_by_id('GO:0005667')
    assert res['accession']

    res = ensembl.get_ontology_by_name('transcription factor complex')
    res = ensembl.get_taxonomy_classification_by_id(9606)
    assert res[0]['children']
    res = ensembl.get_ontology_by_id('GO:0005667')
    assert 'children' in res.keys()
    res = ensembl.get_ontology_by_name('transcription factor complex')
    assert res[0]['children']
    res = ensembl.get_ontology_by_name('transcription factor')
    assert res


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_taxonomy(ensembl):
    res = ensembl.get_taxonomy_by_name('homo')
    assert len(res[0]) > 1

    res = ensembl.get_taxonomy_classification_by_id('9606')

    res = ensembl.get_taxonomy_by_name('Homo')

    ensembl.get_taxonomy_by_id(9606)['scientific_name']

    res = ensembl.get_overlap_by_id("ENSG00000157764", feature='gene')

    res = ensembl.get_overlap_by_region('7:140424943-140624564',
                                       species='human', feature='gene')

    res = ensembl.get_overlap_by_translation('ENSP00000288602',
                                            type='Superfamily')

    res = ensembl.get_overlap_by_translation('ENSP00000288602',
                                            type='missense_variant',
                                            feature='transcript_variation')

    res = ensembl.get_overlap_by_translation('ENSP00000288602',
                                            type='missense_variant',
                                            feature='somatic_transcript_variation')

def _test_regulation(ensembl):
    res = ensembl.get_regulatory_by_id('ENSR00001348195', 'human')
    assert 'ID' in res[0].keys()


def test_sequences(ensembl):
    sequence = ensembl.get_sequence_by_id('ENSG00000157764', frmt='text')
    #assert sequence.startswith("CGCCTCCCTTCCCCCTCCCCGCCCGACAGCGGCCGCTCGGGCCCCG")
    # changed June 2018. double checked on web site
    # http://www.ensembl.org/Homo_sapiens/Gene/Sequence?g=ENSG00000157764;r=7:140719327-140924928
    # fails on Sep 2002
    #assert sequence.startswith("TTCCCCCAATCCCCTCAGGCTCGGCTGCGCCCGGGGCCGCGGGCCGGTACCTGAGGTGGC")

    #FIXME fails on travis
    #sequence = ensembl.get_sequence_by_id('ENSG00000157764', frmt='fasta')
    #assert sequence.startswith(">ENSG00000157764 chromosome:")

    sequence = ensembl.get_sequence_by_id('CCDS5863.1', frmt='fasta',
                                         object_type='transcript', db_type='otherfeatures',
                                         type='cds', species='human')

    sequence = ensembl.get_sequence_by_id('ENSG00000157764', frmt='seqxml',
                                         multiple_sequences=True, type='protein')
    sequence = ensembl.get_sequence_by_region('X:1000000..1000100:1', 'human')
    assert sequence['id'] == 'chromosome:GRCh38:X:1000000:1000100:1'
    sequence = ensembl.get_sequence_by_region('ABBA01004489.1:1..100', 'human',
                                             frmt='json', coord_system='seqlevel')

    seq = ensembl.get_sequence_by_id('ENSE00001154485', expand_5prime=10,
                                     frmt='fasta', type='genomic')
    assert seq == u'>ENSE00001154485.4 chromosome:GRCh38:7:140924566:140924752:-1\nCCCTCCCCGCCCGACAGCGGCCGCTCGGGCCCCGGCTCTCGGTTATAAGATGGCGGCGCT\nGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGGCTCTGTTCAACGGGGACATGGA\nGCCCGAGGCCGGCGCCGGCGCCGGCGCCGCGGCCTCTTCGGCTGCGGACCCTGCCATTCC\nGGAGGAG\n'
    res = ensembl.get_sequence_by_id('ENSG00000157764', frmt='seqxml',
                                    type='protein', multiple_sequences=1)
    assert 'MAAL' in res

    res = ensembl.get_sequence_by_id('GENSCAN00000000001', frmt='json',
                                    object_type='predictiontranscript', db_type='core',
                                    species='homo_sapiens', type='protein')
    assert 'MERGKK' in res['seq']

    res = ensembl.get_sequence_by_id('ENSP00000288602', frmt='json')
    assert res['seq'].startswith("MAAL")


def test_variation(ensembl):
    res = ensembl.get_variation_by_id('rs56116432', 'human')
    assert 'MAF' in res.keys()
    res = ensembl.get_vep_by_id('COSM476', 'human')
    res = ensembl.get_vep_by_id('rs116035550', 'human')
    # FIXME slow or failures jan 2021
    #res = ensembl.get_vep_by_region('9:22125503-22125502:1', 'C', 'human')
    #assert res[0]['most_severe_consequence']
    #ensembl.get_variation_by_id("rs56116432", species='homo_sapiens')
    #ensembl.get_variation_by_id("rs56116432", species='homo_sapiens',
    #                           pops=1, genotypes=1, phenotypes=1)
