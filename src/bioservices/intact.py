#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer
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

"""This module provides a class :class:`IntactComplex`

.. topic:: What is Intact Complex ?

    :URL:  https://www.ebi.ac.uk/intact/complex/
    :REST:  https://www.ebi.ac.uk/intact/complex-ws/details/


    .. highlights::

        "The Complex Portal is a manually curated, encyclopaedic resource of
        macromolecular complexes from a number of key model organisms."

        -- From Intact web page Feb 2015


"""
from bioservices import REST


__all__ = ['IntactComplex']


class Intact(object):
    def __init__(self):
        print("Not implemented yet. For Intact Complex, please use IntactComplex class")


class IntactComplex(REST):
    """Interface to the `Intact <http://www.ebi.ac.uk/intact/>`_ service

    .. doctest::

            >>> from bioservices import IntactComplex
            >>> u = IntactComplex()

    """

    _url = "http://www.ebi.ac.uk/intact/complex-ws"

    def __init__(self, verbose=False, cache=False):
        """**Constructor** IntactComplex

        :param verbose: set to False to prevent informative messages
        """
        super(IntactComplex, self).__init__(name="IntactComplex", url=IntactComplex._url,
                verbose=verbose, cache=cache)

    def search(self, query, frmt='json', facets=None, first=None, number=None, filters=None):
        """Search for a complex inside intact complex.

        :param str query: the query (e.g., ndc80)
        :param str frmt: Defaults to json (could be a Pandas data frame if
            Pandas is installed; set frmt to 'pandas')
        :param str facets: lists of facets as a string (separated by comma)
        :param int first:
        :param int number:
        :param str filter: list of filters. See examples here below.

        .. code-block:: python

            s = IntactComplex()
            # search for ndc80
            s.search('ncd80')

            #  Search for ndc80 and facet with the species field:
            s.search('ncd80', facets='species_f')

            # Search for ndc80 and facet with the species and biological role fields:
            s.search('ndc80', facets='species_f,pbiorole_f')

            # Search for ndc80, facet with the species and biological role
            # fields and filter the species using human:
            s.search('Ndc80', first=0, number=10,
                filters='species_f:("Homo sapiens")',
                facets='species_f,ptype_f,pbiorole_f')

            # Search for ndc80, facet with the species and biological role
            # fields and filter the species using human or mouse:
            s.search('Ndc80, first=0, number=10,
                filters='species_f:("Homo sapiens" "Mus musculus")',
                facets='species_f,ptype_f,pbiorole_f')

            # Search with a wildcard to retrieve all the information:
            s.search('*')

            # Search with a wildcard to retrieve all the information and facet
            # with the species, biological role and interactor type fields:
            s.search('*', facets='species_f,pbiorole_f,ptype_f')

            # Search with a wildcard to retrieve all the information, facet with
            # the species, biological role and interactor type fields and filter
            # the interactor type using small molecule:
            s.search('*', facets='species_f,pbiorole_f,ptype_f',
                filters='ptype_f:("small molecule")'

            # Search with a wildcard to retrieve all the information, facet with
            # the species, biological role and interactor type fields and filter
            # the interactor type using small molecule and the species using human:
            s.search('*', facets='species_f,pbiorole_f,ptype_f',
                filters='ptype_f:("small molecule"),species_f:("Homo sapiens")')

            # Search for GO:0016491 and paginate (first is for the offset and number
            # is how many do you want):
            s.search('GO:0016491', first=10, number=10)

        The organism name used in the filter must be exact. Here is the list
        found by typing::

            res = set(ci.search('*', frmt='pandas')['organismName'])

        ::

           'Bos taurus; 9913',
           'Caenorhabditis elegans; 6239',
           'Canis familiaris; 9615',
           'Drosophila melanogaster; 7227',
           'Escherichia coli (strain K12); 83333',
           'Gallus gallus; 9031',
           'Homo sapiens; 9606',
           'Mus musculus; 10090',
           'Oryctolagus cuniculus; 9986',
           'Rattus norvegicus; 10116',
           'Saccharomyces cerevisiae (strain ATCC 204508 / S288c);559292',
           'Schizosaccharomyces pombe (strain 972 / ATCC 24843);284812',
           'Xenopus laevis; 8355'


        """
        self.devtools.check_param_in_list(frmt, ['pandas', 'json'])

        # note that code format to be json, which is the only option so
        # we can use pandas as a frmt without addition code.
        params = {'format': 'json', 'facets':facets, 'first':None,
                'number':number, 'filters':filters}

        result = self.http_get('search/' + query, frmt="json", params=params)

        #if isinstance(result, int):
        #    raise ValueError("Got a number from Intact request. Check validity of the arguments ")

        if frmt == 'pandas':
            import pandas as pd
            df = pd.DataFrame(result['elements'])
            return df
        else:
            return result

    def details(self, query):
        """Return details about a complex

        :param str query: EBI-1163476

        """
        result = self.http_get('details/' + query, frmt="json")
        return result


