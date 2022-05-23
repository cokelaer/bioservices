#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2020 - EBI-EMBL - Institut Pasteur
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://bioservices.readthedocs.io
#
##############################################################################
"""Interface to the PDBe web Service.

.. topic:: What is PDBe ?

    :URL: https://www.ebi.ac.uk/pdbe/
    :REST: https://www.ebi.ac.uk/pdbe/api/doc/

    .. highlights::

        PDBe is a founding member of the Worldwide Protein Data Bank which
        collects, organises and disseminates data on biological macromolecular
        structures. In collaboration with the other Worldwide Protein Data Bank (wwPDB)
        partners, we work to collate, maintain and provide access to the global
        repository of macromolecular structure models, the Protein Data Bank (PDB).

        -- PDBe home page, June 2020

"""

from bioservices.services import REST

__all__ = ["PDBe"]


class PDBe:
    """Interface to part of the `PDBe <http://www.ebi.ac.uk/pdbe>`_ service

    .. doctest::

        >>> from bioservices import PDBe
        >>> s = PDBe()
        >>> res = s.get_file("1FBV", "pdb")

    """

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages (default is off)

        """
        url = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/"
        self.services = REST(name="PDBe", url=url, verbose=verbose, cache=cache)

    def _check_id(self, pdbid):
        if isinstance(pdbid, list):
            pdbid = ",".join(pdbid)

        if isinstance(pdbid, str):
            for item in pdbid.split(","):
                assert len(item) == 4, "a 4-character PDB id code is required"
        else:
            raise TypeError(
                "pdb id must be either a 4-character pdb id, a list of valid PDB ids, or a string made of pdb ids, separated by commas"
            )

        return pdbid

    def _return(self, res):
        if res == 404:
            return {}
        return res

    def get_summary(self, query):
        """Returns summary of a PDB entry

        This can be title of the entry, list of depositors, date of deposition,
        date of release, date of latest revision, experimental method, list
        of related entries in case split entries, etc.

        :param query: a 4-character PDB id code

        ::

            p.get_summary('1cbs')
            p.get_summary('1cbs,2kv8')
            p.get_summary(['1cbs', '2kv8'])

        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("summary/{}".format(query))
        else:
            res = self.services.http_post("summary", data=query, frmt="json")
        return self._return(res)

    def get_molecules(self, query):
        """Return details of molecules  (or entities in mmcif-speak) modelled in the entry

        This can be entity id, description, type, polymer-type (if applicable), number
        of copies in the entry, sample preparation method, source organism(s)
        (if applicable), etc.

        :param query: a 4-character PDB id code

        ::

            p.get_molecules('1cbs')

        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("molecules/{}".format(query))
        else:
            res = self.services.http_post("molecules", data=query, frmt="json")
        return self._return(res)

    def get_related_publications(self, query):
        """Return publications obtained from both EuroPMC and UniProt. T


        These are articles which cite the primary citation of the entry, or
        open-access articles which mention the entry id without explicitly citing the
        primary citation of an entry.


        :param query: a 4-character PDB id code

        ::

            p.get_related_publications('1cbs')

        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("related_publications/{}".format(query))
        else:
            res = self.services.http_post("related_publications/", data=query, frmt="json")
        return self._return(res)

    def get_experiment(self, query):
        """Provides details of experiment(s) carried out in determining the structure of the entry.

        Each experiment is described in a separate dictionary.
        For X-ray diffraction, the description consists of resolution, spacegroup, cell
        dimensions, R and Rfree, refinement program, etc.
        For NMR, details of spectrometer, sample, spectra, refinement, etc. are
        included.
        For EM, details of specimen, imaging, acquisition, reconstruction, fitting etc.
        are included.

        :param query: a 4-character PDB id code

        ::

            p.get_experiment('1cbs')

        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("experiment/{}".format(query))
        else:
            res = self.services.http_post("experiment/{}", data=query, frmt="json")
        return self._return(res)

    def get_nmr_resources(self, query):
        """This call provides URLs of available additional resources for NMR
        entries. E.g., mapping between structure (PDB) and chemical shift (BMRB)
        entries.
        :param query: a 4-character PDB id code

        ::

            p.get_nmr_resources('1cbs')

        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("nmr_resources/{}".format(query))
        else:
            res = self.services.http_post("nmr_resources/", data=query, frmt="json")
        return self._return(res)

    def get_ligand_monomers(self, query):
        """Provides a a list of modelled instances of ligands,

        ligands i.e. 'bound' molecules that are not waters.

        :param query: a 4-character PDB id code

        ::

            p.get_ligand_monomers('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("ligand_monomers/{}".format(query))
        else:
            res = self.services.http_post("ligand_monomers", data=query, frmt="json")
        return self._return(res)

    def get_modified_residues(self, query):
        """Provides a list of modelled instances of modified amino acids or
        nucleotides in protein, DNA or RNA chains.


        :param query: a 4-character PDB id code

        ::

            p.get_modified_residues('4v5j')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("modified_AA_or_NA/{}".format(query))
        else:
            res = self.services.http_post("modified_AA_or_NA", data=query, frmt="json")
        return self._return(res)

    def get_mutated_residues(self, query):
        """Provides a list of modelled instances of mutated amino acids or
        nucleotides in protein, DNA or RNA chains.


        :param query: a 4-character PDB id code

        ::

            p.get_mutated_residues('1bgj')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("mutated_AA_or_NA/{}".format(query))
        else:
            res = self.services.http_get("mutated_AA_or_NA", data=query, frmt="json")
        return self._return(res)

    def get_release_status(self, query):
        """Provides status of a PDB entry (released, obsoleted, on-hold etc)
        along with some other information such as authors, title, experimental method,
        etc.

        :param query: a 4-character PDB id code

        ::

            p.get_release_status('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("status/{}".format(query))
        else:
            res = self.services.http_get("status/{}", data=query, frmt="json")
        return self._return(res)

    def get_observed_ranges(self, query):
        """Provides observed ranges, i.e., segments of structural coverage of
         polymeric molecues that are modelled fully or partly

        :param query: a 4-character PDB id code

        ::

            p.get_observed_ranges('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("polymer_coverage/{}".format(query))
        else:
            res = self.services.http_post("polymer_coverage", data=query, frmt="json")
        return self._return(res)

    def get_observed_ranges_in_pdb_chain(self, query, chain_id):
        """Provides observed ranges, i.e., segments of structural coverage of
         polymeric molecules in a particular chain

        :param query: a 4-character PDB id code
        :param query: a PDB chain ID

        ::

            p.get_observed_ranges_in_pdb_chain('1cbs', "A")


        """
        assert len(query) == 4, "a 4-character PDB id code is required"
        res = self.services.http_get("polymer_coverage/{}/chain/{}".format(query, chain_id))
        return self._return(res)

    def get_secondary_structure(self, query):
        """Provides residue ranges of regular secondary structure

        (alpha helices and beta strands) found in protein chains of the entry.
        For strands, sheet id can be used to identify a beta sheet.



        :param query: a 4-character PDB id code

        ::

            p.get_secondary_structure('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("secondary_structure/{}".format(query))
        else:
            res = self.services.http_post("secondary_structure/", data=query, frmt="json")
        return self._return(res)

    def get_residue_listing(self, query):
        """Provides lists all residues (modelled or otherwise) in the entry.

        Except waters, along with details of the fraction of expected atoms modelled for
        the residue and any alternate conformers.


        :param query: a 4-character PDB id code

        ::

            p.get_residue_listing('1cbs')


        """
        assert len(query) == 4, "a 4-character PDB id code is required"
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("residue_listing/{}".format(query))
        return self._return(res)

    def get_residue_listing_in_pdb_chain(self, query, chain_id):
        """Provides all residues (modelled or otherwise) in the entry

        Except waters, along with details of the fraction of expected atoms
        modelled for the residue and any alternate conformers.

        :param query: a 4-character PDB id code
        :param query: a PDB chain ID

        ::

            p.get_residue_listing_in_pdb_chain('1cbs')


        """
        assert len(query) == 4, "a 4-character PDB id code is required"
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("residue_listing/{}".format(query, chain_id))
        return self._return(res)

    def get_binding_sites(self, query):
        """Pprovides details on binding sites in the entry

        STRUCT_SITE records in PDB files (or mmcif equivalent thereof), such as ligand,
        residues in the site, description of the site, etc.


        :param query: a 4-character PDB id code

        ::

            p.get_binding_sites('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("binding_sites/{}".format(query))
        else:
            res = self.services.http_post("binding_sites", data=query, frmt="json")
        return self._return(res)

    def get_files(self, query):
        """Provides URLs and brief descriptions (labels) for PDB entry

        Also, for mmcif files, biological assembly files, FASTA file for sequences,
        SIFTS cross reference XML files, validation XML files, X-ray structure
        factor file, NMR experimental constraints files, etc.

        :param query: a 4-character PDB id code

        ::

            p.get_files('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("files/{}".format(query))
        else:
            res = self.services.http_post("files", data=query, frmt="json")
        return self._return(res)

    def get_observed_residues_ratio(self, query):
        """Provides the ratio of observed residues for each chain in each molecule

        The list of chains within an entity is sorted by observed_ratio (descending order),
         partial_ratio (ascending order), and number_residues (descending order).

        :param query: a 4-character PDB id code

        ::

            p.get_observed_residues_ratio('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("observed_residues_ratio/{}".format(query))
        else:
            res = self.services.http_post("observed_residues_ratio", data=query, frmt="json")
        return self._return(res)

    def get_assembly(self, query):
        """Provides information for each assembly of a given PDB ID. T

        This information is broken down at the entity level for each assembly. The
        information given includes the molecule name, type and class, the chains where
        the molecule occur, and the number of copies of each entity in the assembly.

        :param query: a 4-character PDB id code

        ::

            p.get_assembly('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("assembly/{}".format(query))
        else:
            res = self.services.http_post("assembly", data=query, frmt="json")
        return self._return(res)

    def get_electron_density_statistics(self, query):
        """This call details the statistics for electron density.

        :param query: a 4-character PDB id code

        ::

            p.get_electron_density_statistics('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("electron_density_statistics/{}".format(query))
        else:
            res = self.services.http_post("electron_density_statistics", data=query, frmt="json")
        return self._return(res)

    def get_functional_annotation(self, query):
        """Provides functional annotation of all ligands, i.e. 'bound'

        :param query: a 4-character PDB id code

        ::

            p.get_functional_annotation('1cbs')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("cofactor/{}".format(query))
        else:
            res = self.services.http_post("cofactor", data=query, frmt="json")
        return self._return(res)

    def get_drugbank_annotation(self, query):
        """This call provides DrugBank annotation of all ligands, i.e. 'bound'

        :param query: a 4-character PDB id code

        ::

            p.get_drugbank_annotation('5hht')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("drugbank/{}".format(query))
        else:
            res = self.services.http_post("drugbank", data=query, frmt="json")
        return self._return(res)

    def get_related_dataset(self, query):
        """Provides DOI’s for related raw experimental datasets

        Includes diffraction image data, small-angle scattering data and
        electron micrographs.


        :param query: a 4-character PDB id code

        ::

            p.get_cofactor('5o8b')


        """
        query = self._check_id(query)
        if isinstance(query, str) and "," not in query:
            res = self.services.http_get("related_experiment_data/{}".format(query))
        else:
            res = self.services.http_post("related_experiment_data", data=query, frmt="json")
        return self._return(res)
