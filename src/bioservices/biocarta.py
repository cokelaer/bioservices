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
from services import REST
from xmltools import readXML, HTTPError
__all__ = ["BioCarta"]

# method for unicode transformation
try:
    text = unicode
except NameError:
    text = str

class BioCarta(REST):
    """Interface to `BioCarta <http://www.biocarta.com>`_ pages


    This is not a REST interface actually but rather a parser to some of the
    HTML pages relatd to pathways.

    One can retrieve the pathways names and their list of proteins.

        >>> from bioservics import *
        >>> b = BioCarta()
        >>> pathways = b.get_pathway_names()
        >>> proteins = b.get_pathway_protein_names(pathways[0])


    .. warning:: biocarta pathways layout can be accesses from PID

    """
    _url = "http://www.biocarta.com/"

    _organism_prefixes = {'Homo sapiens': 'h', 'Mus musculus': 'm'}
    organisms = set(_organism_prefixes.keys())

    _all_pathways = None
    _pathway_categories = None
    _all_pathways_url =  "http://www.biocarta.com/genes/allPathways.asp"

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

        all human and mouse. can perform a selectiom
        """
        if BioCarta._all_pathways is None:
            BioCarta._all_pathways = readXML(self._all_pathways_url)
        if self._pathways is None:
            url_pattern = re.compile("^/pathfiles/%s_(.+)[Pp]athway.asp" % self._organism_prefix)
            is_pathway_url = lambda tag: tag.name == "a" and not tag.has_attr("class")
            self._pathways = BioCarta._all_pathways.findAll(is_pathway_url, href=url_pattern)
            self._pathways = {url_pattern.match(a["href"]).group(1):
                              text(a.find_previous_sibling("a", class_="genesrch").string.rstrip())
                              for a in self._pathways}
        return self._pathways

    all_pathways = property(_get_all_pathways)

    def get_pathway_protein_names(self, pathway):
        """returns list of list. Each elements is made of 3 items: gene name,
        locusId and accession (often empty

        Requires to parse HTML page such as
        http://www.biocarta.com/pathfiles/m_actinYPathway.asp

        to figure out the URL that would pop up if we press the protein list
        button. For instance:

        http://www.biocarta.com/pathfiles/PathwayProteinList.asp?showPFID=175

        but now we need to parse the HTML, which is not necessaray very robust.
        THere are many tables and we want to access one that is a children of
        another... Finally, We scan the table for tr and td tags.

        The most difficult is to find the good table which is hardcoded to be
        the third that contains a th[0] == "Gene name". Although there is only
        one, 3 are returned due probably to an error in the parsing or the HTMl
        file itself. To be checked and made more robust.

        """
        url_pattern = re.compile('pathfiles/PathwayProteinList\.asp\?showPFID=\d+')
        url = self._url + "pathfiles/{organism}_{name}Pathway.asp"
        url = url.format(organism=self._organism_prefix, name=pathway)
        self.logging.info("Reading " + url)
        try:
            url = readXML(url).soup.find('a', href=url_pattern)
        except HTTPError as error:
            if error.code == 404:
                raise ValueError("Pathway not found ({}): {}".format(self.organism, pathway))
            raise

        url = self._url + url_pattern.search(url['href']).group(0)
        self.logging.info("Reading " + url)
        html = readXML(url).soup

        genes = {}
        header = html.th.parent
        for row in header.find_next_siblings('tr'):
            gene_info = [x.string for x in row.find_all('td')]
            if any(x is None for x in gene_info[:2]):
                raise RuntimeError("Information missing: {}".format(gene_info))
            gene_id = gene_info[1]
            gene_name = gene_info[0].rstrip()
            genes[gene_id] = gene_name
        return genes
