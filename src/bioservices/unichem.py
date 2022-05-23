#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#  Copyright (c) 2022 - Institut Pasteur
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""This module provides a class :class:`UniChem`

.. topic:: What is UniChem

    :URL:  https://www.ebi.ac.uk/unichem/info/webservices
    :REST:  https://www.ebi.ac.uk/unichem/rest


    .. highlights::

        "UniChem is a 'Unified Chemical Identifier' system, designed to assist
        in the rapid cross-referencing of chemical structures, and their identifiers,
        between databases (read more). "

        -- From UniChem web page June 2013


"""
import json

from bioservices import REST
from bioservices import logger

import colorlog

logger = colorlog.getLogger(__name__)


class UniChem:
    """Interface to the `UniChem <https://www.ebi.ac.uk/unichem/>`_ service

    .. doctest::

            >>> from bioservices import UniChem
            >>> u = UniChem()

    There are lots of sources such as Chembl, Chebi, etc. You will probably need the
    identifiers of those sources. You can get all information about a source using
    these methods::

        # Get information about a source
        u.get_source_info_by_name('chembl')
        u.get_source_info_by_id(10)
        u.get_id_from_name('chembl')
        u.get_all_src_ids()

    but for developers, everything is contained in the :attr:`source_ids` dictionary.

    The first important method provided by Unichem API is the :meth:`get_compounds`.
    For example, you can request all compounds related to the CHEMBL12 identifier
    from ChEMBL using::

        res = u.get_compounds('CHEMBL12', 'chembl')
        compounds = res['compounds'][0]

    Note that the second argument is 'chembl' and lower/upper cases is important.
    All names are stored in :attr:`source_ids` together with their identifiers.

    You can use also :meth:`get_id_from_name` and get_name_from_id` if needed.

    Legacy methods are available:


        get_compound_ids_from_src_id            --> use get_compounds()
        get_src_compound_ids_from_inchikey      --> replaced by get_compounds()
        get_all_src_ids()                       --> uses new API
        get_src_compound_ids_all_from_inchikey  --> get_source_by_inchikey()
        get_verbose_src_compound_ids_from_inchikey  --> get_sources_by_inchikey_verbose()
        get_structure                           --> uses new API get_compounds() and bioservices code
        get_structure_all                       --> dropped
        get_src_compound_id_url                 --> dropped. One can use the get_compounds()
        get_src_compound_ids_all_from_obsolete  --> removed

        get_src_compound_ids_from_src_compound_id  --> removed; was obsolet
        get_src_compound_ids_all_from_src_compound_id --> remoed was already obsolet
        get_all_compound_ids_from_all_src_id   --> removed. no more API
        get_mapping                            --> removed. no more API
        get_auxiliary_mappings                 --> removed. no more API

    Most old functions can be replaced by a syntax such as::

        res = u.get_compound('CHEMBL12', 'chembl')
        res['compounds'][0]


    .. changed:: version 1.9. drop xml parser.


    """

    _url = "https://www.ebi.ac.uk/unichem"

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: **Constructor** UniChem

        :param verbose: set to False to prevent informative messages
        """
        self.services = REST(name="UniChem", url=UniChem._url, verbose=verbose, cache=cache)

        # let us define the source and names
        _data = self.services.http_get("api/v1/sources")
        self._data_source = _data["sources"]
        self.source_ids = {x["name"]: x["sourceID"] for x in self._data_source}

    def get_id_from_name(self, name):
        """Return the ID a a source given its name.

        :param str name: a valid database name (e.g., chembl)

        ::

            u.get_id_from_name("chembl")
        """
        if name in self.source_ids.keys():
            return self.source_ids[name]
        else:
            logger.error(f"You provided {name} but only those sources are available: {sorted(self.source_ids.keys())}")

    def get_sources(self):
        """Returns all information about all sources used in Unichem
        ::

            from bioservices import UniChem
            u = UniChem()
            res = u.get_sources_information()
            res['sources']
        """
        return self._data_source

    # NEWS
    def get_inchi_from_inchikey(self, inchikey):
        """Get a list of inchis given a valid inchikey.

        :param inchikey: InChI Key to search. Unlike the rest API, you can also provide a list.
        :return: a list of inchis matching the InChI Key provided. If input is a list, a
            dictionary is returned where keys are the inchikey input lists.

        ::

            from bioservices import UniChem
            u = UniChem()
            res = u.get_inchi("AAOVKJBEBIDNHE-UHFFFAOYSA-N")

        .. note:: this is a legacy function. introduced in v1.9 after unichem API update
        """
        # if inchikey is not found, return empty {}
        if isinstance(inchikey, (list, tuple)):
            data = {}
            for x in inchikey:
                res = self.services.http_get(f"rest/inchi/{x}")
                data[x] = {} if res == 500 else res
            return data
        else:
            res = self.services.http_get(f"rest/inchi/{inchikey}")
            res = {} if res == 500 else res
            return res

    def get_sources_by_inchikey(self, inchikey):
        """Get sources by inchikey

        :param inchikey: InChI Key to search. Unlike the rest API, you can also provide a list.
        :return: A list of sources for the provided InChIKey if input is a single string.
            a dictionary with keys as inchikey if input is a list.


        .. note:: this is a legacy function. introduced in v1.9 after unichem API update
        """
        # if inchikey is not found, return empty {}
        if isinstance(inchikey, (list, tuple)):
            data = {}
            for x in inchikey:
                res = self.services.http_get(f"rest/inchikey/{x}")
                data[x] = {} if res == 500 else res
            return data
        else:
            res = self.services.http_get(f"rest/inchikey/{inchikey}")
            res = {} if res == 500 else res
            return res

    def get_sources_by_inchikey_verbose(self, inchikey):
        """Get sources by inchikey

        :param inchikey: InChI Key to search. Unlike the rest API, you can also provide a list.
        :return: A list of sources for the provided InChIKey if input is a single string.
            a dictionary with keys as inchikey if input is a list.


        .. note:: this is a legacy function. introduced in v1.9 after unichem API update
        """
        # if inchikey is not found, return empty {}
        if isinstance(inchikey, (list, tuple)):
            data = {}
            for x in inchikey:
                res = self.services.http_get(f"rest/verbose_inchikey/{x}")
                data[x] = {} if res == 500 else res
            return data
        else:
            res = self.services.http_get(f"rest/verbose_inchikey/{inchikey}")
            res = {} if res == 500 else res
            return res

    def get_all_src_ids(self):
        """Obtain all src_ids of sources available in UniChem

        :return: list of 'src_id's.

        ::

            uni.get_all_src_ids()

        """
        return sorted([x["sourceID"] for x in self._data_source])

    def get_source_info_by_name(self, src_name):
        """Description:  Obtain all information on a source by querying with a source id

        :param int src_name: valid identifiers can be found in :attr:`source_ids` e.g.
            chebi, chembl)
        :return: dictionary (or list of dictionaries) with following keys:

            * UCICount: number of entries
            * baseIdUrl: URL of the source
            * created: date of creation
            * description: a description of the content of the source
            * lastUpdated: last date of the update
            * name: the unique name for the source in UniChem, always lower case
            * nameLabel: A name for the source suitable for use as a 'label' for the source
            * nameLong: the full name of the source, as defined by the source
            * private: is it private or not ?
            * sourceID: the src_id for this source
            * srcDetails: details about the source
            * srcReleaseDate: release date of the source database
            * srcReleaseNumber: release number of the source
            * srcUrl: src_url (the main home page of the source)
            * updateComments: possible updates from this source

        ::

            >>> res = get_source_by_name("chebi")

        """
        keys = sorted([x["name"] for x in self._data_source])
        if src_name in keys:
            return [x for x in self._data_source if x["name"] == src_name][0]

        logger.warning(f"incorrect {src_name} source name. Use one of {keys}")

    def get_source_info_by_id(self, ID):
        ids = sorted([x["sourceID"] for x in self._data_source])

        if ID in ids:
            return [x for x in self._data_source if x["sourceID"] == ID][0]

        logger.warning(f"incorrect {ID} source name. Use one of {ids}")

    def get_compounds(self, compound, source_type):
        """Get matched compounds information

        :param str compound: InChI, InChIKey, Name, UCI or Compound Source ID
        :param source_type: uci, inchi, inchikey, sourceID (e.g. chembl)
        :param str sourceID: ID for the source assigned in UniChem when the type is "sourceID"
        :return: a list of matched compounds and their assigned sources


        A legacy function allows you to retrieve a compound from its inchikey::

            u.get_sources_by_inchikey('GZUITABIAKMVPG-UHFFFAOYSA-N')

        However, this new function is faster presumably and allows you to do the same::

            res = u.get_compounds('GZUITABIAKMVPG-UHFFFAOYSA-N', 'inchikey')
            res['compounds']

        You can get the first element, from which inchi, sources, standardInchikey, uci can be extracted.
        The **sources** key contains all compound identifiers for each source::

            res['compounds'][0]['uci']
            res['compounds'][0]['sources']

        Looks like there is always a single element in res['compounds'] but since it is a list,
        you must access to first element (unique) using [0] syntax.

        """
        # we need a default value set to empty string
        sourceID = ""

        # source type can be either one of:
        if source_type in ["uci", "inchi", "inchikey"]:
            pass
        # or a valid source identifier from a valid source name.
        elif source_type in self.source_ids.keys():
            sourceID = int(self.source_ids[source_type])
            source_type = "sourceID"
        # or simply the valid source identifier
        elif source_type in self.source_ids.values():
            sourceID = source_type
            source_type = "sourceID"
        else:
            logger.error(
                f"source_type must be one of uci, inchi, inchikey or a valid source from {sorted(self.source_ids.keys())}"
            )
            return {}

        body = {"compound": compound, "sourceID": sourceID, "type": source_type}
        # somehow, the expected input is a json string and output a json string but cannot be
        # encode/devode by the request even though we provide fmrt=json
        body = json.dumps(body)
        res = self.services.http_post("api/v1/compounds", data=body, headers=self.services.get_headers("json"))
        try:  # pragma: no cover
            res = json.loads(res)
            return res
        except TypeError:  # pragma: no cover
            return {}

    def get_connectivity(self, compound, source_type):
        """Fetch multiple source data sets for a given compound
        with common connectivity to a given id on the database
        source, InChI, InChIkey or UCI

        :param str compound: InChI, InChIKey, Name, UCI or Compound Source ID (e.g. chembl)
        :param source_type: uci, inchi, inchikey, sourceID

        The returned dictionary contains 5 keys:

        * response: service response ('Success' if everything is right)
        * searchedCompound: the summary in terms of inchi, standardInchikey and uci
        * sources: a dictionary with e.g. compoundID and name of the source.
            A 'comparison' dictionary is also provided.
        * totalCompounds: number of searchedCompound entries
        * totalSources: number of sources entries

        """

        # we need a default value set to empty string
        sourceID = ""

        # source type can be either one of:
        if source_type in ["uci", "inchi", "inchikey"]:
            pass
        # or a valid source identifier from a valid source name.
        elif source_type in self.source_ids.keys():
            sourceID = int(self.source_ids[source_type])
            source_type = "sourceID"
        # or simply the valid source identifier
        elif source_type in self.source_ids.values():
            sourceID = source_type
            source_type = "sourceID"
        else:
            logger.error(
                f"source_type must be one of uci, inchi, inchikey or a valid source from {sorted(self.source_ids.keys())}"
            )
            return {}

        body = {"compound": compound, "sourceID": sourceID, "type": source_type}
        # somehow, the expected input is a json string and output a json string but cannot be
        # encode/devode by the request even though we provide fmrt=json
        body = json.dumps(body)
        res = self.services.http_post("api/v1/connectivity", data=body, headers=self.services.get_headers("json"))
        try:  # pragma: no cover
            res = json.loads(res)
            return res
        except TypeError:  # pragma: no cover
            return {}

    def get_images(self, uci, filename=None):
        """Return / create compound image

        :param uci: the UCI of the compound
        :param filename: optional file name to save the SVG+XML output
        :return: the SVG+XML string

        .. plot::

            res = u.get_images('304698', filename='test.svg')

        """
        res = self.services.http_get(f"api/v1/images/{uci}", headers=self.services.get_headers("svg+xml"))
        try:
            res = res.content
            if filename:
                with open(filename, "w") as fout:
                    fout.write(res.decode())
            return res
        except AttributeError:
            logger.warning("Invalid UCI request")

    # OLD ------------------------------
    def get_structure(self, compound_id, src_id):
        """Obtain structure(s) CURRENTLY assigned to a query src_compound_id.

        :param str compound_id: a valid compound identifier
        :param int src_id: corresponding database identifier (name or id).

        :return:  dictionary with 'standardinchi' and 'standardinchikey' keys

        ::

            >>> uni.get_structure("CHEMBL12", "chembl")

        """

        res = self.get_compounds(compound_id, src_id)
        res = res["compounds"]
        res = res[0]
        return {"inchi": res["inchi"]["inchi"], "standardInchiKey": res["standardInchiKey"]}
