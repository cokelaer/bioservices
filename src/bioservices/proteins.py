#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      https://github.com/cokelaer/bioservices
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  source: http://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################

"""Interface to the EBI Proteins web service

.. topic:: What is the EBI Proteins API ?

    :URL: https://www.ebi.ac.uk/proteins/api/doc/

    .. highlights::

        The Proteins API provides access to key biological data from UniProt
        and data from Large Scale Studies (LSS) mapped to UniProt. This
        includes sequence features, mutagenesis data, gene-centric information,
        and taxonomy information.

        -- From EBI Proteins API web site

"""

from bioservices import logger
from bioservices.services import REST

logger.name = __name__

__all__ = ["Proteins"]


class Proteins:
    """Interface to the `EBI Proteins API <https://www.ebi.ac.uk/proteins/api/doc/>`_

    This service provides access to protein sequences and functional
    information, sequence features, mutagenesis data, gene-centric information,
    and taxonomy.

    ::

        from bioservices import Proteins
        p = Proteins()
        res = p.get_proteins(accession="P12345")

    """

    _url = "https://www.ebi.ac.uk/proteins/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param bool verbose: print informative messages
        :param bool cache: set to True to use caching
        """
        self.services = REST(name="Proteins", url=Proteins._url, verbose=verbose, cache=cache)

    # ------------------------------------------------------------------
    # Proteins
    # ------------------------------------------------------------------

    def get_proteins(
        self,
        accession=None,
        offset=0,
        size=100,
        reviewed=None,
        isoform=None,
        goterms=None,
        keywords=None,
        ec=None,
        gene=None,
        exact_gene=None,
        protein=None,
        organism=None,
        taxid=None,
        pubmed=None,
        seq_length=None,
        md5=None,
    ):
        """Search and retrieve proteins from UniProt

        :param str accession: UniProt accession(s), comma-separated
        :param int offset: start position in the result set (default 0)
        :param int size: number of results (default 100, max 100)
        :param str reviewed: filter by reviewed status ('true' or 'false')
        :param int isoform: isoform number (0 = canonical only, 1 = all)
        :param str goterms: GO term ID(s), comma-separated
        :param str keywords: keyword ID(s), comma-separated
        :param str ec: EC number(s), comma-separated
        :param str gene: gene name(s), comma-separated
        :param str exact_gene: exact gene name(s), comma-separated
        :param str protein: protein name
        :param str organism: organism name
        :param int taxid: NCBI taxonomy ID(s), comma-separated
        :param str pubmed: PubMed ID(s), comma-separated
        :param str seq_length: sequence length range (e.g. '100-200')
        :param str md5: MD5 checksum of the protein sequence
        :return: list of protein records

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_proteins(accession="P12345")

        """
        optional = {
            "accession": accession,
            "reviewed": reviewed,
            "isoform": isoform,
            "goterms": goterms,
            "keywords": keywords,
            "ec": ec,
            "gene": gene,
            "exact_gene": exact_gene,
            "protein": protein,
            "organism": organism,
            "taxid": taxid,
            "pubmed": pubmed,
            "seqLength": seq_length,
            "md5": md5,
        }
        params = {"offset": offset, "size": size}
        params.update({k: v for k, v in optional.items() if v is not None})

        res = self.services.http_get("proteins", frmt="json", params=params)
        return res

    def get_protein(self, accession):
        """Retrieve a single protein by its UniProt accession

        :param str accession: a valid UniProt accession (e.g. 'P12345')
        :return: protein record as a dictionary

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_protein("P12345")
            >>> res["accession"]
            'P12345'

        """
        res = self.services.http_get(f"proteins/{accession}", frmt="json")
        return res

    # ------------------------------------------------------------------
    # Features
    # ------------------------------------------------------------------

    def get_features(self, accession):
        """Retrieve sequence features for a protein

        :param str accession: a valid UniProt accession (e.g. 'P12345')
        :return: feature data as a dictionary

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_features("P12345")

        """
        res = self.services.http_get(f"features/{accession}", frmt="json")
        return res

    # ------------------------------------------------------------------
    # Mutagenesis
    # ------------------------------------------------------------------

    def get_mutagenesis(self, accession):
        """Retrieve mutagenesis data for a protein

        :param str accession: a valid UniProt accession (e.g. 'P12345')
        :return: mutagenesis data as a dictionary

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_mutagenesis("P12345")

        """
        res = self.services.http_get(f"mutagenesis/{accession}", frmt="json")
        return res

    # ------------------------------------------------------------------
    # Gene-centric
    # ------------------------------------------------------------------

    def get_genecentric(self, accession):
        """Retrieve gene-centric view for a protein

        :param str accession: a valid UniProt accession (e.g. 'P12345')
        :return: gene-centric data as a dictionary

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_genecentric("P12345")

        """
        res = self.services.http_get(f"genecentric/{accession}", frmt="json")
        return res

    # ------------------------------------------------------------------
    # Taxonomy
    # ------------------------------------------------------------------

    def get_taxonomy(self, tax_id):
        """Retrieve taxonomic information by NCBI taxonomy ID

        :param int tax_id: NCBI taxonomy ID (e.g. 9606 for Homo sapiens)
        :return: taxonomy record as a dictionary

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_taxonomy(9606)
            >>> res["taxonomyId"]
            9606

        """
        res = self.services.http_get(f"taxonomy/id/{tax_id}", frmt="json")
        return res

    def get_taxonomy_by_name(self, name, field=None, pageNumber=1, pageSize=200):
        """Retrieve taxonomic information by organism name

        :param str name: organism name (partial or full), e.g. 'homo sapiens'
        :param str field: which field to search. One of 'scientificName',
            'commonName', 'mnemonic'. Defaults to all fields.
        :param int pageNumber: page number for paginated results (default 1)
        :param int pageSize: number of results per page (default 200, max 200)
        :return: list of taxonomy records

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_taxonomy_by_name("homo sapiens")

        """
        params = {"pageNumber": pageNumber, "pageSize": pageSize}
        if field is not None:
            params["fieldName"] = field
        res = self.services.http_get(f"taxonomy/name/{name}", frmt="json", params=params)
        return res

    def get_taxonomy_lineage(self, tax_id):
        """Retrieve taxonomic lineage for an NCBI taxonomy ID

        :param int tax_id: NCBI taxonomy ID (e.g. 9606 for Homo sapiens)
        :return: list of taxonomy records representing the lineage from root
            down to (and including) the specified node

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_taxonomy_lineage(9606)

        """
        res = self.services.http_get(f"taxonomy/lineage/{tax_id}", frmt="json")
        return res

    def get_taxonomy_siblings(self, tax_id, pageNumber=1, pageSize=200):
        """Retrieve the siblings (nodes at the same level) of a taxonomy node

        :param int tax_id: NCBI taxonomy ID
        :param int pageNumber: page number for paginated results (default 1)
        :param int pageSize: number of results per page (default 200, max 200)
        :return: list of sibling taxonomy records

        ::

            >>> from bioservices import Proteins
            >>> p = Proteins()
            >>> res = p.get_taxonomy_siblings(9606)

        """
        params = {"pageNumber": pageNumber, "pageSize": pageSize}
        res = self.services.http_get(f"taxonomy/siblings/{tax_id}", frmt="json", params=params)
        return res
