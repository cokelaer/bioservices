import pytest

from bioservices import BioMart, BioServicesError
from bioservices.biomart import BioMartQuery


@pytest.fixture(scope="module")
def biomart():
    try:
        bm = BioMart(host="www.ensembl.org", verbose=False)
    except Exception:
        pytest.skip("BioMart/Ensembl service unreachable or timed out")
    bm.mart_test = "ENSEMBL_MART_ENSEMBL"
    return bm


# ------------------------------------------------------------------
# BioMartQuery (no network required)
# ------------------------------------------------------------------


def test_biomartquery_get_xml():
    q = BioMartQuery()
    q.add_dataset("mmusculus_gene_ensembl")
    q.add_attribute("""        <Attribute name = "ensembl_gene_id" />""")
    xml = q.get_xml()
    assert "mmusculus_gene_ensembl" in xml
    assert "ensembl_gene_id" in xml
    assert xml.startswith("<?xml")


def test_biomartquery_get_xml_no_dataset():
    q = BioMartQuery()
    with pytest.raises(BioServicesError):
        q.get_xml()


def test_biomartquery_reset():
    q = BioMartQuery()
    q.add_dataset("mmusculus_gene_ensembl")
    q.reset()
    assert q.dataset is None
    assert q.attributes == []
    assert q.filters == []


def test_biomartquery_with_filter():
    q = BioMartQuery()
    q.add_dataset("mmusculus_gene_ensembl")
    q.add_filter("""        <Filter name = "ensembl_gene_id" value = "ENSMUSG00000086981"/>""")
    q.add_attribute("""        <Attribute name = "ensembl_gene_id" />""")
    xml = q.get_xml()
    assert "ENSMUSG00000086981" in xml


# ------------------------------------------------------------------
# Network tests (require www.ensembl.org)
# ------------------------------------------------------------------


@pytest.mark.timeout(120)
def test_version(biomart):
    result = biomart.version(biomart.mart_test)
    assert result is not None


@pytest.mark.timeout(120)
def test_names(biomart):
    assert isinstance(biomart.names, list)
    assert biomart.mart_test in biomart.names


@pytest.mark.timeout(120)
def test_databases(biomart):
    assert isinstance(biomart.databases, list)
    assert len(biomart.databases) > 0


@pytest.mark.timeout(120)
def test_display_names(biomart):
    assert isinstance(biomart.displayNames, list)
    assert len(biomart.displayNames) > 0


@pytest.mark.timeout(120)
def test_datasets(biomart):
    datasets = biomart.datasets(biomart.mart_test)
    assert len(datasets) > 2
    assert "mmusculus_gene_ensembl" in datasets


@pytest.mark.timeout(120)
def test_datasets_invalid_mart(biomart):
    with pytest.raises(BioServicesError):
        biomart.datasets("not_a_real_mart_xyz")


@pytest.mark.timeout(120)
def test_attributes(biomart):
    assert "drerio_gene_ensembl" in biomart.valid_attributes[biomart.mart_test]


@pytest.mark.timeout(120)
def test_filters(biomart):
    result = biomart.filters("drerio_gene_ensembl")
    assert isinstance(result, dict)
    assert len(result) > 0


@pytest.mark.timeout(120)
def test_config(biomart):
    result = biomart.configuration("drerio_gene_ensembl")
    assert result is not None


@pytest.mark.timeout(120)
def test_lookfor(biomart):
    # Should run without error; verbose=False suppresses output
    biomart.lookfor("ensembl", verbose=False)


@pytest.mark.timeout(120)
def test_new_query(biomart):
    biomart.new_query()
    biomart.add_dataset_to_xml("mmusculus_gene_ensembl")
    biomart.add_attribute_to_xml("ensembl_gene_id")
    xml = biomart.get_xml()
    assert "mmusculus_gene_ensembl" in xml
    assert "ensembl_gene_id" in xml


@pytest.mark.timeout(120)
def test_create_filter_integer_value(biomart):
    # create_filter must not crash when value is an integer
    filt = biomart.create_filter("protein_length_greater_than", 1000)
    assert "1000" in filt


@pytest.mark.timeout(120)
def test_xml(biomart):
    biomart.new_query()
    biomart.add_dataset_to_xml("mmusculus_gene_ensembl")
    xml = biomart.get_xml()
    assert "mmusculus_gene_ensembl" in xml
