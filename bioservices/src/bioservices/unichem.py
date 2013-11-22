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






from bioservices import RESTService




class UniChem(RESTService):

    _url = "http://www.ebi.ac.uk/unichem/rest"
    def __init__(self, verbose=True):
        """**Constructor `UniChem <https://www.ebi.ac.uk/unichem/>`_

        :param verbose: set to False to prevent informative messages
        """
        super(UniChem, self).__init__(name="UniChem", url=UniChem._url, verbose=verbose)
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
            "pharmgkb":17
            }# there was no 16 when I looked at the web site June 2013

    def get_source_id(self, src_id):
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
        """Obtain a list of all src_compound_ids from all sources which are
        CURRENTLY assigned to the same structure as a currently assigned query
        src_compound_id. 

        The output will include query src_compound_id if it is a valid
        src_compound_id with a current assignment. Note also, that by adding an
        additional (optional) argument (a valid src_id), then results will be restricted
        to only the source specified with this optional argument.

        :param str src_compound_id: a valid compound identifier
        :param str src_id: one of the valid database ids. See :attr:`source_ids`.
        :param str,int target: database identifier (name or id) to map to.

        :return: list of two element arrays, containing 'src_compound_id' and 'src_id',
            or (if optional 'to_src_id' is specified) list of 'src_compound_id's.

        ::

            >>> get_src_compound_ids_from_src_compound_id("CHEMBL12", "chembl")
            >>> get_src_compound_ids_from_src_compound_id("CHEMBL12", "chembl", "chebi")

        """
        src_id = self.get_source_id(src_id)
        query = "src_compound_id/%s/%s" % (src_compound_id, src_id)
        if target:
            target = self.get_source_id(target)
            query += "/%s" % target

        res = self.request(query)

        # the json string returned can be evaluated in Python.
        res = eval(res)
        return res

    def get_src_compound_ids_all_from_src_compound_id(self, src_compound_id,
        src_id, target=None):
        """Obtain a list of all src_compound_ids from all sources (including
        BOTH current AND obsolete assignments) to the same structure as a currently
        assigned query src_compound_id. 

        The output will include query src_compound_id if
        it is a valid src_compound_id with a current assignment. Note also, that by
        adding an additional (optional) argument (a valid src_id), then results will be
        restricted to only the source specified with this optional argument.

        :param str src_compound_id: a valid compound identifier
        :param source: one of the valid database ids. See :attr:`source_ids`.
        :param target: return answer for a specific target database only. Valid
            database ids can be found in :attr:`source_ids`.
        :return: list of three element arrays, containing 'src_compound_id' and 'src_id',
            and 'Assignment', or (if optional 'to_src_id' is specified) list of two element
            arrays, containing 'src_compound_id' and 'Assignment'.

        ::

            >>> get_src_compound_ids_all_from_src_compound_id("CHEMBL12", "chembl")
            >>> get_src_compound_ids_all_from_src_compound_id("CHEMBL12", "chembl", "chebi")

        """
        src_id = self.get_source_id(src_id)
        query = "src_compound_id_all/%s/%s" % (src_compound_id, src_id)
        if target:
            query += "/%s" % self.source_ids[target]

        res = self.request(query)

        # the json string returned can be evaluated in Python.
        res = eval(res)
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
        self.checkParam(source, self.source_ids.keys())
        self.checkParam(target, self.source_ids.keys())

        query = "mapping/%s/%s/" % (self.source_ids[source], self.source_ids[target])
        res = self.request(query)
        # evaluation the string as a list
        res = eval(res)
        # convert to a convenient dictionary
        mapping = [(x[str(self.source_ids[source])], x[str(self.source_ids[target])]) for x in res]
        mapping = dict(mapping)
        return mapping

    def get_src_compound_ids_from_inchikey(self, inchikey):
        """Obtain a list of all src_compound_ids (from all sources) which are
            CURRENTLY assigned to a query InChIKey

        :param str inchikey: input source identified by its InChiKey
        :return: list of two element arrays, containing 'src_compound_id' and 'src_id'.

        ::

            >>> uni.get_src_compound_ids_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")
        """
        query = "inchikey/%s" % inchikey
        res = self.request(query)
        res = eval(res)
        return res

    def get_src_compound_ids_all_from_inchikey(self, inchikey):
        """Description:  Obtain a list of all src_compound_ids (from all sources) which
        have current AND obsolete assignments to a query InChIKey

        :param str inchikey: input source identified by its InChiKey
        :return: list of two element arrays, containing 'src_compound_id' and 'src_id'.
            and 'Assignment'.

        ::
    
            >>> uni.get_src_compound_ids_all_from_inchikey("AAOVKJBEBIDNHE-UHFFFAOYSA-N")

        """
        query = "inchikey_all/%s" % inchikey
        res = self.request(query)
        res = eval(res)
        return res

    def get_all_src_ids(self):
        """Obtain all src_ids of database currently in UniChem

        :return: list of 'src_id's.

        ::

            >>> uni.get_all_src_ids()

        """
        res = self.request("src_ids")
        res = eval(res)
        return res


    def get_source_information(self, src_id):
        """Description:  Obtain all information on a source by querying with a source id

        :param int src_id: identifier of a source database. 
        :return: dictionary containing:

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

        Example:  https://www.ebi.ac.uk/unichem/rest/sources/1"""

        src_id = self.get_source_id(src_id)
        query = "sources/%s" % src_id
        res = self.request(query)
        res = eval(res)
        res = dict(res[0])
        return res

    def get_structure(self, src_compound_id, src_id):
        """Obtain structure(s) CURRENTLY assigned to a query src_compound_id.

        :param str src_compound_id: a valid compound identifier
        :param int src_id: corresponding database identifier (name or id). 

        :return:  dictionary with 'standardinchi' and 'standardinchikey' keys

        ::

            >>> uni.get_structure("CHEMBL12", "chembl")

        """
        src_id = self.get_source_id(src_id)
        query = "structure/%s/%s" % (src_compound_id, src_id)
        res = self.request(query)
        res = eval(res)
        res = res[0]
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
        src_id = self.get_source_id(src_id)
        query = "structure_all/%s/%s" % (src_compound_id, src_id)
        res = self.request(query)
        res = eval(res)
        res = res[0]
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
        src_id = self.get_source_id(src_id)
        to_src_id = self.get_source_id(to_src_id)
        query = "src_compound_id_url/%s/%s/%s" % (src_compound_id, src_id, to_src_id)
        res = self.request(query)
        res = eval(res)
        res = [x['url'] for x in res]
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

            >>> get_src_compound_ids_all_from_obsolete("DB07699", "2")
            >>> get_src_compound_ids_all_from_obsolete("DB07699", "2", "1")
        """
        src_id = self.get_source_id(src_id)
        query = "src_compound_id_all_obsolete/%s/%s" % (obsolete_src_compound_id, src_id)
        if to_src_id:
            to_src_id = self.get_source_id(to_src_id)
            query += "/%s" % to_src_id

        res = self.request(query)

        # the json string returned can be evaluated in Python.
        res = eval(res)
        return res


    def get_verbose_src_compound_ids_from_inchikey(self, inchikey):
        """Description:  Obtain all src_compound_ids (from all sources) which are CURRENTLY
        assigned to a query InChIKey. However, these are returned as part of the
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

            >>> uni.get_verbose_src_compound_ids_from_inchikey("ZUITABIAKMVPG-UHFFFAOYSA-N")

        """
        query = "verbose_inchikey/%s" % inchikey
        res = self.request(query)
        res = eval(res)
        return res

    def get_auxiliary_mappings(self, src_id):
        """For a single source, obtain a mapping between all current
            src_compound_ids to their corresponding auxiliary data if any.

        Some instances of UniChem may contain sources that create URLs
        for compound-specific pages by using strings or identifiers (called 'auxiliary
        data' here) that are different to the src_compound_ids for the source. This is
        not very common, but is dealt with in UniChem by use of an additional mapping
        step for these sources. This function returns such mapping. 

        .. warning:: this method may return very large data sets, and may therefore take a
            very long time to retrieve. A much faster method of retrieving this same data
            set is to download the pre-cached, gzipped mapping file for the source of
            interest from the `Auxiliary Data Mapping page <https://www.ebi.ac.uk/unichem/wholesourcemap>`_

        :param int src_id: corresponding database identifier (name or id).
        :return: list of two element arrays, containing 'src_compound_id' and 'auxiliary data'.

        ::
        
            >>> uni.get_auxiliary_mappings(15)

        """

        src_id = self.get_source_id(src_id)
        info = self.get_source_information(src_id)
        if info['aux_for_url'] == '1':
            query = "mappingaux/%s" % src_id
            res = self.request(query)
            #res = eval(res)
            return res
        else:
            self.logging.warning("This function accepts src_id that have auxiliary data only")

