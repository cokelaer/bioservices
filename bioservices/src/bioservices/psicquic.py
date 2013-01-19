#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EMBL-EBI
#
#  File author(s): 
#      https://www.assembla.com/spaces/bioservices/team
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id:$
"""Interface to the PSICQUIC web service

.. topic:: What is PSICQUIC ?

    :URL: http://code.google.com/p/psicquic/
    :REST: http://code.google.com/p/psicquic/wiki/PsicquicSpec_1_3_Rest

    .. highlights::

        "PSICQUIC is an effort from the HUPO Proteomics Standard Initiative
        (HUPO-PSI) to standardise the access to molecular interaction databases
        programmatically. The PSICQUIC View web interface shows that PSICQUIC
        provides access to 25 active service "

        -- Dec 2012


About queries
================

.. rubric:: source: PSICQUIC View web page

To do a search you can use the Molecular Interaction Query Language which is
based on Lucene's syntax.

* Use OR or space ' ' to search for ANY of the terms in a field
* Use AND if you want to search for those interactions where ALL of your terms are found
* Use quotes (") if you look for a specific phrase (group of terms that must
  be searched together) or terms containing special characters that may otherwise
  be interpreted by our query engine (eg. ':' in a GO term)
* Use parenthesis for complex queries (e.g. '(XXX OR YYY) AND ZZZ')
* Wildcards (*,?) can be used between letters in a term or at the end of terms to do fuzzy queries,
   but never at the beginning of a term. 
* Optionally, you can prepend a symbol in from of your term.
    *  + (plus): include this term. Equivalent to AND. e.g. +P12345
    *  - (minus): do not include this term. Equivalent to NOT. e.g. -P12345
    *    Nothing in front of the term. Equivalent to OR. e.g. P12345
* Implicit fields are used when no field is specified (simple search). For
  instance, if you put 'P12345' in the simple query box, this will mean the same
  as identifier:P12345 OR pubid:P12345 OR pubauth:P12345 OR species:P12345 OR
  type:P12345 OR detmethod:P12345 OR interaction_id:P12345

=============== =========================================== =============== ======================
Field Name      Searches on                                 Implicit*       Example
=============== =========================================== =============== ======================
idA             Identifier A                                No              idA:P74565
idB             Identifier B                                No              idB:P74565
id              Identifiers (A or B)                        No              id:P74565
alias           Aliases (A or B)                            No              alias:(KHDRBS1 HCK)
identifiers     Identifiers and Aliases undistinctively     Yes             identifier:P74565
pubauth         Publication 1st author(s)                   Yes             pubauth:scott
pubid           Publication Identifier(s) OR                Yes             pubid:(10837477 12029088)
taxidA          Tax ID interactor A: the tax ID or 
                the species name                            No              taxidA:mouse
taxidB          Tax ID interactor B: the tax ID or 
                species name                                No              taxidB:9606
species         Species. Tax ID A or Tax ID B               Yes             species:human
type            Interaction type(s)                         Yes             type:"physical interaction"
detmethod       Interaction Detection method(s)             Yes             detmethod:"two hybrid*"
interaction_id  Interaction identifier(s)                   Yes             interaction_id:EBI-761050
pbioroleA       Biological role A                           Yes             pbioroleA:ancillary
pbioroleB       Biological role B                           Yes             pbioroleB:"MI:0684"
pbiorole        Biological roles (A or B)                   Yes             pbiorole:enzyme
ptypeA          Interactor type A                           Yes             ptypeA:protein
ptypeB          Interactor type B                           Yes             ptypeB:"gene"
ptype           Interactor types (A or B)                   Yes             pbiorole:"small molecule"
pxrefA          Interactor xref A (or Identifier A)         Yes             pxrefA:"GO:0003824"
pxrefB          Interactor xref B (or Identifier B)                         Yes pxrefB:"GO:0003824"
pxref           Interactor xrefs (A or B or Identifier 
                A or Identifier B)                          Yes             pxref:"catalytic activity"
xref            Interaction xrefs (or Interaction 
                identifiers)                                Yes             xref:"nuclear pore"
annot           Interaction annotations and tags            Yes             annot:"internally curated"
udate           Update date                                 Yes             udate:[20100101 TO 20120101]
negative        Negative interaction boolean                Yes             negative:true
complex         Complex expansion                           Yes             complex:"spoke expanded"
ftypeA          Feature type of participant A               Yes             ftypeA:"sufficient to bind"
ftypeB          Feature type of participant B               Yes             ftypeB:mutation
ftype           Feature type of participant A or B          Yes             ftype:"binding site"
pmethodA        Participant identification method A         Yes             pmethodA:"western blot"
pmethodB        Participant identification method B         Yes             pmethodB:"sequence tag identification"
pmethod         Participant identification methods
                 (A or B)                                   Yes             pmethod:immunostaining 
stc             Stoichiometry (A or B). Only true or 
                false, just to be able to filter 
                interaction having stoichiometry available  Yes             stc:true
param           Interaction parameters. Only true or 
                false, just to be able to filter 
                interaction having parameters available     Yes             param:true
=============== =========================================== =============== ======================


"""

from bioservices import RESTService


#http://code.google.com/p/psicquic/wiki/PsicquicSpec_1_3_Rest

#http://www.biocatalogue.org/services/2078#operations

__all__ = ["PSICQUIC"]


class PSICQUIC(RESTService):
    """Interface to the PSICQUIC service

    There are 2 interfaces to the PSICQUIC service (REST and WSDL) but we used
    the REST only.


    This service provides a common interface to more than 25 other services
    related to protein. So, we won't detail all the possiblity of this service.
    Here is an example that consists in looking for interaction between the
    protein called ZAP70 within the ::

        >>> from bioservices import *
        >>> s = psicquic.PSICQUIC()
        >>> res = s.query("intact", "zap70")
        >>> len(res) # there are 11 interactions found
        11
        >>> # Let us look at the second one in particular:
        >>> for x in res[1].split("\t"): 
        ...     print x
        uniprotkb:O95169
        uniprotkb:P43403
        intact:EBI-716238
        intact:EBI-1211276
        psi-mi:ndub8_human(display_long)|uniprotkb:NADH-ubiquinone oxidoreductase ASHI
        .
        .

    Another reaction with reactome::

        res = s.query("reactome", "Q9Y266")

    """

    _formats = ["tab25", "tab25", "tab27", "xml25", "count", "biopax", "xgmml",
        "rdf-xml", "rdf-xml-abbrev", "rdf-n3", "rdf-turtle"]

    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose: print informative messages

        .. doctest:: 

            >>> from bioservices import PSICQUIC
            >>> s = psicquic.PSICQUIC()

        """
        urlStr = 'http://www.ebi.ac.uk/Tools/webservices/psicquic'
        super(PSICQUIC, self).__init__("PSICQUIC", verbose=verbose, url=urlStr)
        self._registry = None

    def _get_formats(self):
        return PSICQUIC._formats
    formats = property(_get_formats, doc="returns the possible output formats")

    def read_registry(self):
        """Reads and returns the active registry 

        """
        url = self.url + '/registry/registry?action=ACTIVE&format=txt'
        res = self.request(url, format='txt')
        return res.split()

    def print_status(self):
        """Prints the services that are available

        :return: nothing

        The output is tabulated. The columns are:

        * names
        * active
        * count
        * version
        * rest URL
        * soap URL
        * rest example
        * restricted

        .. seealso:: if you want the data into lists, see all attributes
            starting with registry such as :meth:`registry_names`
        """
        url = self.url +  '/registry/registry?action=STATUS&format=xml'
        res = self.request(url)
        names = self.registry_names
        counts = self.registry_counts
        versions = self.registry_versions
        actives = self.registry_actives
        resturls = self.registry_resturls
        soapurls = self.registry_soapurls
        restexs = self.registry_restexamples
        restricted = self.registry_restricted
        N = len(names)

        indices = sorted(range(0,N), key=lambda k: names[k])

        for i in range(0,N):
            print("%s\t %s\t %s\t %s\t %s %s %s %s\n" % (names[i], actives[i], 
                counts[i], versions[i], resturls[i], soapurls[i], restexs[i], restricted[i]))


    # todo a property for the version of PISCQUIC

    def _get_registry(self):
        if self._registry == None:
            url = self.url +  '/registry/registry?action=STATUS&format=xml'
            res = self.request(url, format="xml")
            self._registry = res
        return self._registry
    registry = property(_get_registry, doc="returns the registry of psicquic")

    def _get_registry_names(self):
        res = self.registry
        return [x.findAll('name')[0].text for x in res.findAll("service")]
    registry_names = property(_get_registry_names, doc="returns all services available (names)")

    def _get_registry_restricted(self):
        res = self.registry
        return [x.findAll('restricted')[0].text for x in res.findAll("service")]
    registry_restricted = property(_get_registry_restricted, doc="returns restricted status of services" )

    def _get_registry_resturl(self):
        res = self.registry
        data = [x.findAll('resturl')[0].text for x in res.findAll("service")]
        return data
    registry_resturls = property(_get_registry_resturl, doc="returns URL of REST services")

    def _get_registry_restex(self):
        res = self.registry
        data = [x.findAll('restexample')[0].text for x in res.findAll("service")]
        return data
    registry_restexamples = property(_get_registry_restex, doc="retuns REST example for each service")

    def _get_registry_soapurl(self):
        res = self.registry
        return  [x.findAll('soapurl')[0].text for x in res.findAll("service")]
    registry_soapurls = property(_get_registry_soapurl, doc="returns URL of WSDL service")

    def _get_registry_active(self):
        res = self.registry
        return  [x.findAll('active')[0].text for x in res.findAll("service")]
    registry_actives = property(_get_registry_active, doc="returns active state of each service")

    def _get_registry_count(self):
        res = self.registry
        return  [x.findAll('count')[0].text for x in res.findAll("service")]
    registry_counts = property(_get_registry_count, doc="returns number of entries in each service")

    def _get_registry_version(self):
        res = self.registry
        names = [x.findAll('name')[0].text for x in res.findAll("service")]
        N = len(names)
        version = [0] * N
        for i in range(0,N):
            x = res.findAll("service")[i]
            if x.findAll("version"):
                version[i] = x.findAll("version")[0].text
            else:
                version[i] = None 
        return  version
    registry_versions = property(_get_registry_version, doc="returns version of each service")

    def query(self, service, query, output=None, version="current", firstResult=None, maxResults=None):
        """format = count; query = zap70, service intact returns 

        :param str service: a registered service. See :attr:`registry_names`.
        :param str query: a valid query. Can be `*` or a protein name.
        :param str output: a valid format. See r._formats

        ::

            r.query("intact", "brca2", "tab27")
            r.query("intact", "zap70", "xml25")
            r.query("matrixdb", "*", "xml25")

        This is the programmatic approach to this website:

        http://www.ebi.ac.uk/Tools/webservices/psicquic/view/main.xhtml


        Another example consist in accessing the *string* database for fetching 
        protein-protein interaction data of a particular model organism. Here we
        restrict the query to 100 results::

            r.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25")

        """
        params = {}
        if output!=None:
            self.checkParam(output, self.formats)
            params['format'] = output
        else: output="none"

        names = [x.lower() for x in self.registry_names]
        try:
            index = names.index(service)
        except ValueError:
            print("The service you gave (%s) is not registered. See self.registery_names" % service)
            raise ValueError

        # get the base url according to the service requested
        resturl = self.registry_resturls[index]

        if firstResult != None:
            params['firstResult'] = firstResult
        if maxResults != None:
            params['maxResults'] = maxResults

        postData = self.urlencode(params)

        url = resturl  + 'query/' + query 
        if params:
            url += "?" + postData


        if "xml" in output:
            res = self.request(url, format="xml", baseUrl=False)
        else:
            res = self.request(url, format="txt",baseUrl=False)
            res = res.strip().split("\n")

        return res


