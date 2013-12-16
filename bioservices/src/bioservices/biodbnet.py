#!/usr/bin/python
# -*- coding: latin-1 -*-
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
#$Id: biomodels.py 207 2013-06-12 15:48:05Z cokelaer $
"""This module provides a class :class:`~BioDBNet` to access to BioDBNet WS.


.. topic:: What is BioDBNet ?

    :URL: http://www.ebi.ac.uk/biomodels-main/
    :Service: http://www.ebi.ac.uk/biomodels-main/services/BioDBNetWebServices?wsdl
    :Citations: http://www.ncbi.nlm.nih.gov/pubmed/20587024    

    .. highlights::

        "BioDBNet Database is a repository hosting computational models of biological
        systems. A large number of the provided models are published in the
        peer-reviewed literature and manually curated. This resource allows biologists
        to store, search and retrieve mathematical models. In addition, those models can
        be used to generate sub-models, can be simulated online, and can be converted
        between different representational formats. "

        -- From BioDBNet website, Dec. 2012


Some keywords used in this module:


"""
from bioservices.services import WSDLService
import SOAPpy

__all__ = ["BioDBNet"]




class BioDBNet(WSDLService):
    """Interface to the `BioDBNet <http://www.ebi.ac.uk/biomodels>`_ service 

    ::

        >>> from bioservices import *
        >>> s = BioDBNet()
        >>> model = s.getModelSBMLById('BIOMD0000000299')

    The number of models available can be retrieved easily as well as the model IDs::

        >>> len(s)
        >>> s.modelsId

    Most of the BioDBNet WSDL are available. There are functions added to
    the original interface such as :meth:`extra_getReactomeIds`.


    """
    _url = 'http://biodbnet.abcc.ncifcrf.gov/webServices/bioDBnet.wsdl'
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(BioDBNet, self).__init__(name="BioDBNet", url=BioDBNet._url, verbose=verbose)

    def _interpret_input_db(self, inputValues):
        if isinstance(inputValues, list):
            inputValues = ",".join(inputValues)
            return inputValues
        elif isinstance(inputValues, str):
            return inputValues
        else:
            raise NotImplementedError

    def _interpret_output_db(self, input_db, output_db):
        if isinstance(output_db, list):
            outputs = ",".join(output_db)
        else:
            outputs = output_db
        inputResult = self.getInputs()
        #getOutputsForInput method
        outputResult = self.getOutputsForInput(input_db)
        for output in outputs.split(","):
            if output not in outputResult:
                print(output + " not found")
                print(outputResult)
                raise Exception
        return outputs



    def db2db(self, input_db, output_db, inputValues, taxon=9606):
        """Retrieves the models which are associated to the provided Taxonomy text.

        :param str text: free (Taxonomy based) text
        :return:  list of model identifiers 

        input_db = 'Ensembl Gene ID' 
        output_db = ['Gene Symbol, Ensembl Protein ID']
        inputValues = 'ENSG00000121410, ENSG00000171428' 

        """
        inputValues = self._interpret_input_db(inputValues)
        outputs = self._interpret_output_db(input_db, output_db)

        #dbPath = 'Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID' 
        #getDirectOutputsForInput method
        #directOutputResult = self.getDirectOutputsForInput(input_db)

        #db2db method
        if taxon:
            taxonId = str(taxon)
            params = SOAPpy.structType({'input': input_db, 'inputValues':
                inputValues, 'outputs': outputs, 'taxonId': taxonId}) 
        else:

            params = SOAPpy.structType({'input': input, 'inputValues': 
                inputValues, 'outputs': outputs, 'taxonId': ''})

        res = self.serv.db2db(params)


    def dbFind(self, input_db, inputValues, taxon="9606"):
        inputValues = self._interpret_input_db(inputValues)
        taxonId = str(taxon)
        params = SOAPpy.structType({'input': input_db, 'inputValues':
            inputValues, 'taxonId': taxonId}) 
        return self.serv.dbFind(params)
        

    def dbOrtho(self, input_db, output_db, inputValues, input_taxon, output_taxon):
        raise NotImplementedError
        inputValues = self._interpret_input_db(inputValues)
        outputs = self._interpret_output_db(input_db, output_db)

        taxon1 = str(input_taxon)
        taxon2 = str(output_taxon) # could be a list ?

        params = SOAPpy.structType({'input': input, 'output': output,
            'inputValues': inputValues,  'inputTaxon': taxon1, 'outputTaxon':
            taxon2})
        
        return self.serv.dbOrtho(params)

    def dbReport(self, input_db, inputValues, taxon=9606):
        inputValues = self._interpret_input_db(inputValues)
        taxonId = str(taxon)
        params = SOAPpy.structType({'input': input_db, 'inputValues':
            inputValues, 'taxonId': taxonId}) 
        return self.serv.dbReport(params)

    def dbWalk(self , dbPath, inputValues, taxon=9606):
        dbPath = 'Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID'
        inputValues = self._interpret_input_db(inputValues)
        taxonId = str(taxon)
        params = SOAPpy.structType({'dbPath': dbPath, 'inputValues':
            inputValues, 'taxonId': taxonId})
        return self.serv.dbWalk(params)

    def getDirectOutputsForInput(self, input_db):
        return self.serv.getDirectOutputsForInput(input_db).split(",")

    def getInputs(self):
        return self.serv.getInputs().split(",")

    def getOutputsForInput(self, input_db):
        if input_db not in self.getInputs():
            raise ValueError("Invalid input database provided")
        return self.serv.getOutputsForInput(input_db).split(",")



