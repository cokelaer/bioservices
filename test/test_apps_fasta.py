from bioservices.apps.fasta import *
import tempfile


def test_fasta():
    f = FASTA()
    f.load_fasta(None)
    f.load_fasta("P43403")
    f.load_fasta("P43403") # already there 
    f.header
    f.gene_name
    f.sequence
    f.fasta
    f.identifier
    fh = tempfile.NamedTemporaryFile(delete=False)
    f.save_fasta(fh.name)
    f.read_fasta(fh.name)
    fh.delete = True
    fh.close()


def test_multi_fasta():
    f = MultiFASTA()
    try:
        f.fasta
        assert False
    except:
        assert True
    try:
        f.header
        assert False
    except:
        assert True

    f.load_fasta("P43403")
    f.load_fasta("P43408")
    assert len(f) == 2
    
    f.ids
    f.fasta
    fh = tempfile.NamedTemporaryFile(delete=False)
    f.save_fasta(fh.name)
    f.read_fasta(fh.name)

    f.fasta["P43403"]
    f.hist_size()
    f.df
