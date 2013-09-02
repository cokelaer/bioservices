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
"""Interface to some part of the Pfam web service

.. topic:: What is Pfam ?

    :URL: http://www.uniprot.org
    :Citation:

    .. highlights::


        -- From Pfam  web site (help/about), Aug 2013



"""
from services import RESTService
from xmltools import readXML
__all__ = ["Pfam"]


class Pfam(RESTService):
    """Interface to `Pfam <http://pfam.sanger.ac.uk>`_ pages

    This is not a REST interface actually but rather a parser to some of the
    HTML pages relatd to pathways.

    One can retrieve the pathways names and their list of proteins. 

        >>> from bioservics import *
        >>> p = Pfam()

    """
    _url = "http://pfam.sanger.ac.uk/"
    def __init__(self, verbose=True):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(Pfam, self).__init__(name="Pfam", url=Pfam._url, verbose=verbose)


    def show(self, Id):
        """Just an example of opening a web page with a uniprot Id


            p = Pfam()
            p.show("P43403")

        """
        url = self._url + "/protein/" + Id
        print url
        self.onWeb(url)
