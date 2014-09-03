from bioservices import Reactome




class test_Reactome(object):

    @classmethod
    def setup_class(klass):
        klass.e = Reactome(verbose=True)

    def test_biopax_exporter(self):
        res = self.e.biopax_exporter(109581)

    def test_front_page_items(self):
        res = self.e.front_page_items("homo sapiens")

    def _test_highlight_pathway_diagram(self):
        pass

    def test_list_by_query(self):
        classname = 'Pathway'
        res = self.e.list_by_query(classname, name="apostosis")


    def test_pathway_diagram(self):
        res = self.e.pathway_diagram(109581, 'XML')
        res = self.e.pathway_diagram(109581, 'PNG')
        res = self.e.pathway_diagram(109581, 'PDF')
        try:
            res = self.e.pathway_diagram(109581, 'XDF')
            assert False
        except:
            assert True

    def test_pathway_hierarchy(self):
        res = self.e.pathway_hierarchy('homo sapiens')

    def test_pathway_participant(self):
        res = self.e.pathway_participant(109581)

    def test_pathway_complexes(self):
        res = self.e.pathway_complexes(109581)

    def test_query_by_id(self):
        res = self.e.query_by_id("Pathway", 109581)

    def test_query_by_ids(self):
        res = self.e.query_by_ids("Pathway", [109581])


    def _test_pathway_for_entities(self):
        res = self.e.query_pathways_for_entities("CDC2")

    def test_species_list(self):
        res = self.e.species_list()

    def test_sbml_exporter(self):
        res = self.e.SBML_exporter(109581)



