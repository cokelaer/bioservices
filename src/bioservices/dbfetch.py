#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to DBFetch web service

.. topic:: What is DBFetch

    :URL: http://www.ebi.ac.uk/Tools/webservices/services/dbfetch
    :Service: http://www.ebi.ac.uk/Tools/webservices/services/dbfetch_rest

    .. highlights::

        "DBFetch allows you to retrieve entries from various up-to-date biological
        databases using entry identifiers or accession numbers. This is equivalent to
        the CGI based dbfetch service. Like the CGI service a request can return a
        maximum of 200 entries."

        -- From http://www.ebi.ac.uk/Tools/webservices/services/dbfetch , Dec 2012


"""
from bioservices import logger
from bioservices.services import REST

logger.name = __name__


__all__ = ["DBFetch"]


class DBFetch:
    """Interface to `DBFetch <http://www.ebi.ac.uk/Tools/webservices/services/dbfetch_rest>`_ service

    ::

        >>> from bioservices import DBFetch
        >>> w = DBFetch()
        >>> data = w.fetchBatch("uniprot" ,"zap70_human", "xml", "raw")

    For more information about the API, check this page:
    http://www.ebi.ac.uk/Tools/dbfetch/syntax.jsp

    """

    _url = "http://www.ebi.ac.uk/Tools/dbfetch"

    def __init__(self, verbose=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages
        """

        self.services = REST(name="DBfetch", url=DBFetch._url, verbose=verbose)
        self._supportedDBs = None
        self._supportedFormats = None
        self._supportedStyles = None

    def _check_db(self, db):
        if db not in self.supported_databases:
            raise Exception("%s not a supportedDB. " % db)

    def fetch(self, query, db="ena_sequence", format="default", style="raw", pageHtml=False):
        """Fetch an entry in a defined format and style.

        :param str query: the entry identifier in db:id format (e.g. ``'UniProtKB:WAP_RAT'``)
        :param str db: database name (default ``"ena_sequence"``)
        :param str format: the name of the format required (default ``"default"``)
        :param str style: the name of the style required: ``"raw"``, ``"default"``, or ``"html"``
        :param bool pageHtml: if True, return the result wrapped in an HTML page
        :return: entry data; format depends on the format/style parameters

        ::

            from bioservices import DBFetch
            u = DBFetch()
            u.fetch(db="ena_sequence", format="fasta", query="L12344,L12345")
            u.fetch(db="uniprot", format="fasta", query="P53503")

        If *db* is omitted, the default is ``ena_sequence``.
        If *format* is omitted, the default is EMBL format.
        The default style is raw data.

        """
        self._check_db(db)
        res = self.services.http_get(
            "dbfetch",
            params={
                "db": db,
                "format": format,
                "style": style,
                "id": query,
                "pageHtml": pageHtml,
            },
        )
        try:
            res = res.content.decode()
        except Exception:
            pass
        return res

    def get_database_info(self, db=None):
        """Get details describing specific database (data formats, styles)

        :param str db: a valid database.
        :return: dict describing the database; can be introspected for formats, styles, etc.

        ::

            >>> res = u.get_database_info('uniprotkb')
            >>> print(res['description'])
            'The UniProt Knowledgebase (UniProtKB) is the central access point for extensive curated protein information, including function, classification, and cross-references. Search UniProtKB to retrieve everything that is known about a particular sequence.'

        """
        res = self.services.http_get("dbfetch/dbfetch.databases?style=json")
        if db:
            self._check_db(db)
            res = res[db]
        return res

    def get_all_database_info(self):
        """Get details of all available databases, including formats and result styles.

        :return: a dict of data structures describing the databases. See
            :meth:`get_database_info` for a description of each entry.
        """
        return self.get_database_info()

    def get_database_formats(self, db):
        """Get list of format names for a given database.

        :param str db: valid database name

        ::

            >>> db.get_database_formats("uniprotkb")
            ['default',
             'annot',
             'entrysize',
             'fasta',
             'gff3',
             'seqxml',
             'uniprot',
             'uniprotrdfxml',
             'uniprotxml',
             'dasgff',
             'gff2']

        """
        self._check_db(db)
        res = self.services.http_get("dbfetch?info=formats&db={}".format(db)).content
        res = res.decode().split()
        return res

    def get_database_format_styles(self, db, format):
        """Get a list of style names available for a given database and format.

        :param str db: database name to get available styles for (e.g. uniprotkb).
        :param str format: the data format to get available styles for (e.g. fasta).

        :return: list of style name strings

        ::

            >>> u.get_database_format_styles("uniprotkb", "fasta")
            ['default', 'raw', 'html']

        """
        self._check_db(db)
        res = self.services.http_get("dbfetch?info=styles&format={}&db={}".format(format, db)).content
        res = res.decode().split()
        return res

    def _getSupportedDBs(self):
        """Get a list of database names usable with DBFetch.

        Result is buffered in ``_supportedDBs``.
        """
        if self._supportedDBs:
            return self._supportedDBs
        else:
            res = self.services.http_get("dbfetch?info=dbs").content
            self._supportedDBs = res.decode().split() + ["default"]
        return self._supportedDBs

    supported_databases = property(_getSupportedDBs, doc="Alias to getSupportedDBs.")
