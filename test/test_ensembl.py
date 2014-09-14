from bioservices import Ensembl



class test_Ensembl(Ensembl):
                                           
    @classmethod
    def setup_class(klass):
        klass.s = Ensembl(verbose=False)

    def test_genetree(self):
        res = self.s.get_genetree("ENSGT00390000003602", frmt='phyloxml', aligned=False, sequence='cdna')[0:1000]
        assert "taxonomy" in res
        assert "117571" in res
        assert "Euteleos" in res

        self.s.get_genetree('ENSGT00390000003602', frmt='nh', nh_format='simple')
        self.s.get_genetree('ENSGT00390000003602', frmt='phyloxml')
        self.s.get_genetree('ENSGT00390000003602', frmt='phyloxml',aligned=True, sequence='cdna')
        self.s.get_genetree('ENSGT00390000003602', frmt='phyloxml', sequence='none')

    def test_get_sequence(self):

        seq = self.s.get_sequence('ENSE00001154485', expand_5prime=10,frmt='fasta', type='genomic')
        assert seq == u'>ENSE00001154485 chromosome:GRCh38:7:140924566:140924774:-1\nCCCAGCTCTCCGCCTCCCTTCCCCCTCCCCGCCCGACAGCGGCCGCTCGGGCCCCGGCTC\nTCGGTTATAAGATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGG\nCTCTGTTCAACGGGGACATGGAGCCCGAGGCCGGCGCCGGCGCCGGCGCCGCGGCCTCTT\nCGGCTGCGGACCCTGCCATTCCGGAGGAG\n'

        res = self.s.get_sequence('ENSG00000157764', frmt='seqxml', type='protein', multiple_sequences=1)
        assert 'XSTT' in res 

        res = self.s.get_sequence('GENSCAN00000000001', frmt='json', object_type='predictiontranscript', db_type='core', species='homo_sapiens', type='protein')
        assert 'MERGKK' in res['seq']

        res = self.s.get_sequence('ENSP00000288602', frmt='json')
        assert res['seq'].startswith("MAAL")

    def test_variation(self):
        res = self.s.get_variation("rs56116432", species='homo_sapiens')
        assert res['MAF'] ==  u'0.00367309'
        res = self.s.get_variation("rs56116432", species='homo_sapiens', pops=1, genotypes=1, phenotypes=1)
        assert res['MAF'] ==  u'0.00367309'
        assert 'populations' in res.keys()
        assert 'genotypes' in res.keys()
        assert 'phenotypes' in res.keys()

    def test_taxonomy(self):
        res = self.s.get_taxonomy('Homo sapiens', simple=True)
        assert res['id'] == '9606'

    def test_taxonomy_name(self):
        res =self.s.get_taxonomy_name('homo')
        assert len(res[0])>1

    def test_get_archive(self):
        res = self.s.get_archive("ENSG00000157764")
        assert 'id' in res.keys()
    
    def test_get_taxonomy_classification(self):
        res = self.s.get_taxonomy_classification('9606')

    def test_get_ontology(self):
        res = self.s.get_ontology('GO:0005667')
        assert 'children' in res.keys()

    def test_get_ontology_name(self):
        res = e.get_ontology_name('transcription factor complex')
        assert res[0]['children']
        res = e.get_ontology_name('transcription factor')
        assert res == 400 # error here

