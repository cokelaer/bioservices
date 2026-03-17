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
"""Interface to some part of the Pfam web service

.. topic:: What is Pfam ?

    :URL: https://www.ebi.ac.uk/interpro/

    .. highlights::

        "Pfam is a large collection of protein families, each represented by
        multiple sequence alignments and hidden Markov models (HMMs)."

        -- From Pfam web site (help/about)


"""
from bioservices import logger
from bioservices.services import REST

logger.name = __name__

__all__ = ["Pfam"]


class Pfam:
    """Interface to `Pfam <https://www.ebi.ac.uk/interpro/>`_ pages

    This is not a REST interface but rather a parser to some of the
    HTML pages related to Pfam families.

    One can retrieve protein family information and associated sequences.

        >>> from bioservices import *
        >>> p = Pfam()

    """

    _url = "http://pfam.xfam.org/"

    def __init__(self, verbose=True):
        """**Constructor**

        :param bool verbose: set to False to prevent informative messages
        """
        self.services = REST(name="Pfam", url=Pfam._url, verbose=verbose)

    def show(self, Id):
        """Open the Pfam protein page for a UniProt ID in a web browser.

        :param str Id: a UniProt accession (e.g., ``"P43403"``)

        ::

            p = Pfam()
            p.show("P43403")

        """
        url = self._url + "/protein/" + Id
        self.services.on_web(url)

    def get_protein(self, ID, output="json"):
        """Retrieve protein information from Pfam.

        :param str ID: a UniProt accession (e.g., ``"P43403"``)
        :param str output: response format (default ``"json"``)
        :return: raw response content
        """
        res = self.services.http_get("protein", params={"id": ID, "output": output})
        return res.content
