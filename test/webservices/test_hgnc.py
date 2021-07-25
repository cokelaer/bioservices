from bioservices import HGNC


def test_hgnc():

    h = HGNC()
    h.get_info()

    h.fetch('symbol', 'ZNF3')



    h.fetch('alias_name', 'A-kinase anchor protein, 350kDa')


    h.search('BRAF')
    h.search('symbol', 'ZNF*')
    h.search('symbol', 'ZNF?')
    h.search('symbol', 'ZNF*+AND+status:Approved')
    h.search('symbol', 'ZNF3+OR+ZNF12')
    h.search('symbol', 'ZNF*+NOT+status:Approved')

