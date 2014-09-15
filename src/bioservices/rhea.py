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
#$Id$
"""Interface to the Rhea web services

.. topic:: What is Rhea ?

    :URL: http://www.ebi.ac.uk/rhea/
    :Citations: See http://www.ebi.ac.uk/rhea/about.xhtml

    .. highlights::

        Rhea is a reaction database, where all reaction participants (reactants
        and products) are linked to the ChEBI database (Chemical Entities of
        Biological Interest) which provides detailed information about structure,
        formula and charge. Rhea provides built-in validations that ensure both
        elemental and charge balance of the reactions... While the main focus of
        Rhea is enzyme-catalysed reactions, other biochemical reactions are also
        are included.

        The database is extensively cross-referenced. Reactions are currently linked
        to the EC list, KEGG and MetaCyc, and the reactions will be used in the
        IntEnz database and in all relevant UniProtKB entries. Furthermore, the
        reactions will also be used in the UniPathway database to generate
        pathways and metabolic networks.

        -- from Rhea Home page, Dec 2012 (http://www.ebi.ac.uk/rhea/about.xhtml)

"""
from __future__ import print_function

from bioservices.services import REST

__all__ = ["Rhea"]



class Rhea(REST):
    """Interface to the `Rhea <http://www.ebi.ac.uk/rhea/rest/1.0/>`_ service

    You can search by compound name, ChEBI ID, reaction ID, cross reference
    (e.g., EC number) or citation (author name, title, abstract text, publication ID).
    You can use double quotes - to match an exact phrase - and the following
    wildcards:

        * ? (question mark = one character),
        * `*` (asterisk = several characters).

    Searching for caffe* will find reactions with participants such as caffeine,
    trans-caffeic acid or caffeoyl-CoA::

        from bioservices import Rhea
        r = Rhea()
        response = r.search("caffe*")

    Searching for a?e?o* will find reactions with participants such as acetoin,
    acetone or adenosine.::

        from bioservices import Rhea
        r = Rhea()
        response = r.search("a?e?o*")

    See :meth:`search` :meth:`entry` methods for more information about format.

    """
    _url = "http://www.ebi.ac.uk/rhea/rest"
    def __init__(self, version="1.0",  verbose=True, cache=False):
        """.. rubric:: Rhea constructor

        :param str version: the current version of the interface (1.0)
        :param bool verbose: True by default

        ::

            >>> from bioservices import Rhea
            >>> r = Rhea()
        """
        super(Rhea, self).__init__(name="Rhea", url=Rhea._url,
            verbose=verbose, cache=cache)
        self.version = version
        self.format_entry = ["cmlreact", "biopax2", "rxn"]

    def search(self, query, frmt=None):
        """Search for reactions

        :param str query: the search term using format parameter
        :param str format: the biopax2 or cmlreact format (default)

        :Returns: An XML document containing the reactions with undefined
            direction, with links to the corresponding bi-directional ones.
            The format is easyXML.

        ::

            >>> r = Rhea()
            >>> r.search("caffeine")  # id 10280
            >>> r.search("caffeine", frmt="biopax2")  # id 10280

        The output is in XML format. This page from the Rhea web site explains
        what are the `data fields <http://www.ebi.ac.uk/rhea/manual.xhtml>`_ of
        the XML file.

        """
        if frmt is None:
            frmt = "cmlreact" # default is cmlreact
        if frmt not in ["biopax2", "cmlreact"]:
            raise ValueError("format must be either cmlreact (default) or biopax2")

        url = self.version + "/ws/reaction/%s?q=" % frmt
        url += query

        response = self.http_get(url, frmt="xml")
        response = self.easyXML(response)
        return response


    def entry(self, id, frmt):
        """Retrieve a concrete reaction for the given id in a given format

        :param int id: the id of a reaction
        :param format: can be rxn, biopax2, or cmlreact
        :Returns: An XML document containing the reactions with undefined
            direction, with links to the corresponding bi-directional ones.
            The format is easyXML. If frmt is rnx,

        ::

            >>> print r.entry(10281, frmt="rxn")

        The output is in XML format. This page from the Rhea web site explains
        what are the `data fields <http://www.ebi.ac.uk/rhea/manual.xhtml>`_ of
        the XML file.
        """
        self.devtools.check_param_in_list(frmt, self.format_entry)
        url = self.version + "/ws/reaction/%s/%s" % (frmt, id)

        if frmt=="rxn":
            response = self.http_get(url, frmt=frmt)
        else:
            response = self.http_get(url, frmt="xml")
            response = self.easyXML(response)
        return response





