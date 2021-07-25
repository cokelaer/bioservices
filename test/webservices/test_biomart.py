from bioservices import BioMart
import pytest


@pytest.fixture
def biomart():
    biomart = BioMart(host='www.ensembl.org', verbose=False)
    biomart.mart_test = 'ENSEMBL_MART_ENSEMBL'
    return biomart


@pytest.mark.flaky
def test_version(biomart):
    biomart.version(biomart.mart_test)


@pytest.mark.flaky
def _test_datasets(biomart):
    # there are about 70 datasets but let us check that at least the list is
    # not emptyt
    assert len(biomart.datasets(biomart.mart_test)) > 2

    assert "mmusculus_gene_ensembl" in biomart.datasets(biomart.mart_test)


@pytest.mark.flaky
def _test_attributes(biomart):
    assert 'oanatinus_gene_ensembl' in \
        biomart.valid_attributes[biomart.mart_test]


@pytest.mark.flaky
def test_filteres(biomart):
    biomart.filters("oanatinus_gene_ensembl")


@pytest.mark.flaky
def test_config(biomart):
    biomart.configuration("oanatinus_gene_ensembl")


#fails on travais sometines
@pytest.mark.flaky
def _test_query(biomart):
    res = biomart.query(biomart._xml_example)
    assert "ENSMUS" in res


@pytest.mark.flaky
def test_xml(biomart):
    # build own xml using the proper functions
    biomart.add_dataset_to_xml("mmusculus_gene_ensembl")
    biomart.get_xml()


@pytest.mark.flaky
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

