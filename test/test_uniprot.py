from bioservices.uniprot import UniProt
import pytest

@pytest.fixture
def uniprot():
    u = UniProt(verbose=False, cache=False)
    u.logging.level = "ERROR"
    return u


def test_mapping(uniprot):
    res = uniprot.mapping(fr="ACC+ID", to="KEGG_ID", query='P43403')
    assert res['P43403'] == ['hsa:7535']
    try:
        res = uniprot.mapping(fr="AC", to="KEID", query='P434')
        assert False
    except:
        assert True


def test_retrieve(uniprot):
    uniprot.retrieve("P09958", frmt="rdf")
    uniprot.retrieve("P09958", frmt="xml")
    uniprot.retrieve("P09958", frmt="txt")
    uniprot.retrieve("P09958", frmt="fasta")
    uniprot.retrieve("P09958", frmt="gff")
    try:
        uniprot.retrieve("P09958", frmt="dummy")
        assert False
    except:
        assert True

def test_search(uniprot):
    uniprot.search('zap70+AND+organism:9606', frmt='list')
    uniprot.search("zap70+and+taxonomy:9606", frmt="tab", limit=3,
                columns="entry name,length,id, genes, genes(PREFERRED), interpro, interactor")
    uniprot.search("zap70+and+taxonomy:9606", frmt="tab", limit=3,
                columns="entry name, go(biological process), comment(FUNCTION), comment(DOMAIN), lineage(all)")
    uniprot.search("ZAP70_HUMAN", frmt="tab", columns="sequence", limit=1)
    uniprot.quick_search("ZAP70")

def test_uniref(uniprot):
    df = uniprot.uniref("member:Q03063")
    df.Size

def test_get_df(uniprot):
    df = uniprot.get_df(["P43403"])

def test_fasta(uniprot):
    "Q9Y617" in uniprot.get_fasta(["Q9Y617-1"])
    "Q9Y617" not in uniprot.get_fasta_sequence(["Q9Y617-1"])
