from bioservices.wsdbfetch import WSDbfetch
import pytest

@pytest.fixture
def dbfetch():
    return WSDbfetch(verbose=False)


def test_getSupportedDBs(dbfetch):
    res = dbfetch.getSupportedDBs()
    res = dbfetch.getSupportedDBs()
    assert len(res) >10

def test_getSupportedFormats(dbfetch):
    res = dbfetch.getSupportedFormats()
    res = dbfetch.getSupportedFormats()
    assert len(res) >10

def test_getSupportedStyles(dbfetch):
    res = dbfetch.getSupportedStyles()
    res = dbfetch.getSupportedStyles()
    assert len(res) >10

def test_fetchBatch(dbfetch):
    dbfetch.fetchBatch("uniprot" ,"wap_mouse", "xml") 

def test_fetchData(dbfetch):
    dbfetch.fetchData('uniprot:zap70_human')

def test_getDatabaseInfo(dbfetch):
    res = dbfetch.getDatabaseInfo("uniprotkb")
    assert res.displayName == 'UniProtKB'

def test_getDatabaseInfoList(dbfetch):
    assert len(dbfetch.getDatabaseInfoList())>10

def test_getDatavaseInfoList(dbfetch):
    dbfetch.getDatabaseInfoList()

def test_getDbFormats(dbfetch):
    dbfetch.getDbFormats("uniprotkb")

def test_getFormat(dbfetch):
    assert len(dbfetch.getFormatStyles("uniprotkb", "fasta")) >= 3
    #['default', 'raw', 'html']

def test_wrong_db(dbfetch):
    try:
        dbfetch.getDbFormats("uniprot")
        assert False
    except:
        assert True
