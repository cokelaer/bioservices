import os

import pytest

from bioservices import uniprot
from bioservices.muscle import MUSCLE


@pytest.mark.xfail(reason="too slow")
@pytest.mark.timeout(10)
def test_muscle():
    m = MUSCLE(verbose=False)
    m.parameters
    m.get_parameter_details("format")
    try:
        m.get_parameter_details("formattt")
        assert False
    except:
        assert True

    u = uniprot.UniProt(verbose=False)
    f1 = u.get_fasta("P18812")
    f2 = u.get_fasta("P18813")

    jobid = m.run(frmt="fasta", sequence=f1 + f2, email="cokelaer@ebi.ac.uk")
    m.get_status(jobid)
    m.wait(jobid)

    m.get_result_types(jobid)
    m.get_result(jobid, "phylotree")
