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
from easydev import to_list
from bioservices import logger

logger.name = __name__


class OmniPath(REST):
    """Interface to the `OmniPath <http://www.ebi.ac.uk/unichem/>`_ service

    .. doctest::

            >>> from bioservices import OmniPath
            >>> o = OmniPath()
            >>> net = o.get_network()
            >>> interactions = o.get_interactions('P00533')

    """

    _url = "http://omnipathdb.org/"

    def __init__(self, verbose=False, cache=False):
        """**Constructor** OmniPath

        :param verbose: set to False to prevent informative messages
        """
        super(OmniPath, self).__init__(name="OmniPath", url=OmniPath._url, verbose=verbose, cache=cache)

    def get_about(self):
        """Information about the version"""
        res = self.http_get(self.url + "about").content
        return res

    def get_network(self, frmt="json"):
        """Get basic statistics about the whole network including sources"""
        assert frmt in ["json", "tsv"], "frmt must be set to json or tsv"
        res = self.http_get(self.url + "network", frmt=frmt, params={"format": frmt})

        return res

    def get_interactions(self, query="", frmt="json", fields=[]):
        """Interactions of proteins

        :param str query: a valid uniprot identifier (e.g. P00533). It can also
            be a list of uniprot identifiers, or a string with
            comma-separated identifiers.
        :param str fields: additional fields to be added to the output
            (e.g., sources, references)
        :param str frmt: format of the output (json or tabular)


        Example::

            res_one = o.get_interactions('P00533')
            res_many = o.get_interactions('P00533,O15117,Q96FE5')
            res_many = o.get_interactions(['P00533','O15117','Q96FE5'])


            res_one = o.get_interactions('P00533', fields='sources')
            res_one = o.get_interactions('P00533', fields=['source'])
            res_one = o.get_interactions('P00533', fields=['source', 'references'])

        You may also keep query to an empty string, but the entire DB will then
        be downloaded. This may take time and the :attr:`timeout` may need to be
        increased manually.

        If frmt is set to TSV, the output is a TSV table with a header. If set
        to json, a dictionary is returned.
        """
        # make sure there is no spaces
        if isinstance(query, list):
            query = ",".join(query)
        else:
            try:  # if input is a string
                query = query.replace(" ", "")
            except:
                pass
        assert frmt in ["json", "tsv"], "frmt must be set to json or tsv"
        params = {}
        params["format"] = frmt
        from easydev import to_list

        fields = to_list(fields)

        if len(fields):
            params["fields"] = fields

        # TODO handle multiple fields
        res = self.http_get(self.url + "interactions/%s" % query, frmt=frmt, params=params)
        return res

    def get_resources(self, frmt="json"):
        """Return statistics about the databases and their contents"""
        res = self.http_get(self.url + "resources", frmt=frmt, params={"format": frmt})
        return res

    def get_info(self):
        """Currently returns HTML page"""
        from easydev import browser

        browser.browse(self.url + "info")

    def get_ptms(self, query="", ptm_type=None, frmt="json", fields=[]):
        """List enzymes, substrates and PTMs

        :param str query: a valid uniprot identifier (e.g. P00533). It can also
            be a list of uniprot identifiers, or a string with
            comma-separated identifiers.
        :param str ptm_type: restrict the output to this type of PTM
            (e.g., phosphorylation)
        :param str fields: additional fields to be added to the output
            (e.g., sources, references)


        """
        # make sure there is no spaces
        if isinstance(query, list):
            query = ",".join(query)
        else:
            try:  # if input is a string
                query = query.replace(" ", "")
            except:
                pass
        assert frmt in ["json", "tsv"], "frmt must be set to json or tsv"
        params = {}
        params["format"] = frmt
        if len(fields):
            params["fields"] = fields

        res = self.http_get(self.url + "ptms/%s" % query, frmt="json", params=params)
        return res
