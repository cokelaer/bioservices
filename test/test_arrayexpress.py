from bioservices import ArrayExpress
import pytest



@pytest.fixture
def array():
    return ArrayExpress(verbose=False)


@pytest.mark.xfail
def test_retrieveFiles(array):
    #res = array.retrieveFiles(keywords="cancer+breast", species="Home+Sapiens")
    res = array.queryFiles(array="A-AFFY-33")

@pytest.mark.xfail
def test_retrieveExperiments(array):
    #res = array.retrieveExperiments(keywords="cancer+breast", species="Home+Sapiens")

    #res = array.queryExperiments(array="A-AFFY-33")
    #assert len(res.getchildren())>0
    res = array.queryExperiments(array="A-AFFY-33", species="Homo Sapiens",expdesign="dose+response")
    assert res['experiments']['total']>0
    res = array.queryExperiments(array="A-AFFY-33", species="Homo Sapiens",expdesign="dosestupid")
    assert res['experiments']['total']==0
    res = array.queryExperiments(array="A-AFFY-33", species="Homo Sapiens", expdesign="dose+response", 
        sortby="releasedate", sortorder="ascending")

@pytest.mark.xfail
def test_retrieveFile(array):
    res = array.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")
    array.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt", save=True) 
    import os
    os.remove("E-MEXP-31.idf.txt")

    try:
        res == array.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txtdddd")
        assert False
    except:
        pass

@pytest.mark.xfail
def test_retrieveExperiment(array):
    array.retrieveExperiment("E-MEXP-31")

@pytest.mark.xfail
def test_extra1(array):
    # works. just takes 15 seconds so let us skip it.
    res = array.queryFiles(keywords="cancer+breast", wholewords=True)
@pytest.mark.xfail
def test_extra2(array):
    res = array.queryFiles(keywords="cancer+breast", wholewords=True, gxa="true")
@pytest.mark.xfail
def test_extra3(array):
    res = array.queryFiles(keywords="cancer+breast", wholewords=True, directsub="false")


@pytest.mark.xfail
def test_extra4():
    ae = ArrayExpress(verbose=False)
    ae.TIMEOUT = 60
    try:
        res = ae.queryAE(keywords="pneumonia", species='homo+sapiens')
    except:
        pass
