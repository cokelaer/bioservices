
from bioservices import UniProt

class Peptides(object):
    """
    
    ::

        >>> p = Peptides()
        >>> p.get_phosphosite_position("Q8IYB3", "VPKPEPIPEPKEPSPE")
        189

    """
    def __init__(self):

        self.u = UniProt()

    def get_fasta(self, uniprot_name):
        seq = self.u.get_fasta(uniprot_name)
        return seq

    def get_phosphosite_position(self, uniprot_name, peptide):
        fasta = self.get_fasta(uniprot_name)
        if peptide in fasta:
            return fasta.index(peptide)
        else:
            return -1


