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
#$Id$
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


.. mapping betwenn uniprot and bench of other DBs.
.. ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/


"""
from services import Service, RESTService
import urllib2

__all__ = ["UniProt"]


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
    "NextBio": "NEXTBIO_ID"
}




class UniProt(RESTService):
    """Interface to the `UniProt <http://www.uniprot.org>`_ service

    .. warning:: for the time being, this class only provide interface to 
        * the identifier mapping service
        * search of a UniProtKB identifier
        * some experimental interface to the full search 

    Example::

        >>> from bioservices import UniProt
        >>> u = UniProt(verbose=False)
        >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403')
        ['FromACC', 'ToKEGG_ID', 'P43403', 'hsa:7535']
        >>> res = u.search("P43403")

        # Returns sequence on the ZAP70_HUMAN accession Id
        >>> sequence = u.search("ZAP70_HUMAN", columns="sequence")

    """
    _mapping = mapping.copy()
    _url = "http://www.uniprot.org"
    def __init__(self, verbose=True):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(UniProt, self).__init__(name="UniProt", url=UniProt._url, verbose=verbose)


    def mapping(self, fr="ID", to="KEGG_ID", format="tab", query="P13368"):
        """This is an interface to the UniProt mapping service


        :param fr: the source database identifier. See :attr:`_mapping`.
        :param to: the targetted database identifier. See :attr:`_mapping`.
        :param format: the output format (default is tabulated "tab")
        :param query: a string containing one or more IDs separated by a space
        :return: a list. The first element is the source database Id. The second
            is the targetted source identifier. Following elements are alternate
            of one the entry and its mapped Id. If a query has several mapped
            Ids, the query is repeated (see example with PDB mapping here below)


e.g., ["From:ID", "to:PDB_ID", "P43403"]


        ::

            >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403')
            ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535']
            >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403 P00958')
            ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535', 'P00958', 'sce:YGR264C']
            >>> u.mapping(fr="ID", to="PDB_ID", query="P43403", format="tab")
            ['From:ID', 'To:PDB_ID', 'P43403', '1FBV', 'P43403', '1M61', 'P43403', '1U59',
            'P43403', '2CBL', 'P43403', '2OQ1', 'P43403', '2OZO', 'P43403', '2Y1N',
            'P43403', '4A4B', 'P43403', '4A4C']



        There is a web page that gives the list of correct `database identifiers
        <http://www.uniprot.org/faq/28>`_. You can also look at the
        :attr:`_mapping` attribute.

        :URL: http://www.uniprot.org/mapping/

        """
        import urllib
        #self.checkParam(fr, self._mapping.values())
        #self.checkParam(to, self._mapping.values())

        url = self.url + '/mapping/'
        params = {'from':fr, 'to':to, 'format':format, 'query':query}
        data = urllib.urlencode(params)
        self.logging.info(data)
        request = urllib2.Request(url, data)
        # 2 following lines are optional
        contact = ""
        request.add_header('User-Agent', 'Python contact')
        response = urllib2.urlopen(request)
        result = response.read(200000)

        # let us improvve the output a little bit using a list  instead of a
        # string
        try:
            result = result.split()
            result[0]+=':'+fr
            result[1]+=':'+to
        except:
            pass

        return result

    def searchUniProtId(self, uniprot_id, format="xml"):
        """Search for a uniprot ID in UniprotKB database

        :param str uniprot: a valid uniprotKB ID
        :param str format: expected output format amongst xml, txt, fasta, gff, rdf


        ::

            >>> u = UniProt()
            >>> res = u.searchUniProtId("P09958", format="xml")

        """
        _valid_formats = ['txt', 'xml', 'rdf', 'gff', 'fasta']
        self.checkParam(format, _valid_formats)
        #if format not in _valid_formats:
        #    raise ValueError("invalid format provided. Use one of %s" % _valid_formats)
        url = self.url + "/uniprot/" + uniprot_id + '.' + format
        res = self.request(url)
        return res


    def search(self, query, format="tab", columns=None,
        include=False,sort="score", compress=False, limit=None, offset=None, maxTrials=10):
        """Provide some interface to the uniprot search interface.

        :param str query: query must be a valid uniprot query.
            See http://www.uniprot.org/help/text-search, http://www.uniprot.org/help/query-fields 
        :param str format: a valid format amongst html, tab, xls, asta, gff,
            txt, xml, rdf, list, rss. If tab or xls, you can also provide the 
            columns argument.  (default is tab)
        :param str columns: comma-separated list of values. Works only if fomat 
            is tab or xlsFor UnitProtKB, the possible columns are:
            citation, clusters, comments, database, domains, domain, ec, id, entry name
            existence, families, features, genes, go, go-id, interpro, interactor,
            keywords, keyword-id, last-modified, length, organism, organism-id, 
            pathway, protein names, reviewed, score, sequence, 3d, 
            subcellular locations, taxon, tools, version, virus hosts. The
            column database must be follows by the database name in brackets
            (e.g. "database(PDB)")
        :param bool include:  include isoform sequences when the format
            parameter is fasta. Include description when format is rdf. 
        :param sort: by score by default. Set to None to bypass this behaviour
        :param bool compress: gzip the results
        :param int limit: Maximum number of results to retrieve.
        :param int offset:  Offset of the first result, typically used together
            with the limit parameter.
        :param int maxTrials: this request is unstable, so we may want to try
            several time.

        To obtain the list of uniprot ID returned by the search of zap70 can be retrieved as follows
        ::

            >>> u.search('zap70+AND+organism:9606', format='list')
            >>> u.search("zap70+and+taxonomy:9606", format="tab", limit=3, 
            ...    columns="entry name,length,id, genes")
            Entry name  Length  Entry   Gene names
            CBLB_HUMAN  982 Q13191  CBLB RNF56 Nbla00127
            CBL_HUMAN   906 P22681  CBL CBL2 RNF55
            CD3Z_HUMAN  164 P20963  CD247 CD3Z T3Z TCRZ

        other examples::

            u.search("ZAP70+AND+organism:9606", limit=3, columns="id,database(PDB)")


        .. warning:: this function request seems a bit unstable (UniProt web issue ?)
            so we repeat the request if it fails
        """
        params = {}

        if format!=None:
            _valid_formats = ['tab', 'xls', 'fasta', 'gff', 'txt', 'xml', 'rss', 'list', 'rss', 'html']
            self.checkParam(format, _valid_formats)
            params['format'] = format

        if columns!=None:
            self.checkParam(format, ["tab","xls"])
            _valid_columns = ['citation', 'clusters', 'comments','database',
                'domains','domain', 'ec','id','entry name','existence',
        		'families', 'features', 'genes', 'go', 'go-id', 'interpro', 
                'interactor', 'keywords', 'keyword-id', 'last-modified', 
                'length', 'organism', 'organism-id', 'pathway', 'protein names', 
                'reviewed', 'score', 'sequence', '3d', 'subcellular locations', 
                'taxonomy', 'tools', 'version', 'virus hosts']
            # remove unneeded spaces before/after commas if any
            if "," in columns:
                columns = [x.strip() for x in columns.split(",")]
            else:
                columns = [columns]

            for col in columns:
                if col.startswith("database(") == True:
                    pass
                else:
                    self.checkParam(col, _valid_columns)

            # convert back to a string as expected by uniprot
            params['columns'] = ",".join([x.strip() for x in columns])

        if include == True and format in ["fasta", "rdf"]:
            params['include'] = 'yes'

        if compress == True:
            params['compress'] = 'yes'
 
        if sort:
            self.checkParam(sort, ["score"])
            params['sort'] = sort

        if offset != None:
            if isinstance(offset, int):
                params['offset'] = offset

        if limit != None:
            if isinstance(limit, int):
                params['limit'] = limit

        params = self.urlencode(params)
        
        #res = s.request("/uniprot/?query=zap70+AND+organism:9606&format=xml", params)
        trials = 1
        while trials<maxTrials:
            try:
                res = self.request("uniprot/?query=%s" % query + "&" + params, "txt")
                trials = maxTrials + 1
            except:
                self.logging.warning("Trying again...")
                import time
                time.sleep(2)
                trials += 1
        return res



    def quick_search(self, query, include=False,sort="score", limit=None):

        res = self.search(query, "tab", include=include, sort=sort, limit=limit)

        #if empty result, nothing to do
        if len(res) == 0:
            return res
        # else populate a dictionary
        newres = {}
        for line in res.split("\n")[1:-1]:
            print line
            Entry, a,b,c,d,e,f = line.split("\t")
            print Entry, a, b, c, d, e, f
            newres[Entry] = { 'Entry name': a,
                         'Status': b,
                         'Protein names': c,
                         'Gene names': d,
                         'Organism' : e,
                         'Length' : f}
        return newres
