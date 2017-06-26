from bioservices import BioDBNet
from nose.plugins.attrib import attr


class test_biodbnet(object):
    @classmethod
    def setup_class(klass):
        klass.s = BioDBNet(verbose=False)

    def test_db2db(self):
        df = self.s.db2db("UniProt Accession", "Gene ID", "P43403")
        assert df.ix['P43403'].values[0] == "7535"

    def test_dbfind(self):        
        df = self.s.dbFind("Gene ID", ["ZMYM6_HUMAN", "NP_710159", "ENSP00000305919"])
        assert len(df["Gene ID"]) == 3

    def test_Ortho(self):
        df = self.s.dbOrtho("Gene Symbol", "Gene ID", ["MYC", "MTOR", "A1BG"],
                           input_taxon=9606, output_taxon=10090)
        df.loc['MYC'].values[0] == "17869"

    @attr('slow')
    def test_dbreport(self):
        self.s.dbReport("UniProt Accession", "P43403")

    @attr('slow')
    def test_dbwalk(self):
        self.s.dbWalk('Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID', 
            "ENSG00000121410", 9606)

    def test_extra(self):
        self.s.getDirectOutputsForInput("Gene Symbol")
        self.s.getDirectOutputsForInput("genesymbol")
        self.s.getInputs()
        self.s.getOutputsForInput("Uniprot Accession")
