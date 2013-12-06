
from bioservices import UniProt

class Peptides(object):
    """
    
    ::

        >>> p = Peptides()
        >>> p.get_fasta_sequence("Q8IYB3")
        >>> p.get_phosphosite_position("Q8IYB3", "VPKPEPIPEPKEPSPE")
        189


    Sometimes, peptides are provided with a pattern indicating the phospho site.
    e.g., ::

        >>>

    """
    def __init__(self, verbose=False):

        self.u = UniProt(verbose=verbose)

    def get_fasta_sequence(self, uniprot_name):
        seq = self.u.get_fasta_sequence(uniprot_name)
        return seq

    def get_phosphosite_position(self, uniprot_name, peptide):
        fasta = self.get_fasta_sequence(uniprot_name)
        if peptide in fasta:
            return fasta.index(peptide)
        else:
            return -1

    



