from bioservices import BioDBNet

inputValues = 'ENSG00000121410, ENSG00000171428'

def test_db2db():
    b = BioDBNet()
    b.db2db("UniProt Accession", "Gene ID", "P43403")

    
def test_dbfind():
    b = BioDBNet()
    b.dbFind("Ensembl Gene ID", ['ENSG00000121410', 'ENSG00000171428'])
   

def test_dbortho():
    b = BioDBNet()
    pass


def test_dbReport():
    #b.dbReport("UniProt Accession", "P43403")
    pass

def test_dbWalk():
    b = BioDBNet()
    b.dbWalk('Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID', "ENSG00000121410", 9606)




