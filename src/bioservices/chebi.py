#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""This module provides a class :class:`ChEBI`

.. topic:: What is ChEBI

    :URL:  https://www.ebi.ac.uk/chebi/init.do
    :REST: https://www.ebi.ac.uk/chebi/backend/api/public


    .. highlights::

        "The database and ontology of Chemical Entities of Biological Interest

        -- From ChEBI web page June 2013


"""
from bioservices import REST
from bioservices import logger

logger.name = __name__

__all__ = ["ChEBI"]

# Mapping from old SOAP relation type names to new REST API relation type names
_RELATION_TYPE_MAP = {
    "is a": "is_a",
    "has part": "has_part",
    "has role": "has_role",
    "is conjugate base of": "is_conjugate_base_of",
    "is conjugate acid of": "is_conjugate_acid_of",
    "is tautomer of": "is_tautomer_of",
    "is enantiomer of": "is_enantiomer_of",
    "has functional parent": "has_functional_parent",
    "has parent hybride": "has_parent_hydride",
    "is substituent group of": "is_substituent_group_from",
}


class ChebiEntity(dict):
    """A dict subclass returned by ChEBI REST API calls.

    Provides attribute-style access to common compound fields for
    backward compatibility with the old SOAP-based interface.
    """

    @property
    def mass(self):
        """Molecular mass of the compound."""
        chem = self.get("chemical_data") or {}
        return chem.get("mass")

    @property
    def smiles(self):
        """SMILES string of the default structure."""
        struct = self.get("default_structure") or {}
        return struct.get("smiles")

    @property
    def inchiKey(self):
        """Standard InChI key of the default structure."""
        struct = self.get("default_structure") or {}
        return struct.get("standard_inchi_key")

    @property
    def formula(self):
        """Molecular formula."""
        chem = self.get("chemical_data") or {}
        return chem.get("formula")

    @property
    def charge(self):
        """Formal charge."""
        chem = self.get("chemical_data") or {}
        return chem.get("charge")

    @property
    def chebiAsciiName(self):
        """ASCII name of the compound (primary name)."""
        return self.get("ascii_name") or self.get("name")

    @property
    def chebiId(self):
        """ChEBI accession string, e.g. 'CHEBI:27732'."""
        return self.get("chebi_accession") or str(self.get("id", ""))

    @property
    def DatabaseLinks(self):
        """List of ``(accession_number, source_name)`` tuples from all
        database cross-references, mirroring the old SOAP interface."""
        db_accessions = self.get("database_accessions") or {}
        links = []
        for acc_list in db_accessions.values():
            if isinstance(acc_list, list):
                for acc in acc_list:
                    acc_num = acc.get("accession_number", "")
                    src_name = acc.get("source_name", "")
                    if acc_num or src_name:
                        links.append((acc_num, src_name))
        return links


class ChEBI(REST):
    """Interface to the `ChEBI <https://www.ebi.ac.uk/chebi/>`_ REST API.

    ChEBI (Chemical Entities of Biological Interest) is a freely available
    dictionary of molecular entities focused on 'small' chemical compounds.

    The REST API is documented at
    https://www.ebi.ac.uk/chebi/backend/api/docs/

    Example usage::

        >>> from bioservices import ChEBI
        >>> ch = ChEBI()
        >>> res = ch.getCompleteEntity("CHEBI:27732")
        >>> res.smiles
        'Cn1cnc2c1c(=O)n(c(=O)n2C)C'

    """

    _url = "https://www.ebi.ac.uk/chebi/backend/api/public"

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose:
        :param bool cache:
        """
        super(ChEBI, self).__init__(name="ChEBI", url=ChEBI._url, verbose=verbose, cache=cache)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _chebi_num(self, chebiId):
        """Return the numeric part of a ChEBI identifier.

        Accepts both ``"CHEBI:27732"`` and ``"27732"`` (or int ``27732``).
        """
        s = str(chebiId).strip()
        if ":" in s:
            return s.split(":")[-1]
        return s

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def getCompleteEntity(self, chebiId):
        """Retrieve the complete entity for a ChEBI identifier.

        :param str chebiId: a valid ChEBI identifier (e.g. ``"CHEBI:27732"``)
        :return: a :class:`ChebiEntity` dict-like object

        ::

            >>> from bioservices import ChEBI
            >>> ch = ChEBI()
            >>> res = ch.getCompleteEntity("CHEBI:27732")
            >>> float(res.mass)
            194.19076

        .. seealso:: :meth:`conv`, :meth:`getCompleteEntityByList`
        """
        cid = self._chebi_num(chebiId)
        res = self.http_get("compound/{}".format(cid), frmt="json")
        if isinstance(res, dict):
            return ChebiEntity(res)
        return res

    def conv(self, chebiId, target):
        """Return the cross-reference accession number(s) for a given database.

        Calls :meth:`getCompleteEntity` internally and filters the
        ``DatabaseLinks`` by *target*.

        :param str chebiId: a valid ChEBI identifier (e.g. ``"CHEBI:10102"``)
        :param str target: source database name
            (e.g. ``"KEGG COMPOUND accession"``)
        :return: list of accession number strings

        ::

            >>> ch.conv("CHEBI:10102", "KEGG COMPOUND accession")
            ['C07484']

        """
        res = self.getCompleteEntity(chebiId)
        if not isinstance(res, dict):
            raise ValueError("Could not retrieve entity for %s" % chebiId)

        db_accessions = res.get("database_accessions") or {}
        all_sources = set()
        matches = []
        for acc_list in db_accessions.values():
            if isinstance(acc_list, list):
                for acc in acc_list:
                    src = acc.get("source_name", "")
                    all_sources.add(src)
                    if src == target:
                        matches.append(str(acc.get("accession_number", "")))

        if not matches:
            raise ValueError("valid database target are %s" % sorted(all_sources))
        return matches

    def getLiteEntity(self, search, searchCategory="ALL", maximumResults=200, stars="ALL"):
        """Retrieve a list of lite entities matching a search term.

        :param str search: search string (ChEBI name, identifier, SMILES, etc.)
        :param str searchCategory: filter category (default ``"ALL"``)
        :param int maximumResults: maximum number of results (default 200)
        :param str stars: star filter – ``"ALL"``, ``"TWO ONLY"``,
            or ``"THREE ONLY"`` (default ``"ALL"``)
        :return: list of :class:`ChebiEntity` objects

        ::

            >>> res = ch.getLiteEntity("caffeine", maximumResults=10)
            >>> len(res)
            10

        .. seealso:: :meth:`getCompleteEntity`
        """
        params = {"term": search, "size": maximumResults}
        res = self.http_get("es_search/", frmt="json", params=params)
        if isinstance(res, dict) and "results" in res:
            return [ChebiEntity(r.get("_source") or {}) for r in res["results"]]
        return []

    def getUpdatedPolymer(self, chebiId):
        """Return compound data for a polymer ChEBI entry.

        In the REST API this is equivalent to :meth:`getCompleteEntity`.

        :param str chebiId: a valid ChEBI identifier (string)
        :return: a :class:`ChebiEntity` dict-like object
        """
        return self.getCompleteEntity(chebiId)

    def getCompleteEntityByList(self, chebiIdList=None):
        """Retrieve complete entities for a list of ChEBI identifiers.

        :param list chebiIdList: list of ChEBI identifiers
            (maximum 50 entries recommended)
        :return: list of :class:`ChebiEntity` objects

        .. seealso:: :meth:`getCompleteEntity`
        """
        if chebiIdList is None:
            chebiIdList = []
        results = []
        for cid in chebiIdList:
            entity = self.getCompleteEntity(cid)
            if entity is not None:
                results.append(entity)
        return results

    def getOntologyParents(self, chebiId):
        """Retrieve the ontology parents of a ChEBI entity.

        :param str chebiId: a valid ChEBI identifier (string)
        :return: dict with ontology parent information
        """
        cid = self._chebi_num(chebiId)
        res = self.http_get("ontology/parents/{}/".format(cid), frmt="json")
        return res

    def getOntologyChildren(self, chebiId):
        """Retrieve the ontology children of a ChEBI entity.

        :param str chebiId: a valid ChEBI identifier (string)
        :return: dict with ontology children information
        """
        cid = self._chebi_num(chebiId)
        res = self.http_get("ontology/children/{}/".format(cid), frmt="json")
        return res

    def getAllOntologyChildrenInPath(self, chebiId, relationshipType, onlyWithChemicalStructure=False):
        """Retrieve ontology children connected by a specific relationship type.

        :param str chebiId: a valid ChEBI identifier (string)
        :param str relationshipType: one of ``"is a"``, ``"has part"``,
            ``"has role"``, ``"is conjugate base of"``,
            ``"is conjugate acid of"``, ``"is tautomer of"``,
            ``"is enantiomer of"``, ``"has functional parent"``,
            ``"has parent hydride"``, ``"is substituent group of"``
        :param bool onlyWithChemicalStructure: filter to entities with a
            chemical structure (default ``False``)
        :return: list of ontology relation dicts

        ::

            >>> ch.getAllOntologyChildrenInPath("CHEBI:27732", "has part")

        """
        self.devtools.check_param_in_list(
            relationshipType,
            list(_RELATION_TYPE_MAP.keys()),
        )
        rel_type = _RELATION_TYPE_MAP[relationshipType]
        cid = self._chebi_num(chebiId)
        res = self.http_get("ontology/children/{}/".format(cid), frmt="json")
        if isinstance(res, dict):
            ontology = res.get("ontology_relations") or {}
            incoming = ontology.get("incoming_relations") or []
            filtered = [r for r in incoming if r.get("relation_type") == rel_type]
            return filtered
        return res

    def getStructureSearch(
        self,
        structure,
        mode="MOLFILE",
        structureSearchCategory="SIMILARITY",
        totalResults=50,
        tanimotoCutoff=0.25,
    ):
        """Perform a substructure, similarity, or identity search.

        :param str structure: input structure string
        :param str mode: structure format – ``"MOLFILE"``, ``"SMILES"``,
            or ``"CML"``
        :param str structureSearchCategory: search type –
            ``"SIMILARITY"``, ``"SUBSTRUCTURE"``, or ``"IDENTITY"``
        :param int totalResults: maximum number of results (default 50)
        :param float tanimotoCutoff: minimum Tanimoto score (default 0.25,
            only used for ``"SIMILARITY"`` searches)
        :return: list of matching entities

        ::

            >>> ch = ChEBI()
            >>> smiles = ch.getCompleteEntity("CHEBI:27732").smiles
            >>> ch.getStructureSearch(smiles, "SMILES", "SIMILARITY", 3, 0.25)

        """
        self.devtools.check_param_in_list(structureSearchCategory, ["SIMILARITY", "SUBSTRUCTURE", "IDENTITY"])
        self.devtools.check_param_in_list(mode, ["MOLFILE", "SMILES", "CML"])

        _type_map = {"SMILES": "smiles", "MOLFILE": "mol", "CML": "cml"}
        _cat_map = {"SIMILARITY": "similarity", "SUBSTRUCTURE": "substructure", "IDENTITY": "connectivity"}

        params = {
            "structure": structure,
            "type": _type_map[mode],
            "searchCategory": _cat_map[structureSearchCategory],
            "total": totalResults,
            "tanimoto": tanimotoCutoff,
        }
        res = self.http_get("structure_search/", frmt="json", params=params)
        return res
