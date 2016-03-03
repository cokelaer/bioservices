from bioservices.muscle import MUSCLE
from bioservices import uniprot
from nose.plugins.attrib import attr


@attr('skip_travis')
def test_muscle():
    m = MUSCLE(verbose=False)
    m.parameters
    m.getParametersDetails("format")


    u = uniprot.UniProt(verbose=False)
    f1 = u.get_fasta("P18812")
    f2 = u.get_fasta("P18813")


    jobid = m.run(frmt="fasta", sequence=f1+f2, email="cokelaer@ebi.ac.uk")
    m.getStatus(jobid)
    m.wait(jobid)

    m.getResultTypes(jobid)
    m.getResult(jobid, 'phylotree')

