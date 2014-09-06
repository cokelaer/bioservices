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
"""Interface to the PDB web Service.

.. topic:: What is PDB ?

    :URL: http://www.rcsb.org/pdb/
    :REST: http://www.rcsb.org/pdb/software/rest.do

    .. highlights::

        An Information Portal to Biological Macromolecular Structures

        -- PDB home page, Feb 2013

    :Status: in progress not for production

"""
from __future__ import print_function

from bioservices.services import REST

__all__ = ["PDB"]


class PDB(REST):
    """Interface to part of the `PDB <http://www.rcsb.org/pdb>`_ service

    :Status: in progress not for production. You can get all ID and retrieve
        uncompressed file in PDB/FASTA formats for now. New features will be
        added on request.

    .. doctest::

        >>> from bioservices import PDB
        >>> s = PDB()
        >>> res = s.get_file("1FBV", "pdb")

    """

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages (default is off)

        """
        url="http://www.rcsb.org/pdb"
        super(PDB, self).__init__(name="PDB", url=url, verbose=verbose,
            cache=cache)
        self.easyXMLConversion = True

    def search(self, query):
        """
        <?xml version="1.0" encoding="UTF-8"?>
        <orgPdbQuery>
        <version>B0907</version>
        <queryType>org.pdb.query.simple.ExpTypeQuery</queryType>
        <description>Experimental Method Search : Experimental Method=SOLID-STATE NMR</description>
        <mvStructure.expMethod.value>SOLID-STATE NMR</mvStructure.expMethod.value>
        </orgPdbQuery>
        """
        res = self.http_post("search", frmt="", data=query)
        return res

    def get_current_ids(self):
        """Get a list of all current PDB IDs."""
        res = self.http_get("rest/getCurrent", frmt="xml")
        res = self.easyXML(res)
        res = [x.attrib['structureId'] for x in res.getchildren()]
        return res

    def get_file(self, sid, frmt, compression=False, headerOnly=False):
        """Download a file in a specified format

        :param int Id: a valid Identifier. See :meth:`get_current_ids`.
        :param str fileFormat: a valid format in "pdb", "cif", "xml"

        .. doctest::

            >>> from bioservices import PDB
            >>> s = PDB()
            >>> res = s.get_file("1FBV", "pdb")
            >>> import tempfile
            >>> fh = tempfile.NamedTemporaryFile()
            >>> fh.write(res)
            >>> # manipulate the PDB file with your favorite tool
            >>> # close the file ONLY when finished (this is temporary file)
            >>> # fh.close()

        reference: http://www.rcsb.org/pdb/static.do?p=download/http/index.html
        """
        valid_formats = [ "pdb", "cif", "xml"]
        self.devtools.check_param_in_list(frmt, valid_formats)
        self.devtools.check_param_in_list(headerOnly, [True, False])
        if headerOnly == True:
            headerOnly = "YES"
        else:
            headerOnly = "NO"

        query = "files/" + sid + "." + frmt
        if compression == True:
            query += ".gz"

        params = {'headerOnly': headerOnly}

        if frmt == "xml":
            res = self.http_get(query, frmt=frmt, params=params)
            if compression == False:
                res = self.easyXML(res)
        else:
            res = self.http_get(query, frmt="txt", params=params)
        return res

