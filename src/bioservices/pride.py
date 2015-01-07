# -*- python -*-
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

"""Interface to PRIDE web service

.. topic:: What is PRIDE ?

    :URL: http://www.ebi.ac.uk/pride/archive/
    :URL: http://www.ebi.ac.uk/pride/ws/archive

    .. highlights::

         The PRIDE PRoteomics IDEntifications database is a centralized,
         standards compliant, public data repository for proteomics data,
         including protein and peptide identifications, post-translational
         modifications and supporting spectral evidence.

        -- From PRIDE web site, Jan 2015


"""
#from decorator import decorator
import wrapt

from bioservices.services import REST

__all__ = ["PRIDE"]


@wrapt.decorator
def params_to_update(wrapped, instance, args, kwargs):
    vars(wrapped)['actual_kwargs'] = kwargs
    return wrapped(*args, **kwargs)



class PRIDE(REST):
    """Interface to the `PRIDE <http://rest.ensembl.org>`_ service



    """
    _url = "http://www.ebi.ac.uk/pride/ws/archive"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(PRIDE, self).__init__(name="PRIDE", url=PRIDE._url,
                verbose=verbose, cache=cache)

    def get_project(self, identifier):
        """Retrieve project information by accession

        :param str identifier: a valid PRIDE identifier e.g., PRD000001
        :return: a dictionary with the project details. See
            http://www.ebi.ac.uk/pride/ws/archive/#!/project for details

        .. doctest::

            >>> from bioservices import PRIDE
            >>> p = PRIDE()
            >>> res = p.get_project("PRD000001")
            >>> res['numPeptides']
            6758

        """
        res = self.http_get('project/%s' % identifier)
        return res

    @params_to_update
    def get_project_list(self, query="", show=10, page=0, sort=None, order='desc',
                         speciesFilter=None, ptmsFilter=None, tissueFilter=None, diseaseFilter=None,
                         titleFilter=None, instrumentFilter=None, experimentTypeFilter=None,
                         quantificationfilter=None, projectTagFilter=None):
        """list projects or given criteria

        :param str query: search term to query for
        :param int show: how many results to return per page
        :param int page: which page (starting from 0) of the result to return
        :param str sort: the field to sort on
        :param str order: the sorting order (asc or desc)
        :param str speciesFilter: filter by species (NCBI taxon ID or name)
        :param str ptmsFilter: filter by PTM annotation	query
        :param str tissueFilter: filter by tissue annotation
        :param str diseaseFilter: filter by disease annotation
        :param str titleFilter:	filter the title for keywords
        :param str instrumentFilter: filter for instrument names or keywords
        :param str experimentTypeFilter: filter by experiment type
        :param str quantificationFilter: filter by quantification annotation
        :param str projectTagFilter: filter by project tags

        ::

            >>> p = PRIDE()
            >>> projects = p.get_project_list(show=100)

        """
        params = self.get_project_list.actual_kwargs

        res = self.http_get('project/list', params=params)
        try:
            res = res['list']
        except:
            pass
        return res

    @params_to_update
    def get_project_count(self, query="",
            speciesFilter=None, ptmsFilter=None, tissueFilter=None, diseaseFilter=None,
            titleFilter=None, instrumentFilter=None, experimentTypeFilter=None,
            quantificationfilter=None, projectTagFilter=None):

        """Count projects for given criteria

        Takes same query parameters as the /list operation; typically used to
        retrieve number of results before querying with /list

        :param str query: search term to query for
        :param str speciesFilter: filter by species (NCBI taxon ID or name)
        :param str ptmsFilter: filter by PTM annotation	query
        :param str tissueFilter: filter by tissue annotation
        :param str diseaseFilter: filter by disease annotation
        :param str titleFilter:	filter the title for keywords
        :param str instrumentFilter: filter for instrument names or keywords
        :param str experimentTypeFilter: filter by experiment type
        :param str quantificationFilter: filter by quantification annotation
        :param str projectTagFilter: filter by project tags
        :return: number of projects  (integer)
        

        """
        params = self.get_project_count.actual_kwargs
        res = self.http_get('project/count', params=params)
        return res

    def get_assays(self, identifier):
        """Retrieve assay information by assay accession

        :param int identifier: assay accession number

        ::

            >>> p = PRIDE()
            >>> res = p.get_assays(1643)
            >>> res['proteinCount']
            276

        """
        res = self.http_get('assay/%s' % identifier)
        return res

    def get_assay_list(self, identifier):
        """Return list of assays for a project accession nuber

        :param str identifier: project accession number. See :meth:`get_project_list`
        :return: list of dictionaries. Each dictionary represents an assay.

        ::

            >>> p = PRIDE()
            >>> assays = p.get_assay_list('PRD000001')
            >>> len(assays)  # could be found with get_assay_count_project_accession
            5
            >>> assays[1]['assayAccession']
            1643

        """
        res = self.http_get('assay/list/project/%s' % identifier)
        try:
            res = res['list']
        except:
            pass
        return res

    def get_assay_count(self, identifier):
        """Count assays for a project accession number

        :param str identifier: a project accession number
        :return: integer

        ::

            >>> p = PRIDE()
            >>> assays = p.get_assay_count('PRD000001')
            5


        """
        res = self.http_get('assay/count/project/%s' % identifier)
        return res

    def get_file_list(self, identifier):
        """return list of files for a project

        :param str identifier: a project accession number

        ::

            >>> files = p.get_file_count('PRD000001')
            >>> len(files)
            5

        """
        res = self.http_get('file/list/project/%s' % identifier)
        try:
            res = res['list']
        except:
            pass
        return res

    def get_file_count(self, identifier):
        """return count of files in a project

        :param str identifier: a project accession number
        :return: int

        ::

            >>> p.get_file_count('PRD000001')
            5

        """
        res = self.http_get('file/count/project/%s' % identifier)
        return res


    def get_file_list_assay(self, identifier):
        """list files for an assay

        :param int identifier: assay accession number
        :return: list of dictionary, Each dictionary represents a file data structure


        ::

            res = p.get_file_assay(1643)

        """
        res = self.http_get('file/list/assay/%s' % identifier)
        try:
            res = res['list']
        except:
            pass
        return res

    def get_file_count_assay(self, identifier):
        """list files for an assay

        :param int identifier: assay accession number
        :return: int

        ::

            p.get_file_assay(1643)
        """
        res = self.http_get('file/count/assay/%s' % identifier)
        return res

    @params_to_update
    def get_protein_list(self, identifier, show=10, page=0):
        """Retrieve protein identifications by project accession

        :param str identifier: a project accession number
        :param int show:		how many results to return per page
        :param int page:		which page (starting from 0) of the result to return

        """
        params = self.get_protein_list.actual_kwargs
        res = self.http_get('protein/list/project/%s' % identifier, params=params)
        try:
            res = res['list']
        except:
            pass
        return res

    def get_protein_count(self, identifier):
        """Count protein identifications by project accession

        :param str identifier: a project accession number
        :return: int

        """
        res = self.http_get('protein/count/project/%s' % identifier)
        return res

    @params_to_update
    def get_protein_list_assay(self, identifier, show=10, page=0):
        """Retrieve protein identifications by assay accession

        :param str identifier: a project accession number
        :param int show:		how many results to return per page
        :param int page:		which page (starting from 0) of the result to return

        """
        params = self.get_protein_list_assay.actual_kwargs
        res = self.http_get('protein/list/assay/%s' % identifier, params=params)
        try:
            res = res['list']
        except:
            pass
        return res

    def get_protein_count_assay(self, identifier):
        """Count protein identifications by assay accession

        :param str identifier: a project accession number
        :return: int

        """
        res = self.http_get('protein/count/assay/%s' % identifier)
        return res

    @params_to_update
    def get_peptide_list(self, identifier, sequence=None,
                         show=10, page=0):
        """Retrieve peptide identifications by project accession (and sequence)

        :param str identifier: a project accession number
        :param str sequence: the peptide sequence to limit the query on (optional).
            If provided, show and page are not used
        :param int show:		how many results to return per page
        :param int page:		which page (starting from 0) of the result to return

        ::


            >>> peptides = p.get_peptide_list('PRD000001',  sequence='PLIPIVVEQTGR')
            >>> len(peptides)
            4
            >>> peptides = p.get_peptide_list('PRD000001')
            >>> len(peptides)
            10
            >>> peptides = p.get_peptide_list('PRD000001', show=100)

        .. note:: the function merge two functions from the PRIDE API (get_peptide_list and
            get_peptide_list_sequence)
        """
        params = self.get_peptide_list.actual_kwargs
        if sequence is None:
            res = self.http_get('peptide/list/project/%s' % identifier, params=params)
        else:
            res = self.http_get('peptide/list/project/%s/sequence/%s' % (identifier, sequence))

        try:
            res = res['list']
        except:
            pass
        return res

    def get_peptide_count(self, identifier, sequence=None):
        """Count peptide identifications by project accession

        :param str identifier: a project accession number
        :return: int


            >>> p.get_peptide_count('PRD000001', sequence='PLIPIVVEQTGR')
            4
            >>> p.get_peptide_count('PRD000001')
            6758

        """
        if sequence is None:
            res = self.http_get('peptide/count/project/%s' % identifier)
        else:
            res = self.http_get('peptide/count/project/%s/sequence/%s' % (identifier, sequence))
        return res

    @params_to_update
    def get_peptide_list_assay(self, identifier, sequence=None,
                         show=10, page=0):
        """Retrieve peptide identifications by assay accession (and sequence)

        :param str identifier: an assay accession number
        :param str sequence: the peptide sequence to limit the query on (optional).
            If provided, show and page are not used
        :param int show:		how many results to return per page
        :param int page:		which page (starting from 0) of the result to return

        ::

            >>> peptides = p.get_peptide_list_assay(1643,  sequence='AAATQKKVER')
            >>> len(peptides)
            5
            >>> peptides = p.get_peptide_list_assay(1643)
            >>> len(peptides)
            10
            >>> peptides = p.get_peptide_list_assay(1643, show=100)

        .. note:: the function merge two functions from the PRIDE API (get_peptide_list and
            get_peptide_list_sequence)
        """
        params = self.get_peptide_list_assay.actual_kwargs
        if sequence is None:
            res = self.http_get('peptide/list/assay/%s' % identifier, params=params)
        else:
            res = self.http_get('peptide/list/assay/%s/sequence/%s' % (identifier, sequence))
        try:
            res = res['list']
        except:
            pass
        return res

    def get_peptide_count_assay(self, identifier, sequence=None):
        """Count peptide identifications by assay accession

        :param str identifier: an assay accession number
        :return: int

        ::

            >>> p.get_peptide_count_assay(1643, sequence='AAATQKKVER')
            5
            >>> p.get_peptide_count_assay(1643)
            1696

        """
        if sequence is None:
            res = self.http_get('peptide/count/assay/%s' % identifier)
        else:
            res = self.http_get('peptide/count/assay/%s/sequence/%s' % (identifier, sequence))
        return res





