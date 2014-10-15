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
#$Id$
"""Interface to HUGO/HGNC web services

.. topic:: What is HGNC ?

    :URL: http://www.genenames.org
    :Citation:

    .. highlights::

        "The HUGO Gene Nomenclature Committee (HGNC) has assigned unique gene symbols and
        names to over 37,000 human loci, of which around 19,000 are protein coding.
        genenames.org is a curated online repository of HGNC-approved gene nomenclature
        and associated resources including links to genomic, proteomic and phenotypic
        information, as well as dedicated gene family pages."

        -- From HGNC web site, July 2013


"""
from bioservices import REST
from .xmltools import bs4
try:
    from urllib.error import HTTPError
except:
    from urllib2 import HTTPError

__all__ = ["HGNC", 'HGNCDraft']


class HGNCDraft(REST):
    """
    """
    def __init__(self, verbose=False, cache=False):
        url = "http://www.genenames.org/"
        super(HGNCDraft, self).__init__("HGNC", url=url, verbose=verbose, cache=cache)

    def get_info(self, frmt='json'):
        res = self.http_get("", frmt=frmt)
        return res

    def fetch(self):
        pass
        # http://rest.genenames.org/fetch/hgnc_id/6876


class HGNC(REST):
    """Interface to the `HGNC <http://www.genenames.org>`_ service


    ::

        >>> from bioservices import *
        >>> # Fetch XML document for gene ZAP70
        >>> s = HGNC()
        >>> xml = s.get_xml("ZAP70")
        >>> # You can fetch several gene names:
        >>> xml = s.get_xml("ZAP70;INSR")
        >>> # Wrong gene name request returns an empty list
        >>> s.get_xml("wrong")
        []

    For a single name, the following methods are available::

        >>> # get the aliases of a given gene
        >>> print(s.get_aliases("ZAP70"))
        [u'ZAP-70', u'STD']
        >>> # get UniProt accession code
        >>> s.get_xrefs("ZAP70")['UniProt']['xkey']
        'P43403'
        >>> # get XML link to a UniProt cross-reference
        >>> s.get_xrefs("ZAP70", "xml")['UniProt']['link']
        ['http://www.uniprot.org/uniprot/P43403.xml']


    You can access to the links of a cross reference as well::

        values = s.get_xrefs("ZAP70")
        s.on_web(values['EntrezGene']['link'][0])


    :references: http://www.avatar.se/HGNC/doc/tutorial.html

    .. warning:: this is actually the HGNC/wr website. Maybe not the official.

    """
    def __init__(self, verbose=False, cache=False):
        url = "http://www.avatar.se/HGNC/wr/"
        super(HGNC, self).__init__("HGNC", url=url, verbose=verbose, cache=cache)
        self.logging.warning("Service unavailable when testing (Aug 2014). May not work")

        self._always_return_list = False

        # FIXME
        #: Force XML to be checked for unicode consistency see :class:`Service`
        #self._fixing_unicode = True
        #self._fixing_encoding = "utf-8"

    def _set_return(self, mode):
        assert mode in [False, True]
        self._always_return_list = mode
    def _get_return(self):
        return self.always_return_list

    def get_xml(self, gene):
        """Returns XML of a single gene or list of genes


        :param str gene: a valid gene name. Several gene names can be concatenated with
            comma ; character (e.g., 'ZAP70;INSR')


        .. doctest::

            >>> from bioservices import *
            >>> s = HGNC()
            >>> res = s.get_xml("ZAP70")
            >>> res.findAll("alias")
            >>> [x.text for x in res.findAll("alias")]
            [u'ZAP-70', u'STD']

        .. seealso:: :meth:`get_aliases`
        """
        try:
            if ";" in gene:
                res = self.http_get("genes/%s" % gene)
            else:
                res = self.http_get("gene/%s.xml" % gene)
                res = self.easyXML(res)
            #res = bs4.BeautifulSoup(res)
        except HTTPError:
            print("!!BioServices HTTPError caught in HGNC. Probably an invalid gene name")

            res = bs4.BeautifulSoup()
        #except Exception:
        #    raise Exception
        return res

    def _get_attribute(self, gene, attribute):
        res = self.get_xml(gene)
        values = [x.text.strip() for x in res.findAll(attribute)][0]
        if len(values) == 1:
            return values[0]
        else:
            return values

    def get_aliases(self, gene):
        """Get aliases for a single gene name"""
        res = self.get_xml(gene)
        aliases = [x.text for x in res.findAll("alias")]
        return aliases

    def get_name(self, gene):
        """Get name for a single gene name"""
        return self._get_attribute(gene, "name")

    def get_chromosome(self, gene):
        """Get chromosome for a single gene name"""
        return self._get_attribute(gene, "chromosome")

    def get_previous_symbols(self, gene):
        """Get previous symbols for a single gene name"""
        return self._get_attribute(gene, "previous_symbols")

    def get_withdrawn_symbols(self, gene):
        """Get withdrawn symbols for a single gene name"""
        return self._get_attribute(gene, "withdrawn_symbols")

    def get_previous_names(self, gene):
        """Get previous names for a single gene name"""
        return self._get_attribute(gene, "previous_names")

    def get_xrefs(self, gene, keep="html"):
        """Get the cross references for a given single gene name

        ::


            >>> databases = s.get_xrefs("ZAP70").keys()

            >>> # get XML link to a UniProt cross-reference
            >>> s.get_xrefs("ZAP70", "xml")['UniProt']['link']
            ['http://www.uniprot.org/uniprot/P43403.xml']


        """
        assert keep in ["html", "xml", "fasta", "rdf", "txt", "gff", None]
        # returns list of dictionary that contains the attributes of each
        # reference as well as a list of links provided for each reference.

        xml = self.get_xml(gene)
        values = self._get_xref(xml, keep)
        return values

    def _get_xref(self, xml, keep):
        # get all dbs and build up a dict out of it
        dbs =  [x.attrs['xdb'] for x in xml.findAll("xref")]
        values =  dict([(this,{}) for this in dbs])

        # rescan the xml to get the other attributes
        refs = [x.attrs for x in xml.findAll("xref")]
        for ref in refs:
            db = ref['xdb']
            values[db] = ref.copy()
            # this looks quite complicated so here is a bit of explanation:
            # Each reference may have a few links. However, we are interested
            # only in this function by the HTML format. So, for a given database (res.findAll(xref)),
            # we search for all links (findAll(link)) and for each link found, we keep only those where
            # format is HTML. Finally; we get only the attribute 'xlink:href'
            links = [y.attrs['xlink:href'] for y in [x for x in xml.findAll("xref") if x['xdb']==db][0].findAll("link") if y.attrs['format']==keep]
            values[db]['link'] = links[:]

        return values

    def lookfor(self, pattern):
        """Finds all genes that starts with a given pattern

        :param str pattern: a string. Could be the wild character `*`
        :return: list of dictionary. Each dictionary contains the 'acc',
            'xlink:href' and 'xlink:title' keys


        .. doctest::

            >>> from bioservices import *
            >>> s = HGNC()
            >>> s.lookfor("ZAP")
            [{'acc': 'HGNC:12858',
            'xlink:href': '/HGNC/wr/gene/ZAP70',
            'xlink:title': 'ZAP70'}]


        This function may be used to count the number of entries::


            len(s.lookfor('*'))

        """
        params = {'search': 'symbol', 'value':pattern}
        # note the extra s before ;index.xml
        xml = self.http_get("s;index.xml?" + self.urlencode(params))
        xml = self.easyXML(xml)
        res = [x.attrs for x in xml.findAll("gene")]
        return res

    def get_all_names(self):
        """Returns all gene names"""
        entries = self.lookfor("*")
        names = [entry['xlink:title'] for entry in entries]
        return names

    def mapping(self, value):
        """maps an identifier from a database onto HGNC database

        :param str value: a valid DB:id string (e.g. "UniProt:P36888")
        :return: a list of dictionary with the keys 'acc', 'xlink:href', 'xlink:title'

            >>> value = "UniProt:P43403"
            >>> res = s.mapping(value)
            >>> res[0]['xlink:title']
            'ZAP70'
            >>> res[0]['acc']
            'HGNC:12858'


        .. seealso:: :meth:`mapping_all`
        """

        xml = self.http_get("s;index.xml?" + self.urlencode({'search': 'xref', 'value':value}))
        xml = self.easyXML(xml)
        genes = xml.findAll("gene")
        res = [g.attrs for g in genes]
        return res

    def mapping_all(self, entries=None):
        """Retrieves cross references for more than one entry

        :param entries: list of values entries (e.g., returned by the :meth:`lookfor` method.)
            if not provided, this method looks for all entries.
        :returns: list of dictionaries with keys being all entry names. Values is a
            dictionary of cross references.

        .. warning:: takes 10 minutes

        """
        from math import ceil
        results = {}

        if entries is None:
            print("First, get all entries")
            entries = self.lookfor('*')

        names = [entry['xlink:title'] for entry in entries]
        N = len(names)

        # split query in sets of 300 names

        dn = 300
        N = len(names)
        n = int(ceil(N/float(dn)))
        for i in range(0, n):
            print("Completed ", i+1, "/", n)
            query  = ";".join(names[i*dn:(i+1)*dn])
            xml = self.get_xml(query)
            genes = xml.findAll("gene")
            for gene in genes:
                res = self._get_xref(gene, None)
                #acc = gene.attrs['acc'] not needed. can be access from ['HGNC']['xkey']
                name = gene.attrs['symbol']
                results[name] = res.copy()
        return results








