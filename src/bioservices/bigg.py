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
"""Interface to the BiGG Models API Service.

.. topic:: What is BiGG Models?

    :URL: http://bigg.ucsd.edu
    :REST: http://bigg.ucsd.edu/api/v2

    .. highlights::

        "BiGG Models is a knowledgebase of genome-scale metabolic network
        reconstructions. BiGG Models integrates more than 70 published
        genome-scale metabolic networks into a single database with a set of
        standardized identifiers called BiGG IDs. Genes in the BiGG models are
        mapped to NCBI genome annotations, and metabolites are linked to many
        external databases (KEGG, PubChem, and many more)."

        -- BiGG Models Home Page, March 10, 2020.
"""

from bioservices.services import REST
from bioservices.util import sequencify, squash

__all__ = ["BiGG"]


_ACCEPTABLE_MODEL_RESOURCE_TYPES = ("metabolites", "reactions", "genes")
_ACCEPTABLE_SEARCH_TYPES = ("models",) + _ACCEPTABLE_MODEL_RESOURCE_TYPES
_ACCEPTABLE_MODEL_DOWNLOAD_FORMATS = ("xml", "json", "mat")


class BiGG:
    """Interface to the `BiGG Models <http://bigg.ucsd.edu>`_ API.

    BiGG Models is a knowledgebase of genome-scale metabolic network
    reconstructions with standardised BiGG identifiers.

    Example::

        >>> from bioservices import BiGG
        >>> bigg = BiGG()
        >>> bigg.search("e coli", "models")
        [{'bigg_id': 'e_coli_core', 'gene_count': 137, ...}, ...]

    """

    _base_url = "http://bigg.ucsd.edu"
    _api_version = "v2"
    _url = "%s/api/%s" % (_base_url, _api_version)

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages
        :param bool cache: use HTTP cache
        """
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
        """Return the current BiGG database and API version.

        :return: dict with keys ``bigg_models_version``, ``api_version``,
            ``last_updated``.

        Example::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> bigg.version["bigg_models_version"]
            '1.6.0'

        """
        return self.services.http_get("database_version")

    @property
    def models(self):
        """Return the list of all models in BiGG.

        :return: list of dicts, each with keys ``bigg_id``, ``organism``,
            ``metabolite_count``, ``reaction_count``, ``gene_count``.

        Example::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> models = bigg.models
            >>> models[0]["bigg_id"]
            'e_coli_core'

        """
        return self._http_get_results("models")

    def get_model(self, model_id):
        """Retrieve metadata for a specific model.

        :param str model_id: BiGG model identifier (e.g., ``"e_coli_core"``).
        :return: dict with keys ``model_bigg_id``, ``organism``,
            ``metabolite_count``, ``reaction_count``, ``gene_count``,
            ``reference_id``, ``reference_type``, ``escher_maps``,
            ``last_updated``, and download-size fields.

        Example::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> m = bigg.get_model("e_coli_core")
            >>> m["organism"]
            'Escherichia coli str. K-12 substr. MG1655'
            >>> m["reaction_count"]
            95

        """
        return self.services.http_get("models/%s" % model_id)

    def metabolites(self, model_id=None, ids=None):
        """Retrieve metabolites from a model or the universal database.

        :param str model_id: BiGG model identifier (e.g., ``"e_coli_core"``).
            If ``None``, queries the universal metabolite database.
        :param ids: a single metabolite BiGG ID string or a list of IDs.
            If ``None``, returns the full list for the model (or universal DB).
        :return: a list of metabolite dicts when *ids* is ``None`` or a list;
            a single dict when *ids* is a single string.

        **Model metabolites** (list and detail)::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> bigg.metabolites("e_coli_core")          # list all  # doctest: +SKIP
            >>> bigg.metabolites("e_coli_core", "atp_c") # single detail  # doctest: +SKIP
            >>> bigg.metabolites("e_coli_core", ids=["atp_c", "adp_c"])  # doctest: +SKIP

        **Universal metabolites**::

            >>> bigg.metabolites()               # list all universal  # doctest: +SKIP
            >>> bigg.metabolites(ids="atp")      # single universal detail  # doctest: +SKIP

        """
        if model_id is None:
            if ids is None:
                return self._http_get_results("universal/metabolites")
            ids = sequencify(ids)
            queries = ["universal/metabolites/%s" % id_ for id_ in ids]
            return squash(self.services.http_get(queries))

        return self._get_model_resource("metabolites", model_id=model_id, ids=ids)

    def reactions(self, model_id=None, ids=None):
        """Retrieve reactions from a model or the universal database.

        :param str model_id: BiGG model identifier (e.g., ``"e_coli_core"``).
            If ``None``, queries the universal reaction database.
        :param ids: a single reaction BiGG ID string or a list of IDs.
            If ``None``, returns the full list for the model (or universal DB).
        :return: a list of reaction dicts when *ids* is ``None`` or a list;
            a single dict when *ids* is a single string.

        **Model reactions** (list and detail)::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> bigg.reactions("e_coli_core")         # list all  # doctest: +SKIP
            >>> bigg.reactions("e_coli_core", "PFK")  # single detail  # doctest: +SKIP

        **Universal reactions**::

            >>> bigg.reactions()            # list all universal  # doctest: +SKIP
            >>> bigg.reactions(ids="PFK")   # single universal detail  # doctest: +SKIP

        """
        if model_id is None:
            if ids is None:
                return self._http_get_results("universal/reactions")
            ids = sequencify(ids)
            queries = ["universal/reactions/%s" % id_ for id_ in ids]
            return squash(self.services.http_get(queries))

        return self._get_model_resource("reactions", model_id=model_id, ids=ids)

    def genes(self, model_id, ids=None):
        """Retrieve genes from a model.

        :param str model_id: BiGG model identifier (e.g., ``"e_coli_core"``).
        :param ids: a single gene BiGG ID string or a list of IDs.
            If ``None``, returns all genes for the model.
        :return: a list of gene dicts when *ids* is ``None`` or a list;
            a single dict when *ids* is a single string.

        Example::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> bigg.genes("e_coli_core")           # list all  # doctest: +SKIP
            >>> bigg.genes("e_coli_core", "b0351")  # single detail  # doctest: +SKIP

        """
        return self._get_model_resource("genes", model_id=model_id, ids=ids)

    def search(self, query, type_):
        """Search BiGG Models by keyword.

        :param str query: search term (e.g., ``"e coli"``, ``"atp"``,
            ``"phosphate"``).
        :param str type_: resource type to search. One of: ``"models"``,
            ``"metabolites"``, ``"reactions"``, ``"genes"``.
        :return: list of matching result dicts.
        :raises TypeError: if *type_* is not one of the accepted values.

        Example::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> models = bigg.search("e coli", "models")
            >>> models[0]["bigg_id"]  # doctest: +SKIP
            'e_coli_core'
            >>> bigg.search("atp", "metabolites")   # doctest: +SKIP
            >>> bigg.search("gap", "genes")         # doctest: +SKIP
            >>> bigg.search("phosphate", "reactions")  # doctest: +SKIP

        """
        if type_ not in _ACCEPTABLE_SEARCH_TYPES:
            raise TypeError("Unknown type %s. Acceptable types are %s" % (type_, _ACCEPTABLE_SEARCH_TYPES))
        params = {"query": query, "search_type": type_}
        return self._http_get_results("search", params=params)

    def download(self, model_id, format_="json", gzip=True, target=None):
        """Download a model file and save it locally.

        :param str model_id: BiGG model identifier (e.g., ``"e_coli_core"``).
        :param str format_: file format — one of ``"xml"``, ``"json"``,
            ``"mat"`` (default: ``"json"``).
        :param bool gzip: download the gzip-compressed version (default:
            ``True``).
        :param str target: local file path to write to. Defaults to
            ``"<model_id>.<format_>[.gz]"`` in the current directory.
        :raises TypeError: if *format_* is not one of the accepted values.

        Example::

            >>> from bioservices import BiGG
            >>> bigg = BiGG()
            >>> bigg.download("e_coli_core", format_="json", target="/tmp/e_coli_core.json.gz")  # doctest: +SKIP

        """
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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _http_get_results(self, *args, **kwargs):
        """Call http_get and return the ``results`` key from the response."""
        response = self.services.http_get(*args, **kwargs)
        return response["results"]

    def _get_model_resource(self, type_, model_id, ids=None):
        """Fetch a model resource (metabolites, reactions, or genes).

        :param str type_: resource type — one of ``_ACCEPTABLE_MODEL_RESOURCE_TYPES``.
        :param str model_id: BiGG model identifier.
        :param ids: single ID string, list of IDs, or ``None`` for all.
        """
        if type_ not in _ACCEPTABLE_MODEL_RESOURCE_TYPES:
            raise TypeError(
                "Unknown model resource type %s. Acceptable types are %s" % (type_, _ACCEPTABLE_MODEL_RESOURCE_TYPES)
            )

        query = "models/%s/%s" % (model_id, type_)

        if ids is None:
            return self._http_get_results(query)

        ids = sequencify(ids)
        queries = ["%s/%s" % (query, id_) for id_ in ids]
        return squash(self.services.http_get(queries))
