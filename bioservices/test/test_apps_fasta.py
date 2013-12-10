from bioservices.apps.fasta import *
import tempfile


def test_fasta():
    f = FASTA()
    f.load_fasta("P43403")
    fasta = f.get_fasta("P43403")
    f.header
    f.gene_name
    f.sequence
    fh = tempfile.NamedTemporaryFile(delete=False)
    f.save_fasta(fasta, fh.name)
    f.read_fasta(fh.name)
    fh.delete = True
    fh.close()


def test_multi_fasta():
    f = MultiFASTA()
    f.load_fasta("P43403")
    f.load_fasta("P43408")
    f.sequences
    f.ids
    f.fasta

    fh = tempfile.NamedTemporaryFile(delete=False)
    f.save_fasta(fh.name)
    f.read_fasta(fh.name)

    f.fasta["P43403"]
