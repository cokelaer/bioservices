from bioservices import PDB


class test_PDB(PDB):
                                               
    @classmethod
    def setup_class(klass):
        klass.s = PDB(verbose=False)



    def test_pdb(self):
        res = self.s.get_file("1FBV", "pdb")
        res = self.s.get_file("1FBV", "xml", compression=True)
        res = self.s.get_file("1FBV", "cif")
    
        ids = self.s.get_current_ids()

    def test_ligands(self):
        '4HHB' in self.s.get_ligands("4HHB")

    def get_xml_query(self):
        query = """<?xml version="1.0" encoding="UTF-8"?>
<orgPdbQuery>
<version>B0907</version>
<queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
<description>Experimental Method Search : Experimental Method=SOLID-STATE NMR</description>
<mvStructure.expMethod.value>SOLID-STATE NMR</mvStructure.expMethod.value>
</orgPdbQuery>
"""
        res = self.s.get_xml_query(query)
        assert len(res.split("\n"))>10



