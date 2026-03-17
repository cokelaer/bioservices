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
"""Interface to BioContainers.

.. topic:: What is BioContainers?

    :URL: https://biocontainers.pro/
    :REST: https://api.biocontainers.pro/ga4gh/trs/v2

    .. highlights::

        BioContainers is an open-source project that aims to create,
        store, and distribute bioinformatics software containers and
        packages.

        -- From BioContainers (about), Jan 2021

"""
import pandas as pd

from bioservices import logger
from bioservices.services import REST

logger.name = __name__


__all__ = ["Biocontainers"]


class Biocontainers:
    """Interface to the `BioContainers <https://biocontainers.pro>`_ service.

    BioContainers exposes a GA4GH Tool Registry Service (TRS) v2 API for
    discovering bioinformatics containers (Docker, Singularity, Conda).

    Example::

        >>> from bioservices import Biocontainers
        >>> b = Biocontainers()
        >>> b.get_tools(limit=5)
        >>> b.get_tool("samtools")
        >>> b.get_tool_classes()

    """

    _url = "https://api.biocontainers.pro/ga4gh/trs/v2"

    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: set to False to suppress informative messages
        :param bool cache: use HTTP cache
        """
        self.services = REST(
            name="biocontainers",
            url=Biocontainers._url,
            verbose=verbose,
            cache=cache,
            url_defined_later=True,
        )

    def get_tools(self, limit=1000, search=None, toolname=None, sort_field="id", sort_order="asc"):
        """Return a list of available tools.

        :param int limit: maximum number of tools to return (default: 1000).
        :param str search: free-text search filter applied across tool
            names, descriptions and tags (e.g., ``"alignment"``).
        :param str toolname: filter by exact tool name (e.g., ``"samtools"``).
        :param str sort_field: field to sort results by (default: ``"id"``).
        :param str sort_order: sort direction — ``"asc"`` or ``"desc"``
            (default: ``"asc"``).
        :return: :class:`pandas.DataFrame` with one tool per row, or the raw
            list if the response cannot be converted.

        Example::

            >>> from bioservices import Biocontainers
            >>> b = Biocontainers()
            >>> df = b.get_tools(limit=10)
            >>> df.columns.tolist()  # doctest: +SKIP
            ['id', 'name', 'organization', 'toolclass', 'versions', ...]
            >>> b.get_tools(limit=5, search="alignment")  # doctest: +SKIP

        """
        params = {"limit": limit, "sort_field": sort_field, "sort_order": sort_order}
        if search is not None:
            params["search"] = search
        if toolname is not None:
            params["toolname"] = toolname

        res = self.services.http_get("tools", params=params)
        try:
            return pd.DataFrame(res)
        except Exception:
            return res

    def get_tool(self, tool_id):
        """Return metadata for a single tool.

        :param str tool_id: the BiGG/BioContainers tool identifier
            (e.g., ``"samtools"``).
        :return: dict with keys ``id``, ``name``, ``description``,
            ``organization``, ``toolclass``, ``versions``, ``pulls``, etc.

        Example::

            >>> from bioservices import Biocontainers
            >>> b = Biocontainers()
            >>> tool = b.get_tool("samtools")
            >>> tool["name"]
            'samtools'
            >>> tool["pulls"]  # doctest: +SKIP
            381303353

        """
        return self.services.http_get("tools/%s" % tool_id)

    def get_tool_versions(self, tool_id):
        """Return all versions of a given tool.

        :param str tool_id: the tool identifier (e.g., ``"samtools"``).
        :return: :class:`pandas.DataFrame` with one version per row, or the
            raw list if the response cannot be converted.

        Each row contains image information (Docker, Singularity, Conda) and
        metadata such as ``id``, ``name``, ``meta_version``.

        Example::

            >>> from bioservices import Biocontainers
            >>> b = Biocontainers()
            >>> df = b.get_tool_versions("samtools")
            >>> df["id"].tolist()[:3]  # doctest: +SKIP
            ['samtools-0.1.19', 'samtools-0.1.20', 'samtools-0.1.21']

        """
        res = self.services.http_get("tools/%s/versions" % tool_id, params={})
        try:
            return pd.DataFrame(res)
        except Exception:
            return res

    def get_tool_version(self, tool_id, version_id):
        """Return metadata for a specific version of a tool.

        :param str tool_id: the tool identifier (e.g., ``"samtools"``).
        :param str version_id: the version identifier, typically in the form
            ``"<tool>-<version>"`` (e.g., ``"samtools-1.17"``).
        :return: dict with keys ``id``, ``name``, ``meta_version``,
            ``images`` (list of container image records).

        Each image entry includes ``image_name``, ``image_type`` (Docker,
        Singularity, or Conda), ``registry_host``, ``size``, and ``updated``.

        Example::

            >>> from bioservices import Biocontainers
            >>> b = Biocontainers()
            >>> v = b.get_tool_version("samtools", "samtools-1.17")
            >>> v["meta_version"]
            '1.17'
            >>> [img["image_type"] for img in v["images"]]  # doctest: +SKIP
            ['Conda', 'Docker', 'Singularity', ...]

        """
        return self.services.http_get("tools/%s/versions/%s" % (tool_id, version_id))

    def get_tool_classes(self):
        """Return all tool classes defined in BioContainers.

        :return: list of dicts, each with keys ``id``, ``name``,
            ``description``. Current classes are ``CommandLineTool``,
            ``Workflow``, ``CommandLineMultiTool``, and ``Service``.

        Example::

            >>> from bioservices import Biocontainers
            >>> b = Biocontainers()
            >>> classes = b.get_tool_classes()
            >>> [c["name"] for c in classes]
            ['CommandLineTool', 'Workflow', 'CommandLineMultiTool', 'Service']

        """
        return self.services.http_get("toolClasses")

    # ------------------------------------------------------------------
    # Backward-compatible alias
    # ------------------------------------------------------------------

    def get_versions_one_tool(self, tool_id):
        """Return all versions of a given tool.

        This is an alias for :meth:`get_tool_versions`.

        :param str tool_id: the tool identifier (e.g., ``"samtools"``).
        :return: :class:`pandas.DataFrame` or raw list.

        Example::

            >>> from bioservices import Biocontainers
            >>> b = Biocontainers()
            >>> b.get_versions_one_tool("samtools")  # doctest: +SKIP

        """
        return self.get_tool_versions(tool_id)
