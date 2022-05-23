#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
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

from bioservices.services import REST
from bioservices import logger

logger.name = __name__

try:
    import pandas as pd
except:
    pass


__all__ = ["COG"]


class COG:
    """Interface to the COG service


    from bioservices import COG
    c = COG()
    cogs = c.get_all_cogs()   # This is a pandas dataframe

    """

    _url = "https://www.ncbi.nlm.nih.gov/research/cog/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**"""
        self.services = REST(name="cog", url=COG._url, verbose=verbose, cache=cache)

    def get_cogs(self, page=1):
        """Get COGs. Unfortunately, the API sends 10 COGS at a tine given a
        specific page.

        The dictionary returned contains the results, count, previous and next
        page.
        """
        res = self.services.http_get("cog", frmt="json", params={"page": page})
        return res

    def get_cogs_by_gene(self, gene):
        """Filter COGs by gene tag: MK0280"""
        res = self.services.http_get("cog", frmt="json", params={"gene": gene})
        return res

    def get_cogs_by_id(self, cog_id):
        """Filter COGs by COG ID tag: COG0003"""
        res = self.services.http_get("cog", frmt="json", params={"cog": cog_id})
        return res

    def get_cogs_by_assembly_id(self, assembly_id):
        """Filter COGs by assembly ID: GCA_000007185.1"""
        res = self.services.http_get("cog", frmt="json", params={"assembly": assembly_id})
        return res

    def get_cogs_by_orgnanism(self, name):
        """Filter COGs by organism name: Nitrosopumilus_maritimus_SCM1"""
        res = self.services.http_get("cog", frmt="json", params={"organism": name})
        return res

    def get_cogs_by_taxon_id(self, taxon_id):
        """Filter COGs by taxid: 1229908"""
        res = self.services.http_get("cog", frmt="json", params={"taxid": taxon_id})
        return res

    def get_cogs_by_category(self, category):
        """Filter COGs by Taxonomic Category: ACTINOBACTERIA"""
        res = self.services.http_get("cog", frmt="json", params={"category": category})
        return res

    def get_cogs_by_category_id(self, category):
        """Filter COGs by Taxonomic Category taxid: 651137"""
        res = self.services.http_get("cog", frmt="json", params={"cat_taxid": category})
        return res

    def get_cogs_by_category_(self, protein):
        """Filter COGs by Protein name: AJP49128.1"""
        res = self.services.http_get("cog", frmt="json", params={"protein": protein})
        return res

    # The search keywords (cog, assembly, organism, taxid, category, cat_taxid and protein)
    # can be combined to filter the COG lists.

    def get_cogs_by_id_and_category(self, cog_id, category):
        """Filter COGs by COG id and Taxonomy Categories: COG0004 and CYANOBACTERIA"""
        res = self.services.http_get("cog", frmt="json", params={"cog": cog_id, "category": category})
        return res

    def get_cogs_by_id_and_organism(self, cog_id, organism):
        """Filter COGs by COG id and organism: COG0004 and Escherichia_coli_K-12_sub_MG1655"""
        res = self.services.http_get("cog", frmt="json", params={"cog": cog_id, "organism,": organism})
        return res

    def get_all_cogs_definition(self):
        """Get all COG Definitions:"""
        res = self.services.http_get("cogdef", frmt="json")
        return res

    def get_cog_definition_by_cog_id(self, cog_id):
        """Get specific COG Definitions by COG: COG0003"""
        res = self.services.http_get("cogdef", frmt="json", params={"cog": cog_id})
        return res

    def get_cog_definition_by_name(self, cog):
        """Get specific COG Definitions by name: Thiamin-binding stress-response protein YqgV, UPF0045 family"""
        res = self.services.http_get("cogdef", frmt="json", params={"name": cog})
        return res

    def get_taxonomic_categories(self):
        """Get all Taxonomic Categories:"""
        res = self.services.http_get("taxonomy", frmt="json")
        return res

    def get_taxonomic_category_by_name(self, name):
        """Get specific Taxonomic Category by name: ALPHAPROTEOBACTERIA"""
        res = self.services.http_get("taxonomy", frmt="json", params={"name": name})
        return res
