from bioservices import BioDBNet
import pytest


@pytest.fixture
def biodbnet():
    return BioDBNet(verbose=False)

@pytest.mark.xfail
def test_db2db(biodbnet):
    df = biodbnet.db2db("UniProt Accession", "Gene ID", "P43403")
    assert df.loc['P43403'].values[0] == "7535"

@pytest.mark.xfail
def test_dbfind(biodbnet):        
    df = biodbnet.dbFind("Gene ID", ["ZMYM6_HUMAN", "NP_710159", "ENSP00000305919"])
    assert len(df["Gene ID"]) == 3

@pytest.mark.xfail
def test_Ortho(biodbnet):
    df = biodbnet.dbOrtho("Gene Symbol", "Gene ID", ["MYC", "MTOR", "A1BG"],
                       input_taxon=9606, output_taxon=10090)
    df.loc['MYC'].values[0] == "17869"


# SLOW FIXME
def _test_dbreport(biodbnet):
    biodbnet.dbReport("UniProt Accession", "P43403")

@pytest.mark.xfail
def test_dbwalk(biodbnet):
    biodbnet.dbWalk('Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID', 
        "ENSG00000121410", 9606)

@pytest.mark.xfail
def test_extra(biodbnet):
    biodbnet.getDirectOutputsForInput("Gene Symbol")
    biodbnet.getDirectOutputsForInput("genesymbol")
    biodbnet.getInputs()
    biodbnet.getOutputsForInput("Uniprot Accession")
