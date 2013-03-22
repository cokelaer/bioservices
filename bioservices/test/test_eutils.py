from bioservices import eutils


def test_espell():
    e = eutils.EUtils(True)
    ret = e.serv.run_eSpell(db="omim", term="aasthma+OR+alergy")
    assert ret.CorrectedQuery == 'asthma or allergy'

