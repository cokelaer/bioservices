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
"""Interface to the NCBI Gene Expression Omnibus (GEO) web service.

.. topic:: What is NCBI GEO?

    :URL: https://www.ncbi.nlm.nih.gov/geo/
    :REST: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/

    .. highlights::

        GEO is a public functional genomics data repository supporting MIAME-compliant
        data submissions. Array- and sequence-based data are accepted. Tools are provided
        to help users query and download experiments and curated gene expression profiles.

        -- From NCBI GEO Home Page

    The Bioconductor R package ``GEOquery`` provides a similar interface to the
    NCBI GEO database. This module provides an equivalent Python interface using
    the NCBI Entrez utilities (E-utilities) REST API, which is also used by
    the ``rentrez`` Bioconductor package.

    GEO accession types:

    - **GSE** (GEO Series): a set of related Samples that are considered to be
      part of a group
    - **GSM** (GEO Sample): describes the conditions under which an individual
      Sample was handled, the manipulations it underwent, and the abundance
      measurement of each element derived from it
    - **GPL** (GEO Platform): describes the array or sequencer used
    - **GDS** (GEO DataSet): curated set of GEO Sample data from a series

"""

from bioservices import logger
from bioservices.services import REST

logger.name = __name__

__all__ = ["GEO"]


class GEO:
    """Interface to the `NCBI Gene Expression Omnibus (GEO)
    <https://www.ncbi.nlm.nih.gov/geo/>`_ database.

    GEO is a public functional genomics data repository supporting MIAME-compliant
    data submissions. This class provides programmatic access to search and
    retrieve GEO records using the NCBI E-utilities REST API.

    The Bioconductor R package ``GEOquery`` provides an equivalent R interface
    to the same database.

    Example usage::

        from bioservices import GEO
        g = GEO()

        # Search GEO for datasets related to a topic
        results = g.search("breast cancer AND Homo sapiens[organism]")

        # Get a GEO record summary by accession
        summary = g.get_summary("GSE10")

        # Fetch detailed information for a GEO accession
        record = g.fetch("GSE10")

    .. note::

        Some methods use the NCBI E-utilities which may require an API key
        for high-volume access. See https://www.ncbi.nlm.nih.gov/account/ for
        API key registration.

    """

    _url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # Valid GEO databases accessible via E-utilities
    _valid_db = ("gds", "geo")

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param bool verbose: print informative messages (default False)
        :param bool cache: use caching (default False)
        """
        self.services = REST(name="GEO", url=GEO._url, verbose=verbose, cache=cache)

    def search(self, query, db="gds", retmax=20, retstart=0):
        """Search GEO for datasets matching a query term.

        :param str query: search query. Supports NCBI Entrez query syntax.
            Examples:

            - ``"breast cancer"``
            - ``"breast cancer AND Homo sapiens[organism]"``
            - ``"GSE10[ACCN]"``
            - ``"expression profiling[DataSet Type]"``

        :param str db: GEO database to search. Either ``"gds"`` (GEO DataSets,
            default) or ``"geo"`` (all GEO records).
        :param int retmax: maximum number of results to return (default: 20,
            max: 10000)
        :param int retstart: index of first result to return (default: 0,
            used for pagination)
        :return: dict with search results containing ``count``, ``idlist``,
            and ``translationset``
        :rtype: dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> results = g.search("breast cancer AND Homo sapiens[organism]")
            >>> print(results["count"])

        """
        params = {
            "db": db,
            "term": query,
            "retmax": retmax,
            "retstart": retstart,
            "retmode": "json",
        }
        res = self.services.http_get("esearch.fcgi", frmt="json", params=params)
        if isinstance(res, dict) and "esearchresult" in res:
            return res["esearchresult"]
        return res

    def get_summary(self, uid, db="gds"):
        """Get summary information for one or more GEO records by UID or accession.

        :param uid: GEO UID (integer or string) or accession (e.g., ``"GSE10"``).
            Can also be a comma-separated list or a Python list of UIDs.
        :param str db: GEO database. Either ``"gds"`` (default) or ``"geo"``.
        :return: dict with summary data for the requested record(s)
        :rtype: dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> summary = g.get_summary("200000010")  # GDS UID for GSE10
            >>> summary = g.get_summary(["200000010", "200000011"])

        """
        if isinstance(uid, (list, tuple)):
            uid = ",".join(str(u) for u in uid)
        else:
            uid = str(uid)
        params = {
            "db": db,
            "id": uid,
            "retmode": "json",
        }
        res = self.services.http_get("esummary.fcgi", frmt="json", params=params)
        if isinstance(res, dict) and "result" in res:
            return res["result"]
        return res

    def fetch(self, uid, db="gds", rettype="summary", retmode="text"):
        """Fetch detailed information for a GEO record.

        :param uid: GEO UID (integer or string) or accession string.
            Can also be a comma-separated list or Python list of UIDs.
        :param str db: GEO database. Either ``"gds"`` (default) or ``"geo"``.
        :param str rettype: retrieval type. For ``gds``: ``"summary"``
            (default), ``"full"``, ``"brief"``, ``"uilist"``. For sequence
            records other types may apply.
        :param str retmode: retrieval mode. Either ``"text"`` (default)
            or ``"xml"``.
        :return: record text or parsed data
        :rtype: str or dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> record = g.fetch("200000010")

        """
        if isinstance(uid, (list, tuple)):
            uid = ",".join(str(u) for u in uid)
        else:
            uid = str(uid)
        params = {
            "db": db,
            "id": uid,
            "rettype": rettype,
            "retmode": retmode,
        }
        res = self.services.http_get("efetch.fcgi", frmt=retmode, params=params)
        return res

    def get_accession_info(self, accession):
        """Get information about a GEO record by its accession number.

        Accepts GEO accession numbers like ``GSE10``, ``GSM12``, ``GPL96``, or
        ``GDS1234``. First searches for the UID corresponding to the accession,
        then retrieves the summary.

        :param str accession: GEO accession number (e.g., ``"GSE10"``,
            ``"GSM12"``, ``"GPL96"``, ``"GDS1234"``)
        :return: dict with summary information for the accession, or None if
            not found
        :rtype: dict or None

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> info = g.get_accession_info("GSE10")

        """
        # Determine the correct database from the accession prefix
        acc = accession.upper()
        if acc.startswith("GDS"):
            db = "gds"
        elif acc.startswith("GSE") or acc.startswith("GSM") or acc.startswith("GPL"):
            db = "gds"
        else:
            db = "gds"

        # Search by accession
        search_res = self.search(f"{accession}[ACCN]", db=db, retmax=1)
        if not search_res or not search_res.get("idlist"):
            return None

        uid = search_res["idlist"][0]
        return self.get_summary(uid, db=db)

    def get_geo_datasets(self, query, organism=None, dataset_type=None, retmax=20):
        """Search for GEO DataSets (GDS) matching a query.

        :param str query: search query term
        :param str organism: optional organism filter (e.g., ``"Homo sapiens"``,
            ``"Mus musculus"``)
        :param str dataset_type: optional dataset type filter. Common values:
            ``"Expression profiling by array"``,
            ``"Expression profiling by high throughput sequencing"``,
            ``"Genome binding/occupancy profiling by high throughput sequencing"``
        :param int retmax: maximum number of results to return (default: 20)
        :return: dict with search results
        :rtype: dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> results = g.get_geo_datasets("breast cancer", organism="Homo sapiens")

        """
        full_query = query
        if organism:
            full_query += f" AND {organism}[organism]"
        if dataset_type:
            full_query += f' AND "{dataset_type}"[DataSet Type]'
        return self.search(full_query, db="gds", retmax=retmax)

    def get_geo_series(self, query, organism=None, retmax=20):
        """Search for GEO Series (GSE) matching a query.

        :param str query: search query term
        :param str organism: optional organism filter (e.g., ``"Homo sapiens"``)
        :param int retmax: maximum number of results to return (default: 20)
        :return: dict with search results
        :rtype: dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> results = g.get_geo_series("BRCA1 expression", organism="Homo sapiens")

        """
        full_query = f"{query} AND gse[ETYP]"
        if organism:
            full_query += f" AND {organism}[organism]"
        return self.search(full_query, db="gds", retmax=retmax)

    def get_geo_samples(self, query, organism=None, retmax=20):
        """Search for GEO Samples (GSM) matching a query.

        :param str query: search query term
        :param str organism: optional organism filter (e.g., ``"Homo sapiens"``)
        :param int retmax: maximum number of results to return (default: 20)
        :return: dict with search results
        :rtype: dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> results = g.get_geo_samples("breast cancer", organism="Homo sapiens")

        """
        full_query = f"{query} AND gsm[ETYP]"
        if organism:
            full_query += f" AND {organism}[organism]"
        return self.search(full_query, db="gds", retmax=retmax)

    def get_geo_platforms(self, query, organism=None, retmax=20):
        """Search for GEO Platforms (GPL) matching a query.

        :param str query: search query term
        :param str organism: optional organism filter (e.g., ``"Homo sapiens"``)
        :param int retmax: maximum number of results to return (default: 20)
        :return: dict with search results
        :rtype: dict

        ::

            >>> from bioservices import GEO
            >>> g = GEO()
            >>> results = g.get_geo_platforms("Affymetrix", organism="Homo sapiens")

        """
        full_query = f"{query} AND gpl[ETYP]"
        if organism:
            full_query += f" AND {organism}[organism]"
        return self.search(full_query, db="gds", retmax=retmax)
