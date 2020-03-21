# imports - standard imports
from bioservices.services import REST

class OmicsDI(REST):
    _url = "http://www.omicsdi.org/ws"
    _api = {
        "paths": [{
            "path": "/dataset/merge", # TODO
            "method_type": "POST",
            "params": ["mergeCandidate"],
            "method_name": "dataset_merge",
            "doc": """
                Merge datasets

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.dataset_merge()
            """ 
        }, {
            "path": "/dataset/getMergeCandidates",
            "method_name": "dataset_get_merge_candidates",
            
        }, {
            "path": "/database/all",
            "method_name": "databases_all",
            "doc": """

            """
        }, {
            "path": "/term/getTermByPattern",
            "params": ["q", "size"],
            "method_name": "term_get_term_by_pattern",
            "doc": """

            """
        }, {
            "path": "/term/frequentlyTerm/list",
            "params": ["size", "domain", "field"],
            "method_name": "term_frequently_term_list",
            "doc": """

            """
        }, {
            "path": "/seo/home",
            "method_name": "seo_home",
            "doc": """

            """
        }, {
            "path": "/seo/search",
            "method_name": "seo_search",
            "doc": """

            """
        }, {
            "path": "/seo/api",
            "method_name": "seo_api",
            "doc": """

            """
        }, {
            "path": "/seo/database",
            "method_name": "seo_database",
            "doc": """

            """
        }, {
            "path": "/seo/dataset/:domain/:acc",
            "method_name": "seo_dataset_domain_accession",
            "doc": """

            """
        }, {
            "path": "/seo/about",
            "method_name": "seo_about",
            "doc": """

            """
        }, {
            "path": "/statistics/organisms",
            "params": ["size"],
            "method_name": "statistics_organisms",
            "doc": """

            """
        }, {
            "path": "/statistics/tissues",
            "params": ["size"],
            "method_name": "statistics_tissues",
            "doc": """
                Return statistics about the number of datasets per Tissue

                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_tissues()
                    [{'label': 'Total', 'id': None, 'value': '443401', 'name': 'Total'},
                    {'label': 'Liver', 'id': 'Liver', 'value': '135', 'name': 'Liver'},
                    {'label': 'Kidney', 'id': 'Kidney', 'value': '65', 'name': 'Kidney'},...
            """
        }, {
            "path": "/statistics/omics",
            "method_name": "statistics_omics",
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
            """
        }, {
            "path": "/statistics/diseases",
            "method_name": "statistics_diseases",
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
            """
        }, {
            "path": "/statistics/domains",
            "method_name": "statistics_domains",
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
            """
        }, {
            "path": "/statistics/omicsByYear",
            "method_name": "statistics_omics_by_year",
            "doc": """
                Return statistics about the number of datasets per OmicsType on recent 5 years.
                
                :example:
                    >>> from bioservices import OmicsDI
                    >>> omicsdi = OmicsDI()
                    >>> omicsdi.statistics_omics_by_year()
                    [{'year': '2020', 'genomics': '26', 'metabolomics': '41', 'proteomics': '11', 'transcriptomics': '223'}, {'year': '2019', 'genomics': '170', 'metabolomics': '578', 'proteomics': '1779', 'transcriptomics': '927'}, {'year': '2018', 'genomics': '594', 'metabolomics': '678', 'proteomics': '2646', 'transcriptomics': '1609'}, {'year': '2017', 'genomics': '127', 'metabolomics': '716', 'proteomics': '1969', 'transcriptomics': '1015'}]
            """
        }]
    }

    def __init__(self, verbose=False, cache=False):
        self.super = super(OmicsDI, self)
        self.super.__init__(name="OmicsDI", url=OmicsDI._url, verbose=verbose, cache=cache)

        self._build_api()

    def _get_api_function(self, query, params = None, method_type = None):
        def fn(*args, **kwargs):
            data = { }

            if params:
                for param in params:
                    if param in kwargs:
                        value = kwargs.get(param)
                        data[param] = value
            
            method_caller = self.http_get

            args = { "params": params }
            
            if method_type == "POST":
                method_caller = self.http_post
                headers = kwargs.get()
            elif method_type == "PUT":
                method_caller = self.http_put
            elif method_type == "DELETE":
                method_caller = self.http_delete

            return self.method_caller(query, **args)
            
        return fn

    def _build_api(self):
        for path in OmicsDI._api["paths"]:
            query = path["path"]
            params = path.get("params")
            method_name = path["method_name"]
            method_type = path.get("method_type", "GET")

            fn = self._get_api_function(query, params = params,
                method_type = method_type)

            if path.get("doc"):
                fn.__doc__ = path["doc"]

            setattr(self, method_name, fn)