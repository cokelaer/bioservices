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
from bioservices import REST


class UniChem(REST):
    """Interface to the `UniChem <http://www.ebi.ac.uk/unichem/>`_ service

    .. doctest::

            >>> from bioservices import UniChem
            >>> u = UniChem()


    """

    _url = "http://www.ebi.ac.uk/unichem/rest"

    def __init__(self, verbose=False, cache=False):
        """**Constructor** UniChem

        :param verbose: set to False to prevent informative messages
        """
        super(UniChem, self).__init__(name="UniChem", url=UniChem._url, verbose=verbose, cache=cache)
        self.source_ids = {
            "chembl":1,
            "drugbank":2,
            "pdb":3,
            "iuphar":4,
            "pubchem_dotf":5,
            "kegg_ligand":6,
            "chebi":7,
            "nih_ncc":8,
            "zinc":9,
            "emolecules":10,
            "ibm":11,
            "atlas":12,
            "patents":13,
            "fdasrc":14,
            "surechem":15,
            "pharmgkb":17,
            "hmdb":18,
            "selleck":20,
            "pubchem_tpharma":21,
            "pubchem":22,
            "mcule":23,
            }# there was no 16 when I looked at the web site June 2013
        self.source_names = self.devtools.swapdict(self.source_ids)

        maxid_service = max(self.get_all_src_ids())
        maxid_bioservices = max(self.source_ids.values())
        if maxid_bioservices != maxid_service:
            self.logging.warning("UniChem has added new source. "+
                    "Please update the source_ids attribute in bioservices")

    def _process(self, query, frmt, request):
        self.devtools.check_param_in_list(frmt, ["json", "xml", None])
        if isinstance(query, str) or isinstance(query, int):
            res = self.http_get(request % query, frmt=frmt)
        else:
            res = self.http_get([request % x for x in query], frmt=frmt)
        return res

    def _get_source_id(self, src_id):
        """Returns the source id given a source name or source id

        Check that the source id is correct by looking at the :attr:`source_ids`
        attribute.

        """
        if src_id in self.source_ids.keys():
            src_id = self.source_ids[src_id]
        elif isinstance(src_id, int) and src_id in self.source_ids.values():
            pass
        elif isinstance(src_id, str) and src_id.isdigit():
            if int(src_id) in self.source_ids.values():
                src_id = int(src_id)
            else:
                raise ValueError("unrecognised src_id parameter. Valid names are %s"
                    % self.source_ids.keys())
        else:
            raise ValueError("unrecognised src_id parameter. Valid names are %s"
                % self.source_ids.keys())

        return src_id

    def get_src_compound_ids_from_src_compound_id(self, src_compound_id, src_id, target=None):
        self.logging.warning("Deprecated. Please use get_compounds_from_source")
        return self.get_src_compound_ids_from_src_id(src_compound_id, src_id, target=target)

    def get_compound_ids_from_src_id(self, src_compound_id, src_id, target=None):
        """Obtain a list of all src_compound_ids from all sources which are
        CURRENTLY assigned to the same structure as a currently assigned query
        src_compound_id.

        The output will include query src_compound_id if it is a valid
        src_compound_id with a current assignment. Note also, that by adding an
        additional (optional) argument (a valid src_id), then results will be restricted
        to only the source specified with this optional argument.

        :param str src_compound_id: a valid compound identifier (list is possible as well)
        :param str src_id: one of the valid database ids. See :attr:`source_ids`.
        :param str,int target: database identifier (name or id) to map to.

        :return: list of dictionaries with the 'src_compound_id' and 'src_id' keys.
            or (if optional *target* is specified, a list with only 'src_compound_id' keys).

        ::

            >>> get_compound_ids_from_src_id("CHEMBL12", "chembl")
            >>> get_compound_ids_from_src_id("CHEMBL12", "chembl", "chebi")
            [{'src_compound_id': '49575'}]

        """
        src_id = self._get_source_id(src_id)
        request = "src_compound_id/%s/" + "%s" %src_id
        if target:
            target = self._get_source_id(target)
            request += "/%s" % target
        res = self._process(src_compound_id, "json", request)
        return res

    def get_src_compound_ids_all_from_src_compound_id(self, src_compound_id,
            src_id, target=None):
        self.logging.warning("Deprecated us get_compound_ids")
        return self.get_all_compound_ids_from_all_src_id(src_compound_id,
                src_id, target=target)

    def get_all_compound_ids_from_all_src_id(self, src_compound_id,
            src_id, target=None):
        """Obtain a list of all src_compound_ids from all sources (including
        BOTH current AND obsolete assignments) to the same structure as a currently
        assigned query src_compound_id.

        The output will include query src_compound_id if
        it is a valid src_compound_id with a current assignment. Note also, that by
        adding an additional (optional) argument (a valid src_id), then results will be
        restricted to only the source specified with this optional argument.

        :param str src_compound_id: a valid compound identifier (or list)
        :param source: one of the valid database ids. See :attr:`source_ids`.
        :param target: if provided, return answer for a specific target database only. Otherwise
            return answer for all database found in :attr:`source_ids`.

        :return: list of three element arrays, containing 'src_compound_id' and 'src_id',
            and 'Assignment', or (if optional 'to_src_id' is specified) list of two element
            arrays, containing 'src_compound_id' and 'Assignment'.

        ::

            >>> res = s.get_all_compound_ids_from_src_id("CHEMBL12", "chembl")
            >>> s.get_all_compound_ids_from_src_id("CHEMBL12", "chembl", "chebi")
            [{u'assignment': u'1', u'src_compound_id': u'49575'}]

        The second call may return an empty list if there is no target from chebi.

        """
        src_id = self._get_source_id(src_id)
        request = "src_compound_id_all/%s/" + "%s" % src_id
        if target:
            target = self._get_source_id(target)
            request += "/%s" % target
        res = self._process(src_compound_id, "json", request)
        return res

    def get_mapping(self, source, target):
        """Obtain a full mapping between two sources. Uses only currently
        assigned src_compound_ids from both sources.

        :param source: name of the source database
        :param target: name of the target database
        :return: a dictionary. Keys are the source identifiers. Values are the
            target identifiers.

        ::

            >>> get_mapping("kegg_ligand", "chembl")

        """
        self.devtools.check_param_in_list(source, list(self.source_ids.keys()))
        self.devtools.check_param_in_list(target, list(self.source_ids.keys()))

        query = "mapping/%s/%s/" % (self.source_ids[source], self.source_ids[target])
        res = self.http_get(query, frmt=None)
        # evaluation the string as a list
        res = eval(res)
        # convert to a convenient dictionary
        mapping = [(x[str(self.source_ids[source])], x[str(self.source_ids[target])]) for x in res]
        mapping = dict(mapping)
        return mapping

    def get_src_compound_ids_from_inchikey(self, inchikey):
        """Obtain a list of all src_compound_ids (from all sources) which are
            CURRENTLY assigned to a query InChIKey

        :param str inchikey: input source identified by its InChiKey (or list)
        :return: list of dictionaries containing 'src_compound_id' and 'src_id' keys
            (or list of list of dictionaries if input is a list).

        ::

            >>> uni.get_src_compound_ids_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
        """
        res = self._process(inchikey, "json", "inchikey/%s")
        return res

    def get_src_compound_ids_all_from_inchikey(self, inchikey):
        """Description:  Obtain a list of all src_compound_ids (from all sources) which
        have current AND obsolete assignments to a query InChIKey

        :param str inchikey: input source identified by its InChiKey (or list)
            (or list of list of dictionaries if input is a list).
        :return: list of two element arrays, containing 'src_compound_id' and 'src_id'.
            and 'Assignment'.

        ::

            >>> uni.get_src_compound_ids_all_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")

        """
        res = self._process(inchikey, "json", "inchikey_all/%s")
        return res

    def get_all_src_ids(self):
        """Obtain all src_ids of database currently in UniChem

        :return: list of 'src_id's.

        ::

            >>> uni.get_all_src_ids()

        """
        res = self.http_get("src_ids", frmt=None)
        res = [x['src_id'] for x in eval(res)]
        return res

    def get_source_information(self, src_id):
        """Description:  Obtain all information on a source by querying with a source id

        :param int src_id: valid identifiers (values or keys of :attr:`source_ids` e.g.
            chebi, chembl,0,1). could also be a list of those identifiers.
        :return: dictionary (or list of dictionaries) with following keys:

            * src_id (the src_id for this source),
            * src_url (the main home page of the source),
            * name (the unique name for the source in UniChem, always lower case),
            * name_long (the full name of the source, as defined by the source),
            * name_label (A name for the source suitable for use as a 'label' for the source
              within a web-page. Correct case setting for source, and always less than 30
              characters),
            * description (a description of the content of the source),
            * base_id_url_available (an flag indicating whether this source provides a valid
            * base_id_url for creating cpd-specific links [1=yes, 0=no]).
            * base_id_url (the base url for constructing hyperlinks to this source [append an
            * identifier f    rom this source to the end of this url to create a valid url to a
            * specific page for this cpd], unless aux_for_url=1),
            * aux_for_url (A flag to indicate whether the aux_src field should be used to create
              hyperlinks instead of the src_compound_id [1=yes, 0=no]

        ::

            >>> res = get_source_information("chebi")

        """
        if isinstance(src_id, list):
            src_id = [self._get_source_id(this) for this in src_id]
            res = self._process(src_id, "json", "sources/%s")
            res = [x[0] for x in res]
        else:
            src_id = self._get_source_id(src_id)
            res = self._process(src_id, "json", "sources/%s")
            res = res[0]
        return res

    def get_structure(self, src_compound_id, src_id):
        """Obtain structure(s) CURRENTLY assigned to a query src_compound_id.

        :param str src_compound_id: a valid compound identifier
        :param int src_id: corresponding database identifier (name or id).

        :return:  dictionary with 'standardinchi' and 'standardinchikey' keys

        ::

            >>> uni.get_structure("CHEMBL12", "chembl")

        """
        src_id = self._get_source_id(src_id)
        request = "structure/%s" + "/%s" % src_id
        res = self._process(src_compound_id, "json", request)
        # the output is a list but looks like there is only 1 item
        # TODO check that there is indeed only 1 output.
        if len(res) == 1:
            return res[0]
        return res

    def get_structure_all(self, src_compound_id, src_id):
        """Obtain structure(s) with current AND obsolete assignments

        :param str src_compound_id: a valid compound identifier
        :param int src_id: corresponding database identifier (name or id).
        :return:  dictionary with 'standardinchi', 'standardinchikey' and
            'assignment' keys

        ::

            >>> uni.get_structure_all("CHEMBL12", "chembl")

        """
        src_id = self._get_source_id(src_id)
        request = "structure_all/%s" + "/%s" % src_id
        res = self._process(src_compound_id, "json", request)
        if len(res) == 1:
            return res[0]
        return res


    def get_src_compound_id_url(self, src_compound_id, src_id, to_src_id):
        """Obtain a list of URLs for all src_compound_ids

        Obtain a list of URLs for all src_compound_ids
        from a specifiedsource (the 'to_src_id'), which are CURRENTLY assigned to the same structure as
        a currently assigned query src_compound_id. Method only applicable for sources
        which support direct URLs to src_compound_id pages. Method also applicable for
        'to_src_id's where the hyperlink is constructed from auxiliary data [and not
        from the src_compound_id] as per example2 below.

        :param str src_compound_id: a valid compound identifier
        :param int src_id: corresponding database identifier (name or id).
        :param int to_src_id: database identifier (name or id) to map to.
        :param str to_src_id:
        :return: list of URLs.

        ::

            >>> uni.get_src_compound_id_url("CHEMBL12", "chembl", "drugbank")
            >>> # equivalent to
            >>> uni.get_src_compound_id_url("CHEMBL12", 1, 2)


        """
        src_id = self._get_source_id(src_id)
        to_src_id = self._get_source_id(to_src_id)
        request = "src_compound_id_url/%s" + "/%s/%s" % (src_id, to_src_id)
        res = self._process(src_compound_id, "json", request)
        if isinstance(src_compound_id, list):
            res = [x[0]['url'] for x in res]
        else:
            res = res[0]['url']
        return res

    def get_src_compound_ids_all_from_obsolete(self, obsolete_src_compound_id,
            src_id, to_src_id=None):
        """Obtain a list of all src_compound_ids from all sources with BOTH
        current AND obsolete to the same structure with an obsolete assignment to the
        query src_compound_id.

        The output will include query src_compound_id if it is a
        valid src_compound_id with an obsolete assignment. Note also, that by adding an
        additional (optional) argument (a valid src_id), then results will be restricted
        to only the source specified with this optional argument.

        :param str src_compound_id: a valid compound identifier
        :param int src_id: corresponding database identifier (name or id).
        :param int to_src_id: database identifier (name or id) to map to.
        :return: list of four element arrays, containing 'src_compound_id', 'src_id',
            'assignment' and 'UCI', or (if optional 'to_src_id' is specified) list of
            three element arrays, containing 'src_compound_id', 'Assignment' and 'UCI'.

        ::

            >>> from bioservices import UniChem
            >>> u = UniChem()
            >>> u.get_src_compound_ids_all_from_obsolete("DB07699", "2")
            >>> u.get_src_compound_ids_all_from_obsolete("DB07699", "2", "1")
        """
        src_id = self._get_source_id(src_id)
        request = "src_compound_id_all_obsolete/%s" + "/%s" % (src_id)
        if to_src_id:
            to_src_id = self._get_source_id(to_src_id)
            request += "/%s" % to_src_id
        res = self._process(obsolete_src_compound_id, "json", request)
        return res


    def get_verbose_src_compound_ids_from_inchikey(self, inchikey):
        """Obtain all src_compound_ids (from all sources)

        which are CURRENTLY assigned to a query InChIKey. However, these are returned as part of the
        following data structure: A list of sources containing these src_compound_ids,
        including source description, base_id_url, etc. One element in this list is a
        list of the src_compound_ids currently assigned to the query InChIKey.

        :param str inchikey: input source identified by its InChiKey
        :return: list containing

            * src_id (the src_id for this source),
            * src_url (the main home page of the source),
            * name (the unique name for the source in UniChem, always lower case),
            * name_long (the full name of the source, as defined by the source),
            * name_label (A name for the source suitable for use as a 'label' for the source
              within a web-page. Correct case setting for source, and always less than 30
              characters),
            * description (a description of the content of the source),
            * base_id_url_available (an flag indicating whether this source provides a valid
            * base_id_url for creating cpd-specific links [1=yes, 0=no]).
            * base_id_url (the base url for constructing hyperlinks to this source [append an
            * identifier from this source to the end of this url to create a valid url to a
              specific pag    e for this cpd], unless aux_for_url=1),
            * aux_for_url (A flag to indicate whether the aux_src field should be used to
              create hyperlinks instead of the src_compound_id [1=yes, 0=no] ,
            * src_compound_id (a list of src_compound_ids from this source which are currently
              assigned to the query InChIKey.
            * aux_src (a list of src-compound_id keys mapping to corresponding auxiliary data
              (url_id:value), for creating links if aux_for_url=1. Only shown if
              aux_for_url=1).

        ::

            >>> uni.get_verbose_src_compound_ids_from_inchikey("QFFGVLORLPOAEC-SNVBAGLBSA-N")
            >>> # Note that this one is not valid anymore
            >>> uni.get_verbose_src_compound_ids_from_inchikey("ZUITABIAKMVPG-UHFFFAOYSA-N")

        """
        res = self._process(inchikey, "json", "verbose_inchikey/%s")
        return res

    def get_auxiliary_mappings(self, src_id):
        """For a single source, obtain a mapping between all current
        src_compound_ids to their corresponding auxiliary data if any.

        Some instances of UniChem may contain sources that create URLs
        for compound-specific pages by using strings or identifiers (called 'auxiliary
        data' here) that are different to the src_compound_ids for the source. This is
        not very common, but is dealt with in UniChem by use of an additional mapping
        step for these sources. This function returns such mapping.

        .. warning:: this method may return very large data sets. you will need to change
            TIMEOUT to a larger value.

        :param int src_id: corresponding database identifier (name or id).
        :return: list of two element arrays, containing 'src_compound_id' and 'auxiliary data'.

        ::

            >>> uni.get_auxiliary_mappings(15)

        """
        src_id = self._get_source_id(src_id)
        info = self.get_source_information(src_id)

        if info['aux_for_url'] != '1':
            self.logging.warning("This function accepts src_id that have auxiliary data only")

        request = "mappingaux/%s"
        res = self._process(src_id, "json", request)
        return res


