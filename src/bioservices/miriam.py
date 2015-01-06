# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2012 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://www.ebi.ac.uk/~cokelaer/bioservices
#
##############################################################################
"""Interface to the MIRIAM Web Service.

.. topic:: What is Miriam

    :URL: http://www.ebi.ac.uk/miriam/main/
    :WSDL: http://www.ebi.ac.uk/miriamws/main/MiriamWebServices?wsdl

    .. highlights::

        The MIRIAM Registry provides a set of online services for the generation of unique and perennial identifiers, in the form of URIs. It provides the core data which is used by the Identifiers.org resolver.
        The core of the Registry is a catalogue of data collections (corresponding to controlled vocabularies or databases), their URIs and the corresponding physical URLs or resources. Access to this data is made available via exports (XML) and Web Services (SOAP).

        -- From MIRIAM Web Site, Feb 2013

:Terminology:

* URI: Uniform Resource Identifiers
* URL: Uniform Resource Locators

.. testsetup:: miriam

    from bioservices import *
    m = Miriam()


"""
from bioservices import WSDLService

__all__ = ["Miriam"]


class Miriam(WSDLService):
    """Interface to the `MIRIAM <http://www.ebi.ac.uk/miriam/main/>`_ service

    ::

        >>> from bioservices import Miriam
        >>> m = Miriam()
        >>> m.getMiriamURI("http://www.ebi.ac.uk/chebi/#CHEBI:17891")
        'urn:miriam:chebi:CHEBI%3A17891'


    """
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL

        """
        url = "http://www.ebi.ac.uk/miriamws/main/MiriamWebServices?wsdl"
        super(Miriam, self).__init__(name="Miriam", url=url, verbose=verbose)

    def _boolean_convertor(self, boolean):
        if boolean == 'true':
            return True
        elif boolean == 'false':
            return False
        else:
            raise ValueError("boolean can be true or false only (%s)" % boolean)

    def checkRegExp(self, identifier, datatype):
        """Checks if the identifier given follows the regular expression of the data collection

        :param str identifier: internal identifier used by the data collection
        :param str datatype: name, synonym or MIRIAM URI of a data collection
        :return: True if the identifier follows the regular expression, False otherwise

        ::

            >>> m.checkRegExp("P62158", "uniprot")
            True
            >>> m.checkRegExp("!P62158", "uniprot")
            False

        .. warning:: there is no sanity check on the datatype. Default output is
            True. So if you inverse the parameters, you may get True even tough it does not
            make sense. This is a feature of the Web Service.
        """
        res = self.serv.checkRegExp(identifier, datatype)
        res = self._boolean_convertor(res)
        return res

    def convertURL(self, url):
        """Converts an Identifiers.org URL into its equivalent MIRIAM URN.

        This performs a check of the identifier based on the recorded regular expression.
        :param str identifier: an Identifiers.org URL
        :return: the MIRIAM URN corresponding to the provided Identifiers.org URL or 'null' if the provided URL is invalid

        ::

            >>> m.convertURL("http://identifiers.org/ec-code/1.1.1.1")
            'urn:miriam:ec-code:1.1.1.1'

        """
        res = self.serv.convertURL(url)
        return res

    def convertURLs(self, urls):
        """Converts a list of Identifiers.org URLs into their equivalent MIRIAM URNs.

        This performs a check of the identifier based on the recorded regular expression.

        :param str identifier: a list of Identifiers.org URL
        :return: the MIRIAM URN corresponding to the provided Identifiers.org URL or 'null' if the provided URL is invalid

        ::

            >>> m.convertURLs(['http://identifiers.org/pubmed/16333295', 'http://identifiers.org/ec-code/1.1.1.1"])


        """
        res = self.serv.convertURLs(urls)
        return res

    def convertURN(self, urn):
        """Converts a MIRIAM URI into its equivalent Identifiers.org URL.

        This takes care of any necessary conversion, for example in the case
        the URI provided is obsolete.

        :param str urn: a MIRIAM URLs
        :return: the Identifiers.org URL corresponding to the provided MIRIAM

        URI or None if the provided URI does not exist

        ::

            >>> m.serv.convertURN('urn:miriam:ec-code:1.1.1.1')
            'http://identifiers.org/ec-code/1.1.1.1'

        """
        res = self.serv.convertURN(urn)
        return res

    def convertURNs(self, urns):
        """Converts a list of MIRIAM URIs into their equivalent Identifiers.org URLs.

        This takes care of any necessary conversion, for example in the case a
        URI provided is obsolete. If the size of the list of URIs exceeds 200,
        None is returned.

        :param list urns: list of MIRIAM URIs
        :return: a list of Identifiers.org URLs corresponding to the provided URIs

        ::

            >>> m.serv.convertURN(['urn:miriam:ec-code:1.1.1.1'])
            ['http://identifiers.org/ec-code/1.1.1.1']

        """
        res = self.serv.convertURNs(urns)
        return res

    def getDataResources(self, nickname):
        """Retrieves all the physical locations (URLs) of the services providing the data collection (web page).

        :param str nickname: name (can be a synonym) or URL or URN of a data collection name (or synonym) or URI (URL or URN)

        :return: array of strings containing all the address of the main page of the resources of the data collection

        ::

            >>> m.getDataResources("uniprot")
            ['http://www.ebi.uniprot.org/', 'http://www.pir.uniprot.org/', 'http://www.expasy.uniprot.org/', 'http://www.uniprot.org/', 'http://purl.uniprot.org/', 'http://www.ncbi.nlm.nih.gov/protein/']

        """
        res = self.serv.getDataResources(nickname)
        return res


    def getDataTypeDef(self, nickname):
        """Retrieves the definition of a data collection.

        :param str nickname: name or URI (URN or URL) of a data collection
        :return: definition of the data collection

        ::

            >>> m.getDataTypeDef("uniprot")
            'The UniProt Knowledgebase (UniProtKB) is a comprehensive resource for protein sequence and functional information with extensive cross-references to more than 120 external databases. Besides amino acid sequence and a description, it also provides taxonomic data and citation information.'

        """
        res = self.serv.getDataTypeDef(nickname)
        return res

    def getDataTypePattern(self, nickname):
        """Retrieves the pattern (regular expression) used by the identifiers within a data collection.

        :param str nickname: data collection name (or synonym) or URI (URL or URN)
        :return:  pattern of the data collection

        ::

            >>> m.getDataTypePattern("uniprot")
            '^([A-N,R-Z][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9])|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\\.\\d+)?$'
        """
        res = self.serv.getDataTypePattern(nickname)
        return res

    def getDataTypeSynonyms(self, name):
        """Retrieves all the synonym names of a data collection (this list includes the original name).

        :param str name: name or synonym of a data collection
        :return: all the synonym names of the data collection (list of strings)

        ::

            >>> m.getDataTypeSynonyms("uniprot")
            ['UniProt Knowledgebase', 'UniProtKB', 'UniProt']


        """
        res = self.serv.getDataTypeSynonyms(name)
        return res

    def getDataTypeURI(self, name):
        """Retrieves the unique (official) URI of a data collection (example: "urn:miriam:uniprot").

        :param str name: name or synonym of a data collection (examples: "UniProt")
        :return: unique URI of the data collection

        ::

            >>> m.serv.getDataTypeURI("uniprot")
            'urn:miriam:uniprot'

        """
        res = self.serv.getDataTypeURI(name)
        return res

    def getDataTypeURIs(self, name):
        """Retrieves all the URIs of a data collection, including all the deprecated ones (examples: "urn:miriam:uniprot", "http://www.uniprot.org/", "urn:lsid:uniprot.org:uniprot", ...).

        :param str name: name (or synonym) of the data collection (examples: "ChEBI", "UniProt")
        :return:  all the URIs of a data collection (including the deprecated ones)

        ::

            >>> m.getDataTypeURIs("uniprot")
            ['urn:miriam:uniprot', 'urn:lsid:uniprot.org:uniprot', 'urn:lsid:uniprot.org', 'http://www.uniprot.org/']

        """
        res = self.serv.getDataTypeURIs(name)
        return res

    def getDataTypesId(self):
        """Retrieves the internal identifier (stable and perennial) of all the data collections (for example: "MIR:00000005").


        :return: list of the identifier of all the data collections

        ::

            >>> m.getDataTypesId()

        """
        res = self.serv.getDataTypesId()
        return res

    def getDataTypesName(self):
        """Retrieves the list of names of all the data collections available.

        :return: list of the name of all the data collections

        ::

            >>> m = self.getDataTypesName()

        """
        res = self.serv.getDataTypesName()
        return res

    def getJavaLibraryVersion(self):
        res = self.serv.getJavaLibraryVersion()
        return res

    def getLocation(self, uri, resource):
        """Retrieves the physical location (URL) of a web page providing knowledge about a specific entity, using a specific resource.

        :param str uri: MIRIAM URI of an entity (example: 'urn:miriam:obo.go:GO%3A0045202')
        :param sr resource: internal identifier of a resource (example: 'MIR:00100005')
        :return: physical location of a web page providing knowledge about the given entity, using a specific resource

        ::

            >>> m.getLocation("UniProt", "MIR:00100005")
            ['http://www.uniprot.org/uniprot/P62158', 'http://purl.uniprot.org/uniprot/P62158', 'http://www.ncbi.nlm.nih.gov/protein/P62158']

        .. warning:: getLocation needs a proper example
        """
        res = self.serv.getLocation(uri, resource)
        return res

    def getLocations(self, nickname, Id=None):
        """Retrieves the (non obsolete) physical locationS (URLs) of web pageS providing knowledge about an entity.


        :param str nickname: name (can be a synonym) or URI of a data collection (examples: "Gene Ontology", "UniProt"). If Id is None, nickname parameter is a MIRIAM URI of an entity (example: 'urn:miriam:obo.go:GO%3A0045202')
        :param str id: identifier of an entity within the given data collection (examples: "GO:0045202", "P62158").
        :return:  physical locationS of web pageS providing knowledge about the given entity. If the URI is not recognised or the data collection does not exist, an empty array is returned. If the identifier is invalid for the data collection, None is returned. All special characters in the data entry part of the URLs are properly encoded.

        ::

            >>> m.getLocations("UniProt","P62158")
            >>> m.getLocations("urn:miriam:obo.go:GO%3A0045202")

        """
        if Id:
            res = self.serv.getLocations(nickname, Id)
        else:
            res = self.serv.getLocations(nickname)
        return res

    def getLocationsWithToken(self, nickname, token):
        """Retrieves the list of (non obsolete) generic physical locations (URLs) of web pageS providing the dataset of a given data collection.

        :param str nickname: name (can be a synonym) or URI of a data collection (examples: "Gene Ontology", "UniProt", "urn:miriam:biomodels.db")
        :param str token: placeholder which will be put in the URLs at the location of the data entry identifier (default: $id)
        :return: list of (non obsolete) generic physical locations (URLs) of web pageS providing the dataset of a given data collection

        ::

            >>> m.getLocationsWithToken("uniprot", "P43403")

        """
        res = self.serv.getLocationsWithToken(nickname, token)
        return res

    def getMiriamURI(self, name):
        """Transforms a MIRIAM URI into its official equivalent (to transform obsolete URIs into current valid ones).


        :param str uri: deprecated URI (URN or URL), example: "http://www.ebi.ac.uk/chebi/#CHEBI:17891"
        :return: the official URI corresponding to the deprecated one (for example: "urn:miriam:obo.chebi:CHEBI%3A17891") or 'null' if the URN does not exist

        ::

            >>> m.getMiriamURI("http://www.ebi.ac.uk/chebi/#CHEBI:17891")
            'urn:miriam:chebi:CHEBI%3A17891'

        """
        res = self.serv.getMiriamURI(name)
        return res

    def getName(self, uri):
        """Retrieves the common name of a data collection

        :param str uri: URI (URL or URN) of a data collection
        :return:  the common name of the data collection

        ::

            >>> m.getName('urn:miriam:uniprot')
            'UniProt Knowledgebase'

        """
        res = self.serv.getName(uri)
        return res


    def getNames(self, uri):
        """Retrieves all the names (with synonyms) of a data collection.

        :param str uri:  	URI (URL or URN) of a data collection
        :return: the common name of the data collection and all the synonyms

        ::

            >>> m.serv.getNames('urn:miriam:uniprot')
            ['UniProt Knowledgebase', 'UniProtKB', 'UniProt']

        """
        return self.serv.getNames(uri)

    def getOfficialDataTypeURI(self, nickname):
        """Retrieves the official URI (it will always be a URN) of a data collection.

        :param str nickname: name (can be a synonym) or MIRIAM URI (even deprecated one) of a data collection (for example: "ChEBI", "http://www.ebi.ac.uk/chebi/", ...)
        :return:  the official URI of the data collection

        ::

            >>> m.getOfficialDataTypeURI("chEBI")
            'urn:miriam:chebi'

        """
        res = self.serv.getOfficialDataTypeURI(nickname)
        return res

    def getResourceInfo(self, Id):
        """Retrieves the general information about a precise resource of a data collection.

        :param str Id: identifier of a resource (example: "MIR:00100005")
        :return: general information about a resource

        ::

            >>> m.getResourceInfo("MIR:00100005")
            'MIRIAM Resources (data collection)'


        """
        res = self.serv.getResourceInfo(Id)
        return res

    def getResourceInstitution(self, Id):
        """Retrieves the institution which manages a precise resource of a data collection.

        :param str Id: identifier of a resource (example: "MIR:00100005")
        :Returns: institution which manages a resource

        ::

            >>> m.getResourceInstitution("MIR:00100005")
            'European Bioinformatics Institute'


        """
        res = self.serv.getResourceInstitution(Id)
        return res

    def getResourceLocation(self, Id):
        """Retrieves the location of the servers of a location.

        :param str Id: identifier of a resource (example: "MIR:00100005")
        :return:  location of the servers of a resource

        ::

            >>> m.getResourceLocation("MIR:00100005")
            'United Kingdom'

        """
        res = self.serv.getResourceLocation(Id)
        return res

    def getServicesInfo(self):
        """Retrieves some information about these Web Services.

        :return: information about the Web Services

        ::

            >>> m.getServicesInfo()
        """
        res = self.serv.getServicesInfo()
        return res

    def getServicesVersion(self):
        """Retrieves the current version of MIRIAM Web Services.

        :return: Current version of the web services
        """
        return self.serv.getServicesVersion()

    def getURI(self, name, Id):
        """Retrieves the unique URI of a specific entity (example: "urn:miriam:obo.go:GO%3A0045202").

        If the data collection does not exist (or is not recognised), an empty String is returned.

        If the identifier is invalid for the given data collection, 'null' is returned.

        :param str name: name of a data collection (examples: "ChEBI", "UniProt")
        :param str id: identifier of an entity within the data collection (examples: "GO:0045202", "P62158")

        ::

            >>> m.getURI("UniProt", "P62158")
            'urn:miriam:uniprot:P62158'

        """
        res = self.serv.getURI(name, Id)
        return res

    def getURIs(self, names, Ids):
        """Retrieves the unique URIs for a list of specific entities (example: "urn:miriam:obo.go:GO%3A0045202").

        If a data collection does not exist (or is not recognised), an empty String is returned for this data collection.

        If an identifier is invalid for the given data collection, 'null' is returned for this data collection.

        If the provided lists do not have the same size, 'null' is returned.

        If the size of any list exceeds 200, 'null' is returned.

        :return: list of MIRIAM URIs

        ::

            >>> m.serv.getURIs(["UniProt", "GO"], ["P62158", "GO:0045202"])
            ['urn:miriam:uniprot:P62158', 'urn:miriam:obo.go:GO%3A0045202']

        .. todo:: : chracter is not encoded correclty
        """
        names = self.devtools.to_list(names)
        Ids = self.devtools.to_list(Ids)
        res = self.serv.getURIs(names, Ids)
        return res

    def isDeprecated(self, uri):
        """Says if a URI of a data collection is deprecated.

        :return: answer ("true" or "false") to the question: is this URI deprecated?

        ::

            >>> im.isDeprecated("urn:miriam:uniprot")
            False
        """
        res = self.serv.isDeprecated(uri)
        res = self._boolean_convertor(res)
        return res




