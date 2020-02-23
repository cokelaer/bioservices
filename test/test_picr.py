from bioservices.picr import PICR
import pytest

# As of Feb 2020, we cannot find picr service on EBI website anymore.
# Most probably deprecated

"""
@pytest.fixture
def picr():
    return PICR(verbose=True)




def test_getUPIForSequence(picr):
    res = picr.getUPIForSequence(picr._sequence_example,
            ["IPI", "ENSEMBL", "SWISSPROT"])
    res = picr.getUPIForSequence(picr._sequence_example, "SWISSPROT",
            taxid="9606")
    res = picr.getUPIForSequence(picr._sequence_example, "SWISSPROT",
            onlyactive=False, includeattributes=False)

def test_databases(picr):
    assert len(picr.databases) > 0

def test_MappedDB(picr):
    picr.getMappedDatabaseNames()

def test_checkDB(picr):
    picr._checkDBname("IPI")
    try:
        picr._checkDBname("dummy")
        assert False
    except:
        assert True

def test_getUPIForAccession(picr):
    picr.getUPIForAccession(picr._accession_example, ["SWISSPROT"])
    picr.getUPIForAccession(picr._accession_example, "SWISSPROT", taxid="9606")
    res = picr.getUPIForAccession(picr._accession_example, "SWISSPROT", onlyactive=False, includeattributes=False)

# Those ones do not work
def _test_getUPIForBLAST(picr):
    picr.getUPIForBLAST(picr._blastfrag_example, "SWISSPROT", taxid="9606")

def _test_getUPIForBLAST2(picr):
    picr.getUPIForBLAST(picr._blastfrag_example, ["SWISSPROT"], taxid="9606", includeattributes=False)

def _test_getUPIForBLAST3(picr):
    picr.getUPIForBLAST(picr._blastfrag_example, ["SWISSPROT"], taxid="9606", program="blastp",matrix="BLOSUM62")

"""
