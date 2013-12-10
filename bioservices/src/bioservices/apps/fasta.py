from collections import OrderedDict

__all__ = ["FASTA", "MultiFASTA"]

class MultiFASTA(object):
    """Class to manipulate several several FASTA items 


    Here, we load only one FASTA (from P43408 accession entry)  but 
    you can load as many as you want.::

        >>> mf = MultiFASTA()
        >>> mf.load_fasta("P43408")

    You can then get back your accession entries as follows ::

        >>> mf.ids
        ['P43408']
    
    And the sequences in the same order::

        >>> mf.sequences
        ['MKNKVVVVTGVPGVGGTTLTQKTIEKLKEEGIEYKMVNFGTVMFEVAKEEGLVEDRDQMRKLDPDTQKRIQKLAGRKIAEMAKESNVIVDTHSTVKTPKGYLAGLPIWVLEELNPDIIVIVETSSDEILMRRLGDATRNRDIELTSDIDEHQFMNRCAAMAYGVLTGATVKIIKNRDGLLDKAVEELISVLK']

    Each FASTA is stored in :attr:`fasta`, which is a dictionary where each
    values is an instance of :class:`FASTA`::

        >>> print(mf._fasta["P43408"].fasta)
        >sp|P43408|KADA_METIG Adenylate kinase OS=Methanotorris igneus GN=adkA PE=1 SV=2
        MKNKVVVVTGVPGVGGTTLTQKTIEKLKEEGIEYKMVNFGTVMFEVAKEEGLVEDRDQMR
        KLDPDTQKRIQKLAGRKIAEMAKESNVIVDTHSTVKTPKGYLAGLPIWVLEELNPDIIVI
        VETSSDEILMRRLGDATRNRDIELTSDIDEHQFMNRCAAMAYGVLTGATVKIIKNRDGLL
        DKAVEELISVLK

    .. versionadded: 1.2.0 maybe merged with :class:`FASTA` class

    """
    def __init__(self):
        # fetch the sequence using this attribute
        self._fasta_fetcher = FASTA()

        # an ordered dictionary to store the fasta contents
        self._fasta = OrderedDict()

    def _get_fasta(self):
        return self._fasta
    fasta = property(_get_fasta, doc="Returns all FASTA instances ")

    def _get_ids(self):
        return [f for f in self._fasta.keys()]
    ids = property(_get_ids, doc="returns list of keys/accession identifiers")

    def _get_sequences(self):
       return [f.sequence for f in self._fasta.values()]
    sequences = property(_get_sequences, doc="returns list of sequences")

    def load_fasta(self, id_):
        """Loads a single FASTA file into the dictionary

        """
        fasta = self._fasta_fetcher.get_fasta(id_)

        # create a new instance of FASTA and save fasta data
        f = FASTA()
        f._fasta = fasta

        # append in the ordered dictionary
        self._fasta[id_] = f

    def save_fasta(self, filename):
        """Save all FASTA into a file"""
        fh = open(filename, "w")
        for f in self._fasta.itervalues():
            fh.write(f.fasta)
        fh.close()

    def read_fasta(self, filename):
        """Loads several FASTA from a filename"""

        fh = open(filename, "r")
        data = fh.read()
        # we split according to ">sp|" so first element is empty and should
        # be ignored
        for thisfasta in data.split(">sp|")[1:]:
            f = FASTA()
            f._fasta = ">ap|" + thisfasta
            self._fasta[f.accession] = f

        return data


class FASTA(object):
    """Dedicated class to a unique FASTA sequence

    .. doctest::

        >>> from bioservices.apps.fasta import FASTA
        >>> f = FASTA()
        >>> f.load("P43403")
        >>> acc =f.accession    # the accession (P43403)
        >>> fasta = f.fasta     # raw FASTA string
        >>> seq = f.sequence    # the sequence itself

    .. seealso:: :class:`MultiFASTA` for multi FASTA manipulation.
    .. addedversion: 1.2.0 maybe merged with :class:`MulitFASTA` class

    """

    def __init__(self):
        self._fasta = None

    def _get_fasta(self):
        return self._fasta
    fasta = property(_get_fasta, doc="returns FASTA content")

    def _get_sequence(self):
        if self.fasta:
            return "".join(self.fasta.split("\n")[1:])
        else:
            raise ValueError("You need to load a fasta sequence first using get_fasta or read_fasta")
    sequence = property(_get_sequence, doc="returns the sequence only")

    def _get_header(self):
        if self.fasta:
            return self.fasta.split("\n")[0]
        else:
            raise ValueError("You need to load a fasta sequence first using get_fasta or read_fasta")
    header = property(_get_header, doc="returns header only")

    def _get_accession(self):
        return self.header.split("|")[1]
    accession = property(_get_accession, doc="returns accession only")

    def _get_entry(self):
         return self.header.split("|")[2].split(" ")[0]
    entry = property(_get_entry, doc="returns entry only")

    def _get_gene_name(self):
        index = self.header.index("GN=")
        return self.header[index:].split(" ")[0]
    gene_name = property(_get_gene_name, 
        doc="returns gene name from GN keyword found in the header")

    def __str__(self):
        str_ = self.fasta
        return str_

    def get_fasta(self, id_):
        """Fetches FASTA from uniprot and loads into attrbiute :attr:`fasta`
        
        :param str id_: a given uniprot identifier
        :returns: the FASTA contents

        
        """
        from bioservices import UniProt
        u = UniProt(verbose=False)
        res = u.searchUniProtId(id_, format="fasta")
        self._fasta = res[:]
        return res

    def load_fasta(self, id_):
        """Fetches FASTA from uniprot and loads into attribute :attr:`fasta`

        :param str id_: a given uniprot identifier
        :returns: nothing

        .. note:: same as :meth:`get_fasta` but returns nothing
        """
        # save fasta into attributes fasta
        res = self.get_fasta(id_)

    def save_fasta(self, data, filename):
        """Save FASTA file into a filename
        
        :param str data: the FASTA contents
        :param str filename: where to save it
        """
        fh = open(filename, "w")
        fh.write(data)
        fh.close()

    def read_fasta(self, filename):
        """Reads a FASTA file and loads it
        
        Type::

            f = FASTA()
            f.read_fasta(filename)
            f.fasta

        :return: nothing
       
        .. warning:: If more than one FASTA is contained in the file, an error is raised
        """
        fh = open(filename, "r")
        data = fh.read()
        fh.close()
        if data.count(">sp|")>1:
            raise ValueError("""It looks like your FASTA file contains more than
            one FASTA. You must use MultiFASTA class instead""")
            self._fasta = data[:]

