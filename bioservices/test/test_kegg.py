from bioservices import Kegg
from nose import with_setup



class test_Kegg(Kegg):

    def __init__(self):
        super(test_Kegg, self).__init__()

    def test_organisms(self):
        self.organisms # will load once for all
        self.organisms # try again (cost nothing)

    def test_organism(self):
        self.organism = "hsa"
        try:
            self.organism = "dummy"
            assert False
        except:
            assert True

    def test_pathwayIDs(self):
        self.organism = "hsa"
        self.pathwayIDs

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
        self.list("pathway")             # returns the list of reference pathways
        self.list("pathway", "hsa")      # returns the list of human pathways
        self.list("organism")            # returns the list of KEGG organisms with taxonomic classification
        self.list("hsa")                 # returns the entire list of human genes
        self.list("T01001")              # same as above
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

