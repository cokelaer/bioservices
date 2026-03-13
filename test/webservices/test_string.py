from bioservices import STRING

s = STRING()


def test_get_version():
    res = s.get_version()
    assert isinstance(res, list)
    assert len(res) > 0
    assert "string_version" in res[0]


def test_get_string_ids():
    res = s.get_string_ids("TP53", species=9606)
    assert isinstance(res, list)
    assert len(res) > 0
    assert "stringId" in res[0]


def test_get_network():
    res = s.get_network(["TP53", "BRCA1"], species=9606)
    assert isinstance(res, list)
    assert len(res) > 0
    first = res[0]
    assert "stringId_A" in first or "preferredName_A" in first


def test_get_interaction_partners():
    res = s.get_interaction_partners("TP53", species=9606, limit=5)
    assert isinstance(res, list)
    assert len(res) > 0


def test_get_enrichment():
    proteins = ["TP53", "BRCA1", "BRCA2", "ATM", "CHEK2"]
    res = s.get_enrichment(proteins, species=9606)
    assert isinstance(res, list)


def test_get_functional_annotation():
    res = s.get_functional_annotation("TP53", species=9606)
    assert isinstance(res, list)


def test_get_ppi_enrichment():
    proteins = ["TP53", "BRCA1", "BRCA2", "ATM", "CHEK2"]
    res = s.get_ppi_enrichment(proteins, species=9606)
    assert res is not None


def test_identifiers_to_str_list():
    result = s._identifiers_to_str(["TP53", "BRCA1"])
    assert "TP53" in result
    assert "BRCA1" in result
    assert "\n" in result


def test_identifiers_to_str_string():
    result = s._identifiers_to_str("TP53")
    assert result == "TP53"
