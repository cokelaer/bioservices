#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
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

"""This module provides a class :class:`ChEBI` 

.. topic:: What is ChEBI

    :URL:  https://www.ebi.ac.uk/chebi/init.do
    :WSDL: http://www.ebi.ac.uk/webservices/chebi/2.0/webservice


    .. highlights::

        "The database and ontology of Chemical Entities of Biological Interest

        -- From ChEBI web page June 2013


"""
from bioservices import WSDLService


class ChEBI(WSDLService):
    """Interface to `ChEBI <http://www.ebi.ac.u.k/chebi/init.do>`_


        >>> from bioservices import *
        >>> ch = ChEBI()
        >>> res = ch.getCompleteEntity("CHEBI:27732")
        >>> res.smiles
        CN1C(=O)N(C)c2ncn(C)c2C1=O

    """
    _url = "http://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl"
    def __init__(self, verbose=False):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(ChEBI, self).__init__(name="ChEBI", url=ChEBI._url, 
            verbose=verbose)

    def getCompleteEntity(self, chebiId):
        """Retrieves the complete entity including synonyms, database links and
chemical structures, using the ChEBI identifier.

        :param str chebiId: a valid ChEBI identifier (string)
        :return: an object containing fields such as mass, names, smiles

        ::

            >>> from bioservices import *
            >>> ch = ChEBI()
            >>> res = ch.getCompleteEntity("CHEBI:27732")
            >>> res.mass
            194.19076

        The returned structure is the raw object returned by the API.
        You can extract names from other sources for instance::

            >>> [x[0] for x in res.DatabaseLinks if x[1].startswith("KEGG")]
            [C07481, D00528]
            >>> [x[0] for x in res.DatabaseLinks if x[1].startswith("ChEMBL")]
            [116485]

        .. seealso:: :meth:`conv`, :meth:`getCompleteEntity`
        """
        res = self.serv.getCompleteEntity(chebiId)
        # the output in res are made of objects that are cast into strings
        #res = [str(x) for x in res] 
        return res

    def conv(self, chebiId, target):
        """Calls :meth:`getCompleteEntity` and returns the identifier of a given database


        :param str chebiId: a valid ChEBI identifier (string)
        :param target: the identifier of the database
        :return: the identifier

        ::

            >>> ch.conv("CHEBI:10102", "KEGG COMPOUND accession")
            ['C07484']

        """
        res = self.serv.getCompleteEntity(chebiId)
        db = [x[1] for x in res.DatabaseLinks]
        if target not in db:
            raise ValueError("valid database target are %s" % db)
        conv = [str(x[0]) for x in res.DatabaseLinks if x[1] == target]
        return conv

    def getLiteEntity(self, search, searchCategory="ALL", maximumResults=200, stars="ALL"):
        """Retrieves list of entities containing the ChEBI ASCII name or identifier

        :param search: search string or category. 
        :param searchCategory: filter with category. Can be ALL, 
        :param int maximumResults: (default is 200)
        :param str stars: filters that can be set to "TWO ONLY", "ALL", "THREE ONLY"

        The input parameters are a search string and a search category. If the search
        category is null then it will search under all fields. The search string accepts
        the wildcard character "*" and also unicode characters. You can get maximum
        results upto 5000 entries at a time.

        ::

            >>> ch.getLiteEntity("CHEBI:27732")
            [(LiteEntity){
               chebiId = "CHEBI:27732"
               chebiAsciiName = "caffeine"
               searchScore = 4.77
               entityStar = 3
             }]
            >>> res = ch.getLiteEntity("caffeine")
            >>> res = ch.getLiteEntity("caffeine", maximumResults=10)
            >>> len(res)
            10


        .. seealso:: :meth:`getCompleteEntity`
        """
        self.devtools.check_param_in_list(searchCategory, ["ALL", "SMILES", "CHEBI ID", 
            "CHEBI NAME", "DEFINITION", "ALL NAMES", "IUAPC", "MASS", 
            "FORMULA", "INCHI", "INCHI KEY"])
        res = self.serv.getLiteEntity(search, searchCategory, maximumResults, stars)
        if len(res):
            return res[0]
        else:
            return res

    def getUpdatedPolymer(self, chebiId):
        """Returns the UpdatedPolymer object

        :param str chebiId:
        :param str chebiId: a valid ChEBI identifier (string)
        :return: an object with information as described below.

        The object contains the updated 2D MolFile structure, GlobalFormula 
        string containing the formulae for each repeating-unit, the GlobalCharge 
        string containing the charge on individual repeating-units and the 
        primary ChEBI ID of the polymer, even if the secondary Identifier was passed
        to the web-service.

        """
        res = self.serv.getUpdatedPolymer(chebiId)
        return res

    def getCompleteEntityByList(self, chebiIdList=[]):
        """Given a list of ChEBI accession numbers, retrieve the complete Entities. 

        The maximum size of this list is 50. 

        .. seealso:: :meth:`getCompleteEntity`
        """
        res = self.serv.getCompleteEntityByList(chebiIdList)
        return res

    def getOntologyParents(self, chebiId):
        """Retrieves the ontology parents of an entity including the relationship type

        :param str chebiId: a valid ChEBI identifier (string)

        """
        res = self.serv.getOntologyParents(chebiId)
        return res

    def getOntologyChildren(self, chebiId):
        """Retrieves the ontology children of an entity including the relationship type

        :param str chebiId: a valid ChEBI identifier (string)

        """
        res = self.serv.getOntologyChildren(chebiId)
        return res

    def getAllOntologyChildrenInPath(self, chebiId, relationshipType,
            onlyWithChemicalStructure=False):
        """Retrieves the ontology children of an entity including the relationship type

        :param str chebiId: a valid ChEBI identifier (string)
        :param str relationshipType: one of "is a", "has part", "has role", 
            "is conjugate base of", "is conjugate acid of", "is tautomer of"
            "is enantiomer of", "has functional parent" "has parent hybride"
            "is substituent group of"

        ::

            >>> ch.getAllOntologyChildrenInPath("CHEBI:27732", "has part")

        """
        self.devtools.check_param_in_list(relationshipType, 
             ["is a", "has part", "has role", 
            "is conjugate base of", "is conjugate acid of", "is tautomer of",
            "is enantiomer of", "has functional parent", "has parent hybride",
            "is substituent group of"])
        res = self.serv.getAllOntologyChildrenInPath(chebiId, relationshipType, 
            onlyWithChemicalStructure)
        return res

    def getStructureSearch(self, structure, mode="MOLFILE",
            structureSearchCategory="SIMILARITY", totalResults=50,
            tanimotoCutoff=0.25):

        """Does a substructure, similarity or identity search using a structure.

        :param str structure: the input structure
        :param str mode:  type of input (MOLFILE, SMILES, CML" (note that 
            the API uses type but this is a python keyword)
        :param str structureSearchCategory: category of the search. Can be
            "SIMILARITY", "SUBSTRUCTURE", "IDENTITY"
        :param int totalResults: limit the number of results to 50 (default)
        :param tanimotoCuoff: limit results to scores higher than this 
            parameter

        ::

            >>> ch = ChEBI()
            >>> smiles = ch.getCompleteEntity("CHEBI:27732").smiles
            >>> ch.getStructureSearch(smiles, "SMILES", "SIMILARITY", 3, 0.25)
        """

        self.devtools.check_param_in_list(structureSearchCategory, 
                ["SIMILARITY", "SUBSTRUCTURE","IDENTITY"])
        self.devtools.check_param_in_list(mode, ["MOLFILE", "SMILES", "CML"])

        res = self.serv.getStructureSearch(structure, mode, 
            structureSearchCategory, totalResults, tanimotoCutoff)
        return res
