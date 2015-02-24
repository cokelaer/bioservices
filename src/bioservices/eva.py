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
# $Id$
"""Interface to some part of the EVA web service

.. topic:: What is EVA ?

    :URL: http://www.uniprot.org
    :Citation:

    .. highlights::

        "The European Variation Archive is an open-access database of all
        types of genetic variation data from all species. The EVA provides
        access to highly detailed, granular, raw variant data from human, with
        other species to follow."

        -- From Uniprot web site (help/about) , Dec 2012


"""
import types
import io

from bioservices.services import REST
try:
    import pandas as pd
except:
    print("pandas library is not installed. Not all functionalities will be  available")

__all__ = ["EVA"]



class EVA(REST):
    """Interface to the `EVA <http://www.ebi.ac.uk/eva>`_ service


    * version: indicates the version of the API, this defines the available
      filters and JSON schema to be returned. Currently there is only
      version 'v1'.
    * category: this defines what objects we want to query. Currently there
      are five different categories: variants, segments, genes, files and
      studies.
    * resource: specifies the resource to be returned, therefore the JSON
      data model.
    * filters: each specific endpoint allows different filters. 
    """
    _url = "http://wwwdev.ebi.ac.uk/eva/webservices/rest/"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(EVA, self).__init__(name="EVA", url=EVA._url,
                verbose=verbose, cache=cache)
        self.version = "v1"

    def fetch_allinfo(self, name):
        """e.g., PRJEB4019"""
        res = self.http_get(self.version + "/studies/" + name +"/summary")
        return res
