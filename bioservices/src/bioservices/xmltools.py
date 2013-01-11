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
"""This module will include common tools to manipulate XML files"""
import xml.etree.ElementTree as ET
import BeautifulSoup

__all__ = ["easyXML"]


class easyXML(object):
    """class to ease the introspection of XML document.

    This class uses the standard xml module as well as the package BeautifulSoup
    to help introspecting the XML programmatically.

    :: 

        >>> import nciblast
        >>> n = nciblast.NCIBlast()
        >>> res = n.parameters() # res is an instance of easyXML
	    # You can retreive XML from this instance of easyXML and print the content
        # in a more human-readable way.
        >>> print res
        >>> res.soup.findAll('id') # a Beautifulsoup instance is available
        >>> res.root # and the root using xml.etree.ElementTree

    """
    def __init__(self, data):
        """Constructor

        :param data: a document in XML format

        """
        self.data = data[:]
        self.root = ET.fromstring(data)
        self._soup = None
        self.prettify = self.soup.prettify
        self.findAll = self.soup.findAll

    def getchildren(self):
        """returns all children of the root XML document"""
        return self.root.getchildren()

    def _get_soup(self):
        if self._soup == None:
            self._soup = BeautifulSoup.BeautifulSoup(self.data)
        return self._soup
    soup = property(_get_soup)

    def __str__(self):
        txt = self.soup.prettify()
        return txt

