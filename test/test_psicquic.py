from bioservices import PSICQUIC, psicquic
from nose.plugins.attrib import attr


@attr('slow')
class test_psicquic(object):
    @classmethod
    def setup_class(klass):
        klass.s = PSICQUIC(verbose=False)


    def test_read_registry(self):
        self.s.read_registry()

    def test_print_status(self):
        self.s.print_status()

    def test_registry(self):
        N1 = len(self.s.registry_names)
        N2 = len(self.s.registry_versions)
        N2 = len(self.s.registry_restricted)
        assert N1 == N2

    def test_query(self):
        if 'intact' not in self.s.activeDBs or 'matrixdb' not in self.s.activeDBs:
            return

        self.s.query("intact", "brca2", "tab27")
        self.s.query("intact", "zap70", "xml25")
        self.s.query("matrixdb", "*", "xml25")
        try:
            self.s.query("matxdb", "*", "xml25")
            assert False
        except:
            assert True

        self.s.query("matrixdb", "*", "xml25", firstResult=10, maxResults=10)

        # accessing the string DB
        if 'string' in self.s.activeDBs:
            self.s.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25")

@attr('fixme')
def test_appsPPI():
    p = psicquic.AppsPPI(verbose=False)
    p.queryAll("ZAP70", ["intact"])
    p.summary()

