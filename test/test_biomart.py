from bioservices import BioMart
from nose.plugins.attrib import attr


class test_biomart(object):
    @classmethod
    def setup_class(klass):
        klass.s = BioMart(verbose=False)

    def test_general(self):
        # test another host
        s = BioMart(host="www.ensembl.org")

    def test_version(self):
        self.s.version("ensembl")

    def test_datasets(self):
        assert self.s.datasets("prod-intermart_1") == ['protein', 'entry']

        assert "mmusculus_gene_ensembl" in self.s.datasets("ensembl")

    def test_attributes(self):
        assert 'oanatinus_gene_ensembl' in self.s.valid_attributes["ensembl"]

    def test_filteres(self):
        self.s.filters("oanatinus_gene_ensembl")

    def test_config(self):
        self.s.configuration("oanatinus_gene_ensembl")

    def test_query(self):
        res = self.s.query(self.s._xml_example)
        assert "ENSMUS" in res

    def test_xml(self):
        # build own xml using the proper functions
        self.s.add_dataset_to_xml("protein")
        self.s.get_xml()

def _test_reactome_example():
    # this is not working anymore...
    s = BioMart()
    s.lookfor("reactome")
    s.datasets("REACTOME")
    #['interaction', 'complex', 'reaction', 'pathway']
    s.new_query()
    s.add_dataset_to_xml("pathway")
    s.add_filter_to_xml("species_selection", "Homo sapiens")
    s.add_attribute_to_xml("pathway_db_id")
    s.add_attribute_to_xml("_displayname")
    xmlq = s.get_xml()
    res = s.query(xmlq)

