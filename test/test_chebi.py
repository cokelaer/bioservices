from bioservices import ChEBI





def test_chebi():
    ch = ChEBI()
    ch.getCompleteEntity("CHEBI:10102")
    res = ch.conv("CHEBI:10102", "KEGG COMPOUND accession")
    assert res == ['C07484']

    try:
        res = ch.conv("CHEBI:10102", "wrong db")
        assert False
    except:
        assert True

    ch.getOntologyChildren("CHEBI:27732")
    ch.getOntologyParents("CHEBI:27732")
    ch.getUpdatedPolymer("CHEBI:27732")

def test_chebi_mass():
    ch = ChEBI()
    mass1 = ch.getCompleteEntity("CHEBI:27732").mass
    assert float(mass1) == 194.19076

    res = ch.getLiteEntity("194.19076", "MASS", 5, 2)
    assert  res[0]["chebiId"] == "CHEBI:27732"

    # should return nothing
    res = ch.getLiteEntity("194.19076", "SMILES", 5, 2)

def test_polymer():
    ch = ChEBI()
    x = ch.serv.getUpdatedPolymer("CHEBI:27732")
    x.chebiId
    #Out[14]: 27732
    x.globalCharge
    #0
    x.globalFormula
    # C8H10N4O2
    x.updatedStructure

def test_completelist():
    ch = ChEBI()
    names = [x.chebiAsciiName for x in ch.getCompleteEntityByList(["CHEBI:27732","CHEBI:36707"])]

    names = [str(x) for x in names]
    assert names == ["caffeine", "2-acetyl-1-alkyl-sn-glycero-3-phosphocholine"]

def test_search():
    ch = ChEBI()
    smiles = ch.getCompleteEntity("CHEBI:27732").smiles
    ch.serv.getStructureSearch(smiles, "SMILES", "SIMILARITY", 3, 0.25)

def test_ontology():
    ch = ChEBI()
    ch.getAllOntologyChildrenInPath("CHEBI:27732", "has part")

def test_structure():
    ch = ChEBI()
    smiles = ch.getCompleteEntity("CHEBI:27732").smiles
    ch.getStructureSearch(smiles, "SMILES", "SIMILARITY", 3, 0.25)

