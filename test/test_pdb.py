from bioservices import PDB


pdb = PDB(verbose=False)



def test_pdb():
    res = pdb.get_file("1FBV", "pdb")
    res = pdb.get_file("1FBV", "xml", compression=True)
    res = pdb.get_file("1FBV", "cif")
    ids = pdb.get_current_ids()

def test_ligands():
    '4HHB' in pdb.get_ligands("4HHB")

# FIXME
def _test_get_xml_query():
    query = """<?xml version="1.0" encoding="UTF-8"?>
<orgPdbQuery>
<version>B0907</version>
<queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
<description>Experimental Method Search : Experimental Method=SOLID-STATE NMR</description>
<mvStructure.expMethod.value>SOLID-STATE NMR</mvStructure.expMethod.value>
</orgPdbQuery>
"""
    res = pdb.get_xml_query(query)
    assert len(res.split("\n"))>10


def test_get_ligand_info():
    pdb.get_ligand_info("4HHV")

def test_get_go_terms():
    pdb.get_go_terms("4HHV")
