from bioservices import OmniPath



o = OmniPath(cache=True)


def test_omnipath():
    #o.get_info()
    o.get_about()

def test_net():
    o.get_network()


def test_inter():
    o.get_interactions()
    o.get_interactions("P00533")
    o.get_interactions("P00533,O15177,Q96FE5", frmt='json')
    o.get_interactions("P00533", frmt='json', fields=['sources', 'references'])

def test_ptms():
    o.get_ptms()
    o.get_ptms("P00533")
    o.get_ptms("P00533", frmt='json')
    o.get_ptms("P00533", frmt='json', fields=['sources', 'references'])
    
