import pytest

from bioservices import KEGG, KEGGParser


@pytest.fixture(scope="module")
def kegg():
    k = KEGG()
    k.organismIds
    k.organism = "hsa"
    return k


@pytest.fixture(params=[None, "", 0, 400, {}])
def parse_input(request):
    yield request.param


# This is a simple test class that do not test everything on purpose.
# The other class could be use to test the code more thoroughly but it takes several
# minutes so during development this one should be used instead.
# class TestKEGGAll should serve as a complement to this class


def test_get_pathway_by_gene(kegg):
    res = kegg.get_pathway_by_gene("7535", "hsa")
    assert isinstance(res, dict) is True
    assert "hsa04064" in res.keys()


def test_isOrganism(kegg):
    assert kegg.isOrganism("T01440") == True
    assert kegg.isOrganism("hsa") == True
    assert kegg.isOrganism("dummy") == False


def test_database_IDs(kegg):
    kegg.pathwayIds


def test_conv(kegg):
    kegg.conv("ncbi-gi", "hsa:10458+ece:Z5100")


def test_info(kegg):
    kegg.dbinfo("kegg")
    kegg.dbinfo("brite")


def test_list(kegg):
    kegg.list("pathway", "hsa")  # returns the list of human pathways


def test_find(kegg):
    kegg.find("compound", "300-310", "mol_weight")


def test_get(kegg):
    kegg.get("cpd:C01290+gl:G00092")


def test_checkDB(kegg):
    for this in ["info", "list", "find", "link"]:
        with pytest.raises(Exception):
            kegg._checkDB("dummy", this)
        kegg._checkDB("pathway", this)


def test_link(kegg):
    kegg.link("pathway", "hsa:10458+ece:Z5100")


def test_org_conv(kegg):
    assert "hsa" == kegg.Tnumber2code("T01001")
    assert "T01001" == kegg.code2Tnumber("hsa")


def test_parse_kgml_pathway(kegg):
    kegg.parse_kgml_pathway("hsa04660")


# Minimal KGML XML shared fixture used for offline unit tests below
_SHARED_KGML_FIXTURE = b"""<?xml version="1.0"?>
<pathway name="hsa99999" org="hsa" number="99999" title="Test pathway"
         image="https://www.kegg.jp/tmp/kgml.png"
         link="https://www.kegg.jp/pathway/hsa99999">
  <entry id="1" name="hsa:7535" type="gene"
         link="https://www.kegg.jp/dbget-bin/www_bget?hsa:7535">
    <graphics name="ZAP70" fgcolor="#000000" bgcolor="#BFFFBF"
              type="rectangle" x="271" y="200" width="46" height="17"/>
  </entry>
  <entry id="2" name="hsa:916" type="gene"
         link="https://www.kegg.jp/dbget-bin/www_bget?hsa:916">
    <graphics name="CD3D" fgcolor="#000000" bgcolor="#BFFFBF"
              type="rectangle" x="171" y="200" width="46" height="17"/>
  </entry>
  <entry id="3" name="path:hsa04010" type="map"
         link="https://www.kegg.jp/dbget-bin/www_bget?hsa04010">
    <graphics name="MAPK signaling pathway" fgcolor="#000000" bgcolor="#ffffff"
              type="roundrectangle" x="500" y="300" width="134" height="25"/>
  </entry>
  <entry id="4" name="hsa:group1" type="group">
    <component id="1"/>
    <component id="2"/>
  </entry>
  <relation entry1="1" entry2="2" type="PPrel">
    <subtype name="binding/association" value="---"/>
  </relation>
  <relation entry1="1" entry2="3" type="maplink">
  </relation>
</pathway>"""


def test_parse_kgml_pathway_entry_without_graphics():
    """Entries lacking a <graphics> child must not raise AttributeError."""
    from bioservices import KEGG

    k = KEGG(verbose=False)
    res = k.parse_kgml_pathway("hsa99999", res=_SHARED_KGML_FIXTURE)
    # entry id="4" (type="group") has no <graphics> element
    group_entries = [e for e in res["entries"] if e["type"] == "group"]
    assert len(group_entries) == 1
    assert group_entries[0]["gene_names"] is None


def test_parse_kgml_pathway_relation_without_subtype():
    """Relations without <subtype> children must be included with name/value=None."""
    from bioservices import KEGG

    k = KEGG(verbose=False)
    res = k.parse_kgml_pathway("hsa99999", res=_SHARED_KGML_FIXTURE)
    # The maplink relation has no subtype
    maplink_rels = [r for r in res["relations"] if r["link"] == "maplink"]
    assert len(maplink_rels) == 1
    assert maplink_rels[0]["name"] is None
    assert maplink_rels[0]["value"] is None
    assert maplink_rels[0]["entry1"] == "1"
    assert maplink_rels[0]["entry2"] == "3"


def test_parse_kgml_pathway_relation_name_field():
    """The 'name' field of a relation must match the subtype name attribute."""
    from bioservices import KEGG

    k = KEGG(verbose=False)
    res = k.parse_kgml_pathway("hsa99999", res=_SHARED_KGML_FIXTURE)
    pprel_rels = [r for r in res["relations"] if r["link"] == "PPrel"]
    assert len(pprel_rels) == 1
    assert pprel_rels[0]["name"] == "binding/association"
    assert pprel_rels[0]["value"] == "---"


def test_parse_kgml_pathway_sub_pathways():
    """Entries with type='map' represent sub-pathway links and must be returned."""
    from bioservices import KEGG

    k = KEGG(verbose=False)
    res = k.parse_kgml_pathway("hsa99999", res=_SHARED_KGML_FIXTURE)
    sub_pathways = [e for e in res["entries"] if e["type"] == "map"]
    assert len(sub_pathways) == 1
    assert sub_pathways[0]["name"] == "path:hsa04010"


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids1(kegg):
    assert kegg.enzymeIds[0].startswith("1.")


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids2(kegg):
    assert kegg.compoundIds[0].startswith("C")


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids3(kegg):
    assert kegg.glycanIds[0].startswith("G")


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids4(kegg):
    assert kegg.reactionIds[0].startswith("R")


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids5(kegg):
    assert kegg.drugIds[0].startswith("D")


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids6(kegg):
    assert kegg.koIds[0].startswith("K")


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_ids7(kegg):
    assert kegg.briteIds[0].startswith("br")


def test_lookfor(kegg):
    kegg.lookfor_organism("human")
    kegg.lookfor_pathway("cell")


def test_organism(kegg):
    kegg.organism = "hsa"
    with pytest.raises(Exception):
        kegg.organism = "dummy"


def test_pathwayIDs(kegg):
    kegg.organism = "hsa"
    kegg.pathwayIds


def test_info(kegg):
    kegg.dbinfo("hsa")
    with pytest.raises(Exception):
        kegg.dbinfo("dummy")


def test_list_pathway(kegg):
    kegg.list("pathway")  # returns the list of reference pathways


def test_list_org(kegg):
    kegg.list("organism")  # returns the list of KEGG organisms with taxonomic classification


def test_list(kegg):
    kegg.list("T01001")  # same as above
    kegg.list("hsa:10458+ece:Z5100")  # returns the list of a human gene and an E.coli O157 gene
    kegg.list("cpd:C01290+gl:G00092")  # returns the list of a compound entry and a glycan entry
    kegg.list("C01290+G00092")  # same as above

    # invalid queries: organism set but query is not pathway/module → raises
    with pytest.raises(Exception):
        kegg.list("drug", "hsa")

    # unknown database → KEGG returns an HTTP error code
    res = kegg.list("dumy")
    assert isinstance(res, int)


def test_find(kegg):
    kegg.find("genes", "shiga+toxin")  # for keywords "shiga" and "toxin"
    kegg.find("genes", "shiga toxin")  # for keywords "shigatoxin"
    kegg.find("compound", "C7H10O5", "formula")  # for chemicalformula "C7H10O5"
    kegg.find("compound", "O5C7", "formula")  # for chemicalformula containing "O5" and "C7"
    kegg.find("compound", "174.05", "exact_mass")  # for 174.045 =<exact mass < 174.055
    kegg.find("compound", "300-310", "mol_weight")  # for 300 =<molecular weight =< 310


def test_get(kegg):
    kegg.get("C01290+G00092")
    kegg.get("hsa:10458+ece:Z5100")
    kegg.get("hsa:10458+ece:Z5100", "aaseq")
    kegg.get("hsa05130", "image")
    with pytest.raises(Exception):
        kegg.get("hsa05130", "imagffe")
    kegg.get("network:nt06214")


def test_parse(kegg, parse_input):
    # Check that parse can handle return values that get()
    # might reasonably produce like Service.response_codes
    assert isinstance(kegg.parse(parse_input), dict)


def test_conv(kegg):
    kegg.conv("ncbi-gi", "hsa:10458+ece:Z5100")

    # invalid target → raises ValueError before any HTTP call
    with pytest.raises(Exception):
        kegg.conv("unipro", "hsa")

    with pytest.raises(Exception):
        kegg.conv("hs", "unipro")

    # valid target but invalid/unknown source → KEGG returns an HTTP error code
    res = kegg.conv("uniprot", "hs")
    assert isinstance(res, int)

    res = kegg.conv("hsa", "unipr")
    assert isinstance(res, int)

    # asc contains 1500. Try to get even samller to spped up tests.
    # kegg.conv("asc", "uniprot")
    kegg.conv("hsa", "up:Q9BV86+")


def test_show_module(kegg):
    kegg.show_module("md:hsa_M00001")


def test_show_pathway(kegg, tmp_path):
    p = tmp_path / "test.png"
    kegg.show_entry("path:hsa05416")
    kegg.show_pathway("path:hsa05416", scale=50)
    kegg.save_pathway("path:hsa05416", p.name, scale=50)


def pathway2sif(kegg):
    kegg.pathway2sif("path:hsa05416")


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

    d = s.parse(s.get("C15682"))
    assert d["SEQUENCE"][0]["TYPE"] == "PK"
    assert (
        d["SEQUENCE"][0]["GENE"]
        == "0-2 mycAI [UP:Q83WF0]; 3 mycAII [UP:Q83WE9]; 4-5 mycAIII [UP:Q83WE8]; 6 mycAIV [UP:Q83WE7]; 7 mycAV [UP:Q83WE6]"
    )
    assert d["SEQUENCE"][0]["ORGANISM"] == "Micromonospora griseorubida"

    # issue #79

    d = s.parse(s.get("C00395"))
    assert d["SEQUENCE"][0]["GENE"] == "[1] 0-2 pcbAB [UP:P19787] [2] 0-2 pcbAB [UP:P27742]"
    assert (
        d["SEQUENCE"][0]["ORGANISM"]
        == "[1] Penicillium chrysogenum [2] Emericella nidulans (Aspergillus nidulans [GN:ani] )"
    )
    assert d["SEQUENCE"][0]["SEQUENCE"] == "0 Aad  1 Cys  2 Val"
    assert d["SEQUENCE"][0]["TYPE"] == "NRP"

    # issue 225
    d = s.parse(s.get("gn:T40001"))
    assert "DISEASE" in d


def test_KEGGParser_parse_invalid(parse_input):
    kp = KEGGParser()

    # Check that an exception is raised for invalid input
    with pytest.raises(ValueError):
        kp.parse(parse_input)
