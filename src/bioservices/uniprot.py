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
import types
import io

from bioservices.services import REST
try:
    import pandas as pd
except:
    print("pandas library is not installed. Not all functionalities will be  available")

__all__ = ["UniProt"]


# TODO:: falt files to get list of identifiers
# http://www.ebi.ac.uk/uniprot/database/download.html
# grep sp uniprot_sprot.fasta  | grep HUMAN | awk '{print substr($1, 12, length($1))}'

mapping = {"UniProtKB AC/ID":"ACC+ID",
    "UniProtKB": "ACC",
    "UniProtKB": "ID",
    "UniParc": "UPARC",
    "UniRef50": "NF50",
    "UniRef90": "NF90",
    "UniRef100": "NF100",
    "EMBL/GenBank/DDBJ": "EMBL_ID",
    "EMBL/GenBank/DDBJ CDS": "EMBL",
    "PIR": "PIR",
    "UniGene": "UNIGENE_ID",
    "Entrez Gene (GeneID)": "P_ENTREZGENEID",
    "GI number*":"P_GI",
    "IPI": "P_IPI",
    "RefSeq Protein": "P_REFSEQ_AC",
    "RefSeq Nucleotide": "REFSEQ_NT_ID",
    "PDB": "PDB_ID",
    "DisProt": "DISPROT_ID",
    "HSSP": "HSSP_ID",
    "DIP": "DIP_ID",
    "MINT": "MINT_ID",
    "Allergome": "ALLERGOME_ID",
    "MEROPS": "MEROPS_ID",
    "mycoCLAP": "MYCOCLAP_ID",
    "PeroxiBase": "PEROXIBASE_ID",
    "PptaseDB": "PPTASEDB_ID",
    "REBASE": "REBASE_ID",
    "TCDB": "TCDB_ID",
    "PhosSite": "PHOSSITE_ID",
    "DMDM": "DMDM_ID",
    "Aarhus/Ghent-2DPAGE": "AARHUS_GHENT_2DPAGE_ID",
    "World-2DPAGE": "WORLD_2DPAGE_ID",
    "DNASU": "DNASU_ID",
    "Ensembl": "ENSEMBL_ID",
    "Ensembl Protein": "ENSEMBL_PRO_ID",
    "Ensembl Transcript": "ENSEMBL_TRS_ID",
    "Ensembl Genomes": "ENSEMBLGENOME_ID",
    "Ensembl Genomes Protein": "ENSEMBLGENOME_PRO_ID",
    "Ensembl Genomes Transcript": "ENSEMBLGENOME_TRS_ID",
    "GeneID": "P_ENTREZGENEID",
    "GenomeReviews": "GENOMEREVIEWS_ID",
    "KEGG": "KEGG_ID",
    "PATRIC": "PATRIC_ID",
    "UCSC": "UCSC_ID",
    "VectorBase": "VECTORBASE_ID",
    "AGD": "AGD_ID",
    "ArachnoServer": "ARACHNOSERVER_ID",
    "CGD": "CGD",
    "ConoServer": "CONOSERVER_ID",
    "CYGD": "CYGD_ID",
    "dictyBase": "DICTYBASE_ID",
    "EchoBASE": "ECHOBASE_ID",
    "EcoGene": "ECOGENE_ID",
    "euHCVdb": "EUHCVDB_ID",
    "EuPathDB": "EUPATHDB_ID",
    "FlyBase": "FLYBASE_ID",
    "GeneCards": "GENECARDS_ID",
    "GeneFarm": "GENEFARM_ID",
    "GenoList": "GENOLIST_ID",
    "H-InvDB": "H_INVDB_ID",
    "HGNC": "HGNC_ID",
    "HPA": "HPA_ID",
    "LegioList": "LEGIOLIST_ID",
    "Leproma": "LEPROMA_ID",
    "MaizeGDB": "MAIZEGDB_ID",
    "MIM": "MIM_ID",
    "MGI": "MGI_ID",
    "neXtProt": "NEXTPROT_ID",
    "Orphanet": "ORPHANET_ID",
    "PharmGKB": "PHARMGKB_ID",
    "PomBase": "POMBASE_ID",
    "PseudoCAP": "PSEUDOCAP_ID",
    "RGD": "RGD_ID",
    "SGD": "SGD_ID",
    "TAIR": "TAIR_ID",
    "TubercuList": "TUBERCULIST_ID",
    "WormBase": "WORMBASE_ID",
    "WormBase Transcript": "WORMBASE_TRS_ID",
    "WormBase Protein": "WORMBASE_PRO_ID",
    "Xenbase": "XENBASE_ID",
    "ZFIN": "ZFIN_ID",
    "eggNOG": "EGGNOG_ID",
    "GeneTree": "GENETREE_ID",
    "HOGENOM": "HOGENOM_ID",
    "HOVERGEN": "HOVERGEN_ID",
    "KO": "KO_ID",
    "OMA": "OMA_ID",
    "OrthoDB": "ORTHODB_ID",
    "ProtClustDB": "PROTCLUSTDB_ID",
    "BioCyc": "BIOCYC_ID",
    "Reactome": "REACTOME_ID",
    "UniPathWay": "UNIPATHWAY_ID",
    "CleanEx": "CLEANEX_ID",
    "GermOnline": "GERMONLINE_ID",
    "ChEMBL": "CHEMBL_ID",
    "ChiTaRS": "CHITARS_ID",
    "DrugBank": "DRUGBANK_ID",
    "GenomeRNAi": "GENOMERNAI_ID",
    "NextBio": "NEXTBIO_ID"}



class UniProt(REST):
    """Interface to the `UniProt <http://www.uniprot.org>`_ service

    .. rubric:: Identifiers mapping between databases:

    ::

        >>> from bioservices import UniProt
        >>> u = UniProt(verbose=False)
        >>> u.mapping("ACC", "KEGG_ID", query='P43403')
        defaultdict(<type 'list'>, {'P43403': ['hsa:7535']})
        >>> res = u.search("P43403")

        # Returns sequence on the ZAP70_HUMAN accession Id
        >>> sequence = u.search("ZAP70_HUMAN", columns="sequence")

    """
    _mapping = mapping.copy()
    _url = "http://www.uniprot.org"
    _valid_columns = ['citation', 'clusters', 'comments', 'database',
                'domains','domain', 'ec', 'id', 'entry name', 'existence'
                'families', 'feature', 'features', 'genes', 'go', 'go-id', 'interpro'
                'interactor', 'keywords', 'keyword-id', 'last-modified',
                'length', 'organism', 'organism-id', 'pathway', 'protein names',
                'reviewed', 'score', 'sequence', '3d', 'subcellular locations',
                'taxonomy', 'tools', 'version', 'virus hosts', 'lineage-id',
                'sequence-modified', 'proteome']


    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(UniProt, self).__init__(name="UniProt", url=UniProt._url,
                verbose=verbose, cache=cache)
        self.TIMEOUT = 100

    def _download_flat_files(self):
        """could be used to get all data in flat files (about compressed 500Mb )"""
        url = "ftp://ftp.ebi.ac.uk/pub/databases/uniprot/knowledgebase/uniprot_sprot.dat.gz"
        self.logging.info('Downloading uniprot file from the web. May take some time.:')
        import urllib
        urllib.urlretrieve(url, 'uniprot_sprot.dat.gz')

    def mapping(self, fr="ID", to="KEGG_ID",  query="P13368"):
        """This is an interface to the UniProt mapping service

        :param fr: the source database identifier. See :attr:`_mapping`.
        :param to: the targetted database identifier. See :attr:`_mapping`.
        :param query: a string containing one or more IDs separated by a space
            It can also be a list of strings.
        :param format: The output being a dictionary, this parameter is
            deprecated and not used anymore
        :return: a list. The first element is the source database Id. The second
            is the targetted source identifier. Following elements are alternate
            of one the entry and its mapped Id. If a query has several mapped
            Ids, the query is repeated (see example with PDB mapping here below)
            e.g., ["From:ID", "to:PDB_ID", "P43403"]

        ::

            >>> u.mapping("ACC", "KEGG_ID", 'P43403')
            defaultdict(<type 'list'>, {'P43403': ['hsa:7535']})
            >>> u.mapping("ACC", "KEGG_ID", 'P43403 P00958')
            defaultdict(<type 'list'>, {'P00958': ['sce:YGR264C'], 'P43403': ['hsa:7535']})
            >>> u.mapping("ID", "PDB_ID", "P43403")
            defaultdict(<type 'list'>, {'P43403': ['1FBV', '1M61', '1U59',
            '2CBL', '2OQ1', '2OZO', '2Y1N', '3ZNI', '4A4B', '4A4C', '4K2R']})

        There is a web page that gives the list of correct `database identifiers
        <http://www.uniprot.org/faq/28>`_. You can also look at the
        :attr:`_mapping` attribute.

        :URL: http://www.uniprot.org/mapping/

        .. versionchanged:: 1.1.1 to return a dictionary instaed of a list
        .. versionchanged:: 1.1.2 the values for each key is now made of a list
            instead of strings so as to store more than one values.
        .. versionchanged:: 1.2.0 input query can also be a list of strings
            instead of just a string
        .. versionchanged:: 1.3.1:: use http_post instead of http_get. This is 3 times
            faster and allows queries with more than 600 entries in one go.
        """
        url = 'mapping/'  # the slash matters

        query = self.devtools.list2string(query, sep=" ", space=False)
        #if isinstance(query, list):
        #    query = " ".join(query)
        params = {'from':fr, 'to':to, 'format':"tab", 'query':query}
        result = self.http_post(url, frmt="txt", data=params)

        # changes in version 1.1.1 returns a dictionary instead of list
        try:
            result = result.split()
            del result[0]
            del result[0]
        except:
            self.logging.warning("Results seems empty...returning empty dictionary.")
            return {}

        if len(result) == 0:
            return {}
        else:
            # bug fix based on ticket #19 version 1.1.2
            # the default dict set empty list for all keys by default
            from collections import defaultdict
            result_dict = defaultdict(list)

            keys = result[0::2]
            values = result[1::2]
            for i, key in enumerate(keys):
                result_dict[key].append(values[i])
        return result_dict

    def searchUniProtId(self, uniprot_id, frmt="xml"):
        print("DEPRECATED SINCE VERSION 1.3.1. use retrieve instead")

    def retrieve(self, uniprot_id, frmt="xml"):
        """Search for a uniprot ID in UniProtKB database

        :param str uniprot: a valid UniProtKB ID or a list of identifiers.
        :param str frmt: expected output format amongst xml, txt, fasta, gff, rdf
        :return: is a list of identifiers is provided, the output is also a list
            otherwise, a string. The content of the string of items in the list
            depends on the value of **frmt**.

        ::

            >>> u = UniProt()
            >>> res = u.retrieve("P09958", frmt="xml")
            >>> fasta = u.retrieve([u'P29317', u'Q5BKX8', u'Q8TCD6'], frmt='fasta')
            >>> print(fasta[0])

        """
        _valid_formats = ['txt', 'xml', 'rdf', 'gff', 'fasta']
        self.devtools.check_param_in_list(frmt, _valid_formats)

        queries = self.devtools.to_list(uniprot_id)

        url = ["uniprot/" + query + '.' + frmt for query in queries]
        res = self.http_get(url, frmt="txt")
        if frmt == "xml":
            res = [self.easyXML(x) for x in res]
        if isinstance(res, list) and len(res) == 1:
            res = res[0]
        return res

    """def _batch(self, entries):
        #TODO test and validation
        entries = self.devtools.list2string(entries)
        res = self.http_post("batch/", frmt="txt",
                data={'format':'txt'},
                files={'file': entries}, headers={'Content_Type':'form-data'}  )
        return res
    """

    def get_fasta(self, id_):
        """Returns FASTA string given a valid identifier


        .. seealso:: :mod:`bioservices.apps.fasta` for dedicated tools to
            manipulate FASTA
        """
        from bioservices.apps.fasta import FASTA
        f = FASTA()
        f.load_fasta(id_)
        return f.fasta

    def get_fasta_sequence(self, id_):
        """Returns FASTA sequence (Not FASTA)

        :param str id_: Should be the entry name
        :return: returns fasta sequence (string)

        .. warning:: this is the sequence found in a fasta file, not the fasta
            content itself. The difference is that the header is removed and the
            formatting of end of lines every 60 characters is removed.

        """
        from bioservices.apps.fasta import FASTA
        f = FASTA()
        f.load_fasta(id_)
        return f.sequence

    def search(self, query, frmt="tab", columns=None,
            include=False,sort="score", compress=False, limit=None, offset=None, maxTrials=10):
        """Provide some interface to the uniprot search interface.

        :param str query: query must be a valid uniprot query.
            See http://www.uniprot.org/help/text-search, http://www.uniprot.org/help/query-fields
            See also example below
        :param str frmt: a valid format amongst html, tab, xls, asta, gff,
            txt, xml, rdf, list, rss. If tab or xls, you can also provide the
            columns argument.  (default is tab)
        :param str columns: comma-separated list of values. Works only if fomat
            is tab or xls. For UnitProtKB, some possible columns are:
            id, entry name, length, organism. Some column name must be followed by
            database name (e.g., "database(PDB)"). Again, see uniprot website
            for more details. See also :attr:`~bioservices.uniprot.UniProt._valid_columns`
            for the full list of column keyword.
        :param bool include: include isoform sequences when the frmt
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

            >>> u.search('zap70+AND+organism:9606', frmt='list')
            >>> u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3,
            ...    columns="entry name,length,id, genes")
            Entry name  Length  Entry   Gene names
            CBLB_HUMAN  982 Q13191  CBLB RNF56 Nbla00127
            CBL_HUMAN   906 P22681  CBL CBL2 RNF55
            CD3Z_HUMAN  164 P20963  CD247 CD3Z T3Z TCRZ

        other examples::

            >>> u.search("ZAP70+AND+organism:9606", limit=3, columns="id,database(PDB)")

        You can also do a search on several keywords. This is especially useful
        if you have a list of known entry names.::

            >>> u.search("ZAP70_HUMAN+or+CBL_HUMAN", frmt="tab", limit=3,
            ...    columns="entry name,length,id, genes")
            Entry name  Length  Entry   Gene names

        .. warning:: this function request seems a bit unstable (UniProt web issue ?)
            so we repeat the request if it fails

        .. warning:: some columns although valid may not return anything, not even in
            the header: 'score', 'taxonomy', 'tools'. this is a uniprot feature,
            not bioservices.
        """
        params = {}

        if frmt is not None:
            _valid_formats = ['tab', 'xls', 'fasta', 'gff', 'txt', 'xml', 'rss', 'list', 'rss', 'html']
            self.devtools.check_param_in_list(frmt, _valid_formats)
            params['format'] = frmt

        if columns is not None:
            self.devtools.check_param_in_list(frmt, ["tab","xls"])

            # remove unneeded spaces before/after commas if any
            if "," in columns:
                columns = [x.strip() for x in columns.split(",")]
            else:
                columns = [columns]

            for col in columns:
                if col.startswith("database(") is True:
                    pass
                else:
                    self.devtools.check_param_in_list(col, self._valid_columns)

            # convert back to a string as expected by uniprot
            params['columns'] = ",".join([x.strip() for x in columns])

        if include is True and frmt in ["fasta", "rdf"]:
            params['include'] = 'yes'

        if compress is True:
            params['compress'] = 'yes'

        if sort:
            self.devtools.check_param_in_list(sort, ["score"])
            params['sort'] = sort

        if offset is not None:
            if isinstance(offset, int):
                params['offset'] = offset

        if limit is not None:
            if isinstance(limit, int):
                params['limit'] = limit

        # + are interpreted and have a meaning.
        params['query'] = query.replace("+", " ")
        #res = s.request("/uniprot/?query=zap70+AND+organism:9606&format=xml", params)
        #print(params)
        res = self.http_get("uniprot/", frmt="txt", params=params)
        return res

    def quick_search(self, query, include=False,sort="score", limit=None):
        """a specialised version of :meth:`search`

        This is equivalent to::

            u = uniprot.UniProt()
            u.search(query, frmt="tab", include=False, sor="score", limit=None)

        :returns: a dictionary.

        """
        res = self.search(query, "tab", include=include, sort=sort, limit=limit)

        #if empty result, nothing to do
        if len(res) == 0:
            return res
        # else populate a dictionary
        newres = {}
        for line in res.split("\n")[1:-1]:
            #print line
            Entry, a,b,c,d,e,f = line.split("\t")
            #print Entry, a, b, c, d, e, f
            newres[Entry] = {'Entry name': a,
                         'Status': b,
                         'Protein names': c,
                         'Gene names': d,
                         'Organism': e,
                         'Length': f}
        return newres

    def uniref(self, query):
        """Calls UniRef service

        :return: if you have Pandas installed, returns a dataframe (see example)

        ::

            >>> u = UniProt()
            >>> df = u.uniref("member:Q03063")  # of just A03063
            >>> df.Size

        """
        try:
            import pandas as pd
        except:
            print("uniref method requires Pandas")
            return
        res = self.http_get("uniref/", params={"query":query, 'format':'tab'}, frmt="txt")
        res = pd.read_csv(io.StringIO(unicode(res.strip())), sep="\t")
        return res

    def get_df(self, entries, nChunk=100, organism=None):
        """Given a list of uniprot entries, this method returns a dataframe with all possible columns


        :param entries: list of valid entry name. if list is too large (about
            >200), you need to split the list
        :param chunk:
        :return: dataframe with indices being the uniprot id (e.g. DIG1_YEAST)

        .. todo:: cleanup the content of the data frame to replace strings
            separated by ; into a list of strings. e.g. the Gene Ontology IDs

        .. warning:: requires pandas library
        """
        if isinstance(entries, str):
            entries = [entries]
        else:
            entries = list(set(entries))
        output = pd.DataFrame()

        self.logging.info("fetching information from uniprot for {} entries".format(len(entries)))

        nChunk = min(nChunk, len(entries))
        N, rest = divmod(len(entries), nChunk)
        for i in range(0, N+1):
            this_entries = entries[i*nChunk:(i+1)*nChunk]
            if len(this_entries):
                self.logging.info("uniprot.get_df {}/{}".format(i+1, N))
                query = "+or+".join(this_entries)
                if organism:
                    query += "+and+"+organism
                res = self.search(query, frmt="tab",
                                  columns=",".join(self._valid_columns))
            else:
                break
            if len(res) == 0:
                self.logging.warning("some entries %s not found" % entries)
            else:
                df = pd.read_csv(io.StringIO(unicode(res)), sep="\t")
                if isinstance(output, type(None)):
                    output = df.copy()
                else:
                    output = output.append(df, ignore_index=True)

        # you may end up with duplicated...
        output.drop_duplicates(inplace=True)
        # you may have new entries...
        # output = output[output.Entry.apply(lambda x: x in entries)]
        # to transform into list:
        columns = ['PubMed ID', 'Comments', u'Domains', 'Protein families',
                   'Gene names', 'Gene ontology (GO)', 'Gene ontology IDs',
                   'InterPro', 'Interacts with', 'Keywords',
                   'Subcellular location']
        for col in columns:
            try:
                res = output[col].apply(lambda x:[this.strip() for this in str(x).split(";") if this!="nan"])
                output[col] = res
            except:
                self.logging.warning("column could not be parsed. %s" % col)
        # Sequences are splitted into chunks of 10 characters. let us rmeove 
        # the spaces:
        output.Sequence = output['Sequence'].apply(lambda x: x.replace(" ", ""))

        return output
