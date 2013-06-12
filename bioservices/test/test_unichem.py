from bioservices import UniChem




def test_unichem_src_compound():
    uni = UniChem()
    uni.get_src_compound_ids_from_src_compound_id("CHEMBL12", "chembl", "chebi")
    uni.get_src_compound_ids_all_from_src_compound_id("CHEMBL12", "chembl","drugbank")
    #[{'assignment': '1', 'src_compound_id': 'DB00829'},
    #{'assignment': '0', 'src_compound_id': 'DB07699'}]


def test_unichem_src_compound_from_inchikey():
    uni = UniChem()
    uni.get_src_compound_ids_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
    uni.get_src_compound_ids_all_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")


def test_mapping():
    uni = UniChem()
    res1 = uni.get_mapping("kegg_ligand", "chembl")
    assert len(res1)>0

def test_src_ids():
    uni = UniChem()
    uni.get_all_src_ids()
    uni.get_source_information("chembl")


def test_structure():
    uni = UniChem()
    uni.get_structure("CHEMBL12", "chembl")
    uni.get_structure_all("CHEMBL12", "chembl")


def test_get_source_id():
    uni = UniChem()
    assert uni.get_source_id("chembl") == 1
    assert uni.get_source_id("1") == 1
    assert uni.get_source_id(1) == 1

    try:
        uni.get_source_id("wrong")
        assert False
    except:
        assert True

    try:
        uni.get_source_id("20000")
        assert False
    except:
        assert True

def test_get_src_compound_ids_all_from_obsolete():
    uni = UniChem()
    res = uni.get_src_compound_ids_all_from_obsolete("DB07699", 2)
    res = uni.get_src_compound_ids_all_from_obsolete("DB07699", 2, "chembl")

def test_get_verbose_src_compound_ids_fron_inchikey():
    uni = UniChem()
    uni.get_verbose_src_compound_ids_from_inchikey("GZUITABIAKMVPG-UHFFFAOYSA-N")


def test_get_src_compoundid_url():
    uni = UniChem()
    uni.get_src_compound_id_url("CHEMBL12", "chembl", "drugbank")


def test_get_auxiliary_mapping():
    # this does nothing (behaviour of the function)
    uni = UniChem()
    res = uni.get_auxiliary_mappings(1)
    # this returns something but takes lots of time so it is commented
    #res = uni.get_auxiliary_mappings(15)

