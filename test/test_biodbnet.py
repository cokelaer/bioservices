from bioservices import BioDBNet
from nose.plugins.attrib import attr

@attr('skip_travis')
class test_biodbnet(object):
    @classmethod
    def setup_class(klass):
        klass.s = BioDBNet(verbose=False)

    def test_db2db(self):
        self.s.db2db("UniProt Accession", "Gene ID", "P43403")



    def test_dbfind(self):
        inputValues = 'ENSG00000121410, ENSG00000171428'
        self.s.dbFind("Ensembl Gene ID", inputValues)

    @attr('slow')
    def test_dbreport(self):
       self.s.dbReport("UniProt Accession", "P43403")

    def test_dbwald(self):
        self.s.dbWalk('Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID', "ENSG00000121410", 9606)




