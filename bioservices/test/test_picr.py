from bioservices import picr



class TestPICR(picr.PICR):

    def __init__(self):
        super(TestPICR, self).__init__()


    def test_getUPIForSequence(self):
        res = self.getUPIForSequence(self._sequence_example, ["IPI", "ENSEMBL", "SWISSPROT"])
        res = self.getUPIForSequence(self._sequence_example, "SWISSPROT")
        print res

    def test_databases(self):
        assert len(self.databases)>0

    def test_MappedDB(self):
        self.getMappedDatabaseNames()


    def test_getUPIForAccession(self):
        self.getUPIForAccession(self._accession_example, ["SWISSPROT"])
        self.getUPIForAccession(self._accession_example, "SWISSPROT")

    def test_getUPIForBLAST(self):
        self.getUPIForBLAST(self._blastfrag_example, "SWISSPROT",program="blastp",matrix="BLOSUM62")
        self.getUPIForBLAST(self._blastfrag_example, "SWISSPROT")
