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
        super(QuickGO, self).__init__(url="http://www.ebi.ac.uk/QuickGO",
            name="quickGO", verbose=verbose, cache=cache)

    def Term(self, goid, frmt="oboxml"):
        """Obtain Term information


        :param str frmt: the output format (mini, obo, oboxml).

        The format can be:

        * mini:   Mini HTML, suitable for dynamically embedding in popup boxes.
        * obo:    OBO format snippet.
        * oboxml: OBO XML format snippet.

        ::

            from bioservices import QuickGO
            s = QuickGO()
            s.Term("GO:0003824")


        """
        self.devtools.check_param_in_list(frmt, ["mini", "obo", "oboxml"])
        if goid.startswith("GO:")is False:
            raise ValueError("GO id must start with 'GO:'")

        params = {'id':goid, 'format': frmt}
        res = self.http_get("GTerm", frmt="xml", params=params)

        return res

    def Annotation(self, goid=None, protein=None, frmt="gaf", limit=10000,
            gz=False, col=None, db=None, aspect=None, relType=None, termUse=None,
            evidence=None, source=None, ref=None,  tax=None, qualifier=None, q=None, 
            _with=None):
        """Calling the Annotation service

        Mutual exclusive parameters are goid, protein

        :param int limit: download limit (number of lines) (default 10,000 rows,
            which may not be sufficient for the data set that you are
            downloading. To bypass this default, and return the entire data set,
            specify a limit of -1).
        :param str frmt: one of "gaf", "gene2go", "proteinList", "fasta",
            "tsv" or "dict". The "dict" argument is the default and is a
            python dictionary.
        :param bool gz: gzips the downloaded file.
        :param str goid: GO identifiers either directly or indirectly
            (descendant GO identifiers) applied in annotations.
        :param char aspect: use this to limit the annotations returned to a
            specific ontology or ontologies (Molecular Function, Biological
            Process or Cellular Component). The valid character can be F,P,C.
        :param relType: not Implemented. By default, QuickGO will display annotations to GO terms
            that are related to that specified in the goid parameter by is_a,
            part_of and occurs_in relations; this parameter allows you to
            override that behaviour. See `details <http://www.ebi.ac.uk/QuickGO/reference.html#slim_custom>`_
        :param termUse:  if you set this parameter to slim, then QuickGO will
            use the supplied set of GO identifiers as a slim and will map the
            annotations up to these terms. See here for more details:
            http://www.ebi.ac.uk/QuickGO/GMultiTerm
        :param str db: protein database (identifier type). Can be UniProtKB, UniGene, Ensembl.
        :param str evidence: annotation evidence code category (Ev). Example of
            valid evidence are: be IDA, IC, ISS, IEA, IPI, ND, IMP, ISO, IGI
            should be either a string with comma separated values (e.g.,
            IEA,IDA) or a list of strings (e.g. ["IEA","IDA"]).
        :param str source: annotation provider. Examples are 'InterPro', 'UniPathway',
            'MGI', 'FlyBase', 'GOC', 'Source', 'UniProtKB', 'RGD', 'ENSEMBL',
            'ZFIN', 'IntAct'.
        :param str ref: PubMed or GO reference supporting annotation. Can refer to a
            specific reference identifier or category (for category level, use
            `*`  after ref type). Can be 'PUBMED:`*`', 'GO_REF:0000002'.
        :param str with: additional supporting information supplied in IEA, ISS, IPI, IC
            evidenced annotations; see GO documentation. Can refer to a specific
            identifier or category (for category level, use * after with type).
            Examples are: EC:2.5.1.30, IPR000092, HAMAP:*
        :param str qualifier: tags that modify the interpretation of an annotation.
             Examples are NOT, colocalizes_with, contributes_to.

        .. note::
            * Any number of fields can be specified; they will be AND'ed together.
            * Any number of values can be specified for each field; they will be OR'ed together.
            * Values should be URI encoded.
            * The file will be truncated if more than the specified number of annotations are found. The file is roughly 170 bytes/annotation (not gzipped).
            * The file will be gzipped if the gz parameter is supplied.


        ::

            >>> print s.Annotation(protein='P12345', frmt='tsv', col="ref,evidence",
            ... ref='PMID:*')
            >>> print s.Annotation(protein='P12345,Q4VCS5', frmt='tsv',
            ...     col="ref,evidence",ref='PMID:,Reactome:')



        """
        _valid_formats = ["gaf", "gene2go", "proteinList", "fasta", "tsv", "dict"]
        _valid_db = ['UniProtKB', 'UniGene', 'Ensembl']
        _valid_aspect = ['P', 'F', 'C']

        self.devtools.check_param_in_list(frmt, _valid_formats)

        if isinstance(limit, int) is False:
            raise TypeError("limit parameter must be an integer greater than zero")

        # fill params with parameters that have default values.
        params = {'format': frmt, 'limit': limit}

        # beginning of the URL
        url = "GAnnotation?"

        # what is the ID being provided. We can have only one of:
        # protein, goid
        if protein is not None:
            url += "protein=" + protein
        elif goid is not None:
            url += "goid=" + goid
        elif tax is not None:
            url += "tax=" + tax

        #need to check that there are mutualy exclusive
        if goid is None and protein is None and tax is None:
            raise ValueError("you must provide at least one of the following parameter: goid, protein")

        # aspect parameter
        if aspect is not None:
            self.devtools.check_param_in_list(aspect, _valid_aspect)
            params['aspect'] = aspect

        # aspect parameter
        if termUse is not None:
            self.devtools.check_param_in_list(termUse, ["slim"])
            params['termUse'] = termUse

        if relType:
            raise NotImplementedError

        if q:
            raise NotImplementedError

        if evidence:
            if isinstance(evidence,list):
                evidence = ",".join([x.strip() for x in evidence])
            elif isinstance(evidence,str):
                pass
            else:
                raise ValueError("""
Invalid parameter: evidence parameters must be a list of strings ['IDA','IEA']
or a string (e.g., 'IDA', 'IDA,IEA') """)
            params['evidence'] = evidence

        if source:
            if isinstance(source, list):
                source = ",".join([x.strip() for x in source])
            elif isinstance(source, str):
                pass
            else:
                raise ValueError("""
Invalid parameter: source parameters must be a list of strings ['UniProtKB']
or a string (e.g., 'UniProtKB') """)
            params['source'] = source

        if ref:
            if isinstance(ref, list):
                ref = ",".join([x.strip() for x in ref])
            elif isinstance(ref, str):
                pass
            else:
                raise ValueError("""
Invalid parameter: source parameters must be a list of strings ['PUBMED']
or a string (e.g., 'PUBMED:*') """)
            params['ref'] = ref

        if qualifier:
            #NOT, colocalizes_with, contributes_to
            if isinstance(qualifier, list):
                qualifier = ",".join([x.strip() for x in qualifier])
            elif isinstance(qualifier, str):
                pass
            params['qualifier'] = qualifier

        # col parameter
        if frmt == "tsv":
            if col is None:
                col = 'proteinDB,proteinID,proteinSymbol,qualifier,'
                col += 'goID,goName,aspect,evidence,ref,with,proteinTaxon,'
                col += 'date,from,splice,proteinName,proteinSynonym,proteinType,'
                col += 'proteinTaxonName,originalTermID,originalGOName'
            else:
                col = ",".join([x.strip() for x in col.split(",")])

            for c in col.split(','):
                self.devtools.check_param_in_list(c, self._valid_col)
            params["col"] = col

        if frmt not in ["tsv", "dict"]:
            # col is provided but format is not appropriate
            if col is not None:
                raise ValueError("You provided the 'col' parameter but the format is not correct. You should use the frmt='tsv' or frmt='dict' ")

        # gz parameter. do not expect values so need to be added afterwards.
        if gz is True:
            url += '&gz'

        res = self.http_get(url, frmt="txt", params=params)

        return res

    def Annotation_from_goid(self, goid, **kargs):
        """Returns a DataFrame containing annotation on a given GO identifier

        :param str protein: a GO identifier
        :return: all outputs are stored into a Pandas.DataFrame data structure.

        All parameters from :math:`Annotation` are also valid except **format** that
        is set to **tsv**  and cols that is made of all possible column names.

        """
        kargs["frmt"] = "tsv"
        cols = ",".join (self._valid_col)
        kargs['col'] = cols

        data = self.Annotation(goid=goid, **kargs)
        data = data.strip().split("\n")[1:]
        res = {}
        for c in cols.split(","):
            res[c] = []

        for entry in data:
            values = entry.split("\t")
            for k, v in zip(cols.split(","), values):
                res[k].append(v)
        try:
            import pandas as pd
            return pd.DataFrame(res)
        except:
            self.logging.warning("Cannot return a DataFrame. Returns the list. If you want the dataframe, install pandas library")
            return res

    def Annotation_from_protein(self, protein, **kargs):
        """Returns a DataFrame containing annotation on a given protein

        :param str protein: a protein name
        :return: all outputs are stored into a Pandas.DataFrame data structure.

        All parameters from :math:`Annotation` are also valid except **format** that
        is set to **tsv**  and cols that is made of all possible column names.

        """
        kargs["frmt"] = "tsv"
        cols = ",".join (self._valid_col)
        kargs['col'] = cols

        data = self.Annotation(protein=protein, **kargs)
        data = data.strip().split("\n")[1:]
        res = {}
        for c in cols.split(","):
            res[c] = []

        for entry in data:
            values = entry.split("\t")
            for k, v in zip(cols.split(","), values):
                res[k].append(v)
        try:
            import pandas as pd
            return pd.DataFrame(res)
        except:
            self.logging.warning("Cannot return a DAtaFrame. Returns the list")
            return res



class GeneOntology():
    """


    Given a list of GO terms, read them with QuickGO and convert them to a database.

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
        return self._quickgo.Term(goid, frmt="obo")


