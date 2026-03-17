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
"""Interface to the PDBe web Service (v2 API).

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

import json as _json

from bioservices.services import REST

__all__ = ["PDBe"]


class PDBe:
    """Interface to part of the `PDBe <http://www.ebi.ac.uk/pdbe>`_ service

    .. doctest::

        >>> from bioservices import PDBe
        >>> s = PDBe()
        >>> res = s.get_files("1FBV")

    """

    _entry_prefix = "pdb/entry"

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages (default is off)
        :param bool cache: set to True to enable HTTP caching

        """
        url = "https://www.ebi.ac.uk/pdbe/api/v2"
        self.services = REST(name="PDBe", url=url, verbose=verbose, cache=cache, url_defined_later=True)

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
        if res in (404, 410):
            return {}
        return res

    def _post_json(self, endpoint, query):
        """Send a POST request with JSON content type to the v2 API.

        The v2 API expects POST bodies as JSON-encoded strings containing
        comma-separated PDB IDs.
        """
        headers = self.services.get_headers("json")
        return self.services.http_post(
            endpoint,
            data=_json.dumps(query),
            frmt="json",
            headers=headers,
        )

    def _get_or_post(self, endpoint, query):
        """Handle single PDB ID via GET or multiple PDB IDs via POST.

        :param endpoint: the API endpoint name (e.g. 'summary', 'molecules')
        :param query: a PDB id, a comma-separated string of PDB ids, or a list of PDB ids
        :returns: the API response
        """
        query = self._check_id(query)
        if "," not in query:
            res = self.services.http_get("{}/{}/{}".format(self._entry_prefix, endpoint, query))
        else:
            res = self._post_json("{}/{}".format(self._entry_prefix, endpoint), query)
        return self._return(res)

    def get_summary(self, query):
        """Returns summary of a PDB entry

        This can be title of the entry, list of depositors, date of deposition,
        date of release, date of latest revision, experimental method, list
        of related entries in case split entries, etc.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_summary('1cbs')
            p.get_summary('1cbs,2kv8')
            p.get_summary(['1cbs', '2kv8'])

        """
        return self._get_or_post("summary", query)

    def get_molecules(self, query):
        """Return details of molecules (or entities in mmcif-speak) modelled in the entry

        This can be entity id, description, type, polymer-type (if applicable), number
        of copies in the entry, sample preparation method, source organism(s)
        (if applicable), etc.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_molecules('1cbs')
            p.get_molecules('1cbs,2kv8')

        """
        return self._get_or_post("molecules", query)

    def get_entities(self, query):
        """Return details of entities modelled in the entry

        This is an alias for :meth:`get_molecules` using the ``entities`` endpoint.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_entities('1cbs')
            p.get_entities('1cbs,2kv8')

        """
        return self._get_or_post("entities", query)

    def get_publications(self, query):
        """Return publications associated with the entry

        Provides details of publications associated with an entry, such as title
        of the article, journal name, year of publication, volume, pages, doi,
        pubmed_id, etc. Primary citation is listed first.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_publications('1cbs')
            p.get_publications('1cbs,2kv8')

        """
        return self._get_or_post("publications", query)

    def get_related_publications(self, query):
        """Return publications obtained from both EuroPMC and UniProt.

        These are articles which cite the primary citation of the entry, or
        open-access articles which mention the entry id without explicitly citing the
        primary citation of an entry.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_related_publications('1cbs')
            p.get_related_publications('1cbs,2kv8')

        """
        return self._get_or_post("related_publications", query)

    def get_experiment(self, query):
        """Provides details of experiment(s) carried out in determining the structure of the entry.

        Each experiment is described in a separate dictionary.
        For X-ray diffraction, the description consists of resolution, spacegroup, cell
        dimensions, R and Rfree, refinement program, etc.
        For NMR, details of spectrometer, sample, spectra, refinement, etc. are
        included.
        For EM, details of specimen, imaging, acquisition, reconstruction, fitting etc.
        are included.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_experiment('1cbs')
            p.get_experiment('1cbs,2kv8')

        """
        return self._get_or_post("experiment", query)

    def get_ligand_monomers(self, query):
        """Provides a list of modelled instances of ligands,

        i.e. 'bound' molecules that are not waters.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_ligand_monomers('1cbs')
            p.get_ligand_monomers('1cbs,2kv8')

        """
        return self._get_or_post("ligand_monomers", query)

    def get_modified_residues(self, query):
        """Provides a list of modelled instances of modified amino acids or
        nucleotides in protein, DNA or RNA chains.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_modified_residues('4v5j')
            p.get_modified_residues('4v5j,1cbs')

        """
        return self._get_or_post("modified_AA_or_NA", query)

    def get_mutated_residues(self, query):
        """Provides a list of modelled instances of mutated amino acids or
        nucleotides in protein, DNA or RNA chains.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_mutated_residues('1bgj')
            p.get_mutated_residues('1bgj,4v5j')

        """
        return self._get_or_post("mutated_AA_or_NA", query)

    def get_release_status(self, query):
        """Provides status of a PDB entry (released, obsoleted, on-hold etc)
        along with some other information such as authors, title, experimental method,
        etc.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_release_status('1cbs')
            p.get_release_status('1cbs,4v5j')

        """
        return self._get_or_post("status", query)

    def get_observed_ranges(self, query):
        """Provides observed ranges, i.e., segments of structural coverage of
        polymeric molecules that are modelled fully or partly.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_observed_ranges('1cbs')
            p.get_observed_ranges('1cbs,4v5j')

        """
        return self._get_or_post("polymer_coverage", query)

    def get_observed_ranges_in_pdb_chain(self, query, chain_id):
        """Provides observed ranges, i.e., segments of structural coverage of
        polymeric molecules in a particular chain.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs
        :param str chain_id: a PDB chain ID (e.g., ``"A"``)

        ::

            p.get_observed_ranges_in_pdb_chain('1cbs', 'A')

        """
        query = self._check_id(query)
        res = self.services.http_get("{}/polymer_coverage/{}/chain/{}".format(self._entry_prefix, query, chain_id))
        return self._return(res)

    def get_secondary_structure(self, query):
        """Provides residue ranges of regular secondary structure

        (alpha helices and beta strands) found in protein chains of the entry.
        For strands, sheet id can be used to identify a beta sheet.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_secondary_structure('1cbs')
            p.get_secondary_structure('1cbs,4v5j')

        """
        return self._get_or_post("secondary_structure", query)

    def get_residue_listing(self, query):
        """Lists all residues (modelled or otherwise) in the entry.

        Except waters, along with details of the fraction of expected atoms modelled for
        the residue and any alternate conformers.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_residue_listing('1cbs')

        """
        query = self._check_id(query)
        res = self.services.http_get("{}/residue_listing/{}".format(self._entry_prefix, query))
        return self._return(res)

    def get_residue_listing_in_pdb_chain(self, query, chain_id):
        """Lists all residues (modelled or otherwise) in a particular chain.

        Except waters, along with details of the fraction of expected atoms
        modelled for the residue and any alternate conformers.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs
        :param str chain_id: a PDB chain ID (e.g., ``"A"``)

        ::

            p.get_residue_listing_in_pdb_chain('1cbs', 'A')

        """
        query = self._check_id(query)
        res = self.services.http_get("{}/residue_listing/{}/chain/{}".format(self._entry_prefix, query, chain_id))
        return self._return(res)

    def get_binding_sites(self, query, entity_id):
        """Provides details on binding sites for a specific entity in the entry.

        STRUCT_SITE records in PDB files (or mmcif equivalent thereof), such as ligand,
        residues in the site, description of the site, etc.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs
        :param entity_id: an entity ID (integer or string, e.g., ``1``)

        ::

            p.get_binding_sites('1cbs', 1)

        """
        query = self._check_id(query)
        res = self.services.http_get("{}/binding_sites/{}/{}".format(self._entry_prefix, query, entity_id))
        return self._return(res)

    def get_files(self, query):
        """Provides URLs and brief descriptions (labels) for PDB entry

        Also, for mmcif files, biological assembly files, FASTA file for sequences,
        SIFTS cross reference XML files, validation XML files, X-ray structure
        factor file, NMR experimental constraints files, etc.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_files('1cbs')
            p.get_files('1cbs,4v5j')

        """
        return self._get_or_post("files", query)

    def get_observed_residues_ratio(self, query):
        """Provides the ratio of observed residues for each chain in each molecule.

        The list of chains within an entity is sorted by observed_ratio (descending order),
        partial_ratio (ascending order), and number_residues (descending order).

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_observed_residues_ratio('1cbs')
            p.get_observed_residues_ratio('1cbs,4v5j')

        """
        return self._get_or_post("observed_residues_ratio", query)

    def get_assembly(self, query):
        """Provides information for each assembly of a given PDB ID.

        This information is broken down at the entity level for each assembly. The
        information given includes the molecule name, type and class, the chains where
        the molecule occur, and the number of copies of each entity in the assembly.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_assembly('1cbs')
            p.get_assembly('1cbs,4v5j')

        """
        return self._get_or_post("assembly", query)

    def get_electron_density_statistics(self, query):
        """Provides statistics for electron density.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_electron_density_statistics('1cbs')
            p.get_electron_density_statistics('1cbs,4v5j')

        """
        return self._get_or_post("electron_density_statistics", query)

    def get_functional_annotation(self, query):
        """Provides functional annotation of all ligands, i.e. 'bound' molecules.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_functional_annotation('1cbs')

        """
        query = self._check_id(query)
        res = self.services.http_get("{}/cofactor/{}".format(self._entry_prefix, query))
        return self._return(res)

    def get_drugbank_annotation(self, query):
        """Provides DrugBank annotation of all ligands, i.e. 'bound' molecules.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_drugbank_annotation('5hht')

        """
        query = self._check_id(query)
        res = self.services.http_get("{}/drugbank/{}".format(self._entry_prefix, query))
        return self._return(res)

    def get_related_dataset(self, query):
        """Provides DOIs for related raw experimental datasets.

        Includes diffraction image data, small-angle scattering data and
        electron micrographs.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_related_dataset('5o8b')
            p.get_related_dataset('5o8b,5o8b')

        """
        return self._get_or_post("related_experiment_data", query)

    def get_branched_entities(self, query):
        """Provides data for branched carbohydrate entities within an entry.

        Overall information about each unique branched carbohydrate is returned,
        along with detailed information about each carbohydrate monomer within
        the branched entity.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_branched_entities('3d12')
            p.get_branched_entities('3d12,7v7u')

        """
        return self._get_or_post("branched", query)

    def get_carbohydrate_polymer(self, query):
        """Provides data for carbohydrate polymers within an entry.

        :param str query: a 4-character PDB id code, comma-separated list of IDs, or Python list of IDs

        ::

            p.get_carbohydrate_polymer('3d12')
            p.get_carbohydrate_polymer('3d12,7v7u')

        """
        return self._get_or_post("carbohydrate_polymer", query)
