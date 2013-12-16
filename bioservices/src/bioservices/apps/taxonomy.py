from bioservices import *
from easydev import Logging

try:
    import pandas as pd
except:
    pass


__all__ = ["Taxon"]

class Taxon(Logging):
    """Utility to search for information related to a taxon
    
    Uses HGNC service to fetch information about a taxon.
    ::

        >>> from bioservices.apps.taxonomy import Taxon
        >>> t = Taxon()
        >>> t.search_by_taxon("9606")
        {'Scientific Name': 'Homo sapiens', 'taxon': '9606'}

    You can also pop up the Uniprot page using::

        t.uniprot_onweb("9606")


    A full list of taxons is available here::
    
        http://www.uniprot.org/taxonomy/?query=*&format=*


    .. versionadded:: 1.2.0
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


