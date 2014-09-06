from bioservices import Reactome
from nose.plugins.attrib import attr



class test_Reactome(object):

    @classmethod
    def setup_class(klass):
        klass.e = Reactome(verbose=True)

    def test_species(self):
        assert len( self.e.get_species()) > 10

    def test_biopax_exporter(self):
        res = self.e.biopax_exporter(109581)

    def test_front_page_items(self):
        res = self.e.front_page_items("homo sapiens")

    def test_highlight_pathway_diagram(self):
        res = self.e.highlight_pathway_diagram(68875, frmt="PNG", genes="CDC2")

    def test_list_by_query(self):
        assert len(self.e.list_by_query("Pathway", name="Apoptosis"))>1

    def test_pathway_diagram(self):
        res = self.e.pathway_diagram(109581, 'XML')
        res = self.e.pathway_diagram(109581, 'PNG')
        res = self.e.pathway_diagram(109581, 'PDF')
        try:
            res = self.e.pathway_diagram(109581, 'XDF')
            assert False
        except:
            assert True

    @attr('slow')
    def test_pathway_hierarchy(self):
        res = self.e.pathway_hierarchy('homo sapiens')
        assert len(res)>10

    def test_pathway_participants(self):
        res = self.e.pathway_participants(109581)
        assert len(res)>0

    def test_pathway_complexes(self):
        res = self.e.pathway_complexes(109581)
        assert len(res)>1
        assert "dbId" in list(res[0].keys())

    def test_query_by_id(self):
        res = self.e.query_by_id("Pathway", 109581)
        assert len(res)>1

    def test_query_by_ids(self):
        res = self.e.query_by_ids("Pathway", 'CDC2')
        assert len(res)>=1

    def test_query_hit_pathways(self):
        assert len(self.e.query_hit_pathways("CDC2"))>1

    def test_pathway_for_entities(self):
        res = self.e.query_pathway_for_entities("CDC2")

    def test_species_list(self):
        res = self.e.species_list()

    @attr('slow')
    def test_sbml_exporter(self):
        res = self.e.SBML_exporter(109581)



