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
"""Interface to WSDbfetch web service

.. topic:: What is WSDbfetch

    :URL: http://www.ebi.ac.uk/Tools/webservices/services/dbfetch
    :Service: http://www.ebi.ac.uk/Tools/webservices/services/dbfetch_rest

    .. highlights::

        "WSDbfetch allows you to retrieve entries from various up-to-date biological
        databases using entry identifiers or accession numbers. This is equivalent to
        the CGI based dbfetch service. Like the CGI service a request can return a
        maximum of 200 entries."

        -- From http://www.ebi.ac.uk/Tools/webservices/services/dbfetch , Dec 2012


"""
from bioservices.services import WSDLService




class WSDbfetch(WSDLService):
    """Interface to `WSDbfetch <http://www.ebi.ac.uk/Tools/webservices/services/dbfetch_rest>`_ service

    ::

        >>> from bioservices import WSDbfetch
        >>> w = WSDbfetch()
        >>> data = w.fetchBatch("uniprot" ,"zap70_human", "xml", "raw")

    The actual URL used is http://www.ebi.ac.uk/ws/services/WSDbfetchDoclit?wsdl from
    biocatalogue (this one having let functionalities: 
    http://www.ebi.ac.uk/ws/services/WSDbfetch?wsdl).

    """
    _url = 'http://www.ebi.ac.uk/ws/services/WSDbfetchDoclit?wsdl'
    def __init__(self,  verbose=False):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages
        """
        super(WSDbfetch, self).__init__(name="WSDbfetch", url=WSDbfetch._url, 
            verbose=verbose)
        self._supportedDBs = None
        self._supportedFormats = None
        self._supportedStyles = None

    def _check_db(self, db):
        if db not in self.supportedDBs:
            raise Exception("%s not a supportedDB. " %db)


    def fetchBatch(self, db, ids, format="default", style="default"):
        """Fetch a set of entries in a defined format and style.

        :param str db: the name of the database to obtain the entries from (e.g. 'uniprotkb').
        :param list query: list of identifiers (e.g. 'wap_rat, wap_mouse').
        :param str format: the name of the format required. 
        :param str style: the name of the style required. 

        :returns: The format of the response depends on the interface to the service used:

            * WSDBFetchServerService and WSDBFetchDoclitServerService: The entries as a string.
            * WSDBFetchServerLegacyService: An array of strings containing the entries. 


        ::

            from bioservices import WSDbfetch
            u = WSDbfetch()
            u.fetchBatch("uniprot" ,"wap_mouse", "xml")

        """
        res = self.serv.fetchBatch(db, ids, format, style)
        res = self.easyXML(res)
        return res

    def fetchData(self, query, format="default", style="default"):
        """Fetch an entry in a defined format and style.

        :param str query: the entry identifier in db:id format (e.g. 'UniProtKB:WAP_RAT').
        :param str format: the name of the format required. 
        :param str style: the name of the style required. 

        :returns: The format of the response depends on the interface to the service used:

            * WSDBFetchServerService and WSDBFetchDoclitServerService: The entries as a string.
            * WSDBFetchServerLegacyService: An array of strings containing the entries. Generally 
              this will contain only one item which contains the set of entries.

        ::

            from bioservices import WSDbfetch
            u = WSDbfetch()
            u.fetchData('uniprot:zap70_human')

        """
        res = self.serv.fetchData(query, format, style)
        return res


    def getDatabaseInfo(self, db):
        """Get details describing specific database (data formats, styles)

        :param str db: a valid database. 
        :return: The output can be introspected and contains several attributes
            (e.g., displayName).

        :: 

            >>> res = u.getDatabaseInfo("uniprotkb")
            >>> res.displayName
            'UniProtKB'
            >>> print(res.description.encode('utf-8'))
            u'The UniProt Knowledgebase (UniProtKB) is the central access point for extensive curated protein information, including function, classification, and cross-references. Search UniProtKB to retrieve \u201ceverything that is known\u201d about a particular sequence.'

        """
        self._check_db(db)
        return self.serv.getDatabaseInfo(db)

    def getDatabaseInfoList(self):
        """Get details of all available databases, includes formats and result styles.

        :Returns: A list of data structures describing the databases. See
            :meth:`getDatabaseInfo` for a description of the data structure.
        """
        return self.serv.getDatabaseInfoList()

    def getDbFormats(self, db):
        """Get list of format names for a given database.


        :param str db:

        """
        self._check_db(db)
        return self.serv.getDbFormats(db)
    

    def getFormatStyles(self, db, format):
        """Get a list of style names available for a given database and format.

        :param str db: database name to get available styles for (e.g. uniprotkb).
        :param str format: the data format to get available styles for (e.g. fasta).

        :Returns: An array of strings containing the style names. 

        ::

            >>> u.getFormatStyles("uniprotkb", "fasta")
            ['default', 'raw', 'html']
        """

        self._check_db(db)
        return self.serv.getFormatStyles(db, format)

    def getSupportedDBs(self):
        """Get a list of database names usable with WSDbfetch. 

        Buffered in _supportedDB.
        """
        if self._supportedDBs:
            return self._supportedDBs
        else:
            self._supportedDBs = self.serv.getSupportedDBs()
        return self._supportedDBs

    supportedDBs = property(getSupportedDBs, doc="Alias to getSupportedDBs.")

    def getSupportedFormats(self):
        """Get a list of database and format names usable with WSDbfetch.

        .. deprecated:: use Of getDbFormats(db), getDatabaseInfo(db) or  getDatabaseInfoList().



        """
        if self._supportedFormats is None:
            self._supportedFormats = self.serv.getSupportedFormats()
        return self._supportedFormats
    supportedFormats = property(getSupportedFormats)

    def getSupportedStyles(self):
        """Get a list of database and style names usable with WSDbfetch.

        .. deprecated:: use Of getFormatStyles(db, format), getDatabaseInfo(db) or         getDatabaseInfoList() is recommended.

        Returns: An array of strings containing the database and style names. 
        """
        if self._supportedStyles is None:
            self._supportedStyles = self.serv.getSupportedStyles()
        return self._supportedStyles
    supportedStyles = property(getSupportedStyles)




