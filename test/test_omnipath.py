from bioservices import OmniPath





def test_omnipath():
    o = OmniPath()
    o.get_info()
    o.get_about()

    o.get_network()


    o.get_interactions()
    o.get_interactions("P00533")
    o.get_interactions("P00533,O15177,Q96FE5", frmt='json')
    o.get_interactions("P00533", frmt='json', fields=['sources', 'references'])


    o.get_ptms()
    o.get_ptms("P00533")
    o.get_ptms("P00533", frmt='json')
    o.get_ptms("P00533", frmt='json', fields=['sources', 'references'])
    
