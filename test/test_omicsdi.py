import pytest

from bioservices.omicsdi import OmicsDI

@pytest.fixture
def omicsdi():
    return OmicsDI(verbose=True)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def test_dataset_merge(omicsdi):
    with pytest.raises(Exception):
        omicsdi.dataset_merge()

def test_dataset_get_merge_candidates(omicsdi):
    with pytest.raises(Exception):
        omicsdi.dataset_get_merge_candidates()

def test_dataset_domain_accession_files(omicsdi):
    response = omicsdi.dataset_domain_accession_files(
        accession = "PXD000210", domain = "pride", position = 1)

    assert len(response)
    assert keys_exists(response[0], ("type", "url"))

def test_dataset_search(omicsdi):
    response = omicsdi.dataset_search()
    assert keys_exists(response, ("count", "datasets"))

def test_dataset_latest(omicsdi):
    response = omicsdi.dataset_latest()
    assert keys_exists(response, ("count", "datasets"))

def test_dataset_batch(omicsdi):
    response = omicsdi.dataset_batch(accession = "PXD000210", database = "pride")
    assert keys_exists(response, ("failure", "datasets"))

def test_dataset_most_accessed(omicsdi):
    response = omicsdi.dataset_most_accessed(size = 20)
    assert keys_exists(response, ("count", "datasets"))

def test_dataset_get_file_links(omicsdi):
    response = omicsdi.dataset_get_file_links(accession = "PXD000210", database = "pride")
    assert len(response)

def test_dataset_domain_accession(omicsdi):
    response = omicsdi.dataset_domain_accession(accession = "PXD000210", domain = "pride")
    assert keys_exists(response, ("database", "file_versions"))

def test_dataset_get_similar(omicsdi):
    response = omicsdi.dataset_get_similar(accession = "PXD000210", database = "pride")
    assert keys_exists(response, ("count", "datasets"))

def test_dataset_get_similar_by_pubmed(omicsdi):
    response = omicsdi.dataset_get_similar_by_pubmed(pubmed = 16585740)
    assert len(response)
    assert keys_exists(response[0], ("accession", "database", "initHashCode"), test = any)

def test_database_all(omicsdi):
    response = omicsdi.database_all()
    assert len(response)

def test_term_get_term_by_pattern(omicsdi):
    response = omicsdi.term_get_term_by_pattern()
    assert keys_exists(response, ("total_count", "items"))

    response = omicsdi.term_get_term_by_pattern(query = "array", size = 10)
    assert len(response["items"])

def test_term_frequently_term_list(omicsdi):
    response = omicsdi.term_frequently_term_list(domain = "pride", field = "description")
    assert len(response)
    assert keys_exists(response[0], ("label", "frequent"))

def test_seo_home(omicsdi):
    response = omicsdi.seo_home()
    assert keys_exists(response, ("@graph",))

def test_seo_search(omicsdi):
    response = omicsdi.seo_search()
    assert keys_exists(response, ("name", "url", "keywords",
        "description", "variableMeasured", "alternateName",
        "logo", "email", "image", "potentialAction",
        "sameAs", "creator", "citation", "primaryImageOfPage",
        "@context", "@type"))

def test_seo_api(omicsdi):
    response = omicsdi.seo_api()
    assert keys_exists(response, ("name", "url", "keywords",
        "description", "variableMeasured", "alternateName",
        "logo", "email", "image", "potentialAction",
        "sameAs", "creator", "citation", "primaryImageOfPage",
        "@context", "@type"))

def test_seo_database(omicsdi):
    response = omicsdi.seo_database()
    assert keys_exists(response, ("name", "url", "keywords",
        "description", "variableMeasured", "alternateName",
        "logo", "email", "image", "potentialAction",
        "sameAs", "creator", "citation", "primaryImageOfPage",
        "@context", "@type"))

def test_seo_dataset_domain_accession(omicsdi):
    response = omicsdi.seo_dataset_domain_accession(domain = "pride", accession = "PXD000210")
    assert keys_exists(response, ("name", "url", "keywords"), test = any)

def test_seo_about(omicsdi):
    response = omicsdi.seo_about()
    assert keys_exists(response, ("name", "url", "keywords",
        "description", "variableMeasured", "alternateName",
        "logo", "email", "image", "potentialAction",
        "sameAs", "creator", "citation", "primaryImageOfPage"))

def test_statistics_organisms(omicsdi):
    response = omicsdi.statistics_organisms()
    assert len(response)
    assert keys_exists(response[0], ("label", "id", "value", "name"))

    response = omicsdi.statistics_organisms(size = 0)
    assert len(response)

def test_statistics_tissues(omicsdi):
    response = omicsdi.statistics_tissues()
    assert len(response)
    assert keys_exists(response[0], ("label", "id", "value", "name"))

    response = omicsdi.statistics_tissues(size = 0)
    assert len(response)

def test_statistics_omics(omicsdi):
    response = omicsdi.statistics_omics()
    assert len(response)
    assert keys_exists(response[0], ("label", "id", "value", "name"))

def test_statistics_diseases(omicsdi):
    response = omicsdi.statistics_diseases()
    assert len(response)
    assert keys_exists(response[0], ("label", "id", "value", "name"))

def test_statistics_domains(omicsdi):
    response = omicsdi.statistics_domains()
    assert len(response)
    assert keys_exists(response[0], ("domain", "subdomains"))

def test_statistics_omics_by_year(omicsdi):
    response = omicsdi.statistics_omics_by_year()
    assert len(response)
    assert keys_exists(response[0], ("year", "genomics",
        "metabolomics", "proteomics", "transcriptomics"))