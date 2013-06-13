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
#$Id: kegg.py 156 2013-02-17 22:45:39Z cokelaer $
"""Interface to the ArrayExpress web Service.

.. topic:: What is ChemSpider ?


    :Status: in progress
    :URL:  http://www.chemspider.com/
    :REST: http://www.chemspider.com/AboutServices.aspx?

    .. highlights::

        ChemSpider is a free chemical structure database providing fast access to 
        over 28 million structures, properties and associated information. By 
        integrating and linking compounds from more than 400 data sources, ChemSpider 
        enables researchers to discover the most comprehensive view of freely 
        available chemical data from a single online search. It is owned by the Royal Society of Chemistry.

        -- ChemSpider home page, March 2013
"""
from bioservices import RESTService


class ChemSpider(RESTService):
    """ChemSpider Web Service Interface

    :status: in progress you can already search for Id and compound or 
        retrieve the chemical image of an Id


    ::

        >>> from bioservices import *
        >>> s = ChemSpider()
        >>> s.find("Pyridine")
        1020
        >>> results = s.GetExtendedCompoundInfo(1020)
        >>> results['averagemass']
        79.0999


    """
    def __init__(self, verbose=False, token=None):
        if token == None:
            import services
            try:
                token = services.get_bioservices_env("chemspider", "token")
            except Exception,e:
                raise Exception(e)
        self._token = None
        self.token = token
        url = 'http://www.chemspider.com/'
        super(ChemSpider, self).__init__("ChemSpider", url=url, verbose=verbose)
        self._databases = None

    def _set_token(self, token):
        self._token = token
    token = property(None, _set_token)

    def find(self, query):
        """return the first 100 compounds that match the query"""
        import urllib2
        this = "Search.asmx/SimpleSearch?query=%s&token=%s" % (urllib2.quote(query), self._token)
        res = self.request(this)
        Ids = [int(x.text) for x in res.findAll("int")]
        return Ids

    def GetExtendedCompoundInfo(self, Id):
        url = self.url + "/MassSpecAPI.asmx/GetExtendedCompoundInfo?CSID=%s&token=%s" % (Id, self._token) 
        res = self.request(url)

        results = {}
        data = [(x.tag, x.text) for x in res.getchildren()]
        for datum in data:
            tag, value = datum
            ID = tag.split("{http://www.chemspider.com/}")[1]
            try:
                value = float(value)
            except:
                pass
            results[ID.lower()] = value
        return results

    def ImagesHandler(self, Id):
        url = self.url + "/ImagesHandler.ashx?id=%s"  % Id
        res = self.request(url)
        return res

    def image(self, Id):
        """ Return string containing PNG binary image data of 2D structure image 

        ::

            >>> from bioservices import *
            >>> s = ChemSpider()
            >>> ret = s.image(1020)
            >>> with open("test.png", "w") as f:
            ...     f.write(ret)
            >>> s.onWeb("test.png")
        """
        url = self.url + "/Search.asmx/GetCompoundThumbnail?id=%s&token=%s" % (Id, self._token)
        res = self.request(url)
        import base64
        image = base64.b64decode(res.root.text)
        return image

    def mol(self, Id):
        """ Return record in MOL format """
        url = self.url + '/MassSpecAPI.asmx/GetRecordMol?csid=%s&calc3d=false&token=%s' % (Id, self._token)
        ret = self.request(url)
        return ret.root.text

    def mol3d(self, Id):
        """ Return record in MOL format with 3D coordinates calculated """
        url = '/MassSpecAPI.asmx/GetRecordMol?csid=%s&calc3d=true&token=%s' % (Id, self._token)
        ret = self.request(url)
        return ret.root.text

    def _get_databases(self):
        if self._databases == None:
            ret = self.request("/MassSpecAPI.asmx/GetDatabases?")
            self._databases = [x.text for x in ret.getchildren()]
            print self._databases
        return self._databases
    databases = property(_get_databases, doc="Returns databases searched for in chemSpider")

