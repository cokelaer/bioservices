from bioservices.apps.taxonomy import Taxon


def test_taxonomy():
    t = Taxon()
    t.search_by_taxon("9606")
