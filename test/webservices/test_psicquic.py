from bioservices import PSICQUIC, psicquic
import pytest

@pytest.fixture
def psicquic():
    return PSICQUIC(verbose=False)


def test_read_registry(psicquic):
    psicquic.read_registry()

def test_print_status(psicquic):
    psicquic.print_status()

def test_registry(psicquic):
    N1 = len(psicquic.registry_names)
    N2 = len(psicquic.registry_versions)
    N2 = len(psicquic.registry_restricted)
    assert N1 == N2

def test_query(psicquic):
    if 'intact' not in psicquic.activeDBs or 'matrixdb' not in psicquic.activeDBs:
        return

    psicquic.query("intact", "brca2", "tab27")
    psicquic.query("intact", "zap70", "xml25")
    psicquic.query("matrixdb", "*", "xml25")
    try:
        psicquic.query("matxdb", "*", "xml25")
        assert False
    except:
        assert True

    psicquic.query("matrixdb", "*", "xml25", firstResult=10, maxResults=10)

    # accessing the string DB
    if 'string' in psicquic.activeDBs:
        psicquic.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25")

def _test_appsPPI():
    p = psicquic.AppsPPI(verbose=False)
    p.queryAll("ZAP70", ["intact"])
    p.summary()

