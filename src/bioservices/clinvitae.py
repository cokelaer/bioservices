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

    Requests will return a list of json dicts. each dict has the following fields::

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

    example query on BRCA1::

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
        """
        takes gene name and returns json of variants in gene (not case sensitive)

        ::

            >>> c = Clinvitae()
            >>> res = c.query_gene('brca1')
            >>> entry1 = res[0]
            >>> print entry1['accessionId']  # accession id for first entry
            u'SCV000039520'
            >>> print entry1['lastEvaluated']  # date first variant entry was last evaluated
            u'2013-04-03'
            >>> print entry1['source']  # source of first variant entry
            u'ClinVar'

        """
        return self.http_get("variants?q=%s" % gene, frmt='json')

    def query_hgvs(self, hgvs):
        """Takes an hgvs (variant) tag and returns ALL reported variants in the gene in which hgvs is located

        ::

            >>> c = Clinvitae()
            >>> res = c.query_gene('NM_198578.3:c.1847A>G')  # returns all entries in LRRK2 gene
            >>> entry1 = res[0]
            >>> print entry1['accessionId']  # accession id for first entry
            u'SCV000056058'
            >>> print entry1['lastEvaluated']  # date first variant entry was last evaluated
            u'2012-09-13'
            >>> print entry1['source']  # source of first variant entry
            u'ClinVar'

        """
        return self.http_get("variants?q=%s" % hgvs, frmt='json')

    def all_variants(self, gene):
        """
        returns a list of unique hgvs tags reported in gene

        ::
        
            >>> c = Clinvitae()
            >>> res = c.all_variants('MUTYH')  # returns all reported variants in MUTYH gene
            >>> print res[0:5]
            [u'NM_001048171.1:c.-2188C>T',
            u'NM_001048171.1:c.462+35A>G',
            u'NM_001048171.1:c.1099G>T',
            u'NM_001048171.1:c.972G>C',
            u'NM_001048171.1:c.1476+35C>T']

        """
        results = self.query_gene(gene)
        variants = set()
        for result in results:  # each result is json dict of single entry
            variants.add(result['defaultNucleotideChange'])
        return list(variants)

    def get_pathogenic(self, gene):
        """
        returns all fields for entries reported as Pathogenic by any source in Clinvitae

        ::
    
            >>> c = Clinvitae()
            >>> pathogenic = c.get_pathogenic('brca1')  # returns pathogenic or likely pathogenic
            >>> len(pathogenic)  # number of pathogenic variants
            1100

        """
        results = self.query_gene(gene)
        variants = set()
        for result in results:
            if result['reportedClassification'].lower() in ['pathogenic', 'likely pathogenic']:
                variants.add(result['defaultNucleotideChange'])
        return list(variants)

    def get_benign(self, gene):
        """
        returns all fields for entries reported as Benign by any source in Clinvitae

        ::

            >>> c = Clinvitae()
            >>> benign = c.get_benign('brca1')  # returns benign or likely benign
            >>> len(benign)  # number of benign variants
            187

        """
        results = self.query_gene(gene)
        variants = set()
        for result in results:
            if result['reportedClassification'].lower() in ['benign', 'likely benign']:
                variants.add(result['defaultNucleotideChange'])
        return list(variants)

    def get_VUS(self, gene):
        """
        returns all fields for entries not classified as benign or pathogenic -> variant of unknown significance (VUS)

        ::

            >>> c = Clinvitae()
            >>> vus = c.get_VUS('brca1')
            >>> len(vus)  # number of benign variants
            2389
        """
        results = self.query_gene(gene)
        variants = set()
        for result in results:
            if result['reportedClassification'].lower() not in ['pathogenic', 'likely pathogenic', 'benign', 'likely benign']:
                variants.add(result['defaultNucleotideChange'])
        return list(variants)
