from bioservices import UniProt
import re

class Peptides(object):
    """

    ::

        >>> p = Peptides()
        >>> p.get_fasta_sequence("Q8IYB3")
        >>> p.get_peptide_position("Q8IYB3", "VPKPEPIPEPKEPSPE")
        189


    Sometimes, peptides are provided with a pattern indicating the phospho site.
    e.g., ::

        >>>

    """
    def __init__(self, verbose=False):
        self.u = UniProt(verbose=verbose)
        self.sequences = {}

    def get_fasta_sequence(self, uniprot_name):
        seq = self.u.get_fasta_sequence(uniprot_name)
        return seq

    def get_phosphosite_position(self, uniprot_name, peptide):
        if uniprot_name not in self.sequences.keys():
            seq = self.get_fasta_sequence(uniprot_name)
            self.sequences[uniprot_name] = seq[:]
        else:
            seq = self.sequences[uniprot_name][:]
        positions = [x.start() for x in re.finditer("PQS", seq)]
        return positions





