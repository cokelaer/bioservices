#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EMBL-EBI
#
#  File author(s): 
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
"""This module includes common tools to manipulate XML files"""
import xml.etree.ElementTree as ET
import BeautifulSoup

__all__ = ["easyXML"]


class easyXML(object):
    """class to ease the introspection of XML documents.

    This class uses the standard xml module as well as the package BeautifulSoup
    to help introspecting the XML documents.

    :: 

        >>> from bioservices import *
        >>> n = ncbiblast.NCBIblast()
        >>> res = n.getParameters() # res is an instance of easyXML
	>>> # You can retreive XML from this instance of easyXML and print the content
        >>> # in a more human-readable way.
        >>> res.soup.findAll('id') # a Beautifulsoup instance is available
        >>> res.root # and the root using xml.etree.ElementTree

    There is a getitem so you can type::

        res['id']

    which is equivalent to::
        
        res.soup.findAll('id')

    There is also aliases findAll and prettify.

    """
    def __init__(self, data):
        """.. rubric:: Constructor

        :param data: an XML document format

        """
        self.data = data[:]
        self.root = ET.fromstring(data)
        self._soup = None
        self.prettify = self.soup.prettify
        self.findAll = self.soup.findAll

    def getchildren(self):
        """returns all children of the root XML document

        This is just an alias to self.soup.getchildren()
        """
        return self.root.getchildren()

    def _get_soup(self):
        if self._soup == None:
            self._soup = BeautifulSoup.BeautifulSoup(self.data)
        return self._soup
    soup = property(_get_soup, doc="Returns the beautiful soup instance")

    def __str__(self):
        txt = self.soup.prettify()
        return txt

    def __getitem__(self, i):
        return self.findAll(i)
        

