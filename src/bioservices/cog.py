#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2023 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
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
"""Interface to some part of the UniProt web service

.. topic:: What is COG service?

    :URL: https://www.ncbi.nlm.nih.gov/research/cog/webservices/
    :Citation:

    .. highlights::

        Database of Clusters of Orthologous Genes (COGs)

        -- From COG web site, Jan 2021


"""
import types
import io
import sys

from tqdm import tqdm

import pandas as pd

from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["COG"]


class COG:
    """Interface to the COG service

    Note that in addition to the original COG service from NCBI, this interface also
    helps you in searching for orgamism, and retrieve all pages in a single command
    (rather than scanning yourself all pages).

    Here is an example of getting the COG for ecoli. Your first the exact matching name.
    Bioservices provices a function to serch for the exact organism name that will be understood
    by the COG service (here Escherichia_coli_K-12_sub_MG1655 ... you cannot guess it really)
    ::

        from bioservices import COG
        c = COG()
        c.search_organism('coli')

        # the output of the previous command gives you the name
        c.get_cogs_by_orgnanism('Escherichia_coli_K-12_sub_MG1655')
    """

    _url = "https://www.ncbi.nlm.nih.gov/research/cog/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**"""
        self.services = REST(name="cog", url=COG._url, verbose=verbose, cache=cache)
        self.show_progress = True

    def _get_all(self, service_name="cog", params={}):
        page = 1
        params["page"] = page
        res = self.services.http_get(service_name, frmt="json", params=params)
        total = res["count"]

        pbar = tqdm(total=total, disable=not self.show_progress, leave=False)

        # sometimes, a 404 is returned, let us try several times.
        trials = 3

        while True:
            params["page"] += 1
            for _ in range(trials):
                other = self.services.http_get(service_name, frmt="json", params=params)
                try:
                    res["results"].extend(other["results"])
                    break
                except TypeError:
                    pass
                except Exception as err:
                    raise (err)
            pbar.update(len(other["results"]))
            if other["next"] is None:
                break
        pbar.close()

        return res

    def get_cogs(self, **kwargs):
        """Get COGs. Unfortunately, the API sends 10 COGS at a time given a
        specific page.

        The dictionary returned contains the results, count, previous and next
        page.
        """
        if kwargs.get("page") is None:
            res = self._get_all("cog", params=kwargs)
        else:
            res = self.services.http_get("cog", frmt="json", params=kwargs)
        return res

    def get_cogs_by_gene(self, gene, page=None):
        """Filter COGs by gene tag: MK0280"""
        return self.get_cogs(**{"gene": gene, "page": page})

    def get_cogs_by_id(self, cog_id, page=None):
        """Filter COGs by COG ID tag: COG0003"""
        return self.get_cogs(**{"cog": cog_id, "page": page})

    def get_cogs_by_assembly_id(self, assembly_id, page=None):
        """Filter COGs by assembly ID: GCA_000007185.1"""
        return self.get_cogs(**{"assembly": assembly_id, "page": page})

    def get_cogs_by_organism(self, name, page=None):
        """Filter COGs by organism name: Nitrosopumilus_maritimus_SCM1"""
        return self.get_cogs(**{"organism": name, "page": page})

    def get_cogs_by_taxon_id(self, taxon_id, page=None):
        """Filter COGs by taxid: 1229908"""
        return self.get_cogs(**{"taxid": taxon_id, "page": page})

    def get_cogs_by_category(self, category, page=None):
        """Filter COGs by Taxonomic Category: ACTINOBACTERIA"""
        return self.get_cogs(**{"category": category, "page": page})

    def get_cogs_by_category_id(self, category, page=None):
        """Filter COGs by Taxonomic Category taxid: 651137"""
        return self.get_cogs(**{"cat_taxid": category, "page": page})

    def get_cogs_by_protein_name(self, protein, page=None):
        """Filter COGs by Protein name: AJP49128.1"""
        return self.get_cogs(**{"protein": protein, "page": page})

    def get_cogs_by_id_and_category(self, cog_id, category, page=None):
        """Filter COGs by COG id and Taxonomy Categories: COG0004 and CYANOBACTERIA"""
        return self.get_cogs(**{"cog": cog_id, "category": category, "page": page})

    def get_cogs_by_id_and_organism(self, cog_id, organism, page=None):
        """Filter COGs by COG id and organism: COG0004 and Escherichia_coli_K-12_sub_MG1655"""
        return self.get_cogs(**{"cog": cog_id, "organism,": organism, "page": page})

    def get_all_cogs_definition(self, page=None):
        """Get all COG Definitions:"""
        if page is None:
            res = self._get_all("cogdef")
        else:
            res = self.services.http_get("cogdef", frmt="json", params={"page": page})
        return res

    def get_cog_definition_by_cog_id(self, cog_id):
        """Get specific COG Definitions by COG: COG0003"""
        return self.services.http_get("cogdef", frmt="json", params={"cog": cog_id})

    def get_cog_definition_by_name(self, cog, page=None):
        """Get specific COG Definitions by name: Thiamin-binding stress-response protein YqgV, UPF0045 family"""

        if page is None:
            res = self._get_all("cogdef", params={"name": cog})
        else:
            res = self.services.http_get("cogdef", frmt="json", params={"name": cog})
        return res

    def get_taxonomic_categories(self, page=None):
        """Get all Taxonomic Categories.

        if page is set, only that page is returned. There are 10 entires per page.
        if page is unset (default), all results are returned.


        ::

            from bioservices import COG
            c = COG()
            names = [x['name'] for x in c.get_taxonomic_categories()['results']]

        """
        if page is None:
            res = self._get_all("taxonomy", params={})
        else:
            res = self.services.http_get("taxonomy", frmt="json", params={"page": page})

        return res

    def get_taxonomic_category_by_name(self, name, page=None):
        """Get specific Taxonomic Category by name


        c.get_taxonomic_category_by_name("ALPHAPROTEOBACTERIA")
        """
        if page is None:
            res = self._get_all("taxonomy", params={"name": name})
        else:
            res = self.services.http_get("taxonomy", frmt="json", params={"name": name, "page": page})
        return res

    def search_organism(self, name):
        """Return candidates that match the input name.

        :param str name:
        :return: list of items. Each item is a dictionary with genome name, assembly identifier and taxon identifier.

        """
        results = self.get_taxonomic_categories()
        candidates = []
        for x in results["results"]:
            for y in x["organisms"]:
                if name in y["genome_name"].lower():
                    candidates.append(y)
        return candidates
