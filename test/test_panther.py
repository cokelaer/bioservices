from bioservices.panther import Panther


p = Panther()

def test_panther_supported_genomes():
    p.get_supported_genomes()
    p.get_supported_genomes(type="chrLoc")

def test_pathways():
    p.get_pathways()


def test_mapping():


    res = p.get_mapping("zap70,erk,xxxxxx", 9606)
    assert len(res["mapped"]) == 2
    assert res["unmapped"] == ['xxxxxx']

    res = p.get_mapping("zap70,xxxxxx,yyyyyy", 9606)
    assert len(res["mapped"]) == 1
    assert res["unmapped"] == ['xxxxxx', 'yyyyyy']


def test_enrich():
    res = p.get_enrichment("zap70,mek1,erk", 9606, "ANNOT_TYPE_ID_PANTHER_PATHWAY", 
        correction="FDR",enrichment_test="Fisher")
    enrich = [x for x in res['result'] if x['pValue']<0.05 ]
    assert len(enrich) > 0

def test_math_ortholog():

    res = p.get_ortholog("zap70,xxx,yyy", 9606)
    assert len(res['unmapped']) == 2
    res = p.get_ortholog("zap70,xxx", 9606)
    assert len(res['unmapped']) == 1
    res = p.get_ortholog("zap70", 9606) 
    assert len(res['unmapped']) == 0
    assert len(res['mapped'])


def test_homolog_position():
    res = p.get_homolog_position("zap70", 9606, 1)
    res = p.get_homolog_position("xxx", 9606, 1)
    assert res['unmapped']

def test_supported_families():
    res = p.get_supported_families()
    res = p.get_supported_families(progress=False)
    try:
        res = p.get_supported_families(progress=False, N=2000)
        assert False
    except:
        assert True

def test_get_family_ortholog():
    res = p.get_family_ortholog("PTHR10000")
    assert len(res)

def test_get_family_msa():
    res = p.get_family_msa("PTHR10000")
    assert len(res)

def test_get_tree_info():
    res = p.get_tree_info("PTHR10000")

