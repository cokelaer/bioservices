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
#$Id: xmltools.py 230 2013-07-09 17:12:59Z cokelaer $
"""This module includes common tools to manipulate HTML files"""
from __future__ import print_function
from HTMLParser import HTMLParser

__all__ = ["easyHTML"]




class easyHTML(HTMLParser):
    """class to ease the introspection of XML documents.


    """
    def __init__(self, url=None, data=None, filename=None):
        """.. rubric:: Constructor

        :param data: an XML document format
        :param fixing_unicode: use only with HGNC service to fix issue with the
            XML returned by that particular service. No need to use otherwise.
            See :class:`~bioservices.hgnc.HGNC` documentation for details.
        :param encoding: default is utf-8 used. Used to fix the HGNC XML only.

        """
        # cannot use super with HTMLParser
        #super(easyHTML, self).__init__()
        HTMLParser.__init__(self)
        if url and data or url and filename or filename and data:
            raise ValueError("only 1 argument must be provided")
        if url:
            import urllib2
            html = urllib2.urlopen(url, "r")
            self.data = html.read()
        elif data:
            self.data = data[:]
        elif filename:
            self.data = open(filename, "r").read()
        else:
            raise ValueError("at least 1 argument must be provided")

        self.feed(self.data)



