from bioservices import HGNC
from nose.plugins.attrib import attr


@attr('fixme')
class test_hgnc():

    def __init__(self):
        self.s = HGNC(verbose=False)

    @attr('skip')
    def test_get_xml(self):
        xml = self.s.get_xml("ZAP70")
        xml = self.s.get_xml("ZAP70;INSR")
        assert len(xml.findAll("gene")) == 2
        self.s.get_xml("wrong")

    @attr('skip')
    def test_aliases(self):
        assert self.s.get_aliases("ZAP70") == [u'ZAP-70', u'STD']
        self.s.get_name("ZAP70")
        self.s.get_chromosome("ZAP70")
        self.s.get_previous_symbols("ZAP70")
        self.s.get_withdrawn_symbols("ZAP70")
        self.s.get_previous_names("ZAP70")



    @attr('skip')
    def test_xref(self):
        assert self.s.get_xrefs("ZAP70")['UniProt']['xkey'] == 'P43403'
        assert self.s.get_xrefs("ZAP70", "xml")['UniProt']['link'] == ['http://www.uniprot.org/uniprot/P43403.xml']

    @attr('skip')
    def test_lookfor(self):    
        self.s.lookfor("ZAP70")

    @attr('skip')
    def test_mapping(self):
        value = "UniProt:P43403"
        res = self.s.mapping(value)
        res[0]['xlink:title'] == "ZAP70"



