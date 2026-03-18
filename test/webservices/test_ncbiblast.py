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
    ncbi.get_parameter_details("matrix")
    with pytest.raises(Exception):
        ncbi.get_parameter_details("matrixddddd")


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(10)
def test_run(ncbi):

    with pytest.raises(Exception):
        ncbi.jobid = ncbi.run(
            program="blastp", sequence=ncbi._sequence_example, stype="protein", database="uniprotkb_viruses"
        )  # missing email argument
    ncbi.jobid = ncbi.run(
        program="blastp",
        sequence=ncbi._sequence_example,
        stype="protein",
        database="uniprotkb_viruses",
        email="cokelaer@ebi.ac.uk",
        matrix="BLOSUM45",
    )
    ncbi.get_result(ncbi.jobid, "out")

    ncbi.get_result_types(ncbi.jobid)


def test_attributse(ncbi):
    ncbi.databases
