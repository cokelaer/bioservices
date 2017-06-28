from bioservices import NCBIblast
import pytest
import os

skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
    reason="too slow for travis")


@pytest.fixture
def ncbi():
    return NCBIblast()


def test_param(ncbi):
    ncbi.getParameters()
    assert(len(ncbi.parameters)>0)
    assert(len(ncbi.parameters)>0)


def test_paramdetails(ncbi):
    names = ncbi.parametersDetails("matrix") 
    try:
        names = ncbi.parametersDetails("matrixddddd") 
        assert False
    except:
        assert True

@skiptravis
def test_run(ncbi):

    try:
        ncbi.jobid = ncbi.run(program="blastp", sequence=ncbi._sequence_example,
            stype="protein", database="uniprotkb")
        assert False # missing email argument
    except:
        assert True
    ncbi.jobid = ncbi.run(program="blastp", sequence=ncbi._sequence_example,
        stype="protein", database="uniprotkb", email="cokelaer@ebi.ac.uk",
        matrix="BLOSUM45")
    res = ncbi.getResult(ncbi.jobid, "out")

    res = ncbi.getResultTypes(ncbi.jobid)

def test_attributse(ncbi):
    ncbi.databases
