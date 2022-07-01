from bioservices.uniprot import UniProt
import pytest

@pytest.fixture
def uniprot():
    u = UniProt(verbose=False, cache=False)
    u.services.logging.setLevel("ERROR")
    return u


def test_mapping(uniprot):

    assert "KEGG" in uniprot.valid_mapping
    res = uniprot.mapping("UniProtKB_AC-ID", "KEGG", "P43403,P123456")
    res = uniprot.mapping("UniProtKB_AC-ID", "KEGG", ["P43403","P123456"])
    assert len(res['results']) == 1
    assert len(res['failedIds']) == 1
    
    try:
        res = uniprot.mapping("UniProtKB_AC-ID", "KEGGDUMMY", "P43403,P123456")
        assert False
    except:
        assert True


def test_retrieve(uniprot):

    for frmt in ['rdf', 'xml', 'txt', 'fasta', 'gff', 'json']:
        uniprot.retrieve("P09958", frmt=frmt)

    # test input parameters
    assert uniprot.retrieve("P09958", frmt='json') == uniprot.retrieve(['P09958'], frmt='json')

    for frmt in ['rdf', 'xml', 'txt', 'fasta', 'gff', 'json']:
        uniprot.retrieve("P09958", frmt=frmt, database='uniref')

    assert uniprot.retrieve("P09958", frmt='json', database='dummy') in [400, 404]


def test_search(uniprot):
    # two strings, or list, or a single string
    uniprot.search("P43403", columns="id")
        

    uniprot.search('zap70+AND+organism:9606', frmt='list')
    uniprot.search("zap70+and+taxonomy:9606", frmt="tsv", limit=3,
                columns="entry name,length,id, genes, genes(PREFERRED), interpro, interactor")
    uniprot.search("zap70+and+taxonomy:9606", frmt="tsv", limit=3,
                columns="entry name, go(biological process), comment(FUNCTION), comment(DOMAIN), lineage(all)")
    uniprot.search("ZAP70_HUMAN", frmt="tsv", columns="sequence", limit=1)

def test_quick_search(uniprot):
    uniprot.quick_search("ZAP70")
    uniprot.quick_search("ZAP70","ZAP70")

def test_uniref(uniprot):
    assert 'goTerms' in uniprot.uniref("Q03063")

def test_get_df(uniprot):
    df = uniprot.get_df(["P43403"])

def test_fasta(uniprot):
    "Q9Y617" in uniprot.get_fasta(["Q9Y617-1"])
