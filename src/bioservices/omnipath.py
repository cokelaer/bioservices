# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      https://github.com/cokelaer/bioservices
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  source: http://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to OmniPath web service

.. topic:: What is OmniPath ?

    :URL: http://omnipathdb.org
    :URL: https://github.com/saezlab/pypath/blob/master/webservice.rst

    .. highlights::

        A comprehensive collection of literature curated human signaling pathways.

        -- From OmniPath web site, March 2016


"""
from bioservices import REST



class OmniPath(REST):
    """Interface to the `OmniPath <http://www.ebi.ac.uk/unichem/>`_ service

    .. doctest::

            >>> from bioservices import OmniPath
            >>> o = OmniPath()
            >>> net = o.get_network()

    """

    _url = "http://omnipathdb.org/"

    def __init__(self, verbose=False, cache=False):
        """**Constructor** OmniPath

        :param verbose: set to False to prevent informative messages
        """
        super(OmniPath, self).__init__(name="OmniPath", url=OmniPath._url,
            verbose=verbose, cache=cache)


    def get_about(self):
        """Information about the version"""
        res = self.http_get(self.url + "about").content
        return res

    def get_network(self):
        """Get basic statistics about the whole network"""
        res = self.http_get(o.url + "network")
        return res

    def get_interactions(self, entry="", frmt='json', fields=[]):
        """Interactions of proteins

        :param str query: a valid uniprot identifier (e.g. P00533). It can also
            be a list of uniprot identifiers, or a string with
            comma-separated identifiers.
        :param str ptm_type: restrict the output to this type of PTM
            (e.g., phosphorylation)
        :param str fields: additional fields to be added to the output
            (e.g., sources, references)
        :param str frmt: format of the output (json or tabular)


        Example::

            res_one = o.get_interactions('P00533')
            res_many = o.get_interactions('P00533,O15117,Q96FE5')
        """
        # make sure there is no spaces
        query = query.replace(' ', '')
        assert frmt in ["json", ""]
        params = {}
        params['format'] = frmt
        #TODO handle multiple fields
        res = self.http_get(o.url + "interactions/%s" % entry,
            frmt='json', params=params)
        return res

    def get_resources(self):
        res = self.http_get(o.url + "resources")
        return res.content

    def get_info(self):
        """Currently returns HTML page"""
        res = self.http_get(o.url + "info")
        return res.content

    def get_ptms(self, query="", ptm_type=None, fields=[]):
        """List enzymes, substrates and PTMs

        :param str query: a valid uniprot identifier (e.g. P00533). It can also
            be a list of uniprot identifiers, or a string with
            comma-separated identifiers.
        :param str ptm_type: restrict the output to this type of PTM
            (e.g., phosphorylation)
        :param str fields: additional fields to be added to the output
            (e.g., sources, references)


        """
        res = self.http_get(o.url + "ptms/%s" % entry,
            frmt='json', params=params)
        return res


















