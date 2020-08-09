from bioservices.apps.fasta import FASTA, MultiFASTA
import tempfile
import pytest

@pytest.mark.flaky
def test_fasta():
    fasta = FASTA()
    fasta.load_fasta(None)
    fasta.load_fasta("P43403")
    fasta.load_fasta("P43403") # already there 
    fasta.header
    fasta.gene_name
    fasta.sequence
    fasta.fasta
    fasta.identifier
    fh = tempfile.NamedTemporaryFile(delete=False)
    fasta.save_fasta(fh.name)
    fasta.read_fasta(fh.name)
    fh.delete = True
    fh.close()

@pytest.mark.flaky
def test_multi_fasta():
    klass = MultiFASTA()

    try:
        klass.fasta
        assert False
    except:
        assert True
    try:
        f.header
        assert False
    except:
        assert True

    klass.load_fasta("P43403")
    klass.load_fasta("P43408")

    assert len(klass) == 2

    klass.ids
    klass.fasta
    fh = tempfile.NamedTemporaryFile(delete=False)
    klass.save_fasta(fh.name)
    klass.read_fasta(fh.name)

    klass.fasta["P43403"]

