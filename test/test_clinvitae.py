from bioservices import Clinvitae



def test_clinvitae():

    c = Clinvitae()
    res = c.query_gene('brca1')
    entry1 = res[0]
    entry1.keys()
    assert entry1['accessionId'] == 'SCV000039520'
    assert entry1['lastEvaluated'] # not a stable test # == '2013-04-03'
    assert entry1['source'] == 'ClinVar'



    res = c.query_gene('NM_198578.3:c.1847A>G')  # returns all entries in LRRK2 gene
    entry1 = res[0]
    assert entry1['accessionId']  == 'SCV000056058'
    assert entry1['lastEvaluated'] == u'2012-09-13'
    assert entry1['source'] == 'ClinVar'

    res = c.all_variants('MUTYH')  # returns all reported variants in MUTYH gene
    assert len(res)>0


    pathogenic = c.get_pathogenic('brca1')  # returns pathogenic or likely pathogenic
    assert len(pathogenic) > 100


    benign = c.get_benign('brca1')  # returns benign or likely benign
    assert len(benign) > 100

    vus = c.get_VUS('brca1')
    assert len(vus) > 100
