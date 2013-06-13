from bioservices import *




class test_psicquic(PSICQUIC):
    def __init__(self):
        super(test_psicquic, self).__init__(verbose=False)

    def test_read_registry(self):
        self.read_registry()

    def test_print_status(self):
        self.print_status()

    def test_registry(self):
        N1 = len(self.registry_names)
        N2 = len(self.registry_versions)
        N2 = len(self.registry_restricted)
        assert N1 == N2

    def test_query(self):

        self.query("intact", "brca2", "tab27")
        self.query("intact", "zap70", "xml25")
        self.query("matrixdb", "*", "xml25")
        try:
            self.query("matxdb", "*", "xml25")
            assert False
        except:
            assert True


        self.query("matrixdb", "*", "xml25", firstResult=10, maxResults=10)

        # accessing the string DB
        self.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25")


def test_appsPPI():
    p = psicquic.AppsPPI(verbose=False)
    p.queryAll("ZAP70", ["intact"])
    p.summary()

