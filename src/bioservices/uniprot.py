#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to some part of the UniProt web service

.. topic:: What is UniProt ?

    :URL: http://www.uniprot.org
    :Citation:

    .. highlights::

        "The Universal Protein Resource (UniProt) is a comprehensive resource for protein
        sequence and annotation data. The UniProt databases are the UniProt
        Knowledgebase (UniProtKB), the UniProt Reference Clusters (UniRef), and the
        UniProt Archive (UniParc). The UniProt Metagenomic and Environmental Sequences
        (UniMES) database is a repository specifically developed for metagenomic and
        environmental data."

        -- From Uniprot web site (help/about) , Dec 2012


.. mapping between uniprot and bunch of other DBs.
.. ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/
.. http://www.uniprot.org/docs/speclist
.. http://www.uniprot.org/docs/pkinfam

"""
import io
import time
import urllib
import json

import pandas as pd

from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["UniProt"]


class UniProt:
    """Interface to the `UniProt <http://www.uniprot.org>`_ service

    ::

        >>> from bioservices import UniProt
        >>> u = UniProt(verbose=False)
        >>> u.mapping("UniProtKB_AC-ID", "KEGG", query='P43403')
        defaultdict(<type 'list'>, {'P43403': ['hsa:7535']})
        >>> res = u.search("P43403")

        # Returns sequence on the ZAP70_HUMAN accession Id
        >>> sequence = u.search("ZAP70_HUMAN", columns="sequence")


    .. versionchanged:: 1.10 
    
        Uniprot update its service in June 2022. Changes were made in the bioservices
        API with small changes. User API is more or less the same. Main issues that may 
        be faced are related to change of output column names. Please see the 
        :attr:`_legacy_names` for corresponding changes.

        Some notes about searches. The *and* and *or* are now upper cases. 
        The *organism* and *taxonomy* fields are now *organism_id* and *taxonomy_id*


    """

    # June 2022, API changes and these labels changed:
    _legacy_names = {
        'id': 'accession',
        'entry name': 'id',
        'genes': 'gene_names',
        'genes(PREFERRED)':	'gene_primary',
        'genes(ALTERNATIVE)': 'gene_synonym',
        'genes(OLN)': 'gene_oln',
        'genes(ORF)':	'gene_orf',
        'organism':	'organism_name',
        'organism-id':	'organism_id',
        'protein names':	'protein_name',
        'proteome':	'xref_proteomes',
        'lineage(ALL)':	'lineage',
        'virus hosts':	'virus_hosts',

        'comment(ALTERNATIVE PRODUCTS)': 'cc_alternative_products',
        'feature(ALTERNATIVE SEQUENCE)': 'ft_var_seq',
        'comment(ERRONEOUS GENE MODEL PREDICTION)': 'error_gmodel_pred',
        'fragment': 'fragment',
        'encodedon': 'organelle',
        'length': 'length',
        'mass': 'mass',
        'comment(MASS SPECTROMETRY)': 'cc_mass_spectrometry',
        'feature(NATURAL VARIANT)': 'ft_variant',
        'feature(NON ADJACENT RESIDUES)': 'ft_non_cons',
        'feature(NON STANDARD RESIDUE)': 'ft_non_std',
        'feature(NON TERMINAL RESIDUE)': 'ft_non_ter',
        'comment(POLYMORPHISM)': 'cc_polymorphism',
        'comment(RNA EDITING)': 'cc_rna_editing',
        'sequence': 'sequence',
        'comment(SEQUENCE CAUTION)': 'cc_sequence_caution',
        'feature(SEQUENCE CONFLICT)': 'ft_conflict',
        'feature(SEQUENCE UNCERTAINTY)': 'ft_unsure',
        'version(sequence)': 'sequence_version',

        # function
        'comment(ABSORPTION)': 'absorption',
        'feature(ACTIVE SITE)': 'ft_act_site',
        'comment(ACTIVITY REGULATION)': 'cc_activity_regulation',
        'feature(BINDING SITE)': 'ft_binding',
        'chebi': 'ft_ca_bind',
        'chebi(Catalytic activity)': 'cc_catalytic_activity',
        'chebi(Cofactor)': 'cc_cofactor',
        'feature(DNA BINDING)': 'ft_dna_bind',
        'ec': 'ec',
        'comment(FUNCTION)': 'cc_function',
        'comment(KINETICS)': 'kinetics',
        'feature(METAL BINDING)': 'ft_metal',
        'feature(NP BIND)': 'ft_np_bind',
        'comment(PATHWAY)': 'cc_pathway',
        'comment(PH DEPENDENCE)': 'ph_dependence',
        'comment(REDOX POTENTIAL)': 'redox_potential',
        'rhea-id': 'rhea_id',
        'feature(SITE)': 'ft_site',
        'comment(TEMPERATURE DEPENDENCE)': 'temp_dependence',

        # misc
        'annotation score': 'annotation_score',
        'comment(CAUTION)': 'cc_caution',
        'features': 'feature',
        'keyword-id': 'keywordid',
        'keywords': 'keyword',
        'comment(MISCELLANEOUS)': 'cc_miscellaneous',
        'existence': 'protein_existence',
        'reviewed': 'reviewed',
        'tools': 'tools',
        'uniparcid': 'uniparc_id',

        # Interaction =============================
        "interactor": "cc_interaction",
        "comment(SUBUNIT)": "cc_subunit",

        # GO
        "go": "go",
        "go(biological process)": "go_p",
        "go(cellular component)": "go_c",
        "go(molecular function)": "go_f",
        "go-id": "go_id",

        # Date of
        "created": "date_created",
        "last-modified": "date_modified",
        "sequence-modified": "date_sequence_modified",
        "version(entry)": "version",
        # STRUCTURE
        "3d": "structure_3d",
        "feature(BETA STRAND)": "ft_strand",
        "feature(HELIX)": "ft_helix",
        "feature(TURN)": "ft_turn",

        # subcellular function
        "comment(SUBCELLULAR LOCATION)":"cc_subcellular_location",
        "feature(INTRAMEMBRANE)":"ft_intramem",
        "feature(TOPOLOGICAL DOMAIN)":"ft_topo_dom",
        "feature(TRANSMEMBRANE)": "ft_transmem",

        # Pathology
        'comment(ALLERGEN)': 'cc_allergen',
        'comment(BIOTECHNOLOGY)': 'cc_biotechnology',
        'comment(DISRUPTION PHENOTYPE)': 'cc_disruption_phenotype',
        'comment(DISEASE)': 'cc_disease',
        'feature(MUTAGENESIS)': 'ft_mutagen',
        'comment(PHARMACEUTICAL)': 'cc_pharmaceutical',
        'comment(TOXIC DOSE)': 'cc_toxic_dose',

        # PTM
        'feature(CHAIN)': 'ft_chain',
        'feature(CROSS LINK)': 'ft_crosslnk',
        'feature(DISULFIDE BOND)': 'ft_disulfid',
        'feature(GLYCOSYLATION)': 'ft_carbohyd',
        'feature(INITIATOR METHIONINE)': 'ft_init_met',
        'feature(LIPIDATION)': 'ft_lipid',
        'feature(MODIFIED RESIDUE)': 'ft_mod_res',
        'feature(PEPTIDE)': 'ft_peptide',
        'comment(PTM)': 'cc_ptm',
        'feature(PROPEPTIDE)': 'ft_propep',
        'feature(SIGNAL)': 'ft_signal',
        'feature(TRANSIT)': 'ft_transit',

        # Family domains
        'feature(COILED COIL)': 'ft_coiled',
        'feature(COMPOSITIONAL BIAS)': 'ft_compbias',
        'comment(DOMAIN)': 'cc_domain',
        'feature(DOMAIN EXTENT)': 'ft_domain',
        'feature(MOTIF)': 'ft_motif',
        'families': 'protein_families',
        'feature(REGION)': 'ft_region',
        'feature(REPEAT)': 'ft_repeat',
        'comment(SIMILARITY)': '<does not exist>',
        'feature(ZINC FINGER)': 'ft_zn_fing',

    }

    _valid_columns = [
        # Names & Taxonomy ================================================
        "accession",
        "id",
        "gene_names",
        "gene_primary",
        "gene_synonym",
        "gene_oln",
        "gene_orf",
        "organism_name",
        "organism_id",
        "protein_name",
        "xref_proteomes",
        "lineage",
        "virus_hosts",

        # Sequences ========================================================
        "fragment",
        "sequence",
        "length",
        "mass",
        "organelle",
        "cc_alternative_products",
        "error_gmodel_pred",
        "cc_mass_spectrometry",
        "cc_polymorphism",
        "cc_rna_editing",
        "cc_sequence_caution",
        "ft_var_seq",
        "ft_variant",
        "ft_non_cons",
        "ft_non_std",
        "ft_non_ter",
        "ft_conflict",
        "ft_unsure",
        "sequence_version",
        
        # Family and Domains ========================================
        'ft_coiled',
        'ft_compbias',
        'cc_domain',
        'ft_domain',
        'ft_motif',
        'protein_families',
        'ft_region',
        'ft_repeat',
        'ft_zn_fing',

        # Function ===================================================
        'absorption',
        'ft_act_site',
        'cc_activity_regulation',
        'ft_binding',
        'ft_ca_bind',
        'cc_catalytic_activity',
        'cc_cofactor',
        'ft_dna_bind',
        'ec',
        'cc_function',
        'kinetics',
        'ft_metal',
        'ft_np_bind',
        'cc_pathway',
        'ph_dependence',
        'redox_potential',
        #'rhea_id',
        'ft_site',
        'temp_dependence',

        # Gene Ontology ==================================
        "go",
        "go_p",
        "go_f",
        "go_c",
        "go_id",

        # Interaction ======================================
        "cc_interaction",
        "cc_subunit",

        # EXPRESSION =======================================
        "cc_developmental_stage",
        "cc_induction",
        "cc_tissue_specificity",

        # Publications
        "lit_pubmed_id",
        
        # Date of
        "date_created",
        "date_modified",
        "date_sequence_modified",
        "version",

        # Structure
        "structure_3d",
        "ft_strand",
        "ft_helix",
        "ft_turn",

        # Subcellular location
        "cc_subcellular_location",
        "ft_intramem",
        "ft_topo_dom",
        "ft_transmem",

        # Miscellaneous ==========================
        "annotation_score",
        "cc_caution",
        "comment_count",
        #"feature",
        "feature_count",
        "keyword",
        "keywordid",
        "cc_miscellaneous",
        "protein_existence",
        "tools",
        "reviewed",
        "uniparc_id",
        
        # Pathology
        'cc_allergen',
        'cc_biotechnology',
        'cc_disruption_phenotype',
        'cc_disease',
        'ft_mutagen',
        'cc_pharmaceutical',
        'cc_toxic_dose',

        # PTM / Processsing
        'ft_chain',
        'ft_crosslnk',
        'ft_disulfid',
        'ft_carbohyd',
        'ft_init_met',
        'ft_lipid',
        'ft_mod_res',
        'ft_peptide',
        'cc_ptm',
        'ft_propep',
        'ft_signal',
        'ft_transit',

        # not documented
        'xref_pdb'
    ]
    _url = "https://rest.uniprot.org"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        :param cache: set to True to cache request
        """

        self.services = REST(name="UniProt", url=UniProt._url, verbose=verbose, cache=cache, url_defined_later=True)

        self.TIMEOUT = 100
        self._valid_mapping = None
        self._database = "uniprot"

    def _download_flat_files(self, output="uniprot_sprot.dat.gz"): #pragma: no cover
        """could be used to get all data in flat files (about compressed 500Mb )"""
        # deprecated in v1.10 due to API change in uniprot
        url = "ftp://ftp.ebi.ac.uk/pub/databases/uniprot/knowledgebase/uniprot_sprot.dat.gz"
        self.services.logging.info("Downloading uniprot file from the web. May take some time.:")
        urllib.request.urlretrieve(url, output)

    def _get_valid_mapping(self):
        if not self._valid_mapping:
            self._set_valid_mapping()
        return self._valid_mapping

    def _set_valid_mapping(self):
        fields = self.services.http_get("configure/idmapping/fields")
        groups = fields["groups"]
        rules = {}
        for item in fields["rules"]:
            ID = item['ruleId']
            rules[ID] = item

        # This is suppose to be a set of database name available in Uniprot 
        from_to = {}
        for item in [x for group in groups for x in group['items']]:
            # should be name, not DisplayName
            name = item['name']
            if item['from']:
                tos = rules[item['ruleId']]['tos']
                from_to[name] = tos

        self._valid_mapping = from_to
    
    valid_mapping = property(_get_valid_mapping, _set_valid_mapping)

    def mapping(self, fr="UniProtKB_AC-ID", to="KEGG", query="P13368", polling_interval_seconds=3, max_waiting_time=100):
        """This is an interface to the UniProt mapping service

        :param fr: the source database identifier. See :attr:`valid_mapping`.
        :param to: the targetted database identifier. See :attr:`valid_mapping`.
        :param query: a string containing one or more IDs separated by a space
            It can also be a list of strings.
        :param polling_interval_seconds: the number of seconds between each status check of the current job
        :param max_waiting_time: the maximum number of seconds to wait for the final answer.
        :return: a dictionary with two possible keys. The first one is 'results' 
            with the from / to answers and the second one 'failedIds' with Ids that were not found

        ::

            >>> u.mapping("UniProtKB_AC-ID", "KEGG", 'P43403')
            {'results': [{'from': 'P43403', 'to': 'hsa:7535'}]}

        The output is a dictionary. Identifiers that were not found are stored in the keys 
        'failedIds'. Succesful queries are stored in the 'results' key that is a list
        of dictionaries with two keys set to 'from' and 'to'. The 'from' key should be in your input list.
        The 'to' key is the result. Here we have the KEGG identifier recognised by its prefix 'hsa:', which is for human. 
        Sometimes the output ('to') it is more complicated. Consider the following  example::

            u.mapping("UniParc", "UniProtKB", 'UPI0000000001,UPI0000000002')

        You will see that the UniParc results is more complex than just an identifier.

        See :attr:`valid_mapping` attribut for list of valid mapping identifiers.

        Note that according to Uniprot (June 2022), there are various limits on ID Mapping Job Submission:

        ========= =====================================================================================
        Limit	  Details     
        ========= =====================================================================================
        100,000	  Total number of ids allowed in comma separated param ids in /idmapping/run api
        500,000	  Total number of "mapped to" ids allowed
        100,000	  Total number of "mapped to" ids allowed to be enriched by UniProt data
        10,000	  Total number of "mapped to" ids allowed with filtering
        ========= =====================================================================================

        .. versionchanged:: 1.1.1 to return a dictionary instaed of a list
        .. versionchanged:: 1.1.2 the values for each key is now made of a list
            instead of strings so as to store more than one values.
        .. versionchanged:: 1.2.0 input query can also be a list of strings
            instead of just a string
        .. versionchanged:: 1.3.1:: use http_post instead of http_get. This is 3 times
            faster and allows queries with more than 600 entries in one go.
        .. version 1.10.0:: new API due to  uniprot website update
        """

        if isinstance(query, (list, tuple)):
            query = ",".join(query)
        elif isinstance(query,str):
            pass

        # First, we call the real mapping request
        params = {"from": fr, "to": to, "ids": query}

        job = self.services.http_post("idmapping/run", frmt="json", data=params)
        try:
            job_id = job['jobId']
        except TypeError:
             logger.error(self.services.last_response.content.decode())
             return

        # the job id will tell us about the job status 
        results = None
        waiting_time = 0
        while not results and waiting_time < max_waiting_time:   
            logger.info("Waiting for {job_id} to complete")         
            results = self.services.http_get(f"idmapping/status/{job_id}", frmt="json")
            if results != 500 and 'results' in results:
                return results
            else: #pragma: no cover
                time.sleep(polling_interval_seconds)
                results = None
            waiting_time += polling_interval_seconds

    def retrieve(self, uniprot_id, frmt="json", database="uniprot", include=False):
        """Search for a uniprot ID in UniProtKB database

        :param str uniprot: a valid UniProtKB ID, or uniref, uniparc or taxonomy. 
        :param str frmt: expected output format amongst xml, txt, fasta, gff, rdf
        :param str database:  database name in (uniprot, uniparc, uniref, taxonomy)
        :param bool include: include data with RDF format.
        :return: if the parameter uniprot_id is string, the output will be a a list of identifiers is provided, the output is also a list
            otherwise, a string. The content of the string of items in the list
            depends on the value of **frmt**.

        ::

            >>> u = UniProt()
            >>> res = u.retrieve("P09958", frmt="txt")
            >>> fasta = u.retrieve(['P29317', 'Q5BKX8', 'Q8TCD6'], frmt='fasta')
            >>> print(fasta[0])


        .. versionchanged:: 1.10 the xml format is now returned as raw XML. It is not
            interpreted anymore. The RDF has now an additional option to include data 
            from referenced data sets directly in the returned data (set include=True parameter).
            Default output format is now set to json. 
        """
        if database == 'uniprot': 
            if frmt not in ("txt", "xml", "rdf", "gff", "fasta", "json"):#pragma: no cover
                self.services.logging.warning("frmt must be set to one of: txt, xml, rdf, gff, fasta, json.")
        elif database == 'uniparc':
            if frmt not in ( "xml", "rdf", "fasta", 'tsv', 'json'): #pragma: no cover
                raise ValueError("frmt must be set to one of: tsv, xml, rdf, gff, fasta, json")
                self.services.logging.warning("frmt must be set to one of: txt, xml, rdf, gff, fasta.")
        elif database == 'uniref':
            if frmt not in ("xml", "rdf", "fasta", 'tsv', 'json'): #pragma: no cover
                self.services.logging.warning("frmt must be set to one of: xml, rdf, gff, fasta, json.")
        elif database == "taxonomy":
            pass
        else: #pragma: no cover
            self.services.logging.warning("database must be set to uniref, uniparc, uniprot or taxonomy")


        if isinstance(uniprot_id, str):
            queries = uniprot_id.split(",")
        else:
            queries = uniprot_id
        #queries = self.services.devtools.to_list(uniprot_id)

        # some magic here not documented on uniprot website...but multiple queries are possible
        url = [database + "/" + query + "." + frmt for query in queries]

        # the frmt=txt here is for the requests, nothing related to the uniprot format
        res = self.services.http_get(url, frmt="txt", params={'include':include})
        if frmt == 'json':
            for i, x in enumerate(res):
                try:
                    res[i] = json.loads(x)
                except:
                    pass

        if isinstance(res, list) and len(res) == 1:
            res = res[0]
        return res

    def get_fasta(self, uniprot_id):
        """Returns FASTA string given a valid identifier

        :param str uniprot_id: a valid identifier (e.g. P12345)

        This is just an alias to :meth:`retrieve` when setting the format to 'fasta'. 
        Method kept for legacy.

        """
        res = self.retrieve(uniprot_id, frmt='fasta')
        return res

    def search(
        self,
        query,
        frmt="tsv",
        columns=None,
        include_isoforms=False,
        sort="score",
        compress=False,
        limit=None,
        offset=None,
        maxTrials=10,
        database="uniprotkb",
    ):
        """Provide some interface to the uniprot search interface.

        :param str query: query must be a valid uniprot query.
            See https://www.uniprot.org/help/query-fields and examples below
        :param str frmt: a valid format amongst html, tab, xls, asta, gff,
            txt, xml, rdf, list, rss. If tab or xls, you can also provide the
            columns argument.  (default is tab)
        :param str columns: comma-separated list of values. Works only if fomat
            is tsv or xls. For UnitProtKB, some possible columns are:
            id, entry name, length, organism. 
            See also :attr:`~bioservices.uniprot.UniProt.valid_mapping`
            for the full list of column keywords.
        :param bool include_isoform: include isoform sequences when the frmt
            parameter is fasta. Include description when frmt is rdf.
        :param str sort: by score by default. Set to None to bypass this behaviour
        :param bool compress: gzip the results
        :param int limit: Maximum number of results to retrieve.
        :param int offset:  Offset of the first result, typically used together
            with the limit parameter.
        :param int maxTrials: this request is unstable, so we may want to try
            several time.

        To obtain the list of uniprot ID returned by the search of zap70 can be
        retrieved as follows::

            >>> u.search('zap70+AND+organism_id:9606')
            >>> u.search("zap70+AND+taxonomy_id:9606", frmt="tsv", limit=3,
            ...    columns="entry_name,length,id, gene_names")
            Entry name  Length  Entry   Gene names
            CBLB_HUMAN  982 Q13191  CBLB RNF56 Nbla00127
            CBL_HUMAN   906 P22681  CBL CBL2 RNF55
            CD3Z_HUMAN  164 P20963  CD247 CD3Z T3Z TCRZ

        other examples::

            >>> u.search("ZAP70+AND+organism_id:9606", limit=3, columns="id,xref_pdb")

        You can also do a search on several keywords. This is especially useful
        if you have a list of known entry names.::

            >>> u.search("ZAP70_HUMAN+OR+CBL_HUMAN", frmt="tsv", limit=3,
            ...    columns="entry name,length,id, genes")
            Entry name  Length  Entry   Gene names


        Finally, note that when you search for a query, you may have several hits::

            >>> u.search("P12345)

        including the ID P12345 but also related entries. If you 
        need only the entry that perfectly match the query, use::

            >>> u.search("accession:P12345")

        This was provided from a user issue that was solved here:
        https://github.com/cokelaer/bioservices/issues/122


        .. warning:: some columns although valid may not return anything, not even in
            the header: 'score', 'taxonomy', 'tools'. this is a uniprot feature,
            not bioservices.

        .. versionchanged:: 1.10 
        
            Due to uniprot API changes in June 2022:

            * parameter 'include' is not named 'include_isoform
            * default parameter 'tab' is now 'tsv' but does not change the results

        """
        params = {}

        if frmt is not None:
            _valid_formats = [
                "xls",
                "fasta",
                "gff",
                "txt",
                "tsv",
                "xml",
                "rss",
                "list",
                "rss",
                "html",
            ]
            self.services.devtools.check_param_in_list(frmt, _valid_formats)
            params["format"] = frmt

        if columns is not None:
            self.services.devtools.check_param_in_list(frmt, ["tsv", "xls"])

            # remove unneeded spaces before/after commas if any
            if "," in columns:
                columns = [x.strip() for x in columns.split(",")]
            else:
                columns = [columns]


            # convert back to a string as expected by uniprot
            params["fields"] = ",".join([x.strip() for x in columns])

        if include_isoforms is True and frmt in ["fasta", "rdf"]:
            params["includeIsoform"] = "yes"

        if compress is True:
            params["compress"] = "yes"

        if sort:
            self.services.devtools.check_param_in_list(sort, ["score"])
            params["sort"] = sort

        if offset is not None:
            #if isinstance(offset, int):
            params["cursor"] = offset

        if limit is not None:
            if isinstance(limit, int):
                params["size"] = limit

        # + are interpreted and have a meaning. See arrayexpress module for details

        query = query.replace("+", " ")
        params['query'] = query
        del params['sort']

        res = self.services.http_get(f"{database}/search", frmt="txt", params=params)
        return res

    def quick_search(self, query, include_isoforms=False, sort="score", limit=None):
        """a specialised version of :meth:`search`

        This is equivalent to::

            u = uniprot.UniProt()
            u.search(query, frmt='tsv', sort="score", limit=None)

        :returns: a dictionary.

        """
        res = self.search(query, "tsv", include_isoforms=include_isoforms, 
            sort=sort, limit=limit)

        # if empty result, nothing to do
        if res and len(res) == 0:
            return res

        # else populate a dictionary
        newres = {}
        for line in res.split("\n")[1:-1]:
            # print line
            Entry, a, b, c, d, e, f = line.split("\t")
            # print Entry, a, b, c, d, e, f
            newres[Entry] = {
                "Entry name": a,
                "Status": b,
                "Protein names": c,
                "Gene names": d,
                "Organism": e,
                "Length": f,
            }
        return newres

    def uniref(self, query):
        """Calls UniRef service

        This is an alias to :meth:`retrieve`
        ::

            >>> u = UniProt()
            >>> u.uniref("Q03063")

        Another example from https://github.com/cokelaer/bioservices/issues/121
        is the combination of uniprot and uniref filters::

            u.uniref("uniprot:(ec:1.1.1.282 taxonomy_name:bacteria reviewed:true)")

        .. versionchanged:: 1.10 due to uniprot API changes in June 2022, 
            we now return a json instead of a pandas dataframe.
        """
        res = self.services.http_get(
            f"uniref/UniRef90_{query}.json", frmt="json"
        )
        return res

    def get_df(self, entries, nChunk=100, organism=None, limit=10):
        """Given a list of uniprot entries, this method returns a dataframe with all possible columns


        :param entries: list of valid entry name. if list is too large (about
            >200), you need to split the list
        :param chunk:
        :param limit: limit number of entries per identifier to 10. You can
            set it to None to keep all entries but this will be very slow
        :return: dataframe with indices being the uniprot id (e.g. DIG1_YEAST)

        """
        if isinstance(entries, str):
            entries = [entries]
        else:
            entries = list(set(entries))
        output = pd.DataFrame()

        self.services.logging.info(
            "fetching information from uniprot for {} entries".format(len(entries))
        )

        if limit < len(entries):
            self.services.logging.warning("The limit paramter is less than the number of entries. Probably not what you want. set limit to the length of the entries to remove this message")

        nChunk = min(nChunk, len(entries))
        N, rest = divmod(len(entries), nChunk)
        for i in range(0, N + 1):
            this_entries = entries[i * nChunk : (i + 1) * nChunk]
            if len(this_entries):
                self.services.logging.info("uniprot.get_df {}/{}".format(i + 1, N))
                query = "+OR+".join(this_entries)
                if organism:
                    query += f"+AND+{organism}"

                res = self.search(
                    query,
                    frmt="tsv",
                    columns=",".join(self._valid_columns),
                    limit=limit,
                )
            else:
                break

            if len(res) == 0:
                self.services.logging.warning("some entries %s not found" % entries)
            else:
                df = pd.read_csv(io.StringIO(str(res)), sep="\t")

                if isinstance(output, type(None)):
                    output = df.copy()
                else:
                    output = output.append(df, ignore_index=True)

        # you may end up with duplicated...
        output.drop_duplicates(inplace=True)
        columns = [
            "lit_pubmed_id",
            "protein_families",
            "Gene names",
            "go",
            "go_ids",
            "interaction",
            "keyword",
        ]
        for col in columns:
            try:
                res = output[col].apply(
                    lambda x: [
                        this.strip() for this in str(x).split(";") if this != "nan"
                    ]
                )
                output[col] = res
            except:
                self.services.logging.warning("column could not be parsed. %s" % col)
        # Sequences are splitted into chunks of 10 characters. let us rmeove
        # the spaces:
        if "sequence" in output.columns:
            output["sequence"].fillna("", inplace=True)
            output.Sequence = output["sequence"].apply(lambda x: x.replace(" ", ""))

        return output
