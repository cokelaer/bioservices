from bioservices import BioMart


def test_general():
    # test another host
    s = BioMart(host="www.ensembl.org")
    s = BioMart()
    #s.registry()


    assert s.datasets("prod-intermart_1") == ['protein', 'entry', 'uniparc']

    assert "mmusculus_gene_ensembl" in s.datasets("ensembl")
    s.version("ensembl")
    assert 'oanatinus_gene_ensembl' in s.valid_attributes["ensembl"]
    s.filters("oanatinus_gene_ensembl")
    s.configuration("oanatinus_gene_ensembl")




    res = s.query(s._xml_example)
    assert "ENSMUS" in res


    # build own xml using the proper functions
    s.add_dataset_to_xml("protein")
    s.get_xml()

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

