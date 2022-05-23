#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#  Copyright (c) 2021 - Institut Pasteur
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to biocontainer

.. topic:: What is biocontainers

    :URL: https://biocontainers.pro/
    :Citation:

    .. highlights::

        BioContainers is an open-source project that aims to create,
        store, and distribute bioinformatics software containers and
        packages.

        -- From biocontainers (about), Jan 2021

"""
import pandas as pd

from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["Biocontainers"]


class Biocontainers:
    """Interface to Biocontainers service

    ::

        >>> from bioservics import Biocontainers
        >>> b = Biocontainers()
        >>> b.get_tools()

    """

    _url = "https://api.biocontainers.pro/ga4gh/trs/v2/"

    def __init__(self, verbose=True, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        self.services = REST(
            name="biocontainers",
            url=Biocontainers._url,
            verbose=verbose,
            cache=cache,
            url_defined_later=True,
        )

    def get_tools(self, limit=20000):
        """Returns all available tools."""
        params = {"limit": limit, "sort_ield": "id", "sort_order": "asc"}
        res = self.services.http_get("tools", params=params)
        try:
            return pd.DataFrame(res)
        except Exception:
            return res

    def get_stats(self):
        """Returns some stats about numer of versions and tools"""
        res = self.services.http_get("stats")
        return res

    def get_versions_one_tool(self, tool):
        """Returns all versions of a given tool."""
        res = self.services.http_get(f"tools/{tool}/versions", params={})
        try:
            return pd.DataFrame(res)
        except Exception:
            return res
