#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""This module provides a class :class:`~BioModels` to access to BioModels WS.


.. topic:: What is BioModels ?

    :URL: http://www.ebi.ac.uk/biomodels/
    :Service: http://www.ebi.ac.uk/biomodels
    :Citations: please visit https://www.ebi.ac.uk/biomodels/citation for details

    .. highlights::

        "BioModels is a repository of mathematical models of biological and biomedical
        systems. It hosts a vast selection of existing literature-based physiologically
        and pharmaceutically relevant mechanistic models in standard formats. Our
        mission is to provide the systems modelling community with reproducible,
        high-quality, freely-accessible models published in the scientific literature."

        -- From BioModels website, March 2020


"""
import os
import copy
import webbrowser
from functools import wraps
from bioservices import logger

logger.name = __name__

from bioservices.services import REST

try:
    # python 3
    from urllib.request import urlopen
except:
    from urllib2 import urlopen

__all__ = ["BioModels"]


class BioModels(REST):
    """Interface to the `BioModels <http://www.ebi.ac.uk/biomodels>`_ service

    ::

        from bioservices import BioModels
        bm = BioModels()
        model = bm.get_model('BIOMD0000000299')


    Previous API had several functions such as *getAuthorsByModelId*. This is
    easy to mimic with the new API::

        bm = BioModels()
        models = bm.get_all_models()
        [x['submitter'] for x in res if x[] == "MODEL1204280003"][0]

    This is also true for *getDateLastModifByModelId* and *getModelNameById* if
    one use the field *lastModified* or *name*. There was the ability to
    search for models based on their CHEBI identifiers, which is not
    supported anymore; this concerns functions
    *getModelsIdByChEBI*, *getModelsIdByChEBIId*, *getSimpleModelsByChEBIIds*,
    *getSimpleModelsRelatedWithChEBI*. For other searches related to Reactome,
    Uniprot identifiers or GO terms, the :meth:`search` method should work::

        bm.search("P10113")
        bm.search("REACT_33")
        bm.search("GO:0006919")

    """

    _url = "https://www.ebi.ac.uk/biomodels"
    _id_example = "BIOMD0000000100"

    def __init__(self, verbose=True):
        """.. rubric:: constructor

        :param bool verbose:


        """
        super(BioModels, self).__init__(name="BioModels", url=BioModels._url, verbose=verbose)

    def _check_format(self, frmt, supported=["json", "xml", "html"]):
        if frmt not in supported:
            raise ValueError("Supported format for this function are {}. You provided {}".format(supported, frmt))

    def get_all_models(self, chunk=100):
        """Return all models"""
        models = []
        offset = 0
        res = self.search("*.*", numResults=chunk)
        while len(res["facets"]):
            models.extend(res["models"])
            offset += chunk
            res = self.search("*.*", offset=offset, numResults=chunk)
        return models

    def get_model(self, model_id, frmt="json"):
        """Fetch information about a given model at a particular revision."""
        self._check_format(frmt)
        res = self.http_get(model_id, frmt=frmt, params={"format": frmt})
        return res

    def get_model_files(self, model_id, frmt="json"):
        """Extract metadata information of model files of a particular model

        :param model_id: a valid BioModels identifier
        :param frmt: format of the output (json, xml)
        """
        self._check_format(frmt, ["xml", "json"])
        res = self.http_get("model/files/{}".format(model_id), frmt=frmt, params={"format": frmt})
        return res

    def get_model_download(self, model_id, filename=None, output_filename=None):
        """Download a particular file associated with a given model or all its
        files as a COMBINE archive.

        :param model_id: a valid BioModels identifier
        :param str filename: this is the requested filename to be found in the
            model
        :param str output_filename: if you request a different output filename,
            use this parameter
        :param frmt: format of the output (json, xml, html)
        :return:  nothing. This function save the model into a ZIP file called
            after the model identifier. If parameter *filename* is specified,
            then the output file is the requested filename (if found)

        ::

            bm.get_model_download("BIOMD0000000100", filename="BIOMD0000000100.png")
            bm.get_model_download("BIOMD0000000100")


        This function can retrieve all files in a ZIP archive or a single image.
        In the example below, we retrieve the PNG and plot it using matplotlib.
        Using your favorite image viewver, you should get a better resolution.
        Or just download the SVG version of the model.

        .. plot::
            :include-source:

            from bioservices import BioModels
            bm = BioModels()
            from easydev import TempFile
            with TempFile(suffix=".png") as fout:
                bm.get_model_download("BIOMD0000000100",
                        filename="BIOMD0000000100.png",
                        output_filename=fout.name)
                from pylab import imshow, imread
                imshow(imread(fout.name), aspect="auto")
        """
        params = {}
        if filename:
            params["filename"] = filename

        res = self.http_get("model/download/{}".format(model_id), params=params)

        if filename:
            self.logging.info("Saving {}".format(filename))
            if output_filename is None:
                output_filename = filename
            with open(output_filename, "wb") as fout:
                fout.write(res.content)
        else:
            self.logging.info("Saving file {}.zip".format(model_id))
            if output_filename is None:
                output_filename = "{}.zip".format(model_id)
            with open(output_filename, "wb") as fout:
                fout.write(res.content)

    def search(self, query, offset=None, numResults=None, sort=None, frmt="json"):
        """Search models of interest via keywords.

        Examples: PUBMED:"27869123" to search models associated with the PubMed
        record identified by 27869123.

        :param str query: search query. colon character must be escaped
        :param int offset: number of items to skip before starting to collect the
            result set
        :param int numResults: number of items to return
        :param str sort: sort criteria in {id-asc, relevance-asc, relevance-desc,
            first_author-asc, first_author, name-asc, name-desc,
            publication_year-asc, publication_year-desc}
        :param str frmt: format of the output (json, xml)

        """
        self._check_format(frmt, ["xml", "json", "html"])
        params = {"query": query, "format": frmt}
        if offset:
            params["offset"] = offset
        if numResults:
            params["numResults"] = numResults
        if sort:
            params["sort"] = sort

        sort_options = [
            "id-asc",
            "relevance-asc",
            "relevance-desc",
            "first_author-asc",
            "first_author",
            "name-asc",
            "name-desc",
            "publication_year-asc",
            "publication_year-desc",
        ]
        if sort and sort not in sort_options:
            raise ValueError("sort must be in {}. You provided {}".format(sort_options, sort))
        res = self.http_get("search", params=params)
        return res

    def search_download(self, models, output_filename="models.zip", force=False):
        """Returns models (XML) corresponding to a list of model identifiers.

        :param str models: list of model identifiers using comma to separate
            them. Could be a list of string (e.g 'BIOMD1,BIOMD2' or ['BIOMD1',
            'BIOMD2']
        :param str output_filename: file used to save the models. This is a
            zipped file. If the file exists, you must use the *force** parameter

        .. todo:: if no models are found (typos), an error message is printed.
            if one model is not found, there is no warning or errors. Could be
            nice to have a warning by introspecting the number of models in the
            output file
        """
        if isinstance(models, list):
            models = ",".join(models)
        res = self.http_get("search/download", params={"models": models})

        if res == 404:
            self.logging.error("One of your model ID was probably incorrect")
            return

        self.logging.info(output_filename)
        if os.path.exists(output_filename) and force is False:
            raise IOError(
                "{} exists already. Set force to True or change the output_filename argument".format(output_filename)
            )

        with open(output_filename, "wb") as fout:
            fout.write(res.content)

    def search_parameter(self, query, start=0, size=10, sort=None, frmt="json"):
        """Search for parameters of a model

        **Details** BioModels Parameters is a resource that facilitates easy
        search and retrieval of parameter values used in the SBML models stored in the
        BioModels repository. Users can search for a model entity (e.g. a protein or
        drug) to retrieve the rate equations describing it; the associated parameter
        values and the initial concentration from the SBML models in BioModels. Although
        these data are directly extracted from the curated SBML models, they are not
        individually curated or validated; rather presented as such in the table below.
        Hence BioModels Parameters table will only provide a quick overview of available
        parameter values for guidance and original model should be referred to
        understand the complete context of the parameter usage.


        :param str query: A query to search against the model parameter values.
        :param int start: if is the offset of the result set (default 0)
        :param int size: number of items to display per page
        :param str sort: model or entity
        :param str frmt: the format of the result (xml, csv, json)

        ::

            bm.search_parameter("MAPK", size=100, sort="entity")

        """
        self._check_format(frmt, ["xml", "json", "csv"])
        params = {"format": frmt, "size": size, "start": start, "query": query}
        sort_options = ["model", "entity", None]
        if sort not in sort_options:
            raise ValueError("sort must be in {}. You provided {}".format(sort_options, sort))
        if sort:
            params["sort"] = sort

        res = self.http_get("parameterSearch/search", params=params)

        return res

    def get_p2m_missing(self, frmt="json"):
        """Retrieve all models in Path2Models that are now only available indirectly,
        through the representative model for the corresponding genus

        :param str frmt: the format of the result (xml, csv, json)
        :return: list of model identifiers

        """
        self._check_format(frmt)
        res = self.http_get("p2m/missing", params={"format": frmt})
        res = res["missing"]
        self.logging.info("Found {} missing model".format(len(res)))
        return res

    def get_p2m_representative(self, model, frmt="json"):
        """Retrieve a representative model in Path2Models

        Get the representative model identifier for a given missing model in Path2Models.
        This endpoint accepts as parameters a mandatory model identifier and an
        optional response format

        :param str model: The identifier of a model of interest
        :param str frmt: the format of the result (xml, csv, json)

        """
        self._check_format(frmt)
        res = self.http_get("p2m/representative", params={"format": frmt, "model": model})
        return res

    def get_p2m_representatives(self, models, frmt="json"):
        """Find the replacement accessions for a set of Path2Models entries

        Get the representative model identifiers of a set of given missing
        models in Path2Models. This end point expects a comma-separated list of model
        identifiers (without any surrounding whitespace) and an optional response
        format. Examples: BMID000000112902, BMID000000009880, BMID000000027397.

        :param str model: The model identifiers separated by commas, or as a
            list.
        :param str frmt: the format of the result (xml, csv, json)

        .. doctest::

            from bioservices import BioModels
            bm = BioModels()
            bm.get_p2m_representatives("BMID000000112902, BMID000000009880, BMID000000027397")


        """
        if isinstance(models, list):
            models = ",".join(models)
        else:
            # Get rid of possible spaces
            models = ",".join([x.strip() for x in models.split(",")])

        self._check_format(frmt)
        res = self.http_get("p2m/representatives", params={"format": frmt, "modelIds": models})
        return res

    def get_pdgsmm_missing(self, frmt="json"):
        """Retrieve the identifiers of all PDGSMM entries that are no longer directly accessible

        :param str frmt: the format of the result (xml, csv, json)
        :return: list of model identifiers
        """
        self._check_format(frmt)
        res = self.http_get("pdgsmm/missing", params={"format": frmt})
        res = res["missing"]
        self.logging.info("Found {} missing model".format(len(res)))
        return res

    def get_pdgsmm_representative(self, model, frmt="json"):
        """Retrieve a representative model in PDGSMM

        Get the representative model identifier for a given missing model in
        PDGSMM. This endpoint accepts as parameters a mandatory model identifier and an
        optional response format.

        :param str model: The identifier of a model of interest
        :param str frmt: the format of the result (xml, csv, json)

        """
        self._check_format(frmt)
        res = self.http_get("pdgsmm/representative", params={"format": frmt, "model": model})
        return res

    def get_pdgsmm_representatives(self, models, frmt="json"):
        """Find the replacement accessions for a set of PDFSSM

        Get the representative model identifiers of a set of given missing
        models in PDGSMM. This end point expects a comma-separated list of model
        identifiers (without any surrounding whitespace) and an optional response
        format. Examples: MODEL1707110145,MODEL1707112456,MODEL1707115900.

        :param str model: The model identifiers separated by commas, or as a
            list.
        :param str frmt: the format of the result (xml, csv, json)

        """
        if isinstance(models, list):
            models = ",".join(models)
        else:
            # Get rid of possible spaces
            models = ",".join([x.strip() for x in models.split(",")])

        self._check_format(frmt)
        res = self.http_get("pdgsmm/representatives", params={"format": frmt, "modelIds": models})
        return res
