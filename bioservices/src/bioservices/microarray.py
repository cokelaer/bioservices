from bioservices.services import Service
import webbrowser
import copy


class Items(object):
    """Simple class to ease access to some data in the Kegg database


    Used to access to organisms and databases. Could be extended for the
    pathways

    ::

            k = Kegg()
            k.organisms
            k.organisms.items
            k.organisms.entry_id
            k.organisms.definition

    """

    def __init__(self, data, name="items", verbose=True):
        self.verbose = verbose
        self.name = name
        self._items = copy.deepcopy(data)

    def _get_definitions(self):
        ids = [x['definition'] for x in self.items]
        return ids
    definitions = property(_get_definitions, doc="return list of definition")

    def _get_entry_ids(self):
        ids = [x['entry_id'] for x in self.items]
        return ids
    entry_ids = property(_get_entry_ids, doc="return list of Ids")

    def _get_items(self):
        return self._items
    items = property(_get_items, doc=_get_items.__doc__)

    def lookfor(self, query):
        """Search for a pattern in the items

        :param str query: can be an id, a word

        case insensitive
        """
        matches = []
        for i, item in enumerate(self.definitions):
            if query.lower() in item.lower():
                matches.append(i)
        for i, item in enumerate(self.entry_ids):
            if query.lower() in item.lower():
                matches.append(i)
        return [(self.definitions[i], self.entry_ids[i]) for i in matches]

    def __str__(self):
        txt = ""
        txt += "%60s || %s\n" % ("Definition", "ID")
        txt += "="*80 + "\n"
        for x,y in zip(self.definitions, self.entry_ids):
            txt +=  "%60s || %s\n" % (x,y)
        return txt 



class Micro(WSDLService):
    """
    >>> from microarray import *
    >>> m = Micro()
    >>> probes = ['AB002409_at'] # probes=["urn:lsid:affymetrix.com:probeset.hu6800:AF000430_at"]
    >>> queryFields = ['LocusLink LocusLink ID']
    >>> m.serv.annotateProbes(probes, queryFields)
    """
    def __init__(self, verbose=True, debug=False, url=None):
        """Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """
        if url == None:
            url="http://www.broadinstitute.org/webservices/genecruiser/services/Annotation?wsdl"
        super(Micro, self).__init__(name="micorarray",\
                                    url=url,\
                                    verbose=verbose)

    def f_info(self):
        for m in dir(self):
            print m
