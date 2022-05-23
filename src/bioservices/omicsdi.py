"""
Interface to the OmicsDI API Service

.. topic:: What is OmicsDI?

    :URL: https://www.omicsdi.org
    :REST: https://www.omicsdi.org/ws

    .. highlights::

        "Omics Discovery Index is an integrated and open source platform facilitating the access and dissemination of omics datasets. It provides a unique infrastructure to integrate datasets coming from multiple omics studies, including at present proteomics, genomics, transcriptomics and metabolomics.OmicsDI stores metadata coming from the public datasets from every resource using an efficient indexing system, which is able to integrate different biological entities including genes, proteins and metabolites with the relevant life science literature. OmicsDI is updated daily, as new datasets get publicly available in the contributing repositories."

        -- OmicsDI Home Page, March 22, 2020.
"""

# imports - standard imports
import re
import collections

# imports - third-party imports
import requests

# imports - module imports
from bioservices.services import REST
from bioservices.util import sequencify
from bioservices._compat import string_types, iteritems

__all__ = ["OmicsDI"]


def _omicsdi_path_to_method_name(path):
    # strip leading and trailing "/"
    formatted = path.strip("/")
    # replace all "/" with "_"
    formatted = formatted.replace("/", "_")
    # insert "_" before every capital letter.
    formatted = re.sub(r"(\w)([A-Z])", r"\1_\2", formatted)
    # convert to lowercase
    formatted = formatted.lower()

    method_name = formatted

    return method_name


class OmicsDIAuth(requests.auth.AuthBase):
    def __init__(self, token):
        if not isinstance(token, string_types):
            raise TypeError("Authentication Token cannot be %s. Must be of type str." % token)

        self._token = token

    @property
    def token(self):
        return getattr(self, "_token", None)

    @token.setter
    def token(self, value):
        if self.token == value:
            pass
        elif not isinstance(value, string_types):
            raise TypeError("Authentication Token must be of type str.")
        else:
            self._token = token

    def __call__(self, r):
        r.headers["x-auth-token"] = self._token
        return r


class OmicsDI(REST):
    _url = "http://www.omicsdi.org/ws"
    _api = {
        "paths": [
            {
                "path": "/dataset/merge",
                "method": "POST",
                "params": "mergeCandidate",
                "auth": True,
                "doc": """
                Merge datasets

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.set_auth_token("<YOUR_AUTH_TOKEN>")
                    >>> omicsdi.dataset_merge()
            """,
            },
            {
                "path": "/dataset/getMergeCandidates",
                "params": ["start", "size"],
                "auth": True,
                "doc": """
                Retrieve merge candidates

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.set_auth_token("<YOUR_AUTH_TOKEN>")
                    >>> omicsdi.dataset_get_merge_candidates(start = 0, size = 20)
            """,
            },
            {
                "path": "/dataset/:domain/:acc/files",
                "function_name": "dataset_domain_accession_files",
                "params": {
                    "domain": {"type": "path"},
                    "acc": {"type": "path", "argument": "accession"},
                    "position": {"required": True},
                },
                "doc": """
                Get Files At

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_domain_accession_files(accession = "PXD000210",
                        domain = "pride", position = 1)
                    [{'type': 'other',
                    'url': 'ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2013/11/PXD000210/F049708.dat'}]
            """,
            },
            {
                "path": "/dataset/search",
                "params": ["query", "sortfield", "order", "start", "size", "faceCount"],
                "doc": """
                Retrieve datasets in the resource using different queries

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_search()
                    {'count': 454002,
                    'datasets': [{'id': 'E-MTAB-723',
                    'source': 'arrayexpress-repository',
                    'title': 'Transcription profiling by array of human SHSY5Y cells transfected with miR96 and treated with methamphetamine',
                    'description': 'SHSY5Y cells trasnfected ±miR96 ± METH',...
            """,
            },
            {
                "path": "/dataset/latest",
                "params": "size",
                "doc": """
                Retrieve the latest datasets in the repository

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_latest()
                    {'count': 454002,
                    'datasets': [{'id': 'E-MTAB-8031',
                    'source': 'arrayexpress-repository',
                    'title': 'An integrated approach to profile lung tumor endothelial cell heterogeneity across species and models and to identify angiogenic candidates',
            """,
            },
            {
                "path": "/dataset/batch",
                "params": {
                    "accession": {"required": True, "argument": "accession"},
                    "database": {"required": True},
                },
                "doc": """
                Retrieve an specific dataset

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_batch(accession = "PXD000210", database = "pride")
                    {'failure': [],
                    'datasets': [{'id': 'PXD000210',
                    'source': 'pride',
                    'name': 'Proteome analysis by charge state-selective separation of peptides: a multidimensional approach',...
            """,
            },
            {
                "path": "/dataset/mostAccessed",
                "params": {"size": {"required": True}},
                "doc": """
                Retrieve a specific dataset

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_most_accessed(size = 20)
                    {'count': 20,
                    'datasets': [{'id': 'BIOMD0000000048',
                    'source': 'biomodels',
                    'title': 'Kholodenko1999 - EGFR signaling',...
            """,
            },
            {
                "path": "/dataset/getFileLinks",
                "params": {
                    "accession": {"required": True, "argument": "accession"},
                    "database": {"required": True},
                },
                "doc": """
                Retrieve all file links for a given dataset

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_get_file_links(accession = "PXD000210", database = "pride")
                    [
                        "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2013/11/PXD000210/L9822_0872_Lazaro_100812_RH1_MEF_9.RAW",
                        "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2013/11/PXD000210/R8798_Lazaro_RH2_ETD_10.RAW",...
            """,
            },
            {
                "path": "/dataset/:domain/:acc",
                "function_name": "dataset_domain_accession",
                "params": {
                    "domain": {"type": "path"},
                    "acc": {"type": "path", "argument": "accession"},
                    "debug": {"default": False},
                },
                "doc": """
                Get Files At

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_domain_accession(accession = "PXD000210", domain = "pride")
                    {
                        "database": "Pride",
                        "file_versions": [
                        {
                            "files": {
                            "Xlsx": [
                                "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2013/11/PXD000210/identifications RH2 - ETD.xlsx"
                            ],...
            """,
            },
            {
                "path": "/dataset/getSimilar",
                "params": {
                    "accession": {"required": True, "argument": "accession"},
                    "database": {"required": True},
                },
                "doc": """
                Retrieve the related datasets to one Dataset

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_get_similar(accession = "PXD000210", database = "pride")
                    {
                        "count": 14,
                        "datasets": [
                        {
                            "id": "E-PROT-2",
                            "source": "arrayexpress-repository",
                            "title": "Proteomic profiling of NCI60 cell lines from Cancer Cell Line Encyclopedia",...
            """,
            },
            {
                "path": "/dataset/getSimilarByPubmed",
                "params": {"pubmed": {"required": True}},
                "doc": """
                Retrieve all datasets which have same pubmed id

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_get_similar_by_pubmed(pubmed = 16585740)
                    [
                        {
                            "accession": "E-TIGR-123",
                            "database": "ArrayExpress",
                            "initHashCode": -642128312,...
            """,
            },
            {
                "path": "/database/all",
                "doc": """
                Get DataBase List

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.database_all()
                    [
                        {
                            "databaseName": "EGA",
                            "title": "EGA Database",
                            "sourceUrl": "https://ega-archive.org",
                            "imgAlt": "EGA logo",...
            """,
            },
            {
                "path": "/term/getTermByPattern",
                "params": {"q": {"argument": "query"}, "size": {}},
                "doc": """
                Retrieve the Terms for a pattern

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.term_get_term_by_pattern()
                    {
                        "total_count": 0,
                        "items": []
                    }
            """,
            },
            {
                "path": "/term/frequentlyTerm/list",
                "params": {
                    "size": {},
                    "domain": {
                        "required": True,
                    },
                    "field": {"required": True},
                },
                "doc": """
                Retrieve frequently terms from the Repo

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.term_frequently_term_list(domain = "pride", field = "description")
                    [
                        {
                            "label": "analysis",
                            "frequent": "2770"
                        },...
            """,
            },
            {
                "path": "/seo/home",
                "doc": """
                Retrieve data for home page

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.seo_home()
                    {
                        "@graph": [
                            {
                            "name": "Omics Discovery Index - Discovering and Linking Public Omics Datasets",
                            "url": "http://www.omicsdi.org/",...
            """,
            },
            {
                "path": "/seo/search",
                "doc": """
                Retrieve data for browse page

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.seo_search()
                    {
                        "name": "Browse",
                        "url": "http://www.omicsdi.org/search?q=*:*",
                        "keywords": "OmicsDI, Search, Browsers, Datasets, Searching",...
            """,
            },
            {
                "path": "/seo/api",
                "doc": """
                Retrieve data for api page

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.seo_api()
                    {
                        "name": "API",
                        "url": "http://www.omicsdi.org/api",
                        "keywords": "OmicsDI About Page, Help, Consortium",...
            """,
            },
            {
                "path": "/seo/database",
                "doc": """
                Retrieve data for databases page

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.seo_database()
                    {
                        "name": "Databases",
                        "url": "http://www.omicsdi.org/database",
                        "keywords": "OmicsDI Help Page, Training, Examples",...
            """,
            },
            {
                "path": "/seo/dataset/:domain/:acc",
                "function_name": "seo_dataset_domain_accession",
                "params": {
                    "domain": {"type": "path", "required": True},
                    "acc": {"type": "path", "required": True, "argument": "accession"},
                },
                "doc": """
                Retrieve data for dataset page

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.seo_dataset_domain_accession(domain = "pride", accession = "PXD000210")
                    {
                        "name": "Proteome analysis by charge state-selective separation of peptides: a multidimensional approach",
                        "url": null,
                        "keywords": "Mouse,SCX,RP-HPLC basic pH,LC-MSMS",...

            """,
            },
            {
                "path": "/seo/about",
                "doc": """
                Retrieve data for about page

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.seo_about()
                    {
                        "name": "About OmicsDI",
                        "url": "http://www.omicsdi.org/about",
                        "keywords": "OmicsDI About Page, Help, Consortium",...
            """,
            },
            {
                "path": "/statistics/organisms",
                "params": "size",
                "doc": """
                Return statistics about the number of datasets per Organisms

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_organisms()
                    [
                        {
                            "label": "Total",
                            "id": null,
                            "value": "443401",
                            "name": "Total"
                        },...
            """,
            },
            {
                "path": "/statistics/tissues",
                "params": "size",
                "doc": """
                Return statistics about the number of datasets per Tissue

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_tissues()
                    [{'label': 'Total', 'id': None, 'value': '443401', 'name': 'Total'},
                    {'label': 'Liver', 'id': 'Liver', 'value': '135', 'name': 'Liver'},
                    {'label': 'Kidney', 'id': 'Kidney', 'value': '65', 'name': 'Kidney'},...
            """,
            },
            {
                "path": "/statistics/omics",
                "doc": """
                Return statistics about the number of datasets per Omics Type

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_omics()
                    [{'label': 'Total', 'id': None, 'value': '443401', 'name': 'Total'},
                    {'label': 'Transcriptomics',
                    'id': 'Transcriptomics',
                    'value': '126876',
                    'name': 'Transcriptomics'},...
            """,
            },
            {
                "path": "/statistics/diseases",
                "doc": """
                Return statistics about the number of datasets per diseases

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_diseases()
                    [{'label': 'Total', 'id': None, 'value': '443401', 'name': 'Total'},
                    {'label': 'Normal', 'id': 'Normal', 'value': '630', 'name': 'Normal'},
                    {'label': 'Breast Cancer',
                    'id': 'Breast Cancer',
                    'value': '54',
                    'name': 'Breast Cancer'},...
            """,
            },
            {
                "path": "/statistics/domains",
                "doc": """
                Return statistics about the number of datasets per Repository

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_domains()
                    [{'domain': {'label': 'ArrayExpress',
                    'id': None,
                    'value': '72617',
                    'name': 'ArrayExpress'},
                    'subdomains': []},...
            """,
            },
            {
                "path": "/statistics/omicsByYear",
                "doc": """
                Return statistics about the number of datasets per OmicsType on recent 5 years.

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_omics_by_year()
                    [{'year': '2020', 'genomics': '26', 'metabolomics': '41', 'proteomics': '11', 'transcriptomics': '223'}, {'year': '2019', 'genomics': '170', 'metabolomics': '578', 'proteomics': '1779', 'transcriptomics': '927'}, {'year': '2018', 'genomics': '594', 'metabolomics': '678', 'proteomics': '2646', 'transcriptomics': '1609'}, {'year': '2017', 'genomics': '127', 'metabolomics': '716', 'proteomics': '1969', 'transcriptomics': '1015'}]
            """,
            },
        ]
    }

    def __init__(self, token=None, verbose=False, cache=False):
        self.super = super(OmicsDI, self)
        self.super.__init__(name="OmicsDI", url=OmicsDI._url, verbose=verbose, cache=cache)

        self.set_auth_token(token)

        self._build_api()

    @property
    def token(self):
        return getattr(self, "_token", None)

    @token.setter
    def token(self, value):
        if self.token == value:
            pass
        elif not isinstance(value, string_types):
            raise TypeError("Authentication Token must be of type str.")
        else:
            self._token = token

    def set_auth_token(self, token):
        self.token = token

    def _create_api_function(self, api):
        METHOD_CALLERS = {
            "GET": self.http_get,
            "POST": self.http_post,
            "PUT": self.http_put,
            "DELETE": self.http_delete,
        }

        doc = api.get("doc")

        def fn(*args, **kwargs):
            data = {}

            query = api["path"]
            params = api.get("params")
            method = api.get("method", "GET")
            auth_required = api.get("auth", False)

            if params:
                parameters = []

                if isinstance(params, collections.Mapping):
                    for param, info in iteritems(params):
                        type_ = info.get("type", "param")
                        required = info.get("required")
                        argument = info.get("argument", param)
                        default = info.get("default")

                        if (type_ == "path" or required) and argument not in kwargs:
                            raise ValueError("Argument %s is not passed." % argument)

                        if type_ == "path":
                            value = kwargs.get(argument)
                            query = query.replace(":%s" % param, value)
                        else:
                            kwargs[param] = kwargs.get(argument, default)
                            parameters.append(param)

                parameters = sequencify(parameters)
                for parameter in parameters:
                    if parameter in kwargs:
                        value = kwargs.get(parameter)
                        data[parameter] = value

            args = {"params": data, "frmt": "json"}

            if auth_required:
                auth = OmicsDIAuth(token=self.token)
                args.update({"auth": auth})

            method_caller = METHOD_CALLERS.get(method, self.http_get)

            return method_caller(query, **args)

        if doc:
            fn.__doc__ = doc

        return fn

    def _build_api(self):
        for api in OmicsDI._api["paths"]:
            query = api["path"]

            fn = self._create_api_function(api)

            method_name = api.get("function_name", _omicsdi_path_to_method_name(query))

            setattr(self, method_name, fn)
