from bioservices import UniProt


class Mapping(object):
    """


        Could use unichem, uniprot, kegg, chembldb
        Could be HGNC


    """


    def __init__(self):
        self._uniprot = UniProt()
        self._mapping['uniprot'] = self._uniprot._mapping
        self.databases = {}

    def map(self):
        pass

    def search(self):
        pass
