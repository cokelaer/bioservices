from bioservices import OmniPath
from nose.plugins.attrib import attr


o = OmniPath(cache=True)


def test_omnipath():
    #o.get_info()
    o.get_about()

def test_net():
    o.get_network()


def test_inter():
    o.get_interactions()
    o.get_interactions("P00533")
    o.get_interactions(["P00533"])
    o.get_interactions("P00533,O15177,Q96FE5", frmt='json')
    o.get_interactions("P00533", frmt='json', fields=['sources', 'references'])

    try:
        o.get_interactions(00553)
        assert False
    except:
        assert True

def test_ptms():
    o.get_ptms()
    o.get_ptms("P00533")
    o.get_ptms(["P00533"])
    o.get_ptms("P00533", frmt='json')
    o.get_ptms("P00533", frmt='json', fields=['sources', 'references'])
    
    try:
        o.get_ptms(00553)
        assert False
    except:
        assert True

def test_get_resources():
    res = o.get_resources()

@attr('skip_travis')
def test_info():
    o.get_info()

