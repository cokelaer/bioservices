from bioservices import picr
import unittest


class TestPICR(object):

    @classmethod
    def setup_class(klass):
        klass.e = picr.PICR(verbose=False)

    #def __init__(self):
    #    super(TestPICR, self).__init__(verbose=False)


    def test_getUPIForSequence(self):
        res = self.e.getUPIForSequence(self.e._sequence_example, ["IPI", "ENSEMBL", "SWISSPROT"])
        res = self.e.getUPIForSequence(self.e._sequence_example, "SWISSPROT", taxid="9606")
        res = self.e.getUPIForSequence(self.e._sequence_example, "SWISSPROT", onlyactive=False, includeattributes=False)
        print res

    def test_databases(self):
        assert len(self.e.databases)>0

    def test_MappedDB(self):
        #res = xmltools.easyXML(res)
        self.e.getMappedDatabaseNames()

    def test_checkDB(self):
        self.e._checkDBname("IPI")
        try:
            self.e._checkDBname("dummy")
            assert False
        except:
            assert True

    def test_getUPIForAccession(self):
        self.e.getUPIForAccession(self.e._accession_example, ["SWISSPROT"])
        self.e.getUPIForAccession(self.e._accession_example, "SWISSPROT", taxid="9606")
        res = self.e.getUPIForAccession(self.e._accession_example, "SWISSPROT", onlyactive=False, includeattributes=False)

    # this one is failing from time to time even the exemple on the web site.
    @unittest.skip
    def _test_getUPIForBLAST(self):
        self.e.getUPIForBLAST(self.e._blastfrag_example, "SWISSPROT", taxid="9606")
        self.e.getUPIForBLAST(self.e._blastfrag_example, ["SWISSPROT"], taxid="9606", includeattributes=False)
        self.e.getUPIForBLAST(self.e._blastfrag_example, ["SWISSPROT"], taxid="9606", program="blastp",matrix="BLOSUM62")
