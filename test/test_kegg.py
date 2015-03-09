from bioservices import KEGG, KEGGParser
from nose.plugins.attrib import attr





# This is a simple test class that do not test everything on purpose.
# The other class could be use to test the code more thoroughly but it takes several
# minutes so during development this one should be used instead.
# class TestKEGGAll should serve as a complement to this class

@attr('skip_travis')
class TestKEGG(object):

    @classmethod
    def setup_class(klass):
        klass.ws = KEGG()
        klass.ws.organismIds
        klass.ws.organism = "hsa"

    def test_isOrganism(self):
        assert self.ws.isOrganism('T01440') == True
        assert self.ws.isOrganism('hsa') == True
        assert self.ws.isOrganism('dummy') == False

    def test_database_IDs(self):
        self.ws.pathwayIds

    def test_conv(self):
        self.ws.conv("ncbi-gi","hsa:10458+ece:Z5100")

    @attr('slow')
    def test_info(self):
        self.ws.info("kegg")
        self.ws.info("brite")

    def test_list(self):
        self.ws.list("pathway", "hsa")      # returns the list of human pathways

    def test_find(self):
        self.ws.find("compound", "300-310", "mol_weight")

    @attr('slow')
    def test_get(self):
        self.ws.get("cpd:C01290+gl:G00092")

    @attr('slow')
    def test_checkDB(self):
        for this in ["info", "list", "find", "link"]:
            try:
                self.ws._checkDB("dummy", this)
                assert False
            except:
                assert True
            self.ws._checkDB("pathway", this)

    def test_link(self):
        self.ws.link("pathway", "hsa:10458+ece:Z5100")

    @attr('slow')
    def test_org_conv(self):
        assert 'hsa' == self.ws.Tnumber2code("T01001")
        assert 'T01001' == self.ws.code2Tnumber("hsa")

    @attr('slow')
    def test_parse_kgml_pathway(self):
        res = self.ws.parse_kgml_pathway("hsa04660")





@attr('skip_travis')
class TestKEGGALL(object):

    @classmethod
    def setup_class(klass):
        klass.ws = KEGG()
        klass.ws.organismIds
        print(klass)

    @attr('slow')
    def test_ids(self):
        assert self.ws.enzymeIds[0].startswith("ec")
        assert self.ws.compoundIds[0].startswith("cpd")
        assert self.ws.glycanIds[0].startswith("gl")
        assert self.ws.reactionIds[0].startswith("rn")
        assert self.ws.drugIds[0].startswith("dr")
        assert self.ws.koIds[0].startswith("ko")
        assert self.ws.briteIds[0].startswith("br")


    @attr('slow')
    def test_lookfor(self):
        self.ws.lookfor_organism("human")
        self.ws.lookfor_pathway("cell")

    def test_organism(self):
        self.ws.organism = "hsa"
        try:
            self.ws.organism = "dummy"
            assert False
        except:
            assert True

    def test_pathwayIDs(self):
        self.ws.organism = "hsa"
        self.ws.pathwayIds

    def test_info(self):
        self.ws.info("hsa")
        try:
            self.ws.info("dummy")
            assert False
        except:
            assert True

    @attr('slow')
    def test_list(self):
        self.ws.list("pathway")             # returns the list of reference pathways
        self.ws.list("organism")            # returns the list of KEGG organisms with taxonomic classification
        self.ws.list("hsa")                 # returns the entire list of human genes
        self.ws.list("T01001")              # same as above
        self.ws.list("hsa:10458+ece:Z5100") # returns the list of a human gene and an E.coli O157 gene
        self.ws.list("cpd:C01290+gl:G00092")# returns the list of a compound entry and a glycan entry
        self.ws.list("C01290+G00092")       # same as above

        # invalid queries:
        try:
            self.ws.list("drug", "hsa")
            assert False
        except:
            assert True

        try:
            self.ws.list("dumy")
            assert False
        except:
            assert True

    @attr('slow')
    def test_find(self):
        self.ws.find("genes", "shiga+toxin")             # for keywords "shiga" and "toxin"
        self.ws.find("genes", "shiga toxin")            # for keywords "shigatoxin"
        self.ws.find("compound", "C7H10O5", "formula")   # for chemicalformula "C7H10O5"
        self.ws.find("compound", "O5C7","formula")       # for chemicalformula containing "O5" and "C7"
        self.ws.find("compound", "174.05","exact_mass")  # for 174.045 =<exact mass < 174.055
        self.ws.find("compound", "300-310","mol_weight") # for 300 =<molecular weight =< 310

    @attr('slow')
    def test_get(self):
        self.ws.get("C01290+G00092")
        self.ws.get("hsa:10458+ece:Z5100")
        self.ws.get("hsa:10458+ece:Z5100", "aaseq")
        res = self.ws.get("hsa05130", "image")
        try:
            self.ws.get("hsa05130", "imagffe")
            assert False
        except:
            assert True

    @attr('slow')
    def test_conv(self):
        self.ws.conv("ncbi-gi","hsa:10458+ece:Z5100")

        try:
            self.ws.conv("unipro", "hsa")
            assert False
        except:
            assert True

        try:
            self.ws.conv("uniprot", "hs")
            assert False
        except:
            assert True

        try:
            self.ws.conv("hs", "unipro")
            assert False
        except:
            assert True

        try:
            self.ws.conv("hsa", "unipr")
            assert False
        except:
            assert True

        # asc contains 1500. Try to get even samller to spped up tests.
        #self.conv("asc", "uniprot")
        self.ws.conv("hsa","up:Q9BV86+")

    @attr('slow')
    def test_show_module(self):
        self.ws.show_module("md:hsa_M00402")


    @attr('slow')
    def test_show_pathway(self):
        self.ws.show_entry("path:hsa05416")
        self.ws.show_pathway("path:hsa05416", scale=50)

    def pathway2sif(self):
        sif = self.ws.pathway2sif("path:hsa05416")


@attr('slow')
def test_KEGGParser():
    s = KEGG()
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
