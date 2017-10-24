from bioservices.dbfetch import DBFetch
import pytest

@pytest.fixture
def dbfetch():
    return DBFetch(verbose=False)


def test_getSupportedDBs(dbfetch):
    res = dbfetch.supported_databases
    res = dbfetch.supported_databases
    assert len(res) >10

def test_getSupportedFormats(dbfetch):
    res = dbfetch.get_database_formats("uniprotkb")
    assert "fasta" in res

def test_getSupportedStyles(dbfetch):
    res = dbfetch.get_database_format_styles("uniprotkb", "fasta")
    assert "raw" in res


def test_fetchData(dbfetch):
    res = dbfetch.fetch(style="raw", db="uniprotkb", format="fasta", query="zap70_human")

def test_getDatabaseInfo(dbfetch):
    res = dbfetch.get_database_info("uniprotkb")
    assert res['name'] == 'uniprotkb'

def test_getDatabaseInfoList(dbfetch):
    assert len(dbfetch.get_all_database_info())>10

def test_wrong_db(dbfetch):
    try:
        dbfetch.fetch(db="niprot", query="P43403")
        assert False
    except:
        assert True
