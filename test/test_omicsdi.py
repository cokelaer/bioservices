import pytest

from bioservices.omicsdi import OmicsDI

@pytest.fixture
def omicsdi():
    return OmicsDI(verbose=True)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def test_term_get_term_by_pattern(omicsdi):
    response = omicsdi.get_term_by_pattern()
    assert keys_exists(response, ("total_count", "items"))

    response = omicsdi.get_term_by_pattern(q = "array", size = 10)
    assert len(response["items"])

def test_seo_home(omcsidi):
    response = omicsdi.seo_home()
    assert keys_exists(response, ("@graph"))

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
    assert not len(response)

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