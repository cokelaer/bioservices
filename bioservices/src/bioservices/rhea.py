# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#
##############################################################################
"""Interface to the Rhea web services

.. topic:: What is Rhea ?

    :URL: http://www.ebi.ac.uk/rhea/

    .. highlights::

        Rhea is a freely available, manually annotated database of chemical
        reactions created in collaboration with the Swiss Institute of Bioinformatics
        (SIB). All data in Rhea is freely accessible and available for anyone to
        use. 

        -- from Rhea Home page, Dec 2012



.. rubric:: Quick example:

Searching for caffein will find reactions with participants such as caffeine,
trans-caffeic acid or caffeoyl-CoA.

.. doctest::

    >>> from bioservices import Rhea
    >>> r = Rhea()
    >>> response = r.search("caffein")

"""


import urllib2
from services import RESTService




class Rhea(RESTService):
    """Interface to the `Rhea <http://www.ebi.ac.uk/rhea/rest/1.0/>`_ service

    You can search by compound name, ChEBI ID, reaction ID, cross reference
    (e.g. EC number) or citation (author name, title, abstract text, publication ID).
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
    def __init__(self, version="1.0",  verbose=True,
        url="http://www.ebi.ac.uk/rhea/rest"):

        """.. rubric:: Rhea constructor

        :param str url: should not be used in principle.
        :param str version: the current version of the interface (1.0)
        :param bool verbose: True by default

        ::

            >>> from bioservices import Rhea
            >>> r = Rhea()
        """

        super(Rhea, self).__init__(name="Rhea", url=url, 
            verbose=verbose)
        self.version = version
        self.format_entry = ["cmlreact", "biopax2", "rxn"]

    def search(self, query, format=None):
        """Search for reactions

        :param str query: the search term using format parameter
        :param str format: the biopax2 or cmlreact format (default)


        :Returns: an XML document containing the reactions with undefined
            direction, with links to the corresponding bi-directional ones.
            the format is easyXML.

        ::

            >>> r = Rhea()
            >>> r.search("caffeine")  # id 10280
            >>> r.search("caffeine", format="biopax2")  # id 10280

        The output is in XML format. This page from the Rhea web site explains 
        what are the `data fields <http://www.ebi.ac.uk/rhea/manual.xhtml>`_ of 
        the XML file.

        """
        _format = format    # format is a keyword but we want to use it so rhea
                            # users are not confused.
        if _format == None:
            _format = "cmlreact" # default is cmlreact
        if _format not in ["biopax2", "cmlreact"]:
            raise ValueError("format must be either cmlreact (default) or biopax2")

        url = self.url + "/" + self.version + "/ws/reaction/%s?q=" % _format
        url += query

        response = self.request(url)
        return response


    def entry(self, id, format):
        """Retrieve a concrete reaction for the given id in a given format

        :param int id: the id of a reaction
        :param format: can be rxn, biopax2, or cmlreact
        :Returns: an XML document containing the reactions with undefined
            direction, with links to the corresponding bi-directional ones.
            the format is easyXML.

        ::

            >>> print r.entry(10280)

        The output is in XML format. This page from the Rhea web site explains 
        what are the `data fields <http://www.ebi.ac.uk/rhea/manual.xhtml>`_ of 
        the XML file.
        """
        if format not in self.format_entry:
            raise ValueError("format is incorrect (%s). Must be one of\
                %s" % (format, str(self.format_entry)))
        url = self.url + "/" + self.version + "/ws/reaction/%s/%s" % (format, id)

        if format=="rxn":
            save = self.easyXMLConversion
            try:
                self.easyXMLConversion = False
                response = self.request(url)
            except:
                pass
            finally:
                self.easyXMLConversion = save
        else:
            response = self.request(url)
        return response





