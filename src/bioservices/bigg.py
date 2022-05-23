#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2020 - EBI-EMBL
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://bioservices.readthedocs.io
#
##############################################################################
"""
Interface to the BiGG Models API Service

.. topic:: What is BiGG Models?

    :URL: http://bigg.ucsd.edu
    :REST: http://bigg.ucsd.edu/api/v2

    .. highlights::

        "BiGG Models is a knowledgebase of genome-scale metabolic network reconstructions. BiGG Models integrates more than 70 published genome-scale metabolic networks into a single database with a set of standardized identifiers called BiGG IDs. Genes in the BiGG models are mapped to NCBI genome annotations, and metabolites are linked to many external databases (KEGG, PubChem, and many more)."

        -- BiGG Models Home Page, March 10, 2020.
"""

import os.path as osp

from bioservices.services import REST
from bioservices.util import sequencify, squash


__all__ = ["BiGG"]


_ACCEPTABLE_MODEL_RESOURCE_TYPES = ("metabolites", "reactions", "genes")
_ACCEPTABLE_SEARCH_TYPES = tuple(["models"] + list(_ACCEPTABLE_MODEL_RESOURCE_TYPES))
_ACCEPTABLE_MODEL_DOWNLOAD_FORMATS = ("xml", "json", "mat")


class BiGG:
    """
    Interface to the `BiGG Models <http://bigg.ucsd.edu/>` API Service.

    ::

        >>> from bioservices import BiGG
        >>> bigg = BiGG()
        >>> bigg.search("e coli", "models")
        [{'bigg_id': 'e_coli_core',
          'gene_count': 137,
          'reaction_count': 95,
          'organism': 'Escherichia coli str. K-12 substr. MG1655',
          'metabolite_count': 72},
          ...
        ]
    """

    _base_url = "http://bigg.ucsd.edu"
    _api_version = "v2"
    _url = "%s/api/%s" % (_base_url, _api_version)

    def __init__(self, verbose=False, cache=False):

        # http://bigg.ucsd.edu/data_access
        self.services = REST(
            name="BiGG",
            url=BiGG._url,
            cache=cache,
            requests_per_sec=10,
            verbose=verbose,
        )

    def __len__(self):
        return len(self.models)

    @property
    def version(self):
        return self.services.http_get("database_version")

    def _http_get_results(self, *args, **kwargs):
        response = self.services.http_get(*args, **kwargs)
        return response["results"]

    @property
    def models(self):
        return self._http_get_results("models")

    def _get_model_resource(self, type_, model_id, ids=None):
        if type_ not in _ACCEPTABLE_MODEL_RESOURCE_TYPES:
            raise TypeError(
                "Unknown model resource type %s. Acceptable types are %s" % (type_, _ACCEPTABLE_MODEL_RESOURCE_TYPES)
            )

        query = "models/%s/%s" % (model_id, type_)

        if ids is None:
            return self._http_get_results(query)

        ids = sequencify(ids)
        queries = [("%s/%s" % (query, id_)) for id_ in ids]

        response = self.services.http_get(queries)
        return squash(response)

    def metabolites(self, model_id=None, ids=None):
        if model_id is None:
            return self._http_get_results("universal/metabolites")

        return self._get_model_resource("metabolites", model_id=model_id, ids=ids)

    def reactions(self, model_id=None, ids=None):
        if model_id is None:
            return self._http_get_results("universal/reactions")

        return self._get_model_resource("reactions", model_id=model_id, ids=ids)

    def genes(self, model_id, ids=None):
        return self._get_model_resource("genes", model_id=model_id, ids=ids)

    def search(self, query, type_):
        if type_ not in _ACCEPTABLE_SEARCH_TYPES:
            raise TypeError("Unknown type %s. Acceptable types are %s" % (type_, _ACCEPTABLE_SEARCH_TYPES))

        params = {"query": query, "search_type": type_}
        return self._http_get_results("search", params=params)

    def download(self, model_id, format_="json", gzip=True, target=None):
        if format_ not in _ACCEPTABLE_MODEL_DOWNLOAD_FORMATS:
            raise TypeError("Unknown format %s. Accepted types are %s." % (format_, _ACCEPTABLE_MODEL_DOWNLOAD_FORMATS))

        path = "%s.%s" % (model_id, format_)

        if gzip:
            path += ".gz"

        if not target:
            target = path

        url = self.services._build_url("%s/static/models/%s" % (BiGG._base_url, path))

        response = self.services.session.get(url, stream=True)

        if response.ok:
            with open(target, "wb") as f:
                for content in response.iter_content():
                    f.write(content)
        else:
            response.raise_for_status()
