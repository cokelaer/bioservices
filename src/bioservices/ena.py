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
import os
from bioservices.services import REST
import webbrowser
from bioservices import logger

logger.name = __name__


__all__ = ["ENA"]


class ENA:
    """Interface to `ChEMBL <http://www.ebi.ac.uk/ena/index.php>`_

    Here is a quick example to retrieve a target given its ChEMBL Id

    .. doctest::

        >>> from bioservices import ENA
        >>> s = ENA(verbose=False)


    Retrieve read domain metadata in XML format::

        print(e.get_data('ERA000092', 'xml'))

    Retrieve assemble and annotated sequences in fasta format::

        print(e.get_data('A00145', 'fasta'))

    The range parameter can be used in combination to retrieve a subsequence
    from sequence entry A00145 from bases 3 to 63 using ::

        e.get_data('A00145', 'fasta', fasta_range=[3,63])

    Retrieve assembled and annotated subsequences in HTML format (same
    as above but in HTML page).

        e.view_data('A00145')


    Retrieve expanded CON records:

    To retrieve expanded CON records use the expanded=true parameter. For
    example, the expanded CON entry AL513382 in flat file format can be i
    obtained as follows::

        e.get_data('AL513382', frmt='text', expanded=True)

    Expanded CON records are different from CON records in two ways.
    Firstly, the expanded CON records contain the full sequence in addition
    to the contig assembly instructions. Secondly, if a CON record contains
    only source or gap features the expanded CON records will also display
    all features from the segment records.

    Retrieve assembled and annotated sequence header in flat file format

    To retrieve assembled and annotated sequence header in flat file
    format please use the header=true parameter, e.g.:

        e.get_data('BN000065', 'text', header=True)


    Retrieve assembled and annotated sequence records using sequence
    versions::

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
        """

        :param frmt : xml, text, fasta, fastq, html, embl but does depend on the
            entry

        Example:

            get_data("/AL513382", "embl")

        ENA API changed in 2020 but we tried to keep the same services in this
        method.
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
        print("deprecated since v.7.8 due to ENA update")
