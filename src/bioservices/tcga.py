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
"""Interface to the quickGO interface

.. topic:: What is quickGO

    :URL: http://www.ebi.ac.uk/QuickGO/
    :Service: http://www.ebi.ac.uk/QuickGO/WebServices.html

    .. highlights::

        "QuickGO is a fast web-based browser for Gene Ontology terms and
        annotations, which is provided by the UniProt-GOA project at the EBI. "

        -- from QuickGO home page, Dec 2012

"""
from __future__ import print_function

from bioservices.services import REST

__all__ = ["TCGA"]


class TCGA(REST):
    """Interface to the `TCGA`_ service

    DRAFT in progress

    https://wiki.nci.nih.gov/display/TCGA/TCGA+Annotations+Web+Service+User%27s+Guide

    """
    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages.

        """
        super(TCGA,
                self).__init__(url="http://tcga-data.nci.nih.gov",
            name="TCGA", verbose=verbose, cache=cache)

    def search_annotations(self, item, annotationId):
        """Obtain Term information

        """
        params = {'item':item, 'annotationId': annotationId}
        res = self.http_get("annotations/resources/searchannotations/json", 
                frmt="json", params=params)

        return res


    def view_annotations(self):
        raise NotImplementedError





