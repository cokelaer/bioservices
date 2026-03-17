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
"""Interface to the QuickGO interface

.. topic:: What is quickGO

    :URL: http://www.ebi.ac.uk/QuickGO/
    :Service: http://www.ebi.ac.uk/QuickGO/WebServices.html

    .. highlights::

        "QuickGO is a fast web-based browser for Gene Ontology terms and
        annotations, which is provided by the UniProt-GOA project at the EBI. "

        -- from QuickGO home page, Dec 2012

"""
from bioservices.services import REST

__all__ = ["QuickGO"]


class QuickGO:
    """Interface to the `QuickGO <http://www.ebi.ac.uk/QuickGO/WebServices.html>`_ service

    Retrieve information given a GO identifier:

    .. doctest::

        >>> from bioservices import QuickGO
        >>> go = QuickGO()
        >>> res = go.get_go_terms("GO:0003824")

    .. versionchanged:: we use the new QuickGO API since version 1.5.0
        To use the old API, please use version of bioservices below 1.5

    """

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages.
        :param bool cache: set to True to enable HTTP caching

        """
        # super(QuickGO, self).__init__(url="http://www.ebi.ac.uk/QuickGO-Old",
        self.services = REST(url="https://www.ebi.ac.uk/QuickGO", name="quickGO", verbose=verbose, cache=cache)

    def go_search(self, query, limit=600, page=1):
        """Searches a simple user query, e.g., query=apopto

        :param str query: search term (e.g., ``"apopto"``)
        :param int limit: maximum number of results to return (max 600)
        :param int page: page number for paginated results (default 1)
        :return: list of matching GO term results


        """
        url = "services/ontology/go/search"
        query = query.replace(":", "%3A")
        query = query.replace(",", "%2C")
        params = {"query": query, "limit": limit, "page": page}
        res = self.services.http_get(url, frmt="json", params=params, headers=self.services.get_headers("json"))
        try:
            return res["results"]
        except Exception:  # pragma: no cover
            return res

    def get_go_terms(self, query, max_number_of_pages=None):
        """Get information on all terms and page through the result

        :param str query: GO term ID(s) as a comma-separated string (e.g., ``"GO:0003824"``)
        :param max_number_of_pages: maximum number of pages to retrieve
        :return: list of GO term result dictionaries
        """

        query = query.replace(":", "%3A")
        query = query.replace(",", "%2C")
        url = "services/ontology/go/terms/{}".format(query)
        results = self.services.http_get(url, frmt="json", params={}, headers=self.services.get_headers("json"))
        try:
            return results["results"]
        except Exception:  # pragma: no cover
            return results

    def get_go_ancestors(self, query, relations="is_a,part_of,occurs_in,regulates"):
        """Retrieve ancestors of given GO term(s).

        :param str query: GO term ID(s) as a comma-separated string
        :param str relations: comma-separated relationship types to traverse
            (default ``"is_a,part_of,occurs_in,regulates"``)
        :return: list of ancestor GO term results
        """
        query = query.replace(":", "%3A")
        query = query.replace(",", "%2C")
        url = "services/ontology/go/terms/{}/ancestors".format(query)
        results = self.services.http_get(url, frmt="json", params={}, headers=self.services.get_headers("json"))
        try:
            return results["results"]
        except Exception:  # pragma: no cover
            return results

    def get_go_children(self, query):
        """Retrieve direct children of given GO term(s).

        :param str query: GO term ID(s) as a comma-separated string
        :return: list of child GO term results
        """
        query = query.replace(":", "%3A")
        query = query.replace(",", "%2C")
        url = "services/ontology/go/terms/{}/children".format(query)
        results = self.services.http_get(url, frmt="json", params={}, headers=self.services.get_headers("json"))
        try:
            return results["results"]
        except Exception:  # pragma: no cover
            return results

    def get_go_chart(self, query):
        """Return a PNG chart image for the given GO term(s).

        :param str query: GO term ID(s) as a comma-separated string
        :return: raw PNG image bytes

        ::

            res = go.get_chart("GO:0022804")
            with open("temp.png", "wb") as fout:
                fout.write(res)
        """
        query = query.replace(":", "%3A")
        query = query.replace(",", "%2C")
        url = "services/ontology/go/terms/{}/chart".format(query)
        res = self.services.http_get(url, frmt="json", params={}, headers={"Accept": "image/png"})
        # import base64
        # res = base64.b64decode(res).decode()
        return res

    def get_go_paths(self, _from, _to, relations="is_a,part_of,occurs_in,regulates"):
        """Retrieve paths between two specified sets of ontology terms.

        Each path is formed from a list of (term, relationship, term) triples.

        :param str _from: source GO term ID (e.g., ``"GO:0005215"``)
        :param str _to: target GO term ID (e.g., ``"GO:0003674"``)
        :param str relations: comma-separated relationship types to traverse
        :return: dict with ``"results"`` key containing a list of paths

        ::

            paths = go.get_go_paths("GO:0005215", "GO:0003674")
            # First path is found as the first item in the "results"
            paths["results"][0]

        """
        _from = _from.replace(":", "%3A")
        _from = _from.replace(",", "%2C")
        _to = _to.replace(":", "%3A")
        _to = _to.replace(",", "%2C")
        url = "services/ontology/go/terms/{}/paths/{}".format(_from, _to)
        results = self.services.http_get(url, frmt="json", params={}, headers=self.services.get_headers("json"))
        return results

    def Annotation(
        self,
        assignedBy=None,
        includeFields=None,
        limit=100,
        page=1,
        aspect=None,
        reference=None,
        geneProductId=None,
        evidenceCode=None,
        goId=None,
        qualifier=None,
        withFrom=None,
        taxonId=None,
        taxonUsage=None,
        goUsage=None,
        goUsageRelationships=None,
        evidenceCodeUsage=None,
        evidenceCodeUsageRelationships=None,
        geneProductType=None,
        targetSet=None,
        geneProductSubset=None,
        extension=None,
    ):
        """Calling the Annotation service

        .. versionchanged:: 1.4.18 due to service API changes, we refactored
            this method completely

        :param str assignedBy: The database from which this annotation
            originates. Accepts comma separated values.E.g., BHF-UCL,Ensembl.
        :param str includeFields: Optional fields retrieved from external
            services. Accepts comma separated values. accepted values: goName, taxonName,
            name, synonyms.
        :param int limit: download limit (number of lines) (default 10,000 rows,
            which may not be sufficient for the data set that you are
            downloading. To bypass this default, and return the entire data set,
            specify a limit of -1).
        :param int page: results may be stored on several pages. You must
            provide this number. There is no way to retrieve more than 100
            results without calling  this function several times changing this
            parameter (default to 1).
        :param str aspect: use this to limit the annotations returned to a
            specific ontology or ontologies (Molecular Function, Biological
            Process or Cellular Component). The valid character can be F,P,C.
        :param str reference: PubMed or GO reference supporting annotation. Can refer to a
            specific reference identifier or category (for category level, use
            `*`  after ref type). Can be 'PUBMED:`*`', 'GO_REF:0000002'.
        :param str geneProductId: The id of the gene product annotated with the
            GO term. Accepts comma separated values.E.g., URS00000064B1_559292.
        :param str evidenceCode: Evidence code indicating how the annotation is
            supported. Accepts comma separated values. E.g., ECO:0000255.
        :param str goId: The GO id of an annotation. Accepts comma separated
            values. E.g., GO:0070125.
        :param str qualifier: Aids the interpretation of an annotation. Accepts
            comma separated values. E.g., enables,involved_in.
        :param str withFrom: Additional ids for an annotation. Accepts comma
            separated values. E.g., P63328.
        :param str taxonId: The taxonomic id of the species encoding the gene
            product associated to an annotation. Accepts comma separated values. E.g.,
            1310605.
        :param str taxonUsage: Indicates how the taxonomic ids within the
            annotations should be used. E.g., exact.
        :param str goUsage: Indicates how the GO terms within the annotations
            should be used. Used in conjunction with 'goUsageRelationships' filter. E.g.,
            descendants.
        :param str goUsageRelationships: The relationship between the 'goId'
            values found within the annotations. Allows comma separated values. E.g.,
            is_a,part_of.
        :param str evidenceCodeUsage: Indicates how the evidence code terms
            within the annotations should be used. Is used in conjunction with
            'evidenceCodeUsageRelationships' filter. E.g., descendants, exact
        :param str evidenceCodeUsageRelationships: The relationship between the
            provided 'evidenceCode' identifiers. Allows comma separated values. E.g.,
            is_a,part_of.
        :param str geneProductType: The type of gene product. Accepts comma separated
             values. E.g., protein,RNA. can be protein, RNA and/or complex
        :param str targetSet: Gene product set. Accepts comma separated values.
            E.g., KRUK,BHF-UCL,Exosome.
        :param str geneProductSubset: A database that provides a set of gene
            products. Accepts comma separated values. E.g., TrEMBL.
        :param str extension: Extensions to annotations, where each extension
            can be: EXTENSION(DB:ID) / EXTENSION(DB) / EXTENSION.
        :return: a dictionary

        ::

            >>> print(go.Annotation(geneProductId='UniProtKB:P12345', reference='PMID:*'))
            >>> print(go.Annotation(geneProductId='UniProtKB:P12345,UniProtKB:Q4VCS5',
            ...     reference='PMID:,Reactome:'))


        """
        # _valid_formats = ["gaf", "gene2go", "proteinList", "fasta", "tsv", "dict"]
        _valid_aspect = ["P", "F", "C"]
        validity = {"includeFields": ["goName", "taxonName", "name", "synonyms"]}

        if isinstance(limit, int) is False or limit > 100 or limit < 0:
            raise TypeError("limit parameter must be an integer greater than zero and less than 100")
        if isinstance(page, int) is False or limit < 0:
            raise TypeError("page parameter must be an integer greater than zero")

        # fill params with parameters that have default values.
        params = {"limit": limit, "page": page}

        # beginning of the URL
        url = "services/annotation/search?"

        # what is the ID being provided. We can have only one of:
        # taxonId, goid
        if goId is not None:
            params["goId"] = goId

        if taxonId is not None:
            params["taxonId"] = taxonId

        if assignedBy:
            params["assignedBy"] = assignedBy

        if includeFields:
            for this in includeFields.split(","):
                assert this in validity["includeFields"]
            params["includeFields"] = includeFields

        if geneProductType:
            for this in geneProductType.split(","):
                assert this in ["protein", "miRNA", "complex"]
            params["geneProductType"] = geneProductType

        if evidenceCode:
            params["evidenceCode"] = evidenceCode

        if evidenceCodeUsage:
            assert evidenceCodeUsage in ["descendants", "exact"]
            params["evidenceCodeUsage"] = evidenceCodeUsage

        if taxonUsage:
            assert taxonUsage in ["descendants", "exact"]
            params["taxonUsage"] = taxonUsage

        if goUsage:
            assert goUsage in ["descendants", "exact", "slim"]
            params["goUsage"] = goUsage

        if evidenceCodeUsageRelationships:
            for this in evidenceCodeUsageRelationships.split(","):
                assert this in ["part_of", "is_a", "regulates", "occurs_in"]
            params["evidenceCodeUsageRelationships"] = evidenceCodeUsageRelationships

        if goUsageRelationships:
            for this in goUsageRelationships.split(","):
                assert this in ["part_of", "is_a", "regulates", "occurs_in"]
            params["goUsageRelationships"] = goUsageRelationships

        if geneProductId:
            params["geneProductId"] = geneProductId

        if qualifier:
            params["qualifier"] = qualifier

        if withFrom:
            params["withFrom"] = withFrom

        if targetSet:
            params["targetSet"] = targetSet

        if geneProductSubset:
            params["geneProductSubset"] = geneProductSubset

        if extension:
            params["extension"] = extension

        if aspect is not None:
            aspects = {
                "P": "biological_process",
                "F": "molecular_function",
                "C": "cellular_component",
            }
            self.services.devtools.check_param_in_list(aspect, _valid_aspect)
            params["aspect"] = aspects[aspect]

        if reference:
            if isinstance(reference, list):
                reference = ",".join([x.strip() for x in reference])
            elif isinstance(reference, str):
                pass
            else:
                raise ValueError(
                    """
Invalid parameter: source parameters must be a list of strings ['PUBMED']
or a string (e.g., 'PUBMED:') """
                )
            params["reference"] = reference

        res = self.services.http_get(url, frmt="txt", params=params, headers=self.services.get_headers("json"))

        try:
            import json

            res = json.loads(res)
        except Exception:
            pass

        return res

    def Annotation_from_goid(self, goId, max_number_of_pages=25, **kargs):
        """Returns a DataFrame containing annotation on a given GO identifier

        :param str goId: a GO identifier (e.g., ``"GO:0003824"``)
        :param int max_number_of_pages: maximum number of result pages to fetch
        :return: a ``pandas.DataFrame`` containing the annotation data, or a list
            if pandas is not installed

        All parameters from :meth:`Annotation` are also valid except **format** that
        is set to **tsv**  and cols that is made of all possible column names.

        """
        data = self.Annotation(goId=goId, **kargs)
        number_of_pages = data["pageInfo"]["total"]
        if number_of_pages > max_number_of_pages:
            print("As of 23d Oct 2017, the QuickGO API limits the number of pages to 25")
            number_of_pages = max_number_of_pages

        # unfortunately, the new API requires to call the service for each page.
        results = []
        for i in range(0, number_of_pages):
            print("fetching page %s / %s " % (i + 1, number_of_pages))
            data = self.Annotation(goId=goId, page=i + 1, **kargs)
            if data not in [400, "400"]:
                results.extend(data["results"])
        try:
            import pandas as pd

            return pd.DataFrame(results)
        except Exception:
            self.logging.warning(
                "Cannot return a DataFrame. Returns the list. If you want the dataframe, install pandas library"
            )
            return results

    def gene_product_search(
        self,
        query,
        taxonID=None,
        page=1,
        limit=100,
        type=None,
        dbSubSet=None,
        proteome=None,
    ):
        """Search for gene products matching a query string.

        :param str query: search term
        :param str taxonID: NCBI taxonomy ID to filter results (optional)
        :param int page: page number for paginated results (default 1)
        :param int limit: maximum number of results per page (max 100)
        :param str type: gene product type filter (optional)
        :param str dbSubSet: database subset filter (optional)
        :param str proteome: proteome filter (optional)
        :return: dict with gene product search results
        """
        if isinstance(limit, int) is False or limit > 100 or limit < 0:
            raise TypeError("limit parameter must be an integer greater than zero and less than 100")
        if isinstance(page, int) is False or limit < 0:
            raise TypeError("page parameter must be an integer greater than zero")
