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

.. topic:: What is ArrayExpress ?

    :URL: http://www.ebi.ac.uk/arrayexpress/
    :REST: http://www.ebi.ac.uk/arrayexpress/xml/v2/experiments

    .. highlights::

        ArrayExpress is a database of functional genomics experiments that can be queried and the data downloaded. It includes gene expression data from microarray and high throughput sequencing studies. Data is collected to MIAME and MINSEQE standards. Experiments are submitted directly to ArrayExpress or are imported from the NCBI GEO database. 

        -- ArrayExpress home page, Jan 2013

"""
from __future__ import print_function

from bioservices.services import RESTService, BioServicesError


__all__ = ["ArrayExpress"]

class ArrayExpress(RESTService):
    """Interface to the `ArrayExpress <"http://www.ebi.ac.uk/arrayexpress">`_ database

     ::

         >>> from bioservices import Kegg
         >>> s = ArrayExpress()
         >>> res = s.retrieveExperiments(keywords="cancer+breast", wholewords=True)

    * Accession number and keyword searches are case insensitive
    * phrases of more than one word must be entered in quotes e.g. "breast cancer cells"
    * More than one keyword can by searched for using the + sign (e.g. keywords="cancer+breast")
    * Use an asterisk as a multiple chracter wild card (e.g. keywords="colo*")
    * use a question mark ? as a signle character wild card (e.g. keywords="te?t")
 
    More complex queries can be constructed using the operators AND, OR or NOT. AND is the default if no operator is specified. Again, either experiments or files can be searched for in all cases by using the 'experiments' or 'files' term in the URL.::

        keywords=prostate+AND+breast
        keywords=prostate+breast (same as above)
        keywords=prostate+OR+breast
        keywords=prostate+NOT+breast 


    .. warning:: supports only new style (v2). You can still use the old style by 
        setting the request manually using the :meth:`request`.

    """
 
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages

        """
        super(ArrayExpress, self).__init__(name="ArrayExpress", 
            url="http://www.ebi.ac.uk/arrayexpress/", verbose=verbose)
        self.easyXMLConversion = True
        self._format = "xml"
        
    def _set_format(self, f):
        self.checkParam(f, ["json", "xml"])
        self._format = f
    def _get_format(self):
        return self._format
    format = property(_get_format, _set_format)

    def _search(self, mode, **kargs):
        assert mode in ["experiments","files"]
        url = self.url + "/" + self.format + "/v2/" + mode + "?"

        accession = kargs.get("accession", None)
        array = kargs.get("array", None)
        wholewords = kargs.get("wholewords", False)
        ef = kargs.get("ef", None)
        efv = kargs.get("efv", None)
        expdesign = kargs.get("expdesign", None)
        exptype = kargs.get("exptype", None)
        gxa = kargs.get("gxa", None)
        pmid = kargs.get("pmid", None)
        sa = kargs.get("sa", None)
        species = kargs.get("species", None)
        expandefo = kargs.get("expandefo", False)
        directsub = kargs.get("directsub", False)
        keywords = kargs.get("keywords", "")

        url += "keywords=" + keywords
        print(url)
        res = self.request(url)
        return res


    def retrieveFiles(self, **kargs):
        """Retrieve a list of files associated with a set of experiments

        :param str keywords: e.g. "cancer+breast"
        :param str species: e.g. Homo+Sapiens
        :param bool wholewords: 

        ::

            >>> res = a.retrieveFiles(keywords="cancer+breast", wholewords=True)

        """
        res = self._search("files", **kargs)
        return res


    def retrieveExperiments(self, **kargs):
        """Retrieve experiments

        :param str experiment: if provided, other parameters are ignored and i
            experiment must be a particular experiment e.g. E-MEXP-31
        :param str keywords: e.g. "cancer+breast"
        :param str species: e.g. Homo+Sapiens
        :param bool wholewords: 

        ::

            >>> res = a.retrieveExperiments(keywords="cancer+breast", wholewords=True)

        """
        res = self._search("files", **kargs)
        return res


