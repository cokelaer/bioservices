from bioservices import EUtils, Ensembl


__all__ = ["Taxon"]

class Taxon(object):
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
        super(Taxon, self).__init__()
        # self.df = pd.DataFrame(index=[], columns=["Taxon", "Scientific Name"])
        self._eutils_service = EUtils()
        self._ensembl_service = Ensembl() # there is a search by name, easier to use than EUtils


    def search_by_name(self, name):
        """using ensembl, tries to get the taxon identifier from the given  name

        ::

            >>> s.search_by_name('mouse')
            10090

        """
        res = self._ensembl_service.get_taxonomy_name("mouse")[0]
        try:
            return res['id']
        except:
            return res

    def search_by_taxon(self, taxon):
        """
        should be a string without comma (only one entry accepted")
        """
        assert isinstance(taxon, str)
        assert "," not in taxon
        ret = self._eutils_service.taxonomy(taxon)
        if ret == "\n":
            # nothing found
            pass
        else:
            res = {'taxon': taxon, 'Scientific Name': ret.Taxon[0].ScientificName}
            # self.df.append(res)
            return res

    def info(self, taxon, lineage=False):
        """Prints information about a Taxon

        :param str taxon: taxon identifier
        :param bool lineage: prints lineage is set to True
        """
        ret = self._eutils_service.taxonomy(taxon)
        print("Display Name: %s" % ret.Taxon[0].OtherNames.Name.DispName)
        print("GenBank Common name: %s" % ret.Taxon[0].OtherNames.GenbankCommonName)
        print("Taxon Id: %s " % ret.Taxon[0].TaxId)
        if lineage:
            print("Lineage:")
            for i, x in enumerate(ret.Taxon[0].Lineage.split(";")):
                print(i*" "+x)

    def uniprot_onweb(self, taxon):
        """Open Uniprot taxonomy page for a given taxon

        :param str taxon: taxon identifier
        """
        import webbrowser
        try:
            from urllib.request import urlopen
            from urllib.error import HTTPError, URLError
        except:
            from urllib2 import urlopen, HTTPError, URLError
        try:
            urlopen('http://www.uniprot.org/taxonomy/%s' % taxon)
            webbrowser.open("http://www.uniprot.org/taxonomy/%s" % taxon)
        except HTTPError as err:
            print("Invalid taxon")
        except URLError as err:
            print(err.args)

