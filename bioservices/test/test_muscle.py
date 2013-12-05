from bioservices.muscle import MUSCLE
from bioservices import uniprot


def test_muscle():
    m = MUSCLE(verbose=False)
    m.parameters
    m.parametersDetails("format")


    u = uniprot.UniProt(verbose=False)
    f1 = u.searchUniProtId("P18812",format="fasta")
    f2 = u.searchUniProtId("P18813",format="fasta")


    jobid = m.run(format="fasta", sequence=f1+f2, email="cokelaer@ebi.ac.uk")
    m.getStatus(jobid)
    m.wait(jobid)

    m.getResultTypes(jobid)
    m.getResult(jobid, 'phylotree')

