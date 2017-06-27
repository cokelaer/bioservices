from bioservices.rhea import Rhea


def test_rhea():
    rhea = Rhea()
    r1 = rhea.search("caffeine")
    r1= rhea.search("caffeine", frmt="cmlreact")
    r2 = rhea.search("caffeine", frmt="biopax2")
    try:
        rhea.search("caffeine", frmt="biopaxddddddd2")
        assert False
    except:
        assert True

    rhea.entry(10280, "cmlreact")

    rhea.entry(10280, "biopax2")

    rhea.entry(10090, "rxn")

    try:
        rhea.entry(10090, "ggg")
        assert False
    except:
        assert True





