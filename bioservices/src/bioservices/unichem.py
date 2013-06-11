from bioservices import RESTService




class UniChem(RESTService):

    _url = "http://www.ebi.ac.uk/unichem/rest"
    def __init__(self, verbose=False):
        """**Constructor**

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

    def get_src_compound_ids(self, src_compound_id, source, target=None):
        """Obtain a list of all src_compound_ids from all sources which are
            CURRENTLY assigned to the same structure as a currently assigned query
            src_compound_id. 

        The output will include query src_compound_id if it is a valid
        src_compound_id with a current assignment. Note also, that by adding an
        additional (optional) argument (a valid src_id), then results will be restricted
        to only the source specified with this optional argument.

        :param src_compound_id:
        :param source: one of the valid database ids. See :attr:`source_ids`.
        :param target: return answer for a specific target database only. Valid
            database ids can be found in :attr:`source_ids`.

        :return: list of two element arrays, containing 'src_compound_id' and 'src_id',
            or (if optional 'to_src_id' is specified) list of 'src_compound_id's.

            >>> ("CHEMBL12", "chembl")
            >>> ("CHEMBL12", "chembl", "chebi")
        """
        self.checkParam(source, self.source_ids.keys())
        query = "src_compound_id/%s/%s" % (src_compound_id, self.source_ids[source])
        if target:
            query += "/%s" % self.source_ids[target]

        res = self.request(query)

        # the json string returned can be evaluated in Python.
        res = eval(res)
        return res

    def get_src_compound_ids_all(self, src_compound_id, source, target):
        """Description:  Obtain a list of all src_compound_ids from all sources (including
BOTH current AND obsolete assignments) to the same structure as a currently
assigned query src_compound_id. The output will include query src_compound_id if
it is a valid src_compound_id with a current assignment. Note also, that by
adding an additional (optional) argument (a valid src_id), then results will be
restricted to only the source specified with this optional argument.
Number of required input parameters:  2 or 3
Input:  /src_compound_id/src_id(/to_src_id)
Output:  list of three element arrays, containing 'src_compound_id', 'src_id'
and 'Assignment', or (if optional 'to_src_id' is specified) list of two element
arrays, containing 'src_compound_id' and 'Assignment'.
Example:  https://www.ebi.ac.uk/unichem/rest/src_compound_id_all/CHEMBL12/1
Example:  https://www.ebi.ac.uk/unichem/rest/src_compound_id_all/CHEMBL12/1/2"""
        self.checkParam(source, self.source_ids.keys())
        query = "src_compound_id_all/%s/%s" % (src_compound_id, self.source_ids[source])
        if target:
            query += "/%s" % self.source_ids[target]

        res = self.request(query)

        # the json string returned can be evaluated in Python.
        res = eval(res)
        return res





    def get_mapping(self):
        """Description:  Obtain a full mapping between two sources. Uses only currently
assigned src_compound_ids from both sources.
Number of required input parameters:  2
Input:  src_id/to_src_id
Output:  list of two element arrays, containing 'src_compound_id' and
'src_compound_id'.
Example:  https://www.ebi.ac.uk/unichem/rest/mapping/4/1"""
        raise NotImplementedError

    def get_src_compound_ids_from_inchikey(self, InChIKey):
        """Description:  Obtain a list of all src_compound_ids (from all sources) which are
CURRENTLY assigned to a query InChIKey
Number of required input parameters:  1
Input:  /InChIKey
Output:  list of two element arrays, containing 'src_compound_id' and 'src_id'.
Example:
https://www.ebi.ac.uk/unichem/rest/inchikey/AAOVKJBEBIDNHE-UHFFFAOYSA-N"""
        raise NotImplementedError

    def get_src_compound_ids_all_from_inchikey(self, InChIKey):
        """Description:  Obtain a list of all src_compound_ids (from all sources) which
have current AND obsolete assignments to a query InChIKey
Number of required input parameters:  1
Input:  /InChIKey
Output:  list of two element arrays, containing 'src_compound_id', 'src_id' and
'Assignment'.
Example:
https://www.ebi.ac.uk/unichem/rest/inchikey_all/AAOVKJBEBIDNHE-UHFFFAOYSA-N"""
        raise NotImplementedError

    def get_all_src_ids(self):
        """Description:  Obtain all src_ids currently in UniChem
Number of required input parameters:  0
Input:   - none -
Output:  list of 'src_id's.
Example:  https://www.ebi.ac.uk/unichem/rest/src_ids/"""
        raise NotImplementedError

    def get_source_infomation(self):
        """Description:  Obtain all information on a source by querying with a source id
(src_id).
Number of required input parameters:  1
Input:  /src_id
Output:  list containing:
src_id (the src_id for this source),
src_url (the main home page of the source),
name (the unique name for the source in UniChem, always lower case),
name_long (the full name of the source, as defined by the source),
name_label (A name for the source suitable for use as a 'label' for the source
within a web-page. Correct case setting for source, and always less than 30
characters),
description (a description of the content of the source),
base_id_url_available (an flag indicating whether this source provides a valid
base_id_url for creating cpd-specific links [1=yes, 0=no]).
base_id_url (the base url for constructing hyperlinks to this source [append an
identifier from this source to the end of this url to create a valid url to a
specific page for this cpd], unless aux_for_url=1),
aux_for_url (A flag to indicate whether the aux_src field should be used to
create hyperlinks instead of the src_compound_id [1=yes, 0=no]
Example:  https://www.ebi.ac.uk/unichem/rest/sources/1"""
        raise NotImplementedError

    def get_structure(self):
        """Description:  Obtain structure(s) CURRENTLY assigned to a query src_compound_id.
Number of required input parameters:  2
Input:  /src_compound_id/src_id
Output:  list of two element arrays, containing 'Standard InChI', and 'Standard
InChIKey'
Example:  https://www.ebi.ac.uk/unichem/rest/structure/CHEMBL12/1"""
        raise NotImplementedError

    def get_structure_all(self):
        """Description:  Obtain structure(s) with current AND obsolete assignments to a
query src_compound_id.
Number of required input parameters:  2
Input:  /src_compound_id/src_id
Output:  list of three element arrays, containing 'Standard InChI', 'Standard
InChIKey', and 'Assignment'
Example:  https://www.ebi.ac.uk/unichem/rest/structure_all/CHEMBL12/1"""
        raise NotImplementedError

    def get_URL_src_compound_ids(self, src_compound_id):
        """Description:  Obtain a list of URLs for all src_compound_ids, from a specified
source (the 'to_src_id'), which are CURRENTLY assigned to the same structure as
a currently assigned query src_compound_id. Method only applicable for sources
which support direct URLs to src_compound_id pages. Method also applicable for
'to_src_id's where the hyperlink is constructed from auxiliary data [and not
from the src_compound_id] as per example2 below.
Number of required input parameters:  3
Input:  /src_compound_id/src_id/to_src_id
Output:  list of URLs.
Example:  https://www.ebi.ac.uk/unichem/rest/src_compound_id_url/CHEMBL12/1/2
Example:
https://www.ebi.ac.uk/unichem/rest/src_compound_id_url/CHEMBL490/1/15"""
        raise NotImplementedError

    def get_src_compound_ids_all_from_obsolete(self, obsolete_src_compound_id):
        """Obtain a list of all src_compound_ids from all sources with BOTH
current AND obsolete to the same structure with an obsolete assignment to the
query src_compound_id. The output will include query src_compound_id if it is a
valid src_compound_id with an obsolete assignment. Note also, that by adding an
additional (optional) argument (a valid src_id), then results will be restricted
to only the source specified with this optional argument.
Number of required input parameters:  2 or 3

Input:  /src_compound_id/src_id(/to_src_id)
Output:  list of four element arrays, containing 'src_compound_id', 'src_id',
'Assignment' and 'InChIKey', or (if optional 'to_src_id' is specified) list of
three element arrays, containing 'src_compound_id', 'Assignment' and 'UCI'.
Example:
https://www.ebi.ac.uk/unichem/rest/src_compound_id_all_obsolete/DB07699/2
Example:
https://www.ebi.ac.uk/unichem/rest/src_compound_id_all_obsolete/DB07699/2/1"""
        raise NotImplementedError

    def get_verbose_src_compound_ids_from_inchikey(self, InChIKey):
        """Description:  Obtain all src_compound_ids (from all sources) which are CURRENTLY
assigned to a query InChIKey. However, these are returned as part of the
following data structure: A list of sources containing these src_compound_ids,
including source description, base_id_url, etc. One element in this list is a
list of the src_compound_ids currently assigned to the query InChIKey.
Number of required input parameters:  1
Input:  /InChIKey
Output:  list containing:
src_id (the src_id for this source),
src_url (the main home page of the source),
name (the unique name for the source in UniChem, always lower case),
name_long (the full name of the source, as defined by the source),
name_label (A name for the source suitable for use as a 'label' for the source
within a web-page. Correct case setting for source, and always less than 30
characters),
description (a description of the content of the source),
base_id_url_available (an flag indicating whether this source provides a valid
base_id_url for creating cpd-specific links [1=yes, 0=no]).
base_id_url (the base url for constructing hyperlinks to this source [append an
identifier from this source to the end of this url to create a valid url to a
specific page for this cpd], unless aux_for_url=1),
aux_for_url (A flag to indicate whether the aux_src field should be used to
create hyperlinks instead of the src_compound_id [1=yes, 0=no] ,
src_compound_id (a list of src_compound_ids from this source which are currently
assigned to the query InChIKey.
aux_src (a list of src-compound_id keys mapping to corresponding auxiliary data
(url_id:value), for creating links if aux_for_url=1. Only shown if
aux_for_url=1).
Example:
https://www.ebi.ac.uk/unichem/rest/verbose_inchikey/GZUITABIAKMVPG-UHFFFAOYSA-N"""
        raise NotImplementedError

    def get_auxiliary_mappings(self):
        """Description:  For a single source, obtain a mapping between all current
src_compound_ids to their corresponding auxiliary data. See FAQ for an
explanation of 'auxiliary data'. Please note that the only examples available
(below) for this method may be very large data sets, and may therefore take a
very long time to retrieve. A much faster method of retrieving this same data
set is to download the pre-cached, gzipped mapping file for the source of
interest from the Auxiliary Data Mapping page.
Number of required input parameters:  1
Input:  /src_id
Output:  list of two element arrays, containing 'src_compound_id' and 'auxiliary
data'.
Example:  https://www.ebi.ac.uk/unichem/rest/mappingaux/15"""
        raise NotImplementedError

