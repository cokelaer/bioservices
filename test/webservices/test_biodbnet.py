import pytest

from bioservices import BioDBNet


@pytest.fixture(scope="module")
def b():
    return BioDBNet(verbose=False)


# ------------------------------------------------------------------
# Discovery methods
# ------------------------------------------------------------------


def test_getInputs(b):
    inputs = b.getInputs()
    assert isinstance(inputs, list)
    assert len(inputs) > 0
    assert "UniProt Accession" in inputs


def test_getOutputsForInput(b):
    outputs = b.getOutputsForInput("UniProt Accession")
    assert isinstance(outputs, list)
    assert "Gene Symbol" in outputs


def test_getDirectOutputsForInput(b):
    direct = b.getDirectOutputsForInput("Gene Symbol")
    assert isinstance(direct, list)
    assert len(direct) > 0
    # normalised alias also works
    direct2 = b.getDirectOutputsForInput("genesymbol")
    assert isinstance(direct2, list)


def test_check_db_invalid(b):
    with pytest.raises(ValueError):
        b._check_db("NotADatabase_xyz")


# ------------------------------------------------------------------
# Conversion methods
# ------------------------------------------------------------------


def test_db2db(b):
    df = b.db2db("UniProt Accession", "Gene ID", "P43403")
    assert df.loc["P43403"].values[0] == "7535"


def test_db2db_multiple_outputs(b):
    df = b.db2db("UniProt Accession", ["Gene ID", "Gene Symbol"], "P43403")
    assert "Gene ID" in df.columns
    assert "Gene Symbol" in df.columns
    assert df.loc["P43403", "Gene Symbol"] == "ZAP70"


def test_db2db_multiple_inputs(b):
    df = b.db2db("Ensembl Gene ID", ["Gene Symbol"], ["ENSG00000121410", "ENSG00000171428"], taxon=9606)
    assert "ENSG00000121410" in df.index
    assert "ENSG00000171428" in df.index


@pytest.mark.xfail(reason="too slow on CI")
@pytest.mark.timeout(10)
def test_dbfind(b):
    df = b.dbFind("Gene ID", ["ZMYM6_HUMAN", "NP_710159", "ENSP00000305919"])
    assert len(df["Gene ID"]) == 3


def test_dbOrtho(b):
    df = b.dbOrtho("Gene Symbol", "Gene ID", ["MYC", "MTOR", "A1BG"], input_taxon=9606, output_taxon=10090)
    assert "Gene ID" in df.columns
    assert "17869" in df.loc["MYC", "Gene ID"].split("//")


def test_dbReport(b):
    df = b.dbReport("UniProt Accession", ["P43403"])
    assert "Gene Symbol" in df.columns
    assert "P43403" in df.index


def test_dbWalk(b):
    path = "Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID"
    df = b.dbWalk(path, ["ENSG00000121410"], taxon=9606)
    assert len(df) > 0
