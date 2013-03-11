# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#      https://www.assembla.com/spaces/bioservices/team
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id: $
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

from bioservices.services import RESTService

__all__ = ["QuickGO"]

class QuickGO(RESTService):
    """Interface to the `QuickGO <http://www.ebi.ac.uk/QuickGO/WebServices.html>`_ service

    .. doctest::

        >>> from bioservices import QuickGO
        >>> s = QuickGO()
        >>> res = s.Term("GO:0003824")

    """
    _goid_example = "GO:0003824"

    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages.

        """
        super(QuickGO, self).__init__(url="http://www.ebi.ac.uk/QuickGO",
            name="quickGO", verbose=verbose)

    def Term(self, GOid, format="oboxml"):
        """Obtain Term information


        :param str format: the output format (mini, obo, oboxml).

        The format can be:

        * mini:   Mini HTML, suitable for dynamically embedding in popup boxes.
        * obo:    OBO format snippet.
        * oboxml: OBO XML format snippet.

        ::

            from bioservices import QuickGO
            s = QuickGO()
            s.Term("GO:0003824")


        """
        _valid_formats = ["mini", "obo", "oboxml"]
        if GOid.startswith("GO:")==False:
            raise ValueError("GO id must start with 'GO:'")

        if format not in _valid_formats:
            raise ValueError("format provided is incorrect. Choose in %s" % _valid_formats)

        url = self.url + "/GTerm?id=" + GOid
        #GO:0003824
        params = {'format':format}
        postData = self.urlencode(params)
        url += "&" + postData

        if format in ["oboxml"]:
            res = self.request(url, format="xml")
        else:
            res = self.request(url, format=format)

        return res



    def Annotation(self, goid=None, protein=None, format="gaf", limit=10000,
        gz=False, col=None, db=None, aspect=None, relType=None, termUse=None,
        evidence=None, source=None, ref=None,  tax=None, qualifier=None, q=None, _with=None):
        """Calling the Annotation service

        Mutual exclusive parameters are goid, protein

        :param int limit: download limit (number of lines) (default 10,000 rows,
            which may not be sufficient for the data set that you are
            downloading. To bypass this default, and return the entire data set,
            specify a limit of -1).
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
        :param evidence: annotation evidence code category (Ev). Example of
            valid evidence are: be IDA, IC, ISS, IEA, IPI, ND, IMP, ISO, IGI
            should be either a string with comma separated values (e.g.,
            IEA,IDA) or a list of strings (e.g. ["IEA","IDA"]).
        :param source: annotation provider. Examples are 'InterPro', 'UniPathway',
            'MGI', 'FlyBase', 'GOC', 'Source', 'UniProtKB', 'RGD', 'ENSEMBL',
            'ZFIN', 'IntAct'.
        :param ref: PubMed or GO reference supporting annotation. Can refer to a
            specific reference identifier or category (for category level, use
            `*`  after ref type). Can be 'PUBMED:`*`', 'GO_REF:0000002'.
        :param with: additional supporting information supplied in IEA, ISS, IPI, IC
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

            >>> print s.Annotation(protein='P12345', format='tsv', col="ref,evidence",
            ... ref='PMID:*')
            >>> print s.Annotation(protein='P12345,Q4VCS5', format='tsv', 
            ...     col="ref,evidence",ref='PMID:,Reactome:')



        """
        _valid_formats = ["gaf", "gene2go", "proteinList", "fasta", "tsv"]
        _valid_col = ['proteinDB', 'proteinID', 'proteinSymbol', 'qualifier',
            'goID', 'goName', 'aspect', 'evidence', 'ref', 'with', 'proteinTaxon',
            'date', 'from', 'splice', 'proteinName', 'proteinSynonym', 'proteinType',
            'proteinTaxonName', 'originalTermID', 'originalGOName']
        _valid_db = ['UniProtKB', 'UniGene', 'Ensembl']
        _valid_aspect = ['P', 'F', 'C']

        if isinstance(limit, int)==False:
            raise TypeError("limit parameter must be an integer greater than zero")

        # fill params with parameters that have default values.
        params = {'format':format, 'limit':limit}

        # beginning of the URL
        url = self.url + "/GAnnotation?"

        # what is the ID being provided. We can have only one of:
        # protein, goid
        if protein != None:
            url += "protein=" + protein
        elif goid != None:
            url += "goid=" + goid
        elif tax != None:
            url += "tax=" + tax

        #need to check that there are mutualy exclusive
        if goid==None and protein==None and tax==None:
             raise ValueError("you must provide at least one of the following parameter: goid, protein")

        # aspect parameter
        if aspect != None:
            if aspect not in _valid_aspect:
                 raise ValueError("Invalid aspect (%s) must be in %s" % (aspect, _valid_aspect))
            params['aspect'] = aspect

        # aspect parameter
        if termUse != None:
            self.checkParam(termUse, ["slim"])
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
        if format=="tsv":
            if col == None:
                col = 'proteinDB,proteinID,proteinSymbol,qualifier,'
                col += 'goID,goName,aspect,evidence,ref,with,proteinTaxon,date,from,splice'
            for c in col.split(','):
                if c not in _valid_col:
                    raise ValueError("col parameter error: found %s, which is not a valid value." % c)
            params["col"] = col
        if format!="tsv":
            # col is provided but format is not appropriate
            if col!= None:
                raise ValueError("You provided the 'col' parameter but the format is not correct. You should use the 'format=tsv")

        postData = "&" + self.urlencode(params)

        # gz parameter. do not expect values so need to be added afterwards.
        if gz==True:
            url+='&gz'

        url += postData
        res = self.request(url, format="txt")
        return res




