from bioservices import Ensembl


class test_Ensembl(Ensembl):
                                           
    @classmethod
    def setup_class(klass):
        klass.s = Ensembl(verbose=False)

    def test_get_archive(self):
        res = self.s.get_archive("ENSG00000157764")
        assert 'id' in res.keys()

    def test_post_archive(self):
        res = self.s.post_archive(["ENSG00000157764"])
        assert "ENSG00000157764" in [x['id'] for x in res]
       
    def test_genetree_by_id(self):
        res = self.s.get_genetree_by_id("ENSGT00390000003602", 
                frmt='phyloxml', aligned=False, sequence='cdna')[0:1000]
        assert "taxonomy" in res
        assert "117571" in res
        assert "Euteleos" in res

        self.s.get_genetree_by_id('ENSGT00390000003602', frmt='nh', 
                nh_format='simple')
        self.s.get_genetree_by_id('ENSGT00390000003602', frmt='phyloxml')
        self.s.get_genetree_by_id('ENSGT00390000003602', frmt='phyloxml',
                aligned=True, sequence='cdna')
        self.s.get_genetree_by_id('ENSGT00390000003602', frmt='phyloxml', 
                sequence='none')

    def test_get_genetree_by_member_id(self):
        res = self.s.get_genetree_by_member_id('ENSG00000157764', 
                frmt='json', nh_format='phylip')
        assert len(res)>1000

    def test_get_genetree_by_member_symbol(self):
        res = self.s.get_genetree_by_member_symbol('human', 'BRCA2', 
                                                      nh_format='simple')
        # was working until dec 2014 then results changed. so not stable
        #assert res[0:200] == """((((((((ENSPFOP00000001575:0.046083,ENSXMAP00000006983:0.065551):0.43822,ENSONIP00000006940:0.359035):0.019582,((ENSTRUP00000015030:0.077336,ENSTNIP00000002435:0.099898):0.208834,ENSGACP00000015199:0."""

    def test_get_alignment_by_region(self):
        region = '2:106040000-106040050'
        species = 'taeniopygia_guttata'
        res = self.s.get_alignment_by_region(region, species, 
                                                species_set_group='sauropsids')
        
        assert 'gallus_gallus' in res[0]['tree']



    def test_get_homology_by_id(self):
        res = self.s.get_homology_by_id('ENSG00000157764')
        assert res.keys()
        res = self.s.get_homology_by_id('ENSG00000157764', frmt='xml')
        res = self.s.get_homology_by_id('ENSG00000157764', format='condensed', 
                                  type='orthologues', target_taxon='10090')
        assert 'homologies' in res['data'][0].keys()

    def test_references(self):
        res = self.s.get_xrefs_by_id('ENST00000288602', external_db='PDB', 
                                                    all_levels=True)
        assert res[0]['dbname'] == 'PDB'

        res = self.s.get_xrefs_by_name('BRCA2', 'human')    
        assert 'db_display_name' in res[0].keys()

        res = self.s.get_xrefs_by_symbol('BRCA2', 'homo_sapiens',
                                     external_db='HGNC')    
        assert 'id' in res[0]

    def test_info(self):
        assert len(self.s.get_info_analysis('human')) > 0
        assert len(self.s.get_info_assembly('human')['karyotype']) == 25

        self.s.get_info_assembly_by_region('homo_sapiens', 'X')

        assert len(self.s.get_info_biotypes('human'))

        assert self.s.get_info_compara_methods()

        assert self.s.get_info_compara_by_method('EPO')[0]['method'] == 'EPO'

        assert self.s.get_info_comparas()['comparas']

        assert self.s.get_info_data()

        res = self.s.get_info_external_dbs('human')
        assert len([x['name'] for x in res if 'hgnc' in x['name'].lower()])>=5

        assert self.s.get_info_ping()
        assert self.s.get_info_rest()
        assert self.s.get_info_software()
        res = self.s.get_info_species()
        assert 'ovis_aries' in [x['name'] for x in res['species'] if 'ovis' in x['name']]

    def test_lookup(self):
        res = self.s.get_lookup_by_id('ENSG00000157764', expand=True)
        
        res = self.s.get_lookup_by_id('ENSG00000157764', expand=True)
        assert res.keys()
        
        res = self.s.post_lookup_by_id(["ENSG00000157764", "ENSG00000248378" ], 
                    expand=0)

        res = self.s.get_lookup_by_symbol('homo_sapiens', 'BRCA2', expand=True)
        assert len(res['Transcript'])
   
        res = self.s.post_lookup_by_symbol('human', ["BRCA2", "BRAF" ], expand=True)
        assert len(res['BRCA2']['Transcript'])


    def test_mapping(self):
        res = self.s.get_map_assembly_one_to_two('GRCh37', 'GRCh38', 
                  region='X:1000000..1000100:1')
            
        res = self.s.get_map_translation_to_region('ENSP00000288602', '100..300')
        assert res['mappings'][0]  

        res = self.s.get_map_cds_to_region('ENST00000288602', '1..1000')

        res = self.s.get_map_cdna_to_region('ENST00000288602', '100..300')

    def test_ontologies(self):
        res = self.s.get_ontology_ancestors_by_id('GO:0005667')
        res = self.s.get_ontology_ancestors_chart_by_id('GO:0005667')
        res = self.s.get_ontology_descendants_by_id('GO:0005667')
        res = self.s.get_ontology_by_id('GO:0005667')
        assert res['accession']

        res = self.s.get_ontology_by_name('transcription factor complex')
        res = self.s.get_taxonomy_classification_by_id(9606)
        assert res[0]['children']
        res = self.s.get_ontology_by_id('GO:0005667')
        assert 'children' in res.keys()
        res = self.s.get_ontology_by_name('transcription factor complex')
        assert res[0]['children']
        res = self.s.get_ontology_by_name('transcription factor')
        assert res == 400 # error here


    def test_taxonomy(self):

        res = self.s.get_taxonomy_by_name('homo')
        assert len(res[0])>1

        res = self.s.get_taxonomy_classification_by_id('9606')

        res = self.s.get_taxonomy_by_name('Homo')

        self.s.get_taxonomy_by_id(9606)['scientific_name']

        res = self.s.get_overlap_by_id("ENSG00000157764", feature='gene')

        res = self.s.get_overlap_by_region('7:140424943-140624564', 
            species='human', feature='gene')

        res = self.s.get_overlap_by_translation('ENSP00000288602', 
                type='Superfamily')

        res = self.s.get_overlap_by_translation('ENSP00000288602', 
            type='missense_variant',
            feature='transcript_variation')

        res = self.s.get_overlap_by_translation('ENSP00000288602', 
            type='missense_variant',
            feature='somatic_transcript_variation')

    def test_regulation(self):
        res = self.s.get_regulatory_by_id('ENSR00001348195', 'human')
        assert 'ID' in res[0].keys()
   
    def test_sequences(self):
        sequence = self.s.get_sequence_by_id('ENSG00000157764', frmt='text')
        assert sequence[0:120] == """CGCCTCCCTTCCCCCTCCCCGCCCGACAGCGGCCGCTCGGGCCCCGGCTCTCGGTTATAAGATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGGCTCTGTTCAA"""

        sequence = self.s.get_sequence_by_id('ENSG00000157764', frmt='fasta')
        assert sequence.startswith(">ENSG00000157764 chromosome:")

        sequence = self.s.get_sequence_by_id('CCDS5863.1', frmt='fasta', 
            object_type='transcript', db_type='otherfeatures',
            type='cds', species='human')

        sequence = self.s.get_sequence_by_id('ENSG00000157764', frmt='seqxml',
            multiple_sequences=True,type='protein')
        sequence = self.s.get_sequence_by_region('X:1000000..1000100:1', 'human')
        assert sequence['id'] == 'chromosome:GRCh38:X:1000000:1000100:1'
        sequence = self.s.get_sequence_by_region('ABBA01004489.1:1..100', 'human',
                frmt='json', coord_system='seqlevel')

        seq = self.s.get_sequence_by_id('ENSE00001154485', expand_5prime=10,
                frmt='fasta', type='genomic')
        assert seq == u'>ENSE00001154485 chromosome:GRCh38:7:140924566:140924774:-1\nCCCAGCTCTCCGCCTCCCTTCCCCCTCCCCGCCCGACAGCGGCCGCTCGGGCCCCGGCTC\nTCGGTTATAAGATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGG\nCTCTGTTCAACGGGGACATGGAGCCCGAGGCCGGCGCCGGCGCCGGCGCCGCGGCCTCTT\nCGGCTGCGGACCCTGCCATTCCGGAGGAG\n'

        res = self.s.get_sequence_by_id('ENSG00000157764', frmt='seqxml', 
                type='protein', multiple_sequences=1)
        assert 'XSTT' in res 

        res = self.s.get_sequence_by_id('GENSCAN00000000001', frmt='json', 
                object_type='predictiontranscript', db_type='core', 
                species='homo_sapiens', type='protein')
        assert 'MERGKK' in res['seq']

        res = self.s.get_sequence_by_id('ENSP00000288602', frmt='json')
        assert res['seq'].startswith("MAAL")
    
    def test_variation(self):
        res = self.s.get_variation_by_id('rs56116432', 'human')
        assert 'MAF' in res.keys()
        res = self.s.get_vep_by_id('COSM476', 'human')
        res = self.s.get_vep_by_id('rs116035550', 'human')
        res = self.s.get_vep_by_region('9:22125503-22125502:1', 'C', 'human')
        assert res[0]['most_severe_consequence']

        self.s.get_variation_by_id("rs56116432", species='homo_sapiens')
        self.s.get_variation_by_id("rs56116432", species='homo_sapiens', 
                pops=1, genotypes=1, phenotypes=1)




a = test_Ensembl()
a.setup_class()
a.test_get_alignment_by_region()
