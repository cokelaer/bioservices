#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EMBL-EBI
#
#  File author(s):
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
"""This module includes common tools to manipulate XML files"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import bs4

try:
    from urllib.request import urlopen
except:
    from urllib2 import urlopen

__all__ = ["easyXML", "readXML"]


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
    def __init__(self, data, encoding="utf-8"):
        """.. rubric:: Constructor

        :param data: an XML document format
        :param fixing_unicode: use only with HGNC service to fix issue with the
            XML returned by that particular service. No need to use otherwise.
            See :class:`~bioservices.hgnc.HGNC` documentation for details.
        :param encoding: default is utf-8 used. Used to fix the HGNC XML only.


        The data parameter must be a string containing the XML document. If you
        have an URL instead, use :class:`readXML`

        """
        #if fixing_unicode:
        #    x = unicodefix.FixingUnicode(data, verbose=False, encoding=encoding)
        #    self.data = x.fixed_string.encode("utf-8")
        #else:
        self.data = data[:]

        try:
            self.root = ET.fromstring(self.data)
        except:
            self.root = self.data[:]
        self._soup = None
        self.prettify = self.soup.prettify
        self.findAll = self.soup.findAll

    def getchildren(self):
        """returns all children of the root XML document

        This is just an alias to self.soup.getchildren()
        """
        return self.root.getchildren()

    def _get_soup(self):
        if self._soup is None:
            self._soup = bs4.BeautifulSoup(self.data, "html.parser")
        return self._soup
    soup = property(_get_soup, doc="Returns the beautiful soup instance")

    def __str__(self):
        txt = self.soup.prettify()
        return txt

    def __getitem__(self, i):
        return self.findAll(i)


class readXML(easyXML):
    """Read XML and converts to beautifulsoup data structure

    easyXML accepts as input a string. This class accepts a filename instead
    inherits from easyXML

    .. seealso:: :class:`easyXML`

    """
    def __init__(self, url, encoding="utf-8"):
        self.data = urlopen(url).read()
        super(readXML, self).__init__(self.data, encoding)


class XMLObjectify(object):
    def __init__(self, obj):
        """obj can be easyXML data set"""
        from lxml import objectify
        try:
            self.root = objectify.fromstring(obj.data)
        except:
            # try something else
            self.root = objectify.fromstring(obj)
        self.obj = obj

    def __str__(self):
        txt = ""
        for child in self.root.getchildren():
            txt += child.tag + "\n"
        return txt
