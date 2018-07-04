from bioservices import KEGG, KEGGParser
import pytest


@pytest.fixture
def kegg():
    k = KEGG()
    k.organismIds
    k.organism = "hsa"
    return k


# This is a simple test class that do not test everything on purpose.
# The other class could be use to test the code more thoroughly but it takes several
# minutes so during development this one should be used instead.
# class TestKEGGAll should serve as a complement to this class

def test_isOrganism(kegg):
    assert kegg.isOrganism('T01440') == True
    assert kegg.isOrganism('hsa') == True
    assert kegg.isOrganism('dummy') == False

def test_database_IDs(kegg):
    kegg.pathwayIds

def test_conv(kegg):
    kegg.conv("ncbi-gi","hsa:10458+ece:Z5100")

def test_info(kegg):
    kegg.dbinfo("kegg")
    kegg.dbinfo("brite")

def test_list(kegg):
    kegg.list("pathway", "hsa")      # returns the list of human pathways

def test_find(kegg):
    kegg.find("compound", "300-310", "mol_weight")

def test_get(kegg):
    kegg.get("cpd:C01290+gl:G00092")

def test_checkDB(kegg):
    for this in ["info", "list", "find", "link"]:
        try:
            kegg._checkDB("dummy", this)
            assert False
        except:
            assert True
        kegg._checkDB("pathway", this)

def test_link(kegg):
    kegg.link("pathway", "hsa:10458+ece:Z5100")

def test_org_conv(kegg):
    assert 'hsa' == kegg.Tnumber2code("T01001")
    assert 'T01001' == kegg.code2Tnumber("hsa")

def test_parse_kgml_pathway(kegg):
    res = kegg.parse_kgml_pathway("hsa04660")

def test_get_pathway_by_gene(kegg):
    res = kegg.get_pathway_by_gene("7535", "hsa")
    assert isinstance(res, dict) is True
    assert 'hsa04064' in res.keys()

def test_ids(kegg):
    assert kegg.enzymeIds[0].startswith("ec")
    assert kegg.compoundIds[0].startswith("cpd")
    assert kegg.glycanIds[0].startswith("gl")
    assert kegg.reactionIds[0].startswith("rn")
    assert kegg.drugIds[0].startswith("dr")
    assert kegg.koIds[0].startswith("ko")
    assert kegg.briteIds[0].startswith("br")


def test_lookfor(kegg):
    kegg.lookfor_organism("human")
    kegg.lookfor_pathway("cell")

def test_organism(kegg):
    kegg.organism = "hsa"
    try:
        kegg.organism = "dummy"
        assert False
    except:
        assert True

def test_pathwayIDs(kegg):
    kegg.organism = "hsa"
    kegg.pathwayIds

def test_info(kegg):
    kegg.dbinfo("hsa")
    try:
        kegg.dbinfo("dummy")
        assert False
    except:
        assert True

def test_list(kegg):
    kegg.list("pathway") # returns the list of reference pathways
    kegg.list("organism") # returns the list of KEGG organisms with taxonomic classification
    kegg.list("hsa") # returns the entire list of human genes
    kegg.list("T01001") # same as above
    kegg.list("hsa:10458+ece:Z5100") # returns the list of a human gene and an E.coli O157 gene
    kegg.list("cpd:C01290+gl:G00092") # returns the list of a compound entry and a glycan entry
    kegg.list("C01290+G00092") # same as above

    # invalid queries:
    try:
        kegg.list("drug", "hsa")
        assert False
    except:
        assert True

    try:
        kegg.list("dumy")
        assert False
    except:
        assert True

def test_find(kegg):
    kegg.find("genes", "shiga+toxin") # for keywords "shiga" and "toxin"
    kegg.find("genes", "shiga toxin") # for keywords "shigatoxin"
    kegg.find("compound", "C7H10O5", "formula") # for chemicalformula "C7H10O5"
    kegg.find("compound", "O5C7","formula") # for chemicalformula containing "O5" and "C7"
    kegg.find("compound", "174.05","exact_mass") # for 174.045 =<exact mass < 174.055
    kegg.find("compound", "300-310","mol_weight") # for 300 =<molecular weight =< 310

def test_get(kegg):
    kegg.get("C01290+G00092")
    kegg.get("hsa:10458+ece:Z5100")
    kegg.get("hsa:10458+ece:Z5100", "aaseq")
    res = kegg.get("hsa05130", "image")
    try:
        kegg.get("hsa05130", "imagffe")
        assert False
    except:
        assert True

def test_conv(kegg):
    kegg.conv("ncbi-gi","hsa:10458+ece:Z5100")

    try:
        kegg.conv("unipro", "hsa")
        assert False
    except:
        assert True

    try:
        kegg.conv("uniprot", "hs")
        assert False
    except:
        assert True

    try:
        kegg.conv("hs", "unipro")
        assert False
    except:
        assert True

    try:
        kegg.conv("hsa", "unipr")
        assert False
    except:
        assert True

    # asc contains 1500. Try to get even samller to spped up tests.
    #kegg.conv("asc", "uniprot")
    kegg.conv("hsa","up:Q9BV86+")


def test_show_module(kegg):
    kegg.show_module("md:hsa_M00402")


def test_show_pathway(kegg):
    kegg.show_entry("path:hsa05416")
    kegg.show_pathway("path:hsa05416", scale=50)


def pathway2sif(kegg):
    sif = kegg.pathway2sif("path:hsa05416")


def test_KEGGParser(kegg):
    s = kegg
    d = s.parse(s.get("cpd:C00001"))
    d = s.parse(s.get("ds:H00001"))
    d = s.parse(s.get("dr:D00001"))
    d = s.parse(s.get("ev:E00001"))
    d = s.parse(s.get("ec:1.1.1.1"))
    d = s.parse(s.get("hsa:1525"))
    d = s.parse(s.get("genome:T00001"))
    d = s.parse(s.get("gl:G00001"))
    d = s.parse(s.get("md:hsa_M00554"))
    d = s.parse(s.get("ko:K00001"))
    d = s.parse(s.get("path:hsa04914"))
    d = s.parse(s.get("rc:RC00001"))
    d = s.parse(s.get("rn:R00001"))
    d = s.parse(s.get("rp:RP00001"))


    d = s.parse(s.get('C15682'))
    assert d['SEQUENCE'][0]['TYPE'] == 'PK'
    assert d['SEQUENCE'][0]['GENE'] =="0-2 mycAI [UP:Q83WF0]; 3 mycAII [UP:Q83WE9]; 4-5 mycAIII [UP:Q83WE8]; 6 mycAIV [UP:Q83WE7]; 7 mycAV [UP:Q83WE6]"
    assert d['SEQUENCE'][0]['ORGANISM'] == "Micromonospora griseorubida"


    #issue #79

    d = s.parse(s.get("C00395"))
    assert d["SEQUENCE"][0]["GENE"] == '[1] 0-2 pcbAB [UP:P19787] [2] 0-2 pcbAB [UP:P27742]'
    assert d["SEQUENCE"][0]["ORGANISM"] == '[1] Penicillium chrysogenum [2] Emericella nidulans (Aspergillus nidulans [GN:ani] )'
    assert d['SEQUENCE'][0]['SEQUENCE'] == '0 Aad  1 Cys  2 Val'
    assert d['SEQUENCE'][0]['TYPE'] == "NRP"
























