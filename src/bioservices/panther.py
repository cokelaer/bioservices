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
__all__ = ["Panther"]


class Panther(REST):
    """Interface to `Panther <http://www.biocarta.com>`_ pages


    HTML pages relatd to pathways.

    One can retrieve the pathways names and their list of proteins. 

        >>> from bioservics import *
        >>> b = Panther()
        >>> pathways = b.get_pathway_names()
        >>> proteins = b.get_pathway_protein_names(pathways[0])


    .. warning:: biocarta pathways layout can be accesses from PID

    """
    _url = "http://www.pantherdb.org/"
    def __init__(self, verbose=True, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(Panther, self).__init__(name="Panther", url=Panther._url, 
                verbose=verbose, cache=cache)

        self._allPathwaysURL =  "http://www.pantherdb.org/pathway/pathwayList.jsp"

    def get_pathway_names(self, startswith=""):
        """returns pathways from biocarta
        
        all human and mouse. can perform a selectiom
        """
        raise NotImplementedError
        allx = readXML(self._allPathwaysURL)
        pathways = [this.get("href") for this in allx.findAll("a") if "pathfiles" in this.get("href")]
        pathways =  [str(x.split("/")[-1]) for x in pathways] # split the drive
        pathways = sorted(list(set(pathways)))
        pathways = [x for x in pathways if x.startswith(startswith)]
        return pathways

    def get_biopax_pathways(self, name):
        raise NotImplementedError
