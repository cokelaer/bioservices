#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Patrick Short
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################

# About Clinvitae (http://clinvitae.invitae.com/)

# "CLINVITAE is a database of clinically-observed genetic variants aggregated
# from public sources, operated and made freely available by INVITAE." - CLINVITAE website

from bioservices.services import REST

__all__ = ["Clinvitae"]


class Clinvitae(REST):
    """
    class for interfacing with the Clinvitae web service

    Requests will return a list of json dicts. each dict has fields:

    accessionId
    gene
    nucleotideChanges
    description
    classification
    reportedClassification
    url
    region
    proteinChange
    lastUpdated
    alias
    source
    acmgClassification
    submitter
    defaultNucleotideChange
    _id
    transcripts
    lastEvaluated

    example query on BRCA1:

    >>> c = Clinvitae()
    >>> res = c.query_gene('brca1')
    >>> entry1 = res[0]
    >>> print(entry1.keys())  # display fields for first entry
    >>> print(entry1['accessionId']) # accession id for first entry
    >>> print(entry1['lastEvaluated'])  # date first variant entry was last evaluated
    >>> print(entry1['source'])  # source of first variant entry

    """

    def __init__(self):
        url = "http://clinvitae.invitae.com/api/v1"
        super(Clinvitae, self).__init__("Clinvitae", url=url)

    def query_gene(self, gene):
        """takes gene name and returns json of variants in gene (not case sensitive)"""
        return self.http_get("variants?q=%s" % gene, frmt='json')

    def query_hgvs(self, hgvs):
        """takes an hgvs (variant) tag and returns ALL reported variants in the gene in which hgvs is located"""
        return self.http_get("variants?q=%s" % hgvs, frmt='json')

    def all_variants(self, gene):
        """returns a list of unique hgvs tags reported in gene"""
        results = self.query_gene(gene)
        variants = set()
        for result in results:  # each result is json dict of single entry
            print(result)
            variants.add(result['defaultNucleotideChange'])
        return list(variants)
