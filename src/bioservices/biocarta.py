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
import re
import urllib

from bs4 import BeautifulSoup
from bioservices.services import REST
from bioservices.xmltools import readXML, HTTPError

__all__ = ["BioCarta"]

# method for unicode transformation
try:
    text = unicode
except NameError:
    text = str


class BioCarta(REST):
    """Interface to `BioCarta <http://www.biocarta.com>`_ pages

    This is not a REST interface actually but rather a parser to some of the
    HTML pages related to pathways.

    One can retrieve the pathways names and their list of proteins.

        >>> from bioservics import *
        >>> b = BioCarta()
        >>> pathways = b.get_pathway_names()
        >>> proteins = b.get_pathway_protein_names(pathways[0])


    .. warning:: biocarta pathways layout can be accesses from PID

    """
    _url = "http://cgap.nci.nih.gov/Pathways/BioCarta_Pathways"

    _organism_prefixes = {'Homo sapiens': 'h', 'Mus musculus': 'm'}
    organisms = set(_organism_prefixes.keys())

    _all_pathways = None
    _pathway_categories = None
    _all_pathways_url =  "http://cgap.nci.nih.gov/Pathways/BioCarta_Pathways"

    def __init__(self, verbose=True):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(BioCarta, self).__init__(name="BioCarta", url=BioCarta._url, verbose=verbose)
        self.fname  = "biocarta_pathways.txt"

        self._organism = None
        self._organism_prefix = None
        self._pathways = None

    # set the default organism used by pathways retrieval
    def _get_organism(self):
        return self._organism

    def _set_organism(self, organism):
        organism = organism[:1].upper() + organism[1:].lower()
        if organism == self._organism: return
        if organism not in BioCarta.organisms:
            raise ValueError("Invalid organism. Check the list in :attr:`organisms` attribute")

        self._organism = organism
        self._organism_prefix = BioCarta._organism_prefixes[organism]
        self._pathways = None

    organism = property(_get_organism, _set_organism, doc="returns the current default organism")

    def _get_pathway_categories(self):
        if self._pathway_categories is None:
            self._pathway_categories = self.http_get_ou_post()
        return self._pathway_categories
    pathway_categories = property(_get_pathway_categories)

    def _get_all_pathways(self):
        """returns pathways from biocarta

        human and mouse organisms are available but only those corresponding
        to the organism defined in :attr:`organism` are returned.
        """
        if self.organism is None:
           raise ValueError(
                "Please set the organism attribute to one of %s" %
                self._organism_prefixes.keys())

        if BioCarta._all_pathways is None:
            BioCarta._all_pathways = readXML(self._all_pathways_url)

        if self._pathways is None:

            url_pattern = re.compile("http://cgap.nci.nih.gov/Pathways/BioCarta/%s_(.+)[Pp]athway" \
                % (self._organism_prefix))
            is_pathway_url = lambda tag: tag.name == "a" and not tag.has_attr("class")
            self._pathways = BioCarta._all_pathways.findAll(is_pathway_url, href=url_pattern)

            # Now let us select only the name.
            self._pathways = sorted([entry.attrs['href'].rsplit("/", 1)[1]
                              for entry in self._pathways])
        return self._pathways
    all_pathways = property(_get_all_pathways)

    def get_pathway_protein_names(self, pathway):
        """returns list of genes for the corresponding pathway

        This function scans an HTML page. We have not found another way to 
        get the gene list in a more reobust way. This function was tested on 
        one pathway. Please use with caution.


        """
        self.logging.info("Fetching the pathway")
        # first identify gene from GeneInfo tag
        # this is not XML but HTML
        url = "http://cgap.nci.nih.gov/Pathways/BioCarta/%s" % pathway
        html_doc = urllib.urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        links = soup.find_all('area')
        links = [link for link in links if 'GeneInfo' in link.get('href')]

        links = set([link.attrs['href'] for link in links])

        self.logging.info("Scanning information about %s genes" % len(links))
        # open each page and get info
        genes = {}
        for link in links:
            html_doc = urllib.urlopen(link).read()
            soup = BeautifulSoup(html_doc, 'html.parser')

            table_gene_info = soup.findAll("table")[1]

            gene_name = link.rsplit("=", 1)[1]
            self.logging.info(" - " + gene_name)

            genes[gene_name] = {}
            self.tt = table_gene_info
            for row in table_gene_info.find_all('tr'):
                entry = row.find_all('td')
                try:key = entry[0].text.strip()
                except:continue
                try:value = entry[1].text.strip()
                except:continue
                if "[Text]" in key:
                    continue
                genes[gene_name][key] = value


        return genes
