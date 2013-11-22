from bioservices import *
from easydev import Logging
import pandas as pd


class Taxon(Logging):
    """Utility to search for information related to a taxon
    
    Uses HGNC service to fetch information about a taxon.

        from bioservices.mapping.mappers import Taxon
        t = Taxon()
        t.search_by_taxon("9606")
        {'Scientific Name': 'Homo sapiens', 'taxon': '9606'}

    You can also pop up the Uniprot page using::

        t.uniprot_onweb("9606")


    A full list of taxons is available here::
    
        http://www.uniprot.org/taxonomy/?query=*&format=*


    """
    def __init__(self):
        super(Taxon, self).__init__("INFO")
        self.df = pd.DataFrame(index=[], columns=["Taxon", "Scientific Name"])
        self._eutils_service = EUtils()

    def search_by_taxon(self, taxon):
        """
        should be a string without comma (only one entry accepted")
        """
        assert isinstance(taxon,str)
        assert "," not in taxon
        ret = self._eutils_service.taxonomy(taxon)
        if ret == "\n":
            #nothing found
            pass
        else:
            res = {'taxon':taxon, 'Scientific Name':ret.Taxon.ScientificName}
            #self.df.append(res)
            return res

    def info(self, taxon, lineage=False):
        """Prints information about a Taxon

        :param str taxon: taxon identifier 
        :param bool lineage: prints lineage is set to True
        """
        ret = self._eutils_service.taxonomy(taxon)
        print("Display Name: %s" % ret.Taxon.OtherNames.Name.DispName)
        print("GenBank Common name: %s" % ret.Taxon.OtherNames.GenbankCommonName)
        print("Taxon Id: %s " % ret.Taxon.TaxId)
        if lineage:
            print("Lineage:")
            for i,x in enumerate(ret.Taxon.Lineage.split(";")):
                print(i*" "+x)

    def uniprot_onweb(self, taxon):
        """Open Uniprot taxonomy page for a given taxon

        :param str taxon: taxon identifier 
        """
        import webbrowser
        import urllib2
        try:
            urllib2.urlopen('http://www.uniprot.org/taxonomy/%s' % taxon)
            webbrowser.open("http://www.uniprot.org/taxonomy/%s" % taxon)
        except urllib2.HTTPError, e:
            print("Invalid taxon")
        except urllib2.URLError, e:
            print(e.args)


class Mapper(Logging):
    """Accepted code:

        uniprot

    """
    def __init__(self, verbosity="INFO"):
        super(Mapper, self).__init__(level=verbosity)
        self.logging.info("Initialising the services")
        self.logging.info("... uniprots")
        self._uniprot_service = UniProt()
        self.logging.info("... KEGG")
        self._kegg_service = Kegg()
        self.logging.info("... HGNC")
        self._hgnc_service = HGNC()
        self.logging.info("... UniChem")
        self._unichem_service = UniChem()
        self.logging.debug


        self.df = pd.DataFrame()

    def build_mapping(self):
        # build mapping using HGNC
        self.logging.info("Retrieving all information from HGNC")
        res = h.mapping_all()
        mapping = [(c,res[c]['UniProt']['xkey']) if'UniProt' in res[c].keys() else (c, None) for c in res.keys()]

        df = pd.DataFrame(mapping, columns=['HGNC', 'UniProt'])
        self.df.append(df, ignore_index=True)

    def _check_uniprot_id(self):
        raise NotImplementedError

    def get_hgnc_from_uniprot(self, id_):
        return self._hgnc.mapping("UniProt:" + id_)

    def lookfor(self, name):
        res = {}
        res['request'] = name

        self.logging.info("calling HGNC service")
        thisres = self._hgnc_service.lookfor("ZAP")
        acc = [x['acc'] for x in thisres]
        res['hgnc'] = acc
        #[{u'acc': u'HGNC:12858',
        #      u'xlink:href': u'/HGNC/wr/gene/ZAP70',
        #        u'xlink:title': u'ZAP70'}]

        self.logging.info("calling uniprot service")
        thisres = self._uniprot_service.search("ZAP")
        print thisres        

    def entrez2uniprotID(name, mapper=None):
        """name must be a valid uniprot ID"""
        self._uniprot_service.mapping(to="P_ENTREZGENEID", fr="ID", query=name)

    def entrez2uniprotACC(name, mapper=None):
        """name must be a valid uniprot ID"""
        self._uniprot_service.mapping(to="P_ENTREZGENEID", fr="ACC", query=name)

    def kegg2acc(name, mapper=None):
        """name must be a valid uniprot ID"""
        if mapper == None:
            mapper = UniProt()
        return self._uniprot_service.mapping(fr="KEGG_ID", to="ACC", query=name)

    def uniprot2hugo(self, name):
        return self._uniprot_service.mapping(fr="ACC", to="HGNC_ID", query=name)

    def uniprot2refseq(self, name):
        """

        There are 2 refseq alias: REFSEQ_NT_ID and P_REFSEQ_AC.

        Here, we use the first one to agree with wikipedia
        http://en.wikipedia.org/wiki/Protein_Kinase_B

        """
        return self._uniprot_service.mapping(fr="ACC", to="REFSEQ_NT_ID", query="P31749")

    def kegg2uniprot_kegg(self, name):
        return self._kegg_service.conv("uniprot", name)

    def uniprot2kegg_kegg(self, name):
        """name must be a valid uniprot ID"""
        return self._kegg_service.conv("hsa", "up:" + name)




