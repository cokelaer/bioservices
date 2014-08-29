from bioservices import BioDBNet

inputValues = 'ENSG00000121410, ENSG00000171428'

def test_db2db():
    b = BioDBNet(verbose=False)
    b.db2db("UniProt Accession", "Gene ID", "P43403")
    b.dbFind("Ensembl Gene ID", ['ENSG00000121410', 'ENSG00000171428'])
    df = b.dbReport("UniProt Accession", "P43403")
    b.dbWalk('Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID', "ENSG00000121410", 9606)




