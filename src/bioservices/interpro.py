#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2026 - EBI-EMBL
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the InterPro web service

.. topic:: What is InterPro ?

    :URL: https://www.ebi.ac.uk/interpro/
    :REST: https://www.ebi.ac.uk/interpro/api/

    .. highlights::

        InterPro provides functional analysis of proteins by classifying them into
        families and predicting domains and important sites. To classify proteins in
        this way, InterPro uses predictive models, known as signatures, provided by
        several collaborating databases (referred to as member databases) that make
        up the InterPro consortium. We combine protein signatures from these member
        databases into a single searchable resource, capitalising on their individual
        strengths to produce a powerful integrated database and diagnostic tool.

        -- From InterPro home page, 2024

"""
from bioservices import logger
from bioservices.services import REST

logger.name = __name__

__all__ = ["InterPro"]


class InterPro:
    """Interface to the `InterPro <https://www.ebi.ac.uk/interpro/>`_ service

    InterPro provides functional analysis of proteins by classifying them into
    families and predicting domains and important sites.

    ::

        from bioservices import InterPro
        i = InterPro()

        # Get information about an InterPro entry
        entry = i.get_entry("IPR000001")

        # Get all entries for a protein
        entries = i.get_protein_entries("P00734")

        # Search entries by name
        results = i.search_entries("kinase")

    InterPro integrates signatures from the following member databases:

    - CATH-Gene3D
    - CDD
    - HAMAP
    - MobiDB Lite
    - NCBIfam
    - Panther
    - Pfam
    - PIRSF
    - PRINTS
    - ProSite
    - SFLD
    - SMART
    - SUPFAM
    - TIGRFAMs

    """

    _url = "https://www.ebi.ac.uk/interpro/api"

    _member_databases = [
        "cathgene3d",
        "cdd",
        "hamap",
        "mobidblt",
        "ncbifam",
        "panther",
        "pfam",
        "pirsf",
        "prints",
        "profile",
        "prosite",
        "sfld",
        "smart",
        "ssf",
        "tigrfam",
    ]

    _entry_types = [
        "family",
        "domain",
        "homologous_superfamily",
        "repeat",
        "site",
        "active_site",
        "binding_site",
        "conserved_site",
        "ptm",
    ]

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages (default is off)
        :param bool cache: use cache (default is off)

        ::

            >>> from bioservices import InterPro
            >>> i = InterPro(verbose=False)

        """
        self.services = REST(name="InterPro", url=InterPro._url, verbose=verbose, cache=cache)

    # ------------------------------------------------------------------
    # Entry endpoints
    # ------------------------------------------------------------------

    def get_entry(self, accession):
        """Retrieve a specific InterPro entry by accession

        :param str accession: an InterPro accession (e.g. "IPR000001")
        :return: dictionary with entry information

        ::

            i = InterPro()
            entry = i.get_entry("IPR000001")
            print(entry["metadata"]["name"])

        """
        res = self.services.http_get("entry/interpro/{}/".format(accession), frmt="json")
        return res

    def get_entries(self, page_size=20, page=1):
        """Retrieve a paginated list of all InterPro entries

        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with results and pagination info

        ::

            i = InterPro()
            results = i.get_entries(page_size=10)

        """
        params = {"page_size": page_size, "page": page}
        res = self.services.http_get("entry/interpro/", frmt="json", params=params)
        return res

    def get_member_database_entry(self, database, accession):
        """Retrieve a specific entry from a member database

        :param str database: member database name (e.g. "pfam", "prosite")
        :param str accession: accession in the member database (e.g. "PF00001")
        :return: dictionary with entry information

        The supported member databases are: cathgene3d, cdd, hamap, mobidblt,
        ncbifam, panther, pfam, pirsf, prints, profile, prosite, sfld, smart,
        ssf, tigrfam.

        ::

            i = InterPro()
            entry = i.get_member_database_entry("pfam", "PF00001")

        """
        database = database.lower()
        if database not in self._member_databases:
            raise ValueError(
                "Database '{}' is not a valid member database. Choose from: {}".format(
                    database, ", ".join(self._member_databases)
                )
            )
        res = self.services.http_get("entry/{}/{}/".format(database, accession), frmt="json")
        return res

    def get_entries_by_member_database(self, database, page_size=20, page=1):
        """Retrieve entries from a specific member database

        :param str database: member database name (e.g. "pfam", "prosite")
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with results and pagination info

        ::

            i = InterPro()
            results = i.get_entries_by_member_database("pfam")

        """
        database = database.lower()
        if database not in self._member_databases:
            raise ValueError(
                "Database '{}' is not a valid member database. Choose from: {}".format(
                    database, ", ".join(self._member_databases)
                )
            )
        params = {"page_size": page_size, "page": page}
        res = self.services.http_get("entry/{}/".format(database), frmt="json", params=params)
        return res

    def search_entries(self, search, page_size=20, page=1):
        """Search InterPro entries by name or description

        :param str search: search term
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with results and pagination info

        ::

            i = InterPro()
            results = i.search_entries("kinase")

        """
        params = {"search": search, "page_size": page_size, "page": page}
        res = self.services.http_get("entry/interpro/", frmt="json", params=params)
        return res

    def get_entries_by_type(self, entry_type, page_size=20, page=1):
        """Retrieve InterPro entries filtered by type

        :param str entry_type: entry type. One of: family, domain,
            homologous_superfamily, repeat, site, active_site, binding_site,
            conserved_site, ptm
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with results and pagination info

        ::

            i = InterPro()
            results = i.get_entries_by_type("domain")

        """
        entry_type = entry_type.lower()
        if entry_type not in self._entry_types:
            raise ValueError(
                "Entry type '{}' is not valid. Choose from: {}".format(
                    entry_type, ", ".join(self._entry_types)
                )
            )
        params = {"type": entry_type, "page_size": page_size, "page": page}
        res = self.services.http_get("entry/interpro/", frmt="json", params=params)
        return res

    # ------------------------------------------------------------------
    # Protein endpoints
    # ------------------------------------------------------------------

    def get_protein(self, accession, database="uniprot"):
        """Retrieve information about a protein

        :param str accession: a UniProt accession (e.g. "P00734")
        :param str database: protein database, currently only "uniprot" is
            supported (default: "uniprot")
        :return: dictionary with protein information

        ::

            i = InterPro()
            protein = i.get_protein("P00734")
            print(protein["metadata"]["name"])

        """
        res = self.services.http_get("protein/{}/{}/".format(database, accession), frmt="json")
        return res

    def get_protein_entries(self, accession, database="uniprot"):
        """Retrieve InterPro entries associated with a protein

        :param str accession: a UniProt accession (e.g. "P00734")
        :param str database: protein database (default: "uniprot")
        :return: dictionary with entries annotated on the protein

        ::

            i = InterPro()
            entries = i.get_protein_entries("P00734")

        """
        res = self.services.http_get(
            "entry/interpro/protein/{}/{}/".format(database, accession), frmt="json"
        )
        return res

    def get_proteins_by_entry(self, accession, page_size=20, page=1):
        """Retrieve proteins annotated with a given InterPro entry

        :param str accession: an InterPro accession (e.g. "IPR000001")
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with proteins and pagination info

        ::

            i = InterPro()
            proteins = i.get_proteins_by_entry("IPR000001")

        """
        params = {"page_size": page_size, "page": page}
        res = self.services.http_get(
            "protein/uniprot/entry/interpro/{}/".format(accession), frmt="json", params=params
        )
        return res

    # ------------------------------------------------------------------
    # Structure endpoints
    # ------------------------------------------------------------------

    def get_structure(self, accession, database="pdb"):
        """Retrieve information about a structure

        :param str accession: a PDB accession (e.g. "1t2v")
        :param str database: structure database, currently only "pdb" is
            supported (default: "pdb")
        :return: dictionary with structure information

        ::

            i = InterPro()
            structure = i.get_structure("1t2v")

        """
        res = self.services.http_get("structure/{}/{}/".format(database, accession), frmt="json")
        return res

    def get_entry_structures(self, accession, page_size=20, page=1):
        """Retrieve structures associated with a given InterPro entry

        :param str accession: an InterPro accession (e.g. "IPR000001")
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with structures and pagination info

        ::

            i = InterPro()
            structures = i.get_entry_structures("IPR000001")

        """
        params = {"page_size": page_size, "page": page}
        res = self.services.http_get(
            "structure/pdb/entry/interpro/{}/".format(accession), frmt="json", params=params
        )
        return res

    # ------------------------------------------------------------------
    # Taxonomy endpoints
    # ------------------------------------------------------------------

    def get_taxonomy(self, taxon_id, database="uniprot"):
        """Retrieve taxonomy information

        :param str taxon_id: NCBI taxonomy ID (e.g. "9606" for human)
        :param str database: taxonomy database (default: "uniprot")
        :return: dictionary with taxonomy information

        ::

            i = InterPro()
            taxon = i.get_taxonomy("9606")
            print(taxon["metadata"]["scientific_name"])

        """
        res = self.services.http_get("taxonomy/{}/{}/".format(database, taxon_id), frmt="json")
        return res

    def get_entry_taxonomy(self, accession, page_size=20, page=1):
        """Retrieve taxonomy distribution of proteins annotated with an InterPro entry

        :param str accession: an InterPro accession (e.g. "IPR000001")
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with taxonomy distribution

        ::

            i = InterPro()
            taxons = i.get_entry_taxonomy("IPR000001")

        """
        params = {"page_size": page_size, "page": page}
        res = self.services.http_get(
            "taxonomy/uniprot/entry/interpro/{}/".format(accession), frmt="json", params=params
        )
        return res

    # ------------------------------------------------------------------
    # Proteome endpoints
    # ------------------------------------------------------------------

    def get_proteome(self, accession, database="uniprot"):
        """Retrieve information about a proteome

        :param str accession: a UniProt proteome accession (e.g. "UP000005640")
        :param str database: proteome database (default: "uniprot")
        :return: dictionary with proteome information

        ::

            i = InterPro()
            proteome = i.get_proteome("UP000005640")

        """
        res = self.services.http_get("proteome/{}/{}/".format(database, accession), frmt="json")
        return res

    def get_entry_proteomes(self, accession, page_size=20, page=1):
        """Retrieve proteomes containing proteins annotated with a given InterPro entry

        :param str accession: an InterPro accession (e.g. "IPR000001")
        :param int page_size: number of results per page (default 20)
        :param int page: page number (default 1)
        :return: dictionary with proteomes and pagination info

        ::

            i = InterPro()
            proteomes = i.get_entry_proteomes("IPR000001")

        """
        params = {"page_size": page_size, "page": page}
        res = self.services.http_get(
            "proteome/uniprot/entry/interpro/{}/".format(accession), frmt="json", params=params
        )
        return res

    # ------------------------------------------------------------------
    # Set endpoints
    # ------------------------------------------------------------------

    def get_set(self, database, accession):
        """Retrieve information about a set (e.g. a Pfam clan)

        :param str database: member database (e.g. "pfam" for Pfam clans)
        :param str accession: set accession (e.g. "CL0001" for a Pfam clan)
        :return: dictionary with set information

        ::

            i = InterPro()
            pfam_clan = i.get_set("pfam", "CL0001")

        """
        database = database.lower()
        res = self.services.http_get("set/{}/{}/".format(database, accession), frmt="json")
        return res
