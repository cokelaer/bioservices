import os

import pytest

from bioservices import NCBIblast


@pytest.fixture
def ncbi():
    return NCBIblast()


def test_param(ncbi):
    ncbi.get_parameters()
    assert len(ncbi.parameters) > 0
    assert len(ncbi.parameters) > 0


def test_paramdetails(ncbi):
    names = ncbi.get_parameter_details("matrix")
    try:
        names = ncbi.get_parameter_details("matrixddddd")
        assert False
    except:
        assert True


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(10)
def test_run(ncbi):

    try:
        ncbi.jobid = ncbi.run(
            program="blastp", sequence=ncbi._sequence_example, stype="protein", database="uniprotkb_viruses"
        )
        assert False  # missing email argument
    except:
        assert True
    ncbi.jobid = ncbi.run(
        program="blastp",
        sequence=ncbi._sequence_example,
        stype="protein",
        database="uniprotkb_viruses",
        email="cokelaer@ebi.ac.uk",
        matrix="BLOSUM45",
    )
    res = ncbi.get_result(ncbi.jobid, "out")

    res = ncbi.get_result_types(ncbi.jobid)


def test_attributse(ncbi):
    ncbi.databases
