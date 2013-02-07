from bioservices import Kegg, KeggParser
from nose import with_setup



class test_Kegg(Kegg):

    def __init__(self):
        super(test_Kegg, self).__init__(verbose=True)
        #self.test_database_IDs()


    def test_database_IDs(self):
        self.organismIds
        assert self.enzymeIds[0].startswith("ec")
        assert self.compoundIds[0].startswith("cpd")
        assert self.glycanIds[0].startswith("gl")
        assert self.reactionIds[0].startswith("rn")
        assert self.drugIds[0].startswith("dr")
        assert self.koIds[0].startswith("ko")

    def test_organism(self):
        self.organism = "hsa"
        try:
            self.organism = "dummy"
            assert False
        except:
            assert True

    def test_isOrganism(self):
        assert self.isOrganism('T01440') == True
        assert self.isOrganism('hsa') == True
        assert self.isOrganism('dummy') == False

    def test_pathwayIDs(self):
        self.organism = "hsa"
        self.pathwayIds

    def test_info(self):
        self.info()
        self.info("brite")
        self.info("hsa")
        try:
            self.info("dummy")
            assert False
        except:
            assert True


    def test_list(self):
        #self.list("pathway")             # returns the list of reference pathways
        self.list("pathway", "hsa")      # returns the list of human pathways
        self.list("organism")            # returns the list of KEGG organisms with taxonomic classification
        #self.list("hsa")                 # returns the entire list of human genes
        #self.list("T01001")              # same as above
        self.list("hsa:10458+ece:Z5100") # returns the list of a human gene and an E.coli O157 gene
        self.list("cpd:C01290+gl:G00092")# returns the list of a compound entry and a glycan entry
        self.list("C01290+G00092")       # same as above 

        # invalid queries:
        try:
            self.list("drug", "hsa")
            assert False
        except:
            assert True

        try:
            self.list("dumy")
            assert False
        except:
            assert True

    def test_find(self):
        self.find("compound", "300-310", "mol_weight")
        self.find("genes", "shiga+toxin")             # for keywords "shiga" and "toxin"
        self.find("genes", "shiga toxin")            # for keywords "shigatoxin"
        self.find("compound", "C7H10O5", "formula")   # for chemicalformula "C7H10O5"
        self.find("compound", "O5C7","formula")       # for chemicalformula containing "O5" and "C7"
        self.find("compound", "174.05","exact_mass")  # for 174.045 =<exact mass < 174.055
        self.find("compound", "300-310","mol_weight") # for 300 =<molecular weight =< 310 

    def test_get(self):
        self.get("cpd:C01290+gl:G00092")
        self.get("C01290+G00092")
        self.get("hsa:10458+ece:Z5100")
        self.get("hsa:10458+ece:Z5100", "aaseq") 
        res = self.get("hsa05130", "image")      
        try:
            self.get("hsa05130", "imagffe")      
            assert False
        except:
            assert True


    def test_conv(self):

        try:
            self.conv("unipro", "hsa")
            assert False
        except:
            assert True

        try:
            self.conv("uniprot", "hs")
            assert False
        except:
            assert True

        try:
            self.conv("hs", "unipro")
            assert False
        except:
            assert True

        try:
            self.conv("hsa", "unipr")
            assert False
        except:
            assert True

        # asc contains 1500. Try to get even samller to spped up tests.
        #self.conv("asc", "uniprot")


        self.conv("hsa","up:Q9BV86+")

    def _test_show_pathway(self):
        self.show_entry("path:hsa05416")
        self.show_pathway("path:hsa05416", scale=50)

    def test_check_dentries(self):
        assert True == self.check_dbentries("hsa:10458+ece:Z5100")
        try:
            self.check_dbentries("hsa:10458+ece:Z510", checkAll=False)
            assert False
        except:
            assert True

    def test_link(self):
        self.link("pathway", "hsa:10458+ece:Z5100")


    def test_org_conv(self):
        assert 'hsa' == self.Tnumber2code("T01001")
        assert 'T01001' == self.code2Tnumber("hsa")

    def test_parse_kgml_pathway(self):
        res = self.parse_kgml_pathway("hsa04660")


def test_KeggParser():
    s = KeggParser()
    res = s.get("rp:RP00001")
    d = s.parseRpair(res)
