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
"""This module provides a class :class:`~BioModels` to access to BioModels WS.


.. topic:: What is BioModels ?

    :URL: http://www.ebi.ac.uk/biomodels-main/
    :Service: http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl
    :Citations: http://www.ncbi.nlm.nih.gov/pubmed/20587024

    .. highlights::

        "BioModels Database is a repository hosting computational models of biological
        systems. A large number of the provided models are published in the
        peer-reviewed literature and manually curated. This resource allows biologists
        to store, search and retrieve mathematical models. In addition, those models can
        be used to generate sub-models, can be simulated online, and can be converted
        between different representational formats. "

        -- From BioModels website, Dec. 2012


Some keywords used in this module:

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

.. testsetup:: biomodels

    from bioservices import *
    s = BioModels()


"""

import copy
import webbrowser
from functools import wraps

from bioservices.services import WSDLService

__all__ = ["BioModels"]


def encode(fn):
    """a decorator that checks the validity of a model Id"""
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        res = fn(self, *args, **kwargs)
        # somehow this fixes the fact that the __repr__ fails because there
        # are ascii characters in res whereas "" is a unicode so
        # ""+res is cast into a unicode.
        try:
            return "" + res
        except:
            return res
    return wrapped


def checkId(fn):
    """a decorator that checks the validity of a model Id"""
    @wraps(fn)
    def wrapped(self, Id, **kwargs):
        ids = getattr(self, "modelsId")
        if Id in ids:
            res = fn(self, Id, **kwargs)
            return res
        else:
            raise ValueError("""Id provided is not a valid ID. See modelsId attribute.""")
    return wrapped


class BioModels(WSDLService):
    """Interface to the `BioModels <http://www.ebi.ac.uk/biomodels>`_ service

    ::

        >>> from bioservices import *
        >>> s = BioModels()
        >>> model = s.getModelSBMLById('BIOMD0000000299')

    The number of models available can be retrieved easily as well as the model IDs::

        >>> len(s)
        >>> s.modelsId

    Most of the BioModels WSDL are available. There are functions added to
    the original interface such as :meth:`extra_getReactomeIds`.


    """
    _url = "http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl"
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(BioModels, self).__init__(name="BioModels", url=BioModels._url, verbose=verbose)

    #: used to store all model Ids once for all
        self._modelsId = None

    def __len__(self):
        l = len(self.serv.getAllModelsId())
        return l

    def _item2list(self, sid):
        #valid_ids = self.modelsId

        if isinstance(sid, str):
            sid = [sid]
        elif isinstance(sid, list) is False:
            raise TypeError("list of identifiers must be a list of string or one string")

        return sid

    def getAllModelsId(self):
        """Retrieves the identifiers of all published models

        :return: list of model identifiers


        ::

            >>> s.getAllModelsId()

        .. note:: you cal also use the :attr:`modelsId`

        """
        return self.serv.getAllModelsId()

    def _get_models_id(self):
        if self._modelsId is None:
            self._modelsId = self.serv.getAllModelsId()
        return self._modelsId
    modelsId = property(_get_models_id, doc="list of all model Ids")


    def getAllCuratedModelsId(self):
        """Retrieves the identifiers of all published **curated** models

        :return: list of model identifiers

        ::

            >>> s.getAllCuratedModelsId()

        """
        return self.serv.getAllCuratedModelsId()

    def getAllNonCuratedModelsId(self):
        """Retrieves the identifiers of all published **non** **curated** models

        :return: list of model identifiers

        ::

            >>> s.getAllNonCuratedModelsId()

        """
        return self.serv.getAllNonCuratedModelsId()



    @encode
    @checkId
    def getModelById(self, Id):
        """Retrieves the SBML form of a model (in a string) given its identifier

        :param str Id: a valid ,odel Id

    .. warning:: this method is now deprecated!

        ::

            model = s.getModelById("BIOMD0000000256")

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

            >>> s.getAuthorsByModelId("BIOMD0000000299")
            ['Leloup JC', 'Gonze D', 'Goldbeter A']

        """
        return self.serv.getAuthorsByModelId(Id)

    @checkId
    def getDateLastModifByModelId(self, Id):
        """Retrieves the date of last modification of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: date of last modification (expressed according to ISO 8601)

        ::

            >>> s.getLastModifiedDateByModelId("BIOMD0000000256")
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

             >>> s.getEncodersByModelId("BIOMD0000000256")
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

            >>> print(s.getModelNameById("BIOMD0000000256"))
            'Rehm2006_Caspase'

        """
        return self.serv.getModelNameById(Id)

    @encode
    @checkId
    def getModelSBMLById(self, Id):
        """Retrieves the SBML form of a model (in a string) given its identifier

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: str - SBML model in a string

        ::

            >>> from bioservices import *
            >>> s = BioModels()
            >>> s.getModelSBMLById('MODEL1006230101')

        """
        return "" + self.serv.getModelSBMLById(Id)

    def getModelsIdByChEBI(self, Id):
        """Retrieves the identifiers of all models which are **associated** to
        some ChEBI terms. This relies on the method 'getLiteEntity' of the
        ChEBI Web Services (cf. http://www.ebi.ac.uk/chebi/webServices.do).

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.
        :return:  list of model identifiers

        ::

            >>> s.getModelsIdByChEBI("CHEBI:4978")
            ['BIOMD0000000217', 'BIOMD0000000404']

        .. seealso:: :meth:`getSimpleModelsByChEBIIds`,
            :meth:`getSimpleModelsRelatedWithChEBI`, :meth:`getModelsIdByChEBIId`
        """
        return self.serv.getModelsIdByChEBI(Id)

    def getModelsIdByChEBIId(self, Id):
        """Retrieves the identifiers of all the models which are **annotated** with
        a given ChEBI term.

        :param str Id: identifier of a ChEBI term (e.g. CHEBI:4978)
        :return:  list of model identifiers

        .. doctest:: biomodels

            >>> from bioservices import *
            >>> s = BioModels()
            >>> s.getModelsIdByChEBIId('CHEBI:4978')
            ['BIOMD0000000404']

        .. seealso:: :meth:`getSimpleModelsByChEBIIds`,
            :meth:`getSimpleModelsRelatedWithChEBI`,
            :meth:`getModelsIdByChEBI`
        """
        return self.serv.getModelsIdByChEBIId(Id)

    def getSimpleModelsByChEBIIds(self, Id):
        """Retrieves the models which are annotated with the given ChEBI terms.

        :param str Id: identifier of a ChEBI term (e.g. CHEBI:4978)

        :return: list with all models annotated with the provided ChEBI identifiers,
            as a TreeMap (which uses ChEBI identifiers as keys)

        .. seealso:: :meth:`getSimpleModelsByChEBIIds`,
            :meth:`getModelsIdByChEBIId`,
            :meth:`getModelsIdByChEBI`

        .. warning:: this method returns empty models even with example
            provided on BioModels website
        """
        ids = self._item2list(Id)
        return self.serv.getSimpleModelsByChEBIIds(ids)

    def getSimpleModelsRelatedWithChEBI(self):
        """Retrieves all the models which are annotated with ChEBI terms.

        The output of this function is a lengthy XML document containing
        utf-8 characters and the models (in simple models format). You can
        convert it and extract information such as the models ID by using
        the our xml parser and the following code::

            res = s.getSimpleModelsRelatedWithChEBI()
            res = self.easyXML(res.encode('utf-8'))
            set([x.findall('modelId')[0].text for x in res.getchildren()])

        .. note:: the output is a string. You can convert it to a class that
            ease its introspection using :meth:`~bioservices.services.Service.easyXML`.
        .. seealso:: :meth:`getSimpleModelsByChEBIIds`,
            :meth:`getModelsIdByChEBIId`,
            :meth:`getModelsIdByChEBI`

        """
        return self.serv.getSimpleModelsRelatedWithChEBI()

    @checkId
    def getPublicationByModelId(self, Id):
        """Retrieves the publication's identifier of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: publication identifier (can be a PMID, DOI or URL)

        ::

            >>> s.getPublicationByModelId("BIOMD0000000256")
            '16932741'

        .. seealso:: You can open the corresponding pubmed HTML page with
            :meth:`pubmed`
        """
        return self.serv.getPublicationByModelId(Id)

    @checkId
    def getSimpleModelsByIds(self, Ids):
        """Retrieves the main information about given models.

        :param str Ids: a valid model Id. See :attr:`modelsId` attribute.

        :return: a XML representaton (string) of the model meta information including
            identifier, name, publication identifier date of last modification...

        ::

            >>> model = s.getSimpleModelsByIds("BIOMD0000000256")

        .. note:: the output is a string. You can convert it to a class that
            ease its introspection using :meth:`~bioservices.services.Service.easyXML`.
        """
        ids = self._item2list(Ids)
        res = self.serv.getSimpleModelsByIds(ids)
        return res


    def getModelsIdByPerson(self, personName):
        """Retrieves the identifiers of all models which have a given person as
        author or encoder.


        :param str personName: author's or encoder's name
        :return: list of model identifiers

        ::

             >>> print(s.getModelsIdByPerson(u"Novère"))

        .. note:: the use of the letter **u** in front of the string to encode special characters.

        """
        return self.serv.getModelsIdByPerson(personName)

    def getSimpleModelsByReactomeIds(self, reacID, raw=False):
        """Retrieves all the models which are annotated with the given Reactome
records.

        :param: list of reactome identifiers (e.g., REACT_1590)
        :param bool raw: return raw data if True

        :return:  models annotated with the provided Reactome identifiers, as a TreeMap (which uses Reactome identifiers as keys)


        .. seealso:: How to retrieve REACTOME IDs in :meth:`extra_getReactomeIds`
        .. note:: the output is converted to ease introspection
             using :meth:`~bioservices.services.Service.easyXML`.
        """
        reacID = self._item2list(reacID)
        res = self.serv.getSimpleModelsByReactomeIds(reacID)
        if raw is not True:
            res = self.easyXML(res)
        return res


    def getModelsIdByUniprot(self, text):
        """Retrieves all the models which are associated to the provided UniProt text.

        :param str text: a free UniProt based text
        :return:  list of model identifiers

        ::

            >>> s.getModelsIdByUniprot("P10113")
            ['BIOMD0000000033']

        """
        res = self.serv.getModelsIdByUniprot(text)
        return res

    def getModelsIdByUniprotId(self, Id):
        """Retrieves all the models which are annotated with the given UniProt records.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.
        :return:  list of model identifiers

        ::

            >>> s.getModelsIdByUniprot("P10113")
            ['BIOMD0000000033']


        """
        res = self.serv.getModelsIdByUniprotId(Id)
        return res

    def getModelsIdByUniprotIds(self, Ids_list):
        """Retrieves all the models which are annotated with the given UniProt records.

        :param str Ids_list: a valid model Id. See :attr:`modelsId` attribute.
        :return:  list of model identifiers

        ::

            >>> s.getModelsIdByUniprotIds(["P10113", "P10415"])
            ['BIOMD0000000033', 'BIOMD0000000220']

        """
        return self.serv.getModelsIdByUniprotIds(Ids_list)


    def getModelsIdByName(self, name):
        """Retrieves the models' identifiers which name includes the given keyword.

        :param str name:
        :return:  array of strings - list of model identifiers

        ::

            >>> res = s.getModelsIdByName("2009")

        """

        return self.serv.getModelsIdByName(name)

    def getModelsIdByPublication(self, pubId):
        """Retrieves the identifiers of all models related to one (or more) publication(s).


        :param str pubId: publication identifier PMID or DOI or text which occurs in the publications.

        ::

            s.getModelsIdByPublication('18308339')
            ['BIOMD0000000201']

        """
        return self.serv.getModelsIdByPublication(pubId)


    def getModelsIdByGO(self, goId):
        """Retrieves the identifiers of all models related to a Gene Ontology Id.

        :param str goId: a free GO text
        :return:  list of model identifiers

        ::

            >>> s.getModelsIdByGO('0001756')
            ['BIOMD0000000201', 'BIOMD0000000275']

        .. seealso:::meth:`getModelsIdByGOId`

        """
        return self.serv.getModelsIdByGO(goId)

    def getModelsIdByTaxonomy(self, text):
        """Retrieves the models which are associated to the provided Taxonomy text.

        :param str text: free (Taxonomy based) text
        :return:  list of model identifiers

        """
        return self.serv.getModelsIdByTaxonomy(text)

    def getModelsIdByTaxonomyId(self, taxonomyId):
        """Retrieves the models which are annotated with the given taxon.


        :param str taxonomyId: Taxonomy identifier (e.g. 9606)

        """
        return self.serv.getModelsIdByTaxonomyId(taxonomyId)


    @encode
    def getSubModelSBML(self, modelId, elementsIDs):
        """Generates the minimal sub-model of a given model in the database including all selected components.

        :param modelId: identifier of the model from which the sub-model will be extracted
        :param elementsIDs: identifiers of the selected elements. Currently only
            supports identifiers from compartments, species, and reactions.
            could be a string or list of strings

        ::

            s.getSubModelSBML("BIOMD0000000242", "cyclinEdegradation_1")
        """
        sid = self._item2list(elementsIDs)
        return self.serv.getSubModelSBML(modelId, sid)


    def getModelsIdByGOId(self, GOId):
        """Retrieves the models which are annotated with the given Gene Ontology term.

        :param str GOId: Gene Ontology identifier (e.g. GO:0006915)

        .. seealso:::meth:`getModelsIdByGO`

        ::

            >>> s.getModelsIdByGOId("GO:0006919")
            ['BIOMD0000000256', 'BIOMD0000000102', 'BIOMD0000000103']

        """
        return self.serv.getModelsIdByGOId(GOId)

    def extra_getChEBIIds(self, start=0, end=100, verbose=False):
        """Retrieve existing chEBI Ids by scanning the models

        :param int start: starting Id
        :param int end: end Id
        :param bool verbose: show the status of the analysis
        :return: list of chEBI Ids that have been found in the DB.

        This method may be useful to know the ChEBI Ids used in models

        For instance, scanning the database for start=0 and end=200, a list of
        191 chEBI Ids are returned and its takes a minute.

        .. doctest:: biomodels

            >>> s.extra_getChEBIIds(80, 84)
            ['CHEBI:81', 'CHEBI:83', 'CHEBI:84']
        """
        if start > end or start<0:
            raise ValueError("start must be positive and lower than end value")
        Ids = []
        for i in range(start, end+1):
            ChEBI = "CHEBI:" +  str(i)
            if i%100 == 0 and i>0:
                if verbose is True:
                    print("%f %% done" % ((i-start)*100./float(end-start)))
            res = self.getModelsIdByChEBI(ChEBI)
            if res:
                Ids.append(ChEBI)
        return Ids

    def extra_getReactomeIds(self, start=0, end=1000, verbose=False):
        """Retrieve REACTOME Ids by scanning the models

        :param int start: starting Id
        :param int end: end Id
        :param bool verbose: show the status of the analysis
        :return: list of reactome IDs that have been found in the DB.

        Search all models for reactome Ids in range 'REACT_start' to 'REACT_end'.
        Can take a while so do not be greedy and select a short range.

        For instance, scanning the database for start=0 and end=3000, a list of
        106 reactome Id are returned and its takes a minute or two.

        .. doctest:: biomodels

            >>> s.extra_getReactomeIds(0, 100)
            ['REACT_33', 'REACT_42', 'REACT_85', 'REACT_89']
        """
        if start > end or start<0:
            raise ValueError("start must be positive and lower than end value")
        Ids = []
        for i in range(start, end+1):
            if i%100 == 0 and i>0:
                if verbose is True:
                    print("%f %% done" % ((i-start)*100./float(end-start)))
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

            >>> s.extra_getUniprotIds(10000,11200)
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
        if start > end or start<0:
            raise ValueError("start must be positive and lower than end value")
        self.logging.info("Retrieving the uniprot ID from %s to %s" %(start,end))
        Ids = []
        for i in range(start, end):
            if i%100 == 0 and i>0:
                print("%f  done" % ((i-start)*100./float(end-start)))
            res = self.serv.getSimpleModelsByUniprotIds(['P%s'%i])
            if 'P%s' % i in res:
                Ids.append('P%s' % i)
        return Ids


