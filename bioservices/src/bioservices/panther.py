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
#$Id: uniprot.py 226 2013-07-08 07:05:14Z cokelaer $
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
from services import RESTService
from xmltools import readXML
__all__ = ["BioCarta"]


class Panther(RESTService):
    """Interface to `BioCarta <http://www.biocarta.com>`_ pages


    HTML pages relatd to pathways.

    One can retrieve the pathways names and their list of proteins. 

        >>> from bioservics import *
        >>> b = BioCarta()
        >>> pathways = b.get_pathway_names()
        >>> proteins = b.get_pathway_protein_names(pathways[0])


    .. warning:: biocarta pathways layout can be accesses from PID

    """
    _url = "http://www.pantherdb.org/"
    def __init__(self, verbose=True):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(Panther, self).__init__(name="BioCarta", url=Panther._url, verbose=verbose)

        self._allPathwaysURL =  "http://www.pantherdb.org/pathway/pathwayList.jsp"

    def get_pathway_names(self, startswith=""):
        """returns pathways from biocarta
        
        all human and mouse. can perform a selectiom
        """
        raise NotImplementedError
        x = readXML(self._allPathwaysURL)
        pathways = [this.get("href") for this in x.findAll("a") if "pathfiles" in this.get("href")]
        pathways =  [str(x.split("/")[-1]) for x in pathways] # split the drive
        pathways = sorted(list(set(pathways)))
        pathways = [x for x in pathways if x.startswith(startswith)]
        return pathways

    def get_biopax_pathways(self, name):
        raise NotImplementedError
