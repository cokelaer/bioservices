from bioservices.intact import IntactComplex



def test_intact():
    i = IntactComplex()
    res = i.details('EBI-1163476')
    assert res['ac'] == 'EBI-1163476'

    res = i.search('ndc80')
    try:
        res = i.search('ndc80', frmt='pandas')
    except:
        pass

