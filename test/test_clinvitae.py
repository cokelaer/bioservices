from bioservices import Clinvitae



def test_clinvitae():

    c = Clinvitae()
    res = c.query_gene('brca1')
    entry1 = res[0]
    print(entry1.keys())  # display fields for first entry
    print(entry1['accessionId'])  # accession id for first
    print(entry1['lastEvaluated'])  # date first variant
    print(entry1['source'])  # source of first


    #hgvs = ''
    #res = c.query_hgvs(hgvs):

    res = c.all_variants('brca1')

