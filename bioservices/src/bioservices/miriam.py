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
"""This module provides a class :class:`~Miriam` that allows an easy access MIRIAM registry service.

:Website: http://www.ebi.ac.uk/miriam/main/

The MIRIAM Registry provides a set of online services for the generation of unique and perennial identifiers, in the form of URIs.

The Registry was initially created to support MIRIAM, a set of guidelines for the annotation and curation of computational models.

The core of the Registry is a catalogue of data collections (corresponding to controlled vocabularies or databases), their URIs and the corresponding physical URLs or resources. Access to this data is made available via exports (XML) and Web Services (SOAP).

The Registry is developed and maintained under the BioModels.net initiative. All provided services and data is free for use by all. 

"""
from bioservices import WSDLService
import webbrowser
import copy

__all__ = ["Miriam"]

class Miriam(WSDLService):
    """Interface to the Miriam service

    ::


    """
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """
        url = "http://www.ebi.ac.uk/miriamws/main/MiriamWebServices?wsdl"
        super(Miriam, self).__init__(name="Miriam", url=url, verbose=verbose)


    def getLocations(self, request):
        """

        print m.serv.getLocations('http://www.pubmed.gov/#16333295')
        <<class 'SOAPpy.Types.typedArrayType'> getLocationsReturn at 29346320>: ['http://www.ncbi.nlm.nih.gov/pubmed/16333295', 'http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-view+MedlineFull+[medline-PMID:16333295]', 'http://www.ebi.ac.uk/citexplore/citationDetails.do?dataSource=MED&externalId=16333295', 'http://www.hubmed.org/display.cgi?uids=16333295', 'http://europepmc.org/abstract/MED/16333295']
        """
        res = self.serv.getLocations(request)
        for x in res:
            print x

    def checkRegExp(self, identifier, datatype):
        """Checks if the identifier given follows the regular expression of the data collection (also provided).

        :param str identifier: internal identifier used by the data collection
        :param str datatype: name, synonym or MIRIAM URI of a data collection
        :return: True if the identifier follows the regular expression, False otherwise


            >>> m.checkRegExp("uniprot", "P62158")
            True

        """
        res = self.serv.checkRegExp(identifier, datatype)
        return res

    def convertURL(self, url):
        """Converts an Identifiers.org URL into its equivalent MIRIAM URN.

        This performs a check of the identifier based on the recorded regular expression.
        :param str identifier: an Identifiers.org URL
        :return: the MIRIAM URN corresponding to the provided Identifiers.org URL or 'null' if the provided URL is invalid 

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

            >>> m.serv.convertURN(['urn:miriam:ec-code:1.1.1.1'])
            ['http://identifiers.org/ec-code/1.1.1.1']

        """
        res = self.serv.convertURNs(urns)
        return res

    def getDataResources(self, nickname):
        """Retrieves all the physical locations (URLs) of the services providing the data collection (web page).

        :param str nickname: name (can be a synonym) or URL or URN of a data collection name (or synonym) or URI (URL or URN)

        :return: array of strings containing all the address of the main page of the resources of the data collection

        >>> m.getDataResources("uniprot")
        ['http://www.ebi.uniprot.org/', 'http://www.pir.uniprot.org/', 'http://www.expasy.uniprot.org/', 'http://www.uniprot.org/', 'http://purl.uniprot.org/', 'http://www.ncbi.nlm.nih.gov/protein/']
 
        """
        res = self.serv.getDataResources(nickname)
        return res


    def getDataTypeDef(self, nickname):
        """Retrieves the definition of a data collection.

        :param str nickname: name or URI (URN or URL) of a data collection
        :return: definition of the data collection

        >>> m.getDataTypeDef("uniprot")
        'The UniProt Knowledgebase (UniProtKB) is a comprehensive resource for protein sequence and functional information with extensive cross-references to more than 120 external databases. Besides amino acid sequence and a description, it also provides taxonomic data and citation information.'

        """
        res = self.serv.getDataTypeDef(nickname)
        return res

    def getDataTypePattern(self, nickname):
        """Retrieves the pattern (regular expression) used by the identifiers within a data collection.

        :param str nickname: data collection name (or synonym) or URI (URL or URN)
        :return:  pattern of the data collection 


        m.getDataTypePattern()
        """
        res = self.serv.getDataTypePattern(nickname)
        return res

    def getDataTypeSynonyms(self, name):
        """Retrieves all the synonym names of a data collection (this list includes the original name).

        :param str name: name or synonym of a data collection
        :return: all the synonym names of the data collection (list of strings)

        >>> m.getDataTypeSynonyms("uniprot")
        ['UniProt Knowledgebase', 'UniProtKB', 'UniProt']


        """
        res = self.serv.getDataTypeSynonyms(name)
        return res

    def getDataTypeURI(self, name):
        """Retrieves the unique (official) URI of a data collection (example: "urn:miriam:uniprot").

        :param str name: name or synonym of a data collection (examples: "UniProt")
        :return: unique URI of the data collection 

        >>> m.serv.getDataTypeURI("uniprot")
        'urn:miriam:uniprot'

        """
        res = self.serv.getDataTypeURI(name)
        return res

    def getDataTypeURIs(self, name):
        """Retrieves all the URIs of a data collection, including all the deprecated ones (examples: "urn:miriam:uniprot", "http://www.uniprot.org/", "urn:lsid:uniprot.org:uniprot", ...).

        :param str name: name (or synonym) of the data collection (examples: "ChEBI", "UniProt")
        :return:  all the URIs of a data collection (including the deprecated ones)

        >>> m.getDataTypeURIs("uniprot")
        ['urn:miriam:uniprot', 'urn:lsid:uniprot.org:uniprot', 'urn:lsid:uniprot.org', 'http://www.uniprot.org/']

        """
        res = self.serv.getDataTypeURIs(name)
        return res

    def getDataTypesId(self):
        """Retrieves the internal identifier (stable and perennial) of all the data collections (for example: "MIR:00000005").


        :return: list of the identifier of all the data collections 

        m.getDataTypesId()
        """
        res = self.serv.getDataTypesId()
        return res

    def getDataTypesName(self):
        """Retrieves the list of names of all the data collections available.

        :return: list of the name of all the data collections

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

        >>> m.getLocation("", "MIR:00100005")

        """
        raise NotImplementedError
        res = self.serv.getLocation(uri, resource)
        return res

    def getLocations(self, nickname, Id=None):
        """Retrieves the (non obsolete) physical locationS (URLs) of web pageS providing knowledge about an entity.


        :param str nickname: name (can be a synonym) or URI of a data collection (examples: "Gene Ontology", "UniProt"). If Id is None, nickname parameter is a MIRIAM URI of an entity (example: 'urn:miriam:obo.go:GO%3A0045202')
        :param str id: identifier of an entity within the given data collection (examples: "GO:0045202", "P62158"). 
        :return:  physical locationS of web pageS providing knowledge about the given entity. If the URI is not recognised or the data collection does not exist, an empty array is returned. If the identifier is invalid for the data collection, None is returned. All special characters in the data entry part of the URLs are properly encoded.

        >>> m.serv.getLocations("UniProt","P62158")
        >>> m.serv.getLocations("urn:miriam:obo.go:GO%3A0045202")

        
        """
        if Id:
            res = self.serv.getLocations(nickname, Id)
        else:
            res = self.serv.getLocations(nickname)
        return res

    def getLocationsWithToken(self):
        """Retrieves the list of (non obsolete) generic physical locations (URLs) of web pageS providing the dataset of a given data collection.



        """
        raise NotImplementedError
        res = self.serv.getLocationsWithToken()
        return res

    def getMiriamURI(self, name):
        """Transforms a MIRIAM URI into its official equivalent (to transform obsolete URIs into current valid ones).


        :param str uri: deprecated URI (URN or URL), example: "http://www.ebi.ac.uk/chebi/#CHEBI:17891"
        :return: the official URI corresponding to the deprecated one (for example: "urn:miriam:obo.chebi:CHEBI%3A17891") or 'null' if the URN does not exist 

        >>> m.getMiriamURI("http://www.ebi.ac.uk/chebi/#CHEBI:17891")
        'urn:miriam:chebi:CHEBI%3A17891'

        """
        res = self.serv.getMiriamURI(name)
        return res

    def getName(self, uri):
        """Retrieves the common name of a data collection

        :param str uri: URI (URL or URN) of a data collection
        :return:  the common name of the data collection

        
        """
        raise NotImplementedError
    def getNames(self, uri):
        raise NotImplementedError
    
    def getOfficialDataTypeURI(self, nickname):
        """Retrieves the official URI (it will always be a URN) of a data collection.

        :param str nickname: name (can be a synonym) or MIRIAM URI (even deprecated one) of a data collection (for example: "ChEBI", "http://www.ebi.ac.uk/chebi/", ...)
        :return:  the official URI of the data collection
        
        >>> m.getOfficialDataTypeURI("chEBI")
        'urn:miriam:chebi'
        
        """
        res = self.serv.getOfficialDataTypeURI(nickname)
        return res

    def getResourceInfo(self, Id):
        res = self.serv.getResourceInfo(Id)
        return res

    def getResourceInstitution(self, Id):
        res = self.serv.getResourceInstitution(Id)
        return res

    def getResourceLocation(self, Id):
        res = self.self.getResourceLocation(Id)
        return res

    def getServicesInfo(self):
        """Retrieves some information about these Web Services.

        :return: information about the Web Services
        """
        res = self.serv.getServicesInfo()
        return res

    def getServicesVersion(self):
        """Retrieves the current version of MIRIAM Web Services.

        :return: Current version of the web services
        """
        return self.serv.getServicesVersion()

    def getURI(self, name, Id):
        raise NotImplementedError
        #res = self.getURI

    def getURIs(self, name, Id):
        raise NotImplementedError
        #res = self.getURI

    def isDeprecated(self):
        raise NotImplementedError
    



