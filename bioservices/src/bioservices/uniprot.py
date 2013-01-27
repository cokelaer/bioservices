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



class UniProt(RESTService):
    """Interface to the `UniProt <http://www.uniprot.org>`_ service

    .. warning:: for the time being, this class only provide interface to 
        * the identifier mapping service
        * search of a uniprotKB identifier
        * some experimental interface to the full search 

    Example::

        >>> u = Uniprot(verbose=False)
        >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403')
        ['FromACC', 'ToKEGG_ID', 'P43403', 'hsa:7535']
        >>> res = u.search("P43403")


    """
    _url = "http://www.uniprot.org"
    def __init__(self, verbose=True):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(UniProt, self).__init__(name="UniProt", url=UniProt._url, verbose=verbose)


    def mapping(self, fr="ID", to="KEGG_ID", format="tab", query="P13368"):
        """This is an interface to the UniProt mapping service


        ::

            >>> u.mapping(fro="ACC", to="KEGG_ID", query='P43403')
            ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535']
            >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403 P00958')
            ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535', 'P00958', 'sce:YGR264C']


        There is a web page that gives the list of correct `database identifiers
        <http://www.uniprot.org/faq/28>`_

        :URL: http://www.uniprot.org/mapping/

        """
        import urllib
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


    def search(self, query, format="html", columns=None, include=False, 
        	compress=False, limit=None, offset=None):
        """Provide some interface to the uniprot search interface.

        :param str query: query must be a valid uniprot query.
            See http://www.uniprot.org/help/text-search, http://www.uniprot.org/help/query-fields 
        :param str format: a valid format amongst html, tab, xls, asta, gff,
            txt, xml, rdf, list, rss. If tab or xls, you can also provide the 
            columns argument. 
        :param str columns: comma-separated list of values. Works only if fomat 
            is tab or xlsFor UnitProtKB, the possible columns are:
            citation, clusters, comments, database, domains, domain, ec, id, entry name
            existence, families, features, genes, go, go-id, interpro, interactor,
            keywords, keyword-id, last-modified, length, organism, organism-id, 
            pathway, protein names, reviewed, score, sequence, 3d, 
            subcellular locations, taxon, tools, version, virus hosts
        :param bool include:  include isoform sequences when the format parameter is fasta. Include description when format is rdf.
        :param bool compress: gzip the results
        :param int limit: Maximum number of results to retrieve.
        :param int offset:  Offset of the first result, typically used together with the limit parameter. 

        To obtain the list of uniprot ID returned by the search of zap70 can be retrieved as follows
        ::

            >>> u.search('zap70+AND+organism:9606', format='list')
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
                'taxon', 'tools', 'version', 'virus hosts']
            # remove unneeded spaces before/after commas if any
            columns = ",".join([x.strip() for x in columns.split(",")]) 
            for xol in columns:
                self.checkParam(col, _valid_columns)
            params['columns'] = columns

        if include == True and format in ["fasta", "rdf"]:
            params['include'] = 'yes'

        if compress == True:
            params['compress'] = 'yes'
 
        if offset != None:
            if isinstance(offset, int):
                params['offset'] = offset

        if limit != None:
            if isinstance(limit, int):
                params['limit'] = limit

        params = self.urlencode(params)
        
        #res = s.request("/uniprot/?query=zap70+AND+organism:9606&format=xml", params)
        res = self.request("/uniprot/?query=%s" % query + "&" + params, "txt")
        return res


#[x for x in [res.getchildren()[i].getchildren()[0].text for i in range(0,32)] if x.startswith('P43')]
