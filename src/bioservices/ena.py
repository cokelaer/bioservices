#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
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
# $Id: chembldb.py 318 2014-02-28 13:30:26Z cokelaer $

"""This module provides a class :class:`ENA`

.. topic:: What is ENA

    :URL:  https://www.ebi.ac.uk/ena


    .. highlights::

        The European Nucleotide Archive (ENA) provides a comprehensive 
        record of the world's nucleotide sequencing information, covering 
        raw sequencing data, sequence assembly information and functional 
        annotation. 

        -- From ENA web page Jan 2016

.. addedversion:: 1.4.4

"""
import os
from bioservices.services import REST
import webbrowser

__all__ = ["ENA"]


class ENA(REST):
    """Interface to `ChEMBL <http://www.ebi.ac.uk/ena/index.php>`_

    Here is a quick example to retrieve a target given its ChEMBL Id

    .. doctest::

        >>> from bioservices import ChEMBL
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
    


    .. todo:: Taxon viewer, image retrieval.

    """
    _url = "http://www.ebi.ac.uk/ena/data"


    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(ENA, self).__init__(name="ENA", url=ENA._url,
                verbose=verbose, cache=cache)
        self.TIMEOUT = 100

    def get_data(self, identifier, frmt, fasta_range=None, expanded=None,
            header=None, download=None):
        """

        :param frmt : xml, text, fasta, fastq, html


        .. todo:: download and save at the same time. Right now the fasta is
            retuned as a string and needs to be saved manually. It may also be
            an issue with very large fasta files.
        """

        # somehow the params param does not work, we need to construct the
        # entire url
        url = self.url + '/view/' + identifier
        #assert frmt in ['fasta', 'xml', 'text'], \
        #    "Only fasta, xml and text are recognised"
        url += "&display=%s" % frmt

        if fasta_range is not None:
            url += "&range=%s-%s" % (fasta_range[0], fasta_range[1])

        if expanded is not None and expanded is True:
            url += "&expanded=true"

        if header is not None and header is True:
            url += "&header=true"

        if download is not None:
            url += "&download=%s" % download

        res = self.http_get(url)
        res = res.content
        return res

    def view_data(self, identifier, fasta_range=None):
        url = self.url + '/view/' + identifier
        if fasta_range is not None:
            url += "&range=%s-%s" % (fasta_range[0], fasta_range[1])
        self.on_web(url)

    def data_warehouse(self):
        #http://www.ebi.ac.uk/ena/data/warehouse/search?query="geo_circ(-0.587,-90.5713,170)"&result=sequence_release&display=text&download=gzip
        pass

    def get_taxon(self, taxon):
        return e.get_data("Taxon:%s" % taxon, "xml").decode()

