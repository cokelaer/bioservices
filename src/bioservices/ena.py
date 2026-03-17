#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
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
"""This module provides a class :class:`ENA`

.. topic:: What is ENA

    :URL:  https://www.ebi.ac.uk/ena


    .. highlights::

        The European Nucleotide Archive (ENA) provides a comprehensive
        record of the world's nucleotide sequencing information, covering
        raw sequencing data, sequence assembly information and functional
        annotation.

        -- From ENA web page Jan 2016

.. versionadded:: 1.4.4

"""
from bioservices import logger
from bioservices.services import REST

logger.name = __name__


__all__ = ["ENA"]


class ENA:
    """Interface to the `ENA <http://www.ebi.ac.uk/ena>`_ (European Nucleotide Archive)

    .. doctest::

        >>> from bioservices import ENA
        >>> s = ENA(verbose=False)

    Retrieve read domain metadata in XML format::

        print(e.get_data('ERA000092', 'xml'))

    Retrieve assembled and annotated sequences in FASTA format::

        print(e.get_data('A00145', 'fasta'))

    The range parameter can be used to retrieve a subsequence
    from sequence entry A00145 from bases 3 to 63::

        e.get_data('A00145', 'fasta', fasta_range=[3, 63])

    Retrieve assembled and annotated subsequences in HTML format::

        e.view_data('A00145')

    Retrieve expanded CON records:

    To retrieve expanded CON records use the ``expanded=True`` parameter. For
    example, the expanded CON entry AL513382 in flat file format can be
    obtained as follows::

        e.get_data('AL513382', frmt='text', expanded=True)

    Expanded CON records differ from CON records in two ways:
    firstly, they contain the full sequence in addition to the contig assembly
    instructions; secondly, if a CON record contains only source or gap
    features, the expanded CON records will also display all features from the
    segment records.

    Retrieve assembled and annotated sequence header in flat file format using
    the ``header=True`` parameter::

        e.get_data('BN000065', 'text', header=True)

    Retrieve assembled and annotated sequence records using sequence versions::

        e.get_data('AM407889.1', 'fasta')
        e.get_data('AM407889.2', 'fasta')

    """

    url = "http://www.ebi.ac.uk/ena/browser/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        self.services = REST(name="ENA", url=ENA.url, verbose=verbose, cache=cache)
        self.services.TIMEOUT = 100

    def get_data(
        self,
        identifier,
        frmt,
        fasta_range=None,
        expanded=None,
        header=None,
        download=None,
    ):
        """Retrieve an ENA entry in the specified format.

        :param str identifier: ENA accession or identifier (e.g. ``'AL513382'``)
        :param str frmt: output format — one of ``xml``, ``text``, ``fasta``,
            ``fastq``, ``html``, ``embl`` (availability depends on entry type)
        :param list fasta_range: ``[start, end]`` base positions for subsequence
            retrieval (FASTA only)
        :param bool expanded: if True, return expanded CON records
        :param bool header: if True, return only the sequence header
        :param bool download: if True, return data as a downloadable file

        ::

            get_data("AL513382", "embl")

        .. note:: The ENA API changed in 2020; this method wraps the current REST API.
        """

        url = f"{self.url}/{frmt}/{identifier}"

        if frmt in ["text", "fasta", "fastq"]:
            res = self.services.http_get(url, frmt="txt")
        elif frmt in ["html"]:
            res = self.services.http_get(url, frmt="default")
        elif frmt in ["xml"]:
            res = self.services.http_get(url, frmt="xml")
        return res

    def data_warehouse(self):
        # http://www.ebi.ac.uk/ena/data/warehouse/search?query="geo_circ(-0.587,-90.5713,170)"&result=sequence_release&display=text&download=gzip
        pass

    def get_taxon(self, taxon):
        """.. deprecated:: 7.8 — removed due to ENA API update."""
        print("deprecated since v.7.8 due to ENA update")
