from bioservices.rhea import Rhea


def test_rhea():
    rhea = Rhea()
    r1 = rhea.search("caffeine", limit=2)
    df = rhea.query("rhea:10660")




