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
from services import REST
from xmltools import readXML
__all__ = ["BioCarta"]


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
    def __init__(self, verbose=True):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(BioCarta, self).__init__(name="BioCarta", url=BioCarta._url, verbose=verbose)
        self.fname  = "biocarta_pathways.txt"

        self._allPathwaysURL =  "http://www.biocarta.com/genes/allPathways.asp"

    def get_pathway_names(self, startswith=""):
        """returns pathways from biocarta

        all human and mouse. can perform a selectiom
        """
        x = readXML(self._allPathwaysURL)
        pathways = [this.get("href") for this in x.findAll("a") if "pathfiles" in this.get("href")]
        pathways =  [str(xx.split("/")[-1]) for xx in pathways] # split the drive
        pathways = sorted(list(set(pathways)))
        pathways = [xx for xx in pathways if xx.startswith(startswith)]
        return pathways

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
        url = self._url + "/pathfiles/" + pathway
        x = readXML(url)
        self.logging.info("Reading " + url)
        protein_url = [this.get("href") for this in x.findAll("a") \
                if 'href' in this and "Protein" in this.get("href")]
        if len(protein_url) == 0:
            return None
        else:
            link = protein_url[0]
            link = link.split("/pathfiles/")[-1]
            link = str(link) # get rid of unicode ?
            link = link.strip("')")
            url = self._url + "/pathfiles/" + link
            self.logging.info("Reading " + url)
            x = readXML(url)

            # seems to work
            table = [this for this in x.findAll("table") if this.findAll("th")
                    and  this.findAll("th")[0].getText() == "Gene Name"][2]
            # now get the genename, locus and accession
            rows = [[y.getText() for y in xx.findAll("td")] for xx in  table.findAll("tr")]
            rows = [xx for xx in rows if len(x)]
            return rows
