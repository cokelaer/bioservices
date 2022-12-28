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
"""Interface to HUGO/HGNC web services

.. topic:: What is HGNC ?

    :URL: http://www.genenames.org
    :Citation:

    .. highlights::

        "The HUGO Gene Nomenclature Committee (HGNC) has assigned unique gene symbols and
        names to over 37,000 human loci, of which around 19,000 are protein coding.
        genenames.org is a curated online repository of HGNC-approved gene nomenclature
        and associated resources including links to genomic, proteomic and phenotypic
        information, as well as dedicated gene family pages."

        -- From HGNC web site, July 2013


"""
from bioservices import REST
from bioservices.xmltools import bs4
import easydev
from bioservices import logger

logger.name = __name__


try:
    from urllib.error import HTTPError
except:
    from urllib2 import HTTPError


__all__ = ["HGNC"]


class HGNC:
    """Wrapper to the genenames web service


    See details at http://www.genenames.org/help/rest-web-service-help

    """

    def __init__(self, verbose=False, cache=False):
        url = "http://rest.genenames.org/"
        self.services = REST("HGNC", url=url, verbose=verbose, cache=cache)

        self._info = self.get_info()
        self.searchable_fields = self._info["searchableFields"]
        self.stored_fields = self._info["storedFields"]

    def get_info(self, frmt="json"):
        """Request information about the service

        Fields are when the server was last updated (lastModified),
        the number of documents (numDoc), which fields can be queried
        using search and fetch (searchableFields) and which fields may
        be returned by fetch (storedFields).


        """
        headers = self.services.get_headers(content=frmt)
        res = self.services.http_get("info", frmt=frmt, headers=headers)
        return res

    def fetch(self, database, query, frmt="json"):
        """Retrieve particular records from a searchable fields

        Returned object is a json object with fields as in
        :attr:`stored_field`, which is returned from :meth:`get_info` method.

        Only one query at a time. No wild cards are accepted.
        ::

            >>> h = HGNC()
            >>> h.fetch('symbol', 'ZNF3')
            >>> h.fetch('alias_name', 'A-kinase anchor protein, 350kDa')
        """
        easydev.check_param_in_list(database, self.searchable_fields)
        url = "fetch/{0}/{1}".format(database, query)
        headers = self.services.get_headers(content=frmt)
        res = self.services.http_get(url, frmt=frmt, headers=headers)
        return res

    def search(self, database_or_query=None, query=None, frmt="json"):
        """Search a searchable field (database) for a pattern

        The search request is more powerful than fetch for querying the
        database, but search will only returns the fields hgnc_id, symbol and
        score. This is because this tool is mainly intended to query the server
        to find possible entries of interest or to check data (such as your own
        symbols) rather than to fetch information about the genes. If you want
        to retrieve all the data for a set of genes from the search result, the
        user could use the hgnc_id returned by search to then fire off a fetch
        request by hgnc_id.

        :param database: if not provided, search all databases.


        ::

            # Search all searchable fields for the tern BRAF
            h.search('BRAF')

            # Return all records that have symbols that start with ZNF
            h.search('symbol', 'ZNF*')

            # Return all records that have symbols that start with ZNF
            # followed by one and only one character (e.g. ZNF3)
            # Nov 2015 does not work neither here nor in within in the
            # official documentation
            h.search('symbol', 'ZNF?')

            # search for symbols starting with ZNF that have been approved
            # by HGNC
            h.search('symbol', 'ZNF*+AND+status:Approved')

            # return ZNF3 and ZNF12
            h.search('symbol', 'ZNF3+OR+ZNF12')

            # Return all records that have symbols that start with ZNF which
            # are not approved (ie entry withdrawn)
            h.search('symbol', 'ZNF*+NOT+status:Approved')

        """
        if database_or_query is None and query is None:
            raise ValueError("you must provide at least one parameter")
        elif database_or_query is not None and query is None:
            # presumably user wants to search all databases
            query = database_or_query
            url = "search/{0}".format(query)
        else:
            database = database_or_query
            easydev.check_param_in_list(database, self.searchable_fields)
            url = "search/{0}/{1}".format(database, query)

        headers = self.services.get_headers(content=frmt)
        res = self.services.http_get(url, frmt=frmt, headers=headers)
        return res


