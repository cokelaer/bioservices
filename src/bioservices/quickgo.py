# -*- python -*-
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
# $Id$
"""Interface to the quickGO interface

.. topic:: What is quickGO

    :URL: http://www.ebi.ac.uk/QuickGO/
    :Service: http://www.ebi.ac.uk/QuickGO/WebServices.html

    .. highlights::

        "QuickGO is a fast web-based browser for Gene Ontology terms and
        annotations, which is provided by the UniProt-GOA project at the EBI. "

        -- from QuickGO home page, Dec 2012

"""
from __future__ import print_function
import json

from bioservices.services import REST

__all__ = ["QuickGO"]


class QuickGO(REST):
    """Interface to the `QuickGO <http://www.ebi.ac.uk/QuickGO/WebServices.html>`_ service

    Retrieve information given a GO identifier:

    .. doctest::

        >>> from bioservices import QuickGO
        >>> s = QuickGO()
        >>> res = s.Term("GO:0003824")

    Retrieve information about a protein given its uniprot identifier, a
    taxonomy number. Let us also restrict the search to the UniProt database and
    print only 3 columns of information (protein name, GO identifier and GO
    name)::

        print(s.Annotation(protein="Q8IYB3", frmt="tsv", tax=9606,
            source="UniProt", col="proteinName,goID,goName"))

    Here is the Term output for a given GO identifier::

        >>> print(s.Term("GO:0000016", frmt="obo"))
        [Term]
        id: GO:0000016
        name: lactase activity
        def: "Catalysis of the reaction: lactose + H2O = D-glucose + D-galactose."
        synonym: "lactase-phlorizin hydrolase activity" broad
        synonym: "lactose galactohydrolase activity" exact
        xref: EC:3.2.1.108
        xref: MetaCyc:LACTASE-RXN
        xref: RHEA:10079
        is_a: GO:0004553 ! hydrolase activity, hydrolyzing O-glycosyl compounds

    .. versionchanged:: we use the new QuickGO API since version 1.5.0
        To use the old API, please use version of bioservices below 1.5

    """
    _goid_example = "GO:0003824"
    _valid_col = ['proteinDB', 'proteinID', 'proteinSymbol', 'qualifier',
                  'goID', 'goName', 'aspect', 'evidence', 'ref', 'with', 'proteinTaxon',
                  'date', 'from', 'splice', 'proteinName', 'proteinSynonym', 'proteinType',
                  'proteinTaxonName', 'originalTermID', 'originalGOName']

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages.

        """
        #super(QuickGO, self).__init__(url="http://www.ebi.ac.uk/QuickGO-Old",
        super(QuickGO, self).__init__(url="https://www.ebi.ac.uk/QuickGO",
                                      name="quickGO", verbose=verbose, cache=cache)

    def gosearch(self, query, limit=600, page=1):
        """Searches a simple user query, e.g., query=apopto

        :param str query: 
        :param int limit: max 600
        :param int page:


        """
        url = "services/ontology/go/search"
        params = {"query":query, 'limit':limit, "page":page}
        res = self.http_get(url, frmt="txt", params=params)
        res = json.loads(res)
        return res

    def goterms(self, max_number_of_pages=None):
        """Get information on all terms and page through the result"""
        url = "services/ontology/go/terms"
        results = []

        data = self.http_get(url, frmt="txt", params={"page":1})
        data = json.loads(data)
        number_of_pages = data['pageInfo']['total']
        if max_number_of_pages:
            number_of_pages = max_number_of_pages

        # unfortunately, the new API requires to call the service for each page.
        results = []
        for i in range(1, number_of_pages + 1):
            print("fetching page %s / %s " % (i+1, number_of_pages))
            json.loads
            data = self.http_get(url, frmt="txt", params={'page':i+1})
            data = json.loads(data)['results']
            results.extend(data)
        return results

    def Annotation(self,
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
                    extension=None
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
            results without calling  this function several times chanding this 
            parameter (default to 1).
        :param char aspect: use this to limit the annotations returned to a
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
            'evidenceCodeUsageRelationships' filter. E.g., descendants, exact<F12>
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

            >>> print(s.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",
            ... reference='PMID:*'))
            >>> print(s.Annotation(protein='P12345,Q4VCS5', frmt='tsv',
            ...     col="ref,evidence",reference='PMID:,Reactome:'))


        """
        #_valid_formats = ["gaf", "gene2go", "proteinList", "fasta", "tsv", "dict"]
        _valid_db = ['UniProtKB', 'UniGene', 'Ensembl']
        _valid_aspect = ['P', 'F', 'C']
        validity = {
            "includeFields": ['goName', 'taxonName', 'name', 'synonyms']

        }

        if isinstance(limit, int) is False or limit >100 or limit<0:
            raise TypeError("limit parameter must be an integer greater than zero and less than 100")
        if isinstance(page, int) is False or limit<0:
            raise TypeError("page parameter must be an integer greater than zero")

        # fill params with parameters that have default values.
        params = {'limit': limit, "page":page}

        # beginning of the URL
        url = "services/annotation/search?"

        # what is the ID being provided. We can have only one of:
        # taxonId, goid
        if goId is not None:
            params['goId'] = goId

        if taxonId is not None:
            params["taxonId"] = taxonId

        if assignedBy:
            params['assignedBy'] = assignedBy

        if includeFields:
            for this in includeFields.split(","):
                assert this in validity['includeFields']
            params['includeFields'] = includeFields

        if geneProductType:
            for this in geneProductType.split(","):
                assert this in ["protein", "RNA", "complex"]
            params['geneProductType'] = geneProductType

        if evidenceCode:
            params['evidenceCode'] = evidenceCode

        if evidenceCodeUsage:
            assert evidenceCodeUsage in ['descendants', 'exact']
            params['evidenceCodeUsage'] = evidenceCodeUsage

        if taxonUsage:
            assert taxonUsage in ['descendants', 'exact']
            params['taxonUsage'] = taxonUsage

        if goUsage:
            assert goUsage in ['descendants', 'exact', 'slim']
            params['goUsage'] = goUsage

        if evidenceCodeUsageRelationships:
            for this in evidenceCodeUsageRelationships.split(","):
                assert this in ['part_of', 'is_a', 'regulates', 'occurs_in']
            params['evidenceCodeUsageRelationships'] = evidenceCodeUsageRelationships

        if goUsageRelationships:
            for this in goUsageRelationships.split(","):
                assert this in ['part_of', 'is_a', 'regulates', 'occurs_in']
            params['goUsageRelationships'] = goUsageRelationships

        if geneProductId:
            params['geneProductId'] = geneProductId

        if qualifier:
            params['qualifier'] = qualifier 

        if withFrom:
            params['withFrom'] = withFrom

        if targetSet:
            params['targetSet'] = targetSet

        if geneProductSubset:
            params['geneProductSubset'] = geneProductSubset

        if extension:
            params['extension'] = extension

        if aspect is not None:
            aspects = {
                "P": "biological_process",
                "F": "molecular_function",
                "C": "cellular_component" }
            self.devtools.check_param_in_list(aspect, _valid_aspect)
            params['aspect'] = aspects[aspect]

        if reference:
            if isinstance(reference, list):
                reference = ",".join([x.strip() for x in reference])
            elif isinstance(reference, str):
                pass
            else:
                raise ValueError("""
Invalid parameter: source parameters must be a list of strings ['PUBMED']
or a string (e.g., 'PUBMED:') """)
            params['reference'] = reference

        res = self.http_get(url, frmt="txt", params=params)

        try:
            import json
            res = json.loads(res)
        except:
            pass

        return res

    def Annotation_from_goid(self, goId, max_number_of_pages=25, **kargs):
        """Returns a DataFrame containing annotation on a given GO identifier

        :param str protein: a GO identifier
        :return: all outputs are stored into a Pandas.DataFrame data structure.

        All parameters from :math:`Annotation` are also valid except **format** that
        is set to **tsv**  and cols that is made of all possible column names.

        """
        data = self.Annotation(goId=goId, **kargs)
        number_of_pages = data['pageInfo']['total']
        if number_of_pages > max_number_of_pages:
            print("As of 23d Oct 2017, the QuickGO API limits the number of pages to 25")
            number_of_pages = max_number_of_pages

        # unfortunately, the new API requires to call the service for each page.
        results = []
        for i in range(1, number_of_pages + 1):
            print("fetching page %s / %s " % (i+1, number_of_pages))
            data = self.Annotation(goId=goId, page=i+1, **kargs)
            if data not in [400, '400']:
                results.extend(data['results'])
        try:
            import pandas as pd
            return pd.DataFrame(results)
        except:
            self.logging.warning(
                "Cannot return a DataFrame. Returns the list. If you want the dataframe, install pandas library")
            return results


    def Terms(self, query):
        url = "services/ontology/go/terms/"
        url += query
        res =self.http_get(url, frmt="txt")
        if res not in [400,"400"]:
            res = json.loads(res)['results'] 
        return res


class GeneOntology():
    """


    Given a list of GO terms, read them with QuickGO and convert them to a list.
    Each entry contains a dictionary

    [Term]
    id: GO:0031655
    name: negative regulation of heat dissipation
    def: "Any process that stops, prevents, or reduces the rate or extent of heat dissipation."
    synonym: "downregulation of heat dissipation" exact
    synonym: "inhibition of heat dissipation" narrow
    synonym: "down-regulation of heat dissipation" exact
    synonym: "down regulation of heat dissipation" exact
    is_a: GO:0031654 ! regulation of heat dissipation
    is_a: GO:0032845 ! negative regulation of homeostatic process
    is_a: GO:0051241 ! negative regulation of multicellular organismal process

    """
    def __init__(self):
        self._quickgo = QuickGO(verbose=False)

    def getGOTerm(self, goid):
        return self._quickgo.Term(goid)
