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
"""This module provides a class :class:`~BioModels` that allows an easy access to all the
BioModel service.


"""


from services import Service
import webbrowser
import copy



class BioModels(Service):
    """Interface to the KEGG database

    ::


    """
    def __init__(self, verbose=True, debug=False, url=None):
        """Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """
        if url == None:
            url = "http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl"
        super(BioModels, self).__init__(name="BioModels", url=url, verbose=verbose)

        self._modelsId = None



    def __len__(self):
        l = len(self.serv.getAllModelsId())
        return l


    def getAllModelsId(self):
        """Retrieves the identifiers of all published models

        :return: list of models identifiers
        """
        return self.serv.getAllModelsId()

    def _get_models_id(self):
        if self._modelsId == None:
            self._modelsId = self.serv.getAllModelsId()
        return self._modelsId
    modelsId = property(_get_models_id)


    def getAllCuratedModelsId(self):
        """Retrieves the identifiers of all published curated models

        :return: list of models identifiers
        """
        return self.serv.getAllCuratedModelsId()

    def getAllNonCuratedModelsId(self):
        """Retrieves the identifiers of all published curated models

        :return: list of models identifiers
        """
        return self.serv.getAllNonCuratedModelsId()

    def getModelById(self, Id):
        if Id in self.modelsId:
            return self.serv.getModelById(Id)
        else:
            raise ValueError("Id provided is not a valid ID. See modelsId attribute.")

    
todo = [
 u'getAuthorsByModelId',
 u'getDateLastModifByModelId',
 u'getEncodersByModelId',
 u'getLastModifiedDateByModelId',
 u'getModelNameById',
 u'getModelSBMLById',
 u'getModelsIdByChEBI',
 u'getModelsIdByChEBIId',
 u'getModelsIdByGO',
 u'getModelsIdByGOId',
 u'getModelsIdByName',
 u'getModelsIdByPerson',
 u'getModelsIdByPublication',
 u'getModelsIdByTaxonomy',
 u'getModelsIdByTaxonomyId',
 u'getModelsIdByUniprot',
 u'getModelsIdByUniprotId',
 u'getModelsIdByUniprotIds',
 u'getPublicationByModelId',
 u'getSimpleModelById',
 u'getSimpleModelsByChEBIIds',
 u'getSimpleModelsByIds',
 u'getSimpleModelsByReactomeIds',
 u'getSimpleModelsByUniprotIds',
 u'getSimpleModelsRelatedWithChEBI',
 u'getSubModelSBML',
 u'helloBioModels']


