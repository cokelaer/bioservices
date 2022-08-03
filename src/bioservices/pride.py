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

    :URL: http://www.ebi.ac.uk/pride/ws/archive/v2

    .. highlights::

         The PRIDE PRoteomics IDEntifications database is a centralized,
         standards compliant, public data repository for proteomics data,
         including protein and peptide identifications, post-translational
         modifications and supporting spectral evidence.

        -- From PRIDE web site, Jan 2015


"""
import tqdm

from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["PRIDE"]


class PRIDE:
    """Interface to the `PRIDE <http://rest.ensembl.org>`_ service



    ::

        from bioservices import PRIDE
        p = PRIDE()
        p.get_peptide_evidence(projectAccession)

    .. versionchanged:: 1.10.1

        Due to new API:

        - the method project_count was dropped.
        - get_project_list was renamed in get_project_files
        - get_assays, get_assay_count, get_assay_count_project_accession, get_assay_list were dropped in v2
        - get_protein_list, get_protein_count, get_protein_count_assay, get_protein_list, get_protein_list_assay
          replaced by get_protein_evidences method
        - get_peptide_list_assay, get_peptide_count, get_peptide_list, get_peptide_list_sequence,
          get_peptide_count_assay replaced by get_peptide_evidence.

    """

    _url = "https://www.ebi.ac.uk/pride/ws/archive/v2"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        :param cache: set to True to use caching. Not recommended for
            this service that evolves a lot
        """
        self.services = REST(name="PRIDE", url=PRIDE._url, verbose=verbose, cache=cache)

    def get_project(self, identifier):
        """Retrieve project information by accession

        List of PRIDE Archive Projects. The following method do not allows
        to perform search, for search functionality you will need to use
        the search/projects. The result list is Paginated using the pageSize and page.

        :param str identifier: a valid PRIDE identifier e.g., PRD000001

        :return: if identifier is invalid, returns an emppty dictionary {}

        .. doctest::

            >>> from bioservices import PRIDE
            >>> p = PRIDE()
            >>> res = p.get_project("PRD000001")
            >>> res['title']
            'COFRADIC proteome of unstimulated human blood platelets'

        """
        res = self.services.http_get(f"projects/{identifier}")
        if res == 400:
            logger.warning(
                f"Nothing found for {identifier}. may be this is not a valid identifier. Use get_projects"
            )
            return {}
        return res

    def get_projects(self, pageSize=100, max_pages=1e9):
        """Get list of all projects"""
        N = self.get_projects_count()
        Npages = int(N / pageSize)
        Npages = min(Npages, max_pages)

        results = []
        page_count = 0
        for page in tqdm.tqdm(range(Npages)):
            res = self.services.http_get("projects", params={"pageSize": pageSize, "page": page})
            results.extend(res["_embedded"]["projects"])
            page_count += 1
            if page_count > max_pages:
                break

        return results

    def get_projects_count(self):
        res = self.services.http_get("projects")
        return res["page"]["totalElements"]

    def get_project_files(self, accession, pageSize=100, page=0, sortConditions=None, sortDirection="DESC", filters=""):
        """list projects or given criteria

        :param str accession: the accession number to look for
        :param int pageSize: how many results to return per page
        :param int page: which page (starting from 0) of the result to return
        :param str sortConditions: default is submission_date but more fields
            can be separated by comma and passed. Example: submission_date,project_title
        :param str sortDirection: the sorting order (ASC or DESC)
        :param str filters: Parameters to filter the search results. The structure of
            the filter is: field1==value1, field2==value2. Example accession==PRD000001

        ::

            >>> p = PRIDE()
            >>> results = p.get_project_files(accession="PRD000001", pageSize=10, page=1)


        In v1.10.1 due to new PRIDE API, the method **get_file_count** was dropped. You can use::

            len(results['_embedded']['files'])

        Similarly the **get_file_list** method was dropped since all results are
        stored in the output of this method


        """
        params = {
            "pageSize": pageSize,
            "page": page,
            "sortDirection": sortDirection,
            "sortConditions": sortConditions,
            "filter": filters,
        }

        res = self.services.http_get(f"projects/{accession}/files", params=params)
        try:
            res = res["list"]
        except:
            pass
        return res

    def get_protein_evidences(
        self,
        project_accession=None,
        assay_accession=None,
        reported_accession=None,
        pageSize=100,
        page=0,
        sortDirection="DESC",
        sortConditions="projectAccession",
    ):

        """Get all proteins evidence

        :param project_accession:
        :param assay_accession:
        :param reported_accession:
        :param int pageSize: how many results to return per page
        :param int page: which page (starting from 0) of the result to return
        :param str sortConditions: default is submission_date but more fields
            can be separated by comma and passed. Example: submission_date,project_title
        :param str sortDirection: the sorting order (ASC or DESC)

        ::

            p.get_protein_evidences()['_embedded']['proteinevidences']
        """

        params = {}
        if project_accession:
            params["projectAccession"] = project_accession
        if assay_accession:  # pragma: no cover
            params["assayAccession"] = assay_accession
        if reported_accession:  # pragma: no cover
            params["reportedAccession"] = reported_accession
        params["pageSize"] = pageSize
        params["page"] = page
        params["sortConditions"] = sortConditions
        params["sortDirection"] = sortDirection

        res = self.services.http_get(f"proteinevidences", params=params)
        return res

    def get_peptide_evidence(
        self,
        project_accession=None,
        assay_accession=None,
        protein_accession=None,
        peptide_evidence_accession=None,
        peptide_sequence=None,
        pageSize=100,
        page=0,
        sortDirection="DESC",
        sortConditions="projectAccession",
    ):
        """Get all the peptide evidences for an specific protein evidence


        :param project_accession:
        :param assay_accession:
        :param protein_accession:
        :param peptide_evidence_accession:
        :param peptide_sequence:
        :param int pageSize: how many results to return per page
        :param int page: which page (starting from 0) of the result to return
        :param str sortConditions: default is submission_date but more fields
            can be separated by comma and passed. Example: submission_date,project_title
        :param str sortDirection: the sorting order (ASC or DESC)

        Retrieving data from project accession should be fast::

            p.get_peptide_evidence(protein_accession="Q8IX30")

        but other methods may be slow::

            p.get_peptide_evidence(peptide_sequence="CQGSPGASKAMLSCNR")
        """
        params = {}
        if project_accession:
            params["projectAccession"] = project_accession
        if assay_accession:  # pragma: no cover
            params["assayAccession"] = assay_accession
        if protein_accession:  # pragma: no cover
            params["proteinAccession"] = protein_accession
        if peptide_evidence_accession:  # pragma: no cover
            params["peptideEvidenceAccession"] = peptide_evidence_accession
        if peptide_sequence:  # pragma: no cover
            params["peptideSequence"] = peptide_sequence
        params["pageSize"] = pageSize
        params["page"] = page
        params["sortConditions"] = sortConditions

        res = self.services.http_get(f"peptideevidences", params=params)
        return res

    def get_stats(self, name=None):
        """Retrieve statistics by Name

        If you do not have the name, just type::

            p.get_stats()

        and then, e.g., ::

            p.get_stats("SUBMISSIONS_PER_YEAR")

        """

        if name is None:
            res = self.services.http_get("stats/")
        else:
            res = self.services.http_get(f"stats/{name}")
        return res
