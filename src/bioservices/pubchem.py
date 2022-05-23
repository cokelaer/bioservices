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
"""Interface to PubChem web service

.. topic:: What is PubChem ?

    :URL: http://pubchem.ncbi.nlm.nih.gov/pug_rest/

    .. highlights::

        TODO

        -- puchem web site, Oct 2014


"""
import sys

from bioservices.services import REST

__all__ = ["PubChem"]


class PubChem(REST):
    """Interface to the `PubChem <todo>`_ service"""

    _url = "http://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        print(
            "PubChem is not finalised yet. This is currently only a draft version",
            file=sys.stderr,
        )
        super(PubChem, self).__init__(name="PubChem", url=PubChem._url, verbose=verbose, cache=cache)

    def get_compound_by_smiles(self, identifier, frmt="json"):

        res = self.http_get(
            "compound/smiles/" + identifier + "/cids/%s" % frmt,
            frmt=frmt,
            headers=self.get_headers(content=frmt),
        )
        return res
