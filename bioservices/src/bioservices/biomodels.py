#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
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
#$Id$
"""This module provides a class :class:`~BioModels` that allows an easy access to all the BioModel service.


.. topic:: What is BioModels ?

    :URL: http://www.ebi.ac.uk/biomodels-main/
    :Service: http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl
    

    .. highlights::

        "BioModels Database is a repository hosting computational models of biological
        systems. A large number of the provided models are published in the
        peer-reviewed literature and manually curated. This resource allows biologists
        to store, search and retrieve mathematical models. In addition, those models can
        be used to generate sub-models, can be simulated online, and can be converted
        between different representational formats. "

        -- From BioModels website, Dec. 2012


Some keywords:

======================= ============================================================
identifier              Description/example
======================= ============================================================
ChEBIIds                identifiers of a ChEBI terms (e.g. CHEBI:4991)
id                      model identifier (e.g. BIOMD0000000408 or MODEL1201250000)
modelId                 model identifier (e.g. BIOMD0000000408 or MODEL1201250000)
uniprotIds              Uniprot identifier (e.g., P41000)
taxonomyId              Taxonomy identifier (e.g. 9606)
GOId                    Gene Ontology identifier (e.g. GO:0006915)
publicationIdOrText     publication identifier (PMID or DOI) or text
                        which occurs in the publication's title or abstract
======================= ============================================================

"""


from services import WSDLService
import webbrowser
import copy
from functools import wraps

__all__ = ["BioModels"]


def checkId(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        ids = getattr(self, "modelsId")
        if args[0] in ids:
            res = fn(self, *args, **kwargs)
            return res
        else:
            raise ValueError("""
    Id provided is not a valid ID. See modelsId attribute.""")
    return wrapped


class BioModels(WSDLService):
    """Interface to the `BioModels <http://www.ebi.ac.uk/biomodels>`_ service 

    ::

        >>> from bioservices import biomodels
        >>> b = biomodels.BioModels()
        >>> model = b.getModelSBMLById('BIOMD0000000299')

    The number of models available can be retrieved easily as well as the model IDs::

        >>> len(b)
        >>> b.modelsID


    """
    _url = "http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl"
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:
        :param str url: redefine the wsdl URL 

        """
        super(BioModels, self).__init__(name="BioModels", url=BioModels._url, verbose=verbose)

	#: used to store all model Ids once for all
        self._modelsId = None

    def __len__(self):
        l = len(self.serv.getAllModelsId())
        return l


    def getAllModelsId(self):
        """Retrieves the identifiers of all published models

        :return: list of models identifiers


        ::

            >>> b.getAllModelsId()

        .. note:: you cal also use the :attr:`modelsId`

        """
        return self.serv.getAllModelsId()

    def _get_models_id(self):
        if self._modelsId == None:
            self._modelsId = self.serv.getAllModelsId()
        return self._modelsId
    modelsId = property(_get_models_id, doc="list of all models Id")


    def getAllCuratedModelsId(self):
        """Retrieves the identifiers of all published **curated** models

        :return: list of models identifiers

        ::

            >>> b.getAllCuratedModelsId()

        """
        return self.serv.getAllCuratedModelsId()

    def getAllNonCuratedModelsId(self):
        """Retrieves the identifiers of all published **non** **curated** models

        :return: list of models identifiers

        ::

            >>> b.getAllNonCuratedModelsId()

        """
        return self.serv.getAllNonCuratedModelsId()

    @checkId
    def getModelById(self, Id):
        """Retrieves the SBML form of a model (in a string) given its identifier

        :param str Id: a valid ,odel Id

	.. warning:: this method is now deprecated!

        ::

            model = b.getModelById("BIOMD0000000256") 

        Instead, please use: :meth:`getModelSBMLById`

        """
        return self.serv.getModelById(Id)

    @checkId
    def getAuthorsByModelId(self, Id):
        """Retrieves the name of the authors of the publication associated with
        a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.


        :return: list of names of the publication's authors

	::

            >>> b.getAuthorsByModelId("BIOMD0000000299")
            ['Leloup JC', 'Gonze D', 'Goldbeter A']

        """
        return self.serv.getAuthorsByModelId(Id)

    @checkId
    def getDateLastModifByModelId(self, Id):
        """Retrieves the date of last modification of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: date of last modification (expressed according to ISO 8601)

        ::

            >>> b.getLastModifiedDateByModelId("BIOMD0000000256")
            '2012-05-16T14:44:17+00:00'


        .. note:: same as :meth:`getLastModifiedDateByModelId`.
        """
        return self.serv.getDateLastModifByModelId(Id)

    @checkId
    def getEncodersByModelId(self, Id):
        """Retrieves the name of the encoders of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: list of names of the model's encoders


         ::

             >>> b.getEncodersByModelId("BIOMD0000000256")
             ['Lukas Endler']

        """
        return self.serv.getEncodersByModelId(Id)

    @checkId
    def getLastModifiedDateByModelId(self, Id):
        """Retrieves the date of last modification of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: date of last modification (expressed according to ISO 8601)

        """
        return self.serv.getLastModifiedDateByModelId(Id)

    @checkId
    def getModelNameById(self, Id):
        """Retrieves the name of a model name given its identifier.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: model name

        ::

            >>> print b.getModelNameById("BIOMD0000000256")
            'Rehm2006_Caspase'

        """
        return self.serv.getModelNameById(Id)

    @checkId
    def getModelSBMLById(self, Id):
        """Retrieves the SBML form of a model (in a string) given its identifier

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: str - SBML model in a string

        ::

            >>> b = BioModels()
            >>> b.getModelSBMLById('MODEL1006230101')

        """
        return self.serv.getModelSBMLById(Id)

    def getModelsIdByChEBI(self, Id):
        """

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.


        ::
      
            >>> b.getModelsIdByChEBI("CHEBI:4978")
            ['BIOMD0000000217', 'BIOMD0000000404']

        """
        return self.serv.getModelsIdByChEBI(Id)

    def getModelsIdByChEBIId(self, Id):
        """Retrieves the identifiers of all the models which are annotated with
        a given ChEBI term.

        :param str Id: identifier of a ChEBI term (e.g. CHEBI:4978)

        .. doctest::
 
            >>> b = BioModel()
            >>> b.getModelsIdByChEBIId('CHEBI:4978')
            ['BIOMD0000000404']

        """
        return self.serv.getModelsIdByChEBIId(Id)

    def getSimpleModelsByChEBIIds(self, Ids):
        """Retrieves the models which are annotated with the given ChEBI terms.

        :param str Id: identifier of a ChEBI term (e.g. CHEBI:4978)
 
        :return: list with all models annotated with the provided ChEBI identifiers, 
            as a TreeMap (which uses ChEBI identifiers as keys) 

        """
        return self.serv.getSimpleModelsByChEBIIds(Ids)

    def getSimpleModelsRelatedWithChEBI(self):
        """Retrieves all the models which are annotated with ChEBI terms.

        The output of this function is a lengthy XML document containing 
        utf-8 characters and the models (in simple models format). You can 
        convert it and extract information such as the models ID by using 
        the our xml parser and the following code:: 

            res = b.getSimpleModelsRelatedWithChEBI()
            xmltools.easyXML(res.encode('utf-8'))    
            set([x.findall('modelId')[0].text for x in res.getchildren()])

        """
        return self.serv.getSimpleModelsRelatedWithChEBI()

    @checkId
    def getPublicationByModelId(self, Id):
        """Retrieves the publication's identifier of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: publication identifier (can be a PMID, DOI or URL)

        ::

            >>> b.getPublicationByModelId("BIOMD0000000256")
            '16932741'

        """
        return self.serv.getPublicationByModelId(Id)

    @checkId
    def getSimpleModelsByIds(self, Id):
        """Retrieves the main information about given models.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: a XML representaton of the model meta information including
            identifier, name, publication identifierm date of last modification...

        ::

            >>> model = b.getSimpleModelsByIds("BIOMD0000000256")
            
        """
        res = self.serv.getSimpleModelsByIds(Id)
        res = self.easyXML(res) 
        return res


    def getModelsIdByPerson(self, personName):
        """Retrieves the identifiers of all models which have a given person as
        author or encoder.


        :param str personName: author's or encoder's name
        :return: list of models identifiers

        ::

             >>> print b.getModelsIdByPerson(u"Novère")

        .. note:: the use of the letter **u** in front of the string to encode special characters.

        """
        return self.serv.getModelsIdByPerson(personName)

    def getSimpleModelsByReactomeIds(self, reacID):
        """Retrieves all the models which are annotated with the given Reactome
records.

        :param: list of reactome identifiers (e.g., REACT_1590)

        :return:  models annotated with the provided Reactome identifiers, as a TreeMap (which uses Reactome identifiers as keys) 


        .. seealso:: How to retrieve REACTOME IDs in :meth:`extra_getReactomeIds`
        """
        res = self.serv.getSimpleModelsByReactomeIds(reacID)
        res = self.easyXML(res) 
        return res


    def getModelsIdByUniprotId(self, Id):
        """Retrieves all the models which are annotated with the given UniProt records.


            >>> ID = 'BIOMD0000000033'
            >>> b.serv.getSimpleModelsByIds(ID)

        Working Uniprot Id returns the same Model (sameId) but note the
        reference. It is now a uniprot reference::

            >>> b.serv.getSimpleModelsByUniprotIds('P10113')

        The issue is to figure out the uniprot Id from the model... similarly to        the search with Reactome Id, we provide a function to retrieve Uniprot 
        Id found in the models.
    

        """
        res = self.serv.getModelsIdByUniprotId(Id)
        return res

    def getModelsIdByName(self, name):
        """Retrieves the models' identifiers which name includes the given keyword.

        :param str name: 
        :return:  array of strings - list of models identifiers

        ::

            >>> b.getModelsIdByName("2009")

        """
        
        return self.serv.getModelsIdByName(name)

    def getModelsIdByPublication(self, pubId):
        """Retrieves the identifiers of all models related to one (or more) publication(s).


        :param str pubId: publication identifier PMID or DOI or text which occurs in the publications.
        
        ::

            b.getModelsIdByPublication('18308339')
            ['BIOMD0000000201']

        """
        return self.serv.getModelsIdByPublication(pubId)


    def getModelsIdByGO(self, goId):
        """Retrieves the identifiers of all models related to a Gene Ontology Id.
    
        ::

            >>> b.getModelsIdByGO('0001756')
            ['BIOMD0000000201', 'BIOMD0000000275']

        .. seealso:::meth:`getModelsIdByGOId`

        """
        return self.serv.getModelsIdByGO(goId)

    def getModelsIdByTaxonomy(self, text):
        """Retrieves the models which are associated to the provided Taxonomy text.

        :param str text: free text

        """
        return self.serv.getModelsIdByTaxonomy(text)

    def getModelsIdByTaxonomyId(self, taxonomyId):
        """Retrieves the models which are annotated with the given taxon.


        :param str text: free text

        Taxonomy identifier (e.g. 9606)

        """
        return self.serv.getModelsIdByTaxonomyId(taxonomyId)


    def getSubModelSBML(self, modelId, elementsIDs):
        """


        :param modelId: identifier of the model from which the sub-model will be extracted
        :param elementsIDs: identifiers of the selected elements. Currently only
            supports identifiers from compartments, species, and reactions.
        """
        return self.serv.getSubModelSBML(modelId, elementsIDs)


    def getModelsIdByGOId(self, GOId):
        """Retrieves the models which are annotated with the given Gene Ontology term.

        :param str GOId: Gene Ontology identifier (e.g. GO:0006915)

        .. seealso:::meth:`getModelsIdByGO`

        """
        return self.serv.getModelsIdByGOId(GOId)


    def extra_getReactomeIds(self, start=0, end=1000):
        """Retrive value REACTOME Ids by scanning all Ids in a given range

        :param int start:
        :param int end:

        Search all models for reactome Ids in range REACT_start to REACT_end. 
        Can take a while.


        For instance, scanning the database for start=0 and end=3000, a list of
        106 reactome Id are returned and its takes a minute or two.
        """
        Ids = []
        for i in range(start, end):
            if i%100 == 0 and i>0:
                print("%f  done" % ((i-start)*100./float(end-start)))
            res = self.serv.getSimpleModelsByReactomeIds(['REACT_%s'%i])
            if 'REACT' in res:
                Ids.append('REACT_%s' % i)
        return Ids


    def extra_getUniprotIds(self, start=10000, end=11000):
        """Retrieve the Uniprot IDs  

        :param int start: starting ID value used to scan the database
        :param int end: ending ID value used to to scan the database
        :return: list of uniprot IDs that have been found in the DB.

        It may be useful to know the uniprot IDs that are available in all
        models. Not all of them are indeed available. This function is slow and
        you should use it with parcimony. This is why we set start and end IDs.

        ::

            >>> res = b.extra_getUniprotIds(10000,11200)
            ['P10113',
             'P10415',
             'P10523',
             'P10600',
             'P10646',
             'P10686',
             'P10687',
             'P10815',
             'P11071']
        """

        Ids = []
        for i in range(start, end):
            if i%100 == 0 and i>0:
                print("%f  done" % ((i-start)*100./float(end-start)))
            res = self.serv.getSimpleModelsByUniprotIds(['P%s'%i])
            if 'P%s' % i in res:
                Ids.append('P%s' % i)
        return Ids


