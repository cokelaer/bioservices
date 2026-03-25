#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EMBL-EBI
#
#  File author(s):
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
"""Interface to the NCBI BLAST URL API

.. topic:: What is the NCBI BLAST URL API?

    :URL: https://blast.ncbi.nlm.nih.gov/
    :API: https://ncbi.github.io/blast-cloud/dev/api.html

    .. highlights::

        "NCBI BLAST finds regions of similarity between biological sequences.
        The program compares nucleotide or protein sequences to sequence
        databases and calculates the statistical significance."

        -- NCBI BLAST documentation

    Unlike :class:`~bioservices.ncbiblast.NCBIblast`, which wraps the EBI
    mirror of NCBI BLAST, this class submits jobs **directly to NCBI's own
    BLAST server**.  This gives access to NCBI databases (``nt``, ``nr``,
    ``refseq_genomic``, …) under their native GenBank accession format,
    with no EBI-specific database name translation required.

    Typical usage::

        from bioservices import NCBIBlastAPI
        b = NCBIBlastAPI()
        rid, rtoe = b.run(
            program="blastn",
            database="nt",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTTT",
            email="you@example.org",
        )
        b.wait(rid, rtoe)
        xml = b.get_result(rid)   # BLAST XML string

"""
import re
import time

from bioservices import logger
from bioservices.services import REST

logger.name = __name__

__all__ = ["NCBIBlastAPI"]

# NCBI recommends ≤3 requests/sec without an API key, ≤10/sec with one.
_MIN_POLL_INTERVAL = 15  # seconds — NCBI asks clients not to poll more often


class NCBIBlastAPI:
    """Interface to NCBI BLAST via NCBI's own URL API.

    Jobs are submitted with :meth:`run`, polled with :meth:`get_status` or
    :meth:`wait`, and results retrieved with :meth:`get_result`.

    :param bool verbose: print debug messages (default False).
    :param api_key: NCBI API key.  Raises the rate limit from 3 to 10
        requests per second.  Obtain one at
        https://www.ncbi.nlm.nih.gov/account/

    Common databases
    ----------------
    =====================  ================================================
    ``nt``                 NCBI nucleotide collection (all GenBank + RefSeq)
    ``nr``                 NCBI non-redundant protein sequences
    ``refseq_genomic``     RefSeq genomic sequences
    ``refseq_rna``         RefSeq RNA sequences
    ``refseq_protein``     RefSeq protein sequences
    ``swissprot``          UniProtKB/Swiss-Prot
    ``pdbaa``              PDB protein sequences
    ``pdbnt``              PDB nucleotide sequences
    ``env_nt``             Environmental nucleotide sequences (metagenomics)
    =====================  ================================================

    Example::

        from bioservices import NCBIBlastAPI

        b = NCBIBlastAPI()
        rid, rtoe = b.run(
            program="blastn",
            database="nt",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTTT",
            email="you@example.org",
            hitlist_size=10,
        )
        b.wait(rid, rtoe)
        xml_text = b.get_result(rid)

    """

    _url = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"

    _nucleotide_example = "ATGAAAGCAATTTTCGTACTGAAAGGTTTTGTTGGTTTTTTTTCGTTTTTGAATC"
    _protein_example = "MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"

    _programs = ["blastn", "blastp", "blastx", "tblastn", "tblastx"]

    def __init__(self, verbose=False, api_key=None):
        self.services = REST(name="NCBIBlastAPI", url=self._url, verbose=verbose)
        self.api_key = api_key
        self.check_interval = _MIN_POLL_INTERVAL

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, program, database, sequence, email, evalue="1e-10", hitlist_size=100, **kwargs):
        """Submit a BLAST job to NCBI and return the request identifier.

        :param str program: BLAST program — one of ``blastn``, ``blastp``,
            ``blastx``, ``tblastn``, ``tblastx``.
        :param str database: target database (e.g. ``"nt"``, ``"nr"``).
        :param str sequence: query sequence in FASTA or bare sequence format.
        :param str email: contact address forwarded to NCBI (required by their
            usage policy).
        :param str evalue: E-value threshold (default ``"1e-10"``).
        :param int hitlist_size: maximum number of hits to return (default 100).
        :param kwargs: additional NCBI BLAST parameters forwarded verbatim,
            e.g. ``WORD_SIZE``, ``FILTER``, ``GAPCOSTS``, ``MATRIX_NAME``,
            ``MEGABLAST``.
        :returns: ``(rid, rtoe)`` — the NCBI request ID and estimated wait
            time in seconds.
        :rtype: tuple[str, int]

        Example::

            rid, rtoe = b.run(
                program="blastn",
                database="nt",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTTT",
                email="you@example.org",
            )

        """
        if program not in self._programs:
            raise ValueError(f"Invalid program '{program}'. Choose from: {self._programs}")

        params = {
            "CMD": "Put",
            "PROGRAM": program,
            "DATABASE": database,
            "QUERY": sequence,
            "HITLIST_SIZE": hitlist_size,
            "EXPECT": evalue,
            "EMAIL": email,
            "TOOL": "bioservices",
            "FORMAT_TYPE": "XML",
        }
        if self.api_key:
            params["api_key"] = self.api_key
        params.update(kwargs)

        response = self.services.session.post(self._url, data=params)
        response.raise_for_status()
        return self._parse_submission(response.text)

    def get_status(self, rid):
        """Return the current status of a submitted job.

        :param str rid: request ID returned by :meth:`run`.
        :returns: one of ``"WAITING"``, ``"READY"``, ``"FAILED"``,
            ``"UNKNOWN"``.
        :rtype: str

        """
        params = {
            "CMD": "Get",
            "FORMAT_OBJECT": "SearchInfo",
            "RID": rid,
        }
        if self.api_key:
            params["api_key"] = self.api_key

        response = self.services.session.get(self._url, params=params)
        response.raise_for_status()
        return self._parse_status(response.text)

    def get_result(self, rid, format_type="XML"):
        """Retrieve results for a finished job.

        :param str rid: request ID returned by :meth:`run`.
        :param str format_type: output format.  ``"XML"`` (default) returns
            standard BLAST XML; ``"Text"`` returns the pairwise text report;
            ``"Tabular"`` returns tab-separated hits; ``"JSON2"`` returns
            JSON.
        :returns: result content as a string.
        :rtype: str
        :raises RuntimeError: if the job is not yet ready.

        """
        status = self.get_status(rid)
        if status == "WAITING":
            raise RuntimeError(f"Job {rid} is still running. Call wait() first.")
        if status == "FAILED":
            raise RuntimeError(f"Job {rid} failed on NCBI's servers.")

        params = {
            "CMD": "Get",
            "RID": rid,
            "FORMAT_TYPE": format_type,
        }
        if self.api_key:
            params["api_key"] = self.api_key

        response = self.services.session.get(self._url, params=params)
        response.raise_for_status()
        return response.text

    def wait(self, rid, rtoe=None):
        """Block until the job identified by *rid* is finished.

        :param str rid: request ID returned by :meth:`run`.
        :param int rtoe: estimated wait time in seconds returned by
            :meth:`run`.  When provided, the first poll is delayed by
            *rtoe* seconds so NCBI is not hit unnecessarily early.
        :returns: final status string (``"READY"`` or ``"FAILED"``).
        :rtype: str

        """
        if rtoe:
            self.services.logging.info(f"Waiting {rtoe}s before first poll (RTOE from NCBI)…")
            time.sleep(max(rtoe, self.check_interval))

        while True:
            status = self.get_status(rid)
            self.services.logging.info(f"Job {rid}: {status}")
            if status in ("READY", "FAILED", "UNKNOWN"):
                return status
            time.sleep(self.check_interval)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_submission(html):
        """Extract RID and RTOE from the NCBI submission response."""
        rid_match = re.search(r"RID\s*=\s*(\S+)", html)
        rtoe_match = re.search(r"RTOE\s*=\s*(\d+)", html)
        if not rid_match:
            raise RuntimeError(
                "Could not extract RID from NCBI BLAST response. "
                "NCBI may be temporarily unavailable or the request was malformed."
            )
        rid = rid_match.group(1)
        rtoe = int(rtoe_match.group(1)) if rtoe_match else _MIN_POLL_INTERVAL
        return rid, rtoe

    @staticmethod
    def _parse_status(html):
        """Extract job status from the NCBI status-check response."""
        match = re.search(r"Status\s*=\s*(\w+)", html)
        if not match:
            return "UNKNOWN"
        return match.group(1).upper()
