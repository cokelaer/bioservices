#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the PubChem PUG REST web service

.. topic:: What is PubChem?

    :URL: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest

    .. highlights::

        PubChem is the world's largest collection of freely accessible chemical
        information. The PUG REST (Power User Gateway REST) API provides
        programmatic access to PubChem's compound, substance and assay data.

        -- PubChem web site


"""
from bioservices.services import REST

__all__ = ["PubChem", "COMPOUND_PROPERTIES", "XREF_TYPES"]

#: Properties available via the ``/property/`` endpoint of the PUG REST API.
COMPOUND_PROPERTIES = [
    "MolecularFormula",
    "MolecularWeight",
    "CanonicalSMILES",
    "IsomericSMILES",
    "InChI",
    "InChIKey",
    "IUPACName",
    "Title",
    "XLogP",
    "ExactMass",
    "MonoisotopicMass",
    "TPSA",
    "Complexity",
    "Charge",
    "HBondDonorCount",
    "HBondAcceptorCount",
    "RotatableBondCount",
    "HeavyAtomCount",
    "IsotopeAtomCount",
    "AtomStereoCount",
    "DefinedAtomStereoCount",
    "UndefinedAtomStereoCount",
    "BondStereoCount",
    "DefinedBondStereoCount",
    "UndefinedBondStereoCount",
    "CovalentUnitCount",
    "Volume3D",
    "XStericQuadrupole3D",
    "YStericQuadrupole3D",
    "ZStericQuadrupole3D",
    "FeatureCount3D",
    "FeatureAcceptorCount3D",
    "FeatureDonorCount3D",
    "FeatureAnionCount3D",
    "FeatureCationCount3D",
    "FeatureRingCount3D",
    "FeatureHydrophobeCount3D",
    "ConformerDependentDescriptorCount",
    "ConformerCount3D",
    "Fingerprint2D",
]

#: Valid cross-reference types for the ``/xrefs/`` endpoint of the PUG REST API.
XREF_TYPES = [
    "RegistryID",
    "RN",
    "PubMedID",
    "MMDBID",
    "DBURL",
    "SBURL",
    "AmericanChemicalSocietyID",
    "WikipediaURL",
    "PatentID",
    "GeneID",
    "ProteinGI",
    "TaxonomyID",
    "MIMID",
    "BioSystemID",
    "ReactomeID",
    "BioCycID",
]


class PubChem:
    """Interface to the `PubChem <https://pubchem.ncbi.nlm.nih.gov>`_ PUG REST service.

    The PubChem PUG REST API provides access to compound, substance and assay
    data stored in PubChem. URL structure follows the pattern::

        https://pubchem.ncbi.nlm.nih.gov/rest/pug/{domain}/{namespace}/{identifier}/{operation}/{format}

    Example usage::

        from bioservices import PubChem
        p = PubChem()

        # Get CIDs for aspirin by name
        cids = p.get_cids_by_name("aspirin")

        # Get compound record by CID
        record = p.get_compound_by_cid(2244)

        # Get specific properties for aspirin (CID 2244)
        props = p.get_properties(2244, properties=["MolecularFormula", "MolecularWeight"])

        # Get synonyms for aspirin
        synonyms = p.get_synonyms(2244)

    .. seealso:: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
    """

    _url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param bool verbose: set to False to prevent informative messages
        :param bool cache: set to True to cache requests
        """
        self.services = REST(name="PubChem", url=PubChem._url, verbose=verbose, cache=cache)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, path, frmt="json"):
        """Perform a GET request to the PUG REST API.

        :param str path: URL path appended to the base URL
        :param str frmt: response format (json, xml, txt, …)
        :return: parsed response
        """
        return self.services.http_get(path, frmt=frmt)

    def _post(self, path, data, frmt="json"):
        """Perform a POST request to the PUG REST API.

        POST is used when the identifier may contain characters that cannot
        be safely embedded in a URL (e.g. SMILES or InChI strings).

        :param str path: URL path appended to the base URL
        :param str data: URL-encoded form data (e.g. ``"smiles=CC(=O)O"``)
        :param str frmt: response format (json, xml, …)
        :return: parsed response
        """
        return self.services.http_post(
            path,
            frmt=frmt,
            data=data,
            headers={
                "User-Agent": self.services.getUserAgent(),
                "Accept": self.services.content_types[frmt],
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

    # ------------------------------------------------------------------
    # Compound lookup – return CIDs
    # ------------------------------------------------------------------

    def get_cids_by_name(self, name, frmt="json"):
        """Return CIDs for a compound name.

        :param str name: compound name (e.g. ``"aspirin"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list

        Example::

            p.get_cids_by_name("aspirin")
        """
        return self._get(f"compound/name/{name}/cids/{frmt.upper()}", frmt=frmt)

    def get_cids_by_smiles(self, smiles, frmt="json"):
        """Return CIDs for a SMILES string.

        Uses a POST request so that special characters in the SMILES are
        handled correctly.

        :param str smiles: SMILES string (e.g. ``"CC(=O)Oc1ccccc1C(=O)O"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list

        Example::

            p.get_cids_by_smiles("CC(=O)Oc1ccccc1C(=O)O")
        """
        return self._post(f"compound/smiles/cids/{frmt.upper()}", data=f"smiles={smiles}", frmt=frmt)

    def get_cids_by_inchi(self, inchi, frmt="json"):
        """Return CIDs for an InChI string.

        Uses a POST request to safely transmit InChI strings that contain
        special characters.

        :param str inchi: InChI string
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list
        """
        return self._post(f"compound/inchi/cids/{frmt.upper()}", data=f"inchi={inchi}", frmt=frmt)

    def get_cids_by_inchikey(self, inchikey, frmt="json"):
        """Return CIDs for an InChIKey.

        :param str inchikey: InChIKey (e.g. ``"BSYNRYMUTXBXSQ-UHFFFAOYSA-N"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list

        Example::

            p.get_cids_by_inchikey("BSYNRYMUTXBXSQ-UHFFFAOYSA-N")
        """
        return self._get(f"compound/inchikey/{inchikey}/cids/{frmt.upper()}", frmt=frmt)

    def get_cids_by_formula(self, formula, frmt="json"):
        """Return CIDs for a molecular formula.

        :param str formula: molecular formula (e.g. ``"C9H8O4"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list

        Example::

            p.get_cids_by_formula("C9H8O4")
        """
        return self._get(f"compound/formula/{formula}/cids/{frmt.upper()}", frmt=frmt)

    # ------------------------------------------------------------------
    # Compound records
    # ------------------------------------------------------------------

    def get_compound_by_cid(self, cid, frmt="json"):
        """Return the full compound record for a CID.

        :param cid: PubChem compound identifier (integer or string)
        :param str frmt: response format (default ``"json"``)
        :return: full compound record

        Example::

            p.get_compound_by_cid(2244)   # aspirin
        """
        return self._get(f"compound/cid/{cid}/{frmt.upper()}", frmt=frmt)

    def get_compound_by_name(self, name, frmt="json"):
        """Return the full compound record for a compound name.

        :param str name: compound name (e.g. ``"aspirin"``)
        :param str frmt: response format (default ``"json"``)
        :return: full compound record

        Example::

            p.get_compound_by_name("aspirin")
        """
        return self._get(f"compound/name/{name}/{frmt.upper()}", frmt=frmt)

    # ------------------------------------------------------------------
    # Compound properties, synonyms and descriptions
    # ------------------------------------------------------------------

    def get_properties(self, identifier, namespace="cid", properties=None, frmt="json"):
        """Return computed properties for a compound.

        :param identifier: compound identifier (e.g. CID ``2244`` or name ``"aspirin"``)
        :param str namespace: identifier type – one of ``"cid"``, ``"name"``,
            ``"smiles"``, ``"inchikey"`` (default ``"cid"``)
        :param properties: property name(s) to retrieve. Either a comma-separated
            string or a list of names from :data:`~bioservices.pubchem.COMPOUND_PROPERTIES`.
            Defaults to all properties when ``None``.
        :param str frmt: response format (default ``"json"``)
        :return: dict containing ``PropertyTable`` with the requested properties

        Example::

            p.get_properties(2244, properties=["MolecularFormula", "MolecularWeight"])
            p.get_properties("aspirin", namespace="name", properties="InChIKey,XLogP")
        """
        if properties is None:
            prop_str = ",".join(COMPOUND_PROPERTIES)
        elif isinstance(properties, list):
            prop_str = ",".join(properties)
        else:
            prop_str = properties

        if namespace in ("smiles", "inchi"):
            return self._post(
                f"compound/{namespace}/property/{prop_str}/{frmt.upper()}",
                data=f"{namespace}={identifier}",
                frmt=frmt,
            )
        return self._get(f"compound/{namespace}/{identifier}/property/{prop_str}/{frmt.upper()}", frmt=frmt)

    def get_synonyms(self, identifier, namespace="cid", frmt="json"):
        """Return synonyms for a compound.

        :param identifier: compound identifier
        :param str namespace: identifier type (default ``"cid"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict containing ``InformationList`` with synonym lists

        Example::

            p.get_synonyms(2244)
        """
        if namespace in ("smiles", "inchi"):
            return self._post(
                f"compound/{namespace}/synonyms/{frmt.upper()}",
                data=f"{namespace}={identifier}",
                frmt=frmt,
            )
        return self._get(f"compound/{namespace}/{identifier}/synonyms/{frmt.upper()}", frmt=frmt)

    def get_description(self, identifier, namespace="cid", frmt="json"):
        """Return the description for a compound.

        :param identifier: compound identifier
        :param str namespace: identifier type (default ``"cid"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict containing ``InformationList`` with description text

        Example::

            p.get_description(2244)
            p.get_description("aspirin", namespace="name")
        """
        if namespace in ("smiles", "inchi"):
            return self._post(
                f"compound/{namespace}/description/{frmt.upper()}",
                data=f"{namespace}={identifier}",
                frmt=frmt,
            )
        return self._get(f"compound/{namespace}/{identifier}/description/{frmt.upper()}", frmt=frmt)

    def get_xrefs(self, identifier, xref_type, namespace="cid", frmt="json"):
        """Return cross-references for a compound.

        :param identifier: compound identifier
        :param str xref_type: cross-reference type, one of
            ``"RegistryID"``, ``"RN"``, ``"PubMedID"``, ``"MMDBID"``,
            ``"PatentID"``, ``"WikipediaURL"``, ``"GeneID"``, etc.
            See :data:`~bioservices.pubchem.XREF_TYPES` for the full list.
        :param str namespace: identifier type (default ``"cid"``)
        :param str frmt: response format (default ``"json"``)
        :return: dict containing cross-reference list

        Example::

            p.get_xrefs(2244, "PatentID")
        """
        return self._get(f"compound/{namespace}/{identifier}/xrefs/{xref_type}/{frmt.upper()}", frmt=frmt)

    # ------------------------------------------------------------------
    # Compound cross-domain links
    # ------------------------------------------------------------------

    def get_sids_by_cid(self, cid, frmt="json"):
        """Return substance IDs (SIDs) deposited for a given compound CID.

        :param cid: PubChem compound identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``SID`` list

        Example::

            p.get_sids_by_cid(2244)
        """
        return self._get(f"compound/cid/{cid}/sids/{frmt.upper()}", frmt=frmt)

    def get_aids_by_cid(self, cid, frmt="json"):
        """Return assay IDs (AIDs) that tested a given compound CID.

        :param cid: PubChem compound identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``AID`` list

        Example::

            p.get_aids_by_cid(2244)
        """
        return self._get(f"compound/cid/{cid}/aids/{frmt.upper()}", frmt=frmt)

    def get_assay_summary(self, cid, frmt="json"):
        """Return a bioactivity summary for a compound.

        :param cid: PubChem compound identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict containing assay summary data

        Example::

            p.get_assay_summary(2244)
        """
        return self._get(f"compound/cid/{cid}/assaysummary/{frmt.upper()}", frmt=frmt)

    # ------------------------------------------------------------------
    # Substance operations
    # ------------------------------------------------------------------

    def get_substance_by_sid(self, sid, frmt="json"):
        """Return the full substance record for a SID.

        :param sid: PubChem substance identifier
        :param str frmt: response format (default ``"json"``)
        :return: full substance record

        Example::

            p.get_substance_by_sid(100)
        """
        return self._get(f"substance/sid/{sid}/{frmt.upper()}", frmt=frmt)

    def get_cids_by_sid(self, sid, frmt="json"):
        """Return compound CIDs standardised from a given substance SID.

        :param sid: PubChem substance identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list

        Example::

            p.get_cids_by_sid(100)
        """
        return self._get(f"substance/sid/{sid}/cids/{frmt.upper()}", frmt=frmt)

    # ------------------------------------------------------------------
    # Assay operations
    # ------------------------------------------------------------------

    def get_assay(self, aid, frmt="json"):
        """Return the full assay record for an AID.

        :param aid: PubChem assay identifier
        :param str frmt: response format (default ``"json"``)
        :return: full assay record

        Example::

            p.get_assay(1)
        """
        return self._get(f"assay/aid/{aid}/{frmt.upper()}", frmt=frmt)

    def get_assay_description(self, aid, frmt="json"):
        """Return the description section of an assay.

        :param aid: PubChem assay identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict containing assay description

        Example::

            p.get_assay_description(1)
        """
        return self._get(f"assay/aid/{aid}/description/{frmt.upper()}", frmt=frmt)

    def get_cids_by_aid(self, aid, frmt="json"):
        """Return CIDs tested in a given assay.

        :param aid: PubChem assay identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list

        Example::

            p.get_cids_by_aid(1)
        """
        return self._get(f"assay/aid/{aid}/cids/{frmt.upper()}", frmt=frmt)

    def get_sids_by_aid(self, aid, frmt="json"):
        """Return SIDs tested in a given assay.

        :param aid: PubChem assay identifier
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``SID`` list

        Example::

            p.get_sids_by_aid(1)
        """
        return self._get(f"assay/aid/{aid}/sids/{frmt.upper()}", frmt=frmt)

    # ------------------------------------------------------------------
    # Backward compatibility
    # ------------------------------------------------------------------

    def get_compound_by_smiles(self, identifier, frmt="json"):
        """Return CIDs for a SMILES string.

        .. deprecated::
            Use :meth:`get_cids_by_smiles` instead. This method is kept for
            backward compatibility.

        :param str identifier: SMILES string
        :param str frmt: response format (default ``"json"``)
        :return: dict with ``IdentifierList`` key containing ``CID`` list
        """
        return self.get_cids_by_smiles(identifier, frmt=frmt)
