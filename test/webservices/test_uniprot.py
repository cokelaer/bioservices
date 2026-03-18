import pytest

from bioservices.uniprot import UniProt

protein_queries = [
    "Q89B22",
    "P57224",
    "Q89B11",
    "P57601",
    "P25749",
    "P59526",
    "P59491",
    "P57659",
    "P57263",
    "P57337",
    "P57411",
    "Q89A85",
    "P57576",
    "Q89AJ8",
    "P57524",
    "Q89AK2",
    "Q89B42",
    "P57362",
    "P59460",
    "P57559",
    "P57226",
    "P57463",
    "P57529",
    "P57213",
    "P57525",
    "P57230",
    "P12345",
    "D3DT31",
    "P21802",
    "P12345",
]


@pytest.fixture(scope="module")
def uniprot():
    u = UniProt(verbose=False, cache=False)
    u.services.logging.setLevel("ERROR")
    return u


def test_mapping(uniprot):

    assert "KEGG" in uniprot.valid_mapping
    res = uniprot.mapping("UniProtKB_AC-ID", "KEGG", "P43403,P123456")
    res = uniprot.mapping("UniProtKB_AC-ID", "KEGG", ["P43403", "P123456"])
    assert len(res["results"]) == 1
    assert len(res["failedIds"]) == 1

    with pytest.raises(Exception):
        uniprot.mapping("UniProtKB_AC-ID", "KEGGDUMMY", "P43403,P123456")


def test_retrieve(uniprot):

    for frmt in ["txt", "fasta", "gff", "json"]:
        uniprot.retrieve("P09958", frmt=frmt)

    # test input parameters
    assert uniprot.retrieve("P09958", frmt="json") == uniprot.retrieve(["P09958"], frmt="json")

    for frmt in ["txt", "fasta", "gff", "json"]:
        uniprot.retrieve("P09958", frmt=frmt, database="uniref")

    assert uniprot.retrieve("P09958", frmt="json", database="dummy") in [400, 404]


def test_search(uniprot):
    # two strings, or list, or a single string
    uniprot.search("P43403", columns="id", progress=False, limit=1)

    uniprot.search(
        "zap70+and+taxonomy_id:9606",
        frmt="tsv",
        limit=3,
        columns="id,length,accession,gene_names,gene_primary,cc_interaction",
    )

    uniprot.search(
        "zap70+and+taxonomy_id:9606", frmt="tsv", limit=3, columns="accession,go_p,cc_function,cc_domain,lineage"
    )

    uniprot.search("ZAP70_HUMAN", frmt="tsv", columns="sequence", limit=1)

    uniprot.search("+OR+".join(protein_queries), columns="accession,lineage", frmt="tsv", limit=10)


def test_quick_search(uniprot):
    assert len(uniprot.quick_search("ZAP70")) == 1


def test_uniref(uniprot):
    assert "entryType" in uniprot.uniref("Q03063")


def test_get_df(uniprot):
    uniprot.get_df("acc:P43403", limit=10)


def test_fasta(uniprot):
    "Q9Y617" in uniprot.get_fasta(["Q9Y617-1"])


def test_get_next_link(uniprot):
    # header contains a valid next link
    headers = {"Link": '<https://rest.uniprot.org/idmapping/results/job123?cursor=abc>; rel="next"'}
    link = uniprot._get_next_link(headers)
    assert link == "https://rest.uniprot.org/idmapping/results/job123?cursor=abc"

    # no Link header returns None
    assert uniprot._get_next_link({}) is None

    # Link header present but not a next-rel link returns None
    assert uniprot._get_next_link({"Link": '<https://example.com>; rel="prev"'}) is None


# https://github.com/cokelaer/bioservices/issues/245
def test_mapping_regression(uniprot):
    # P123456 is a failed ID
    res = uniprot.mapping("UniProtKB_AC-ID", "KEGG", "P43403,P123456")
    assert res["failedIds"]
    # here no failedId but we expect an empty failedIds in the returned dictionary (empty list)
    res = uniprot.mapping("UniProtKB_AC-ID", "KEGG", "P43403")
    assert res["failedIds"] == []
