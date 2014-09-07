from bioservices.apps.fasta import FASTA, MultiFASTA
import tempfile
from nose.plugins.attrib import attr


class test_FASTA(object):
    @classmethod
    def setup_class(klass):
        klass.s = FASTA(verbose=False)

    def test_fasta(self):
        self.s.load_fasta(None)
        self.s.load_fasta("P43403")
        self.s.load_fasta("P43403") # already there 
        self.s.header
        self.s.gene_name
        self.s.sequence
        self.s.fasta
        self.s.identifier
        fh = tempfile.NamedTemporaryFile(delete=False)
        self.s.save_fasta(fh.name)
        self.s.read_fasta(fh.name)
        fh.delete = True
        fh.close()

class test_FASTA(object):
    @classmethod
    def setup_class(klass):
        klass.s = MultiFASTA()

        try:
            klass.s.fasta
            assert False
        except:
            assert True
        try:
            f.header
            assert False
        except:
            assert True

        klass.s.load_fasta("P43403")
        klass.s.load_fasta("P43408")

    def test_attributes(self):
        assert len(self.s) == 2
    
        self.s.ids
        self.s.fasta
        fh = tempfile.NamedTemporaryFile(delete=False)
        self.s.save_fasta(fh.name)
        self.s.read_fasta(fh.name)

        self.s.fasta["P43403"]

    @attr('skip')
    def test_extra(self):

        self.s.hist_size()
        self.s.df
