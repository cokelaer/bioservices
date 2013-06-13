from bioservices import Kegg
#from nose import with_setup

#import easydev
#import os
#sharepath = easydev.get_shared_directory_path("bioservices") + os.sep + "data"
#sharepath = easydev.get_shared_directory_path("bioservices") + os.sep  



class _test_Kegg(Kegg):

    def __init__(self):
        super(test_Kegg, self).__init__(verbose=verbose)

        #self.k.load_mapping(sharepath+os.sep+"kegg-hsa-gene_mapping_oct_2012.dat.zip")

    def test_init(self):
        self.k.methods
        self.k.bget("hsa:7535")
        print len(self.k.pathways)
        assert self.k.organism=="hsa" #hsa (homo sapiens by default)

    def test_info(self):
        self.k.info()

    def test_properties(self):
        self.k.organisms

        self.k.organisms.entry_ids
        self.k.organisms.definitions

        self.k.databases.definitions

        self.k.pathways

    def test_bget(self):
        self.k.bget("hsa:7535")

    def test_get_pathways_by_genes(self):
        self.k.get_pathways_by_genes(["hsa:3568", "hsa:3577"])

    def test_binfo(self):
        self.k.binfo("gb")

    def _test_get_number_of_genes_by_organism(self):
        self.k.get_number_of_genes_by_organism()



    def _test_retrieveKGML(self):
        self.k.retrieveKGML(pathwayid="05210", organism="hsa", filename="test.xml")
        #"http://www.genome.jp/dbget-bin/show_pathway?hsa05210"

    def _test_get_genes_by_motifs(self):
        self.k.serv.get_genes_by_motifs(["pf:DnaJ", "ps:DNAJ_2"], 1, 10)


    def _test_get_reactions_by_pathway(self):
        self.k.get_reactions_by_pathway('path:eco00260')
        self.k.get_reactions_by_pathway("path:hsa00010")

    def _test_misc(self):
        self.k.bfind("gb E-cadherin human")
        #self.k.btit("hsa:1798")

    def _test_color_pathway_by_elements(self):
        element_id_list = [ 78, 79, 51, 47 ]
        fg_list  = [ '#ff0000', '#0000ff', '#ff0000', '#0000ff' ]
        bg_list  = [ '#ffff00', '#ffff00', '#ffcc00', '#ffcc00' ]
        self.k.color_pathway_by_elements('path:bsu00010', element_id_list, fg_list, bg_list)


    def _test_get_compounds_by_pathway(self):
        cpds = self.k.get_compounds_by_pathway("path:hsa04064") 
        assert cpds == ['cpd:C00076', 'cpd:C00165', 'cpd:C01245']


    def _test_lookfor_specy(self):
        self.k.lookfor_specy("ZAP70")
