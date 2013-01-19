from bioservices import picr



class TestPICR(picr.PICR):

    def __init__(self):
        super(TestPICR, self).__init__(verbose=False)


    def test_getUPIForSequence(self):
        res = self.getUPIForSequence(self._sequence_example, ["IPI", "ENSEMBL", "SWISSPROT"])
        res = self.getUPIForSequence(self._sequence_example, "SWISSPROT", taxid="9606")
        res = self.getUPIForSequence(self._sequence_example, "SWISSPROT", onlyactive=False, includeattributes=False)
        print res

    def test_databases(self):
        assert len(self.databases)>0

    def test_MappedDB(self):
        #res = xmltools.easyXML(res)
        self.getMappedDatabaseNames()

    def test_checkDB(self):
        self._checkDBname("IPI")
        try:
            self._checkDBname("dummy")
            assert False
        except:
            assert True

    def test_getUPIForAccession(self):
        self.getUPIForAccession(self._accession_example, ["SWISSPROT"])
        self.getUPIForAccession(self._accession_example, "SWISSPROT", taxid="9606")
        res = self.getUPIForAccession(self._accession_example, "SWISSPROT", onlyactive=False, includeattributes=False)

    def test_getUPIForBLAST(self):
        self.getUPIForBLAST(self._blastfrag_example, "SWISSPROT", taxid="9606")
        self.getUPIForBLAST(self._blastfrag_example, ["SWISSPROT"], taxid="9606", includeattributes=False)
        self.getUPIForBLAST(self._blastfrag_example, ["SWISSPROT"], taxid="9606", program="blastp",matrix="BLOSUM62")
