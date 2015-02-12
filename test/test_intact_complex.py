from bioservices.intact import Intact



def test_intact():
    i = Intact()
    res = i.details('EBI-1163476')
    assert res['ac'] == 'EBI-1163476'

    res = i.search('ndc80')
    try:
        res = i.search('ndc80', frmt='pandas')
    except:
        pass

