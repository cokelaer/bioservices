from bioservices import BioMart
from nose.plugins.attrib import attr


class test_biomart(object):
    @classmethod
    def setup_class(klass):
        # ideally we should not provide a host to be more generic 
        # but this takes lots of time or is simply down.
        klass.s = BioMart(host='www.ensembl.org', verbose=False)
        klass.mart_test = 'ENSEMBL_MART_ENSEMBL'

    def test_general(self):
        # test another host
        s = BioMart(host="www.ensembl.org")

    def test_version(self):
        self.s.version(self.mart_test)

    def test_datasets(self):
        # there are about 70 dataset but let us check that at least the list is
        # not empty
        assert len(self.s.datasets(self.mart_test)) > 2

        assert "mmusculus_gene_ensembl" in self.s.datasets(self.mart_test)

    def test_attributes(self):
        assert 'oanatinus_gene_ensembl' in \
            self.s.valid_attributes[self.mart_test]

    def test_filteres(self):
        self.s.filters("oanatinus_gene_ensembl")

    def test_config(self):
        self.s.configuration("oanatinus_gene_ensembl")

    
    #fails on travais sometines
    @attr("fixme")
    def test_query(self):
        res = self.s.query(self.s._xml_example)
        assert "ENSMUS" in res

    def test_xml(self):
        # build own xml using the proper functions
        self.s.add_dataset_to_xml("mmusculus_gene_ensembl")
        self.s.get_xml()

def test_biomart_constructor():
    s = BioMart()
    try:
        s.registry()
    except:
        pass
    try:
        s.host = "dummy"
    except:
        pass
    s.host = "www.ensembl.org"

# # reactome not maintained anymore ?
# https://support.bioconductor.org/p/62622/
def _test_reactome_example():
    # this is not working anymore...
    s = BioMart("reactome.org")
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

