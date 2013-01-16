from bioservices import RESTService


#http://code.google.com/p/psicquic/wiki/PsicquicSpec_1_3_Rest

#http://www.biocatalogue.org/services/2078#operations

__all__ = ["PSICQUIC"]


class PSICQUIC(RESTService):

    _formats = ["tab25", "tab25", "tab27", "xml25", "count", "biopax", "xgmml",
        "rdf-xml", "rdf-xml-abbrev", "rdf-n3", "rdf-turtle"]

    def __init__(self, verbose=True):
        urlStr = 'http://www.ebi.ac.uk/Tools/webservices/psicquic'
        super(PSICQUIC, self).__init__("PSICQUIC", verbose=verbose, url=urlStr)
        self._registry = None

    def read_registry(self):
        """Reads and returns the active registry 

        """
        url = self.url + '/registry/registry?action=ACTIVE&format=txt'
        res = self.request(url, format='txt')
        return res.split()

    def print_status(self):
        """Prints the services that are available"""
        url = self.url +  '/registry/registry?action=STATUS&format=xml'
	res = self.request(url)
        names = self.registry_names
        counts = self.registry_counts
        versions = self.registry_versions
        actives = self.registry_actives
        resturls = self.registry_resturls
        soapurls = self.registry_soapurls
        restexs = self.registry_restexamples
        restricted = self.registry_restricted
        N = len(names)

        indices = sorted(range(0,N), key=lambda k: names[k])

        for i in range(0,N):
            print("%s\t %s\t %s\t %s\t %s %s %s %s\n" % (names[i], actives[i], 
                counts[i], versions[i], resturls[i], soapurls[i], restexs[i], restricted[i]))


    # todo a property for the version of PISCQUIC

    def _get_registry(self):
        if self._registry == None:
            url = self.url +  '/registry/registry?action=STATUS&format=xml'
            res = self.request(url, format="xml")
            self._registry = res
        return self._registry
    registry = property(_get_registry, doc="returns the registry of psicquic")

    def _get_registry_names(self):
        res = self.registry
        return [x.findAll('name')[0].text for x in res.findAll("service")]
    registry_names = property(_get_registry_names, doc="returns all services available (names)")

    def _get_registry_restricted(self):
        res = self.registry
        return [x.findAll('restricted')[0].text for x in res.findAll("service")]
    registry_restricted = property(_get_registry_restricted, doc="returns restricted status of services" )

    def _get_registry_resturl(self):
        res = self.registry
        data = [x.findAll('resturl')[0].text for x in res.findAll("service")]
        return data
    registry_resturls = property(_get_registry_resturl, doc="returns URL of REST services")

    def _get_registry_restex(self):
        res = self.registry
        data = [x.findAll('restexample')[0].text for x in res.findAll("service")]
        return data
    registry_restexamples = property(_get_registry_restex, doc="retuns REST example for each service")

    def _get_registry_soapurl(self):
        res = self.registry
        return  [x.findAll('soapurl')[0].text for x in res.findAll("service")]
    registry_soapurls = property(_get_registry_soapurl, doc="returns URL of WSDL service")

    def _get_registry_active(self):
        res = self.registry
        return  [x.findAll('active')[0].text for x in res.findAll("service")]
    registry_actives = property(_get_registry_active, doc="returns active state of each service")

    def _get_registry_count(self):
        res = self.registry
        return  [x.findAll('count')[0].text for x in res.findAll("service")]
    registry_counts = property(_get_registry_count, doc="returns number of entries in each service")

    def _get_registry_version(self):
        res = self.registry
        names = [x.findAll('name')[0].text for x in res.findAll("service")]
        N = len(names)
        version = [0] * N
        for i in range(0,N):
            x = res.findAll("service")[i]
            if x.findAll("version"):
                version[i] = x.findAll("version")[0].text
            else:
                version[i] = None 
        return  version
    registry_versions = property(_get_registry_version, doc="returns version of each service")

    def query(self, service, query, output="xml25", version="current", firstResult=None, maxResults=None):
        """format = count; query = zap70, service intact returns 

        :param str service: a registered service. See :attr:`registry_names`.
        :param str query: a valid query. Can be `*` or a protein name.
        :param str output: a valid format. See r._formats


        ::

            r.query("intact", "brca2", "tab27")
            r.query("intact", "zap70", "xml25")
            r.query("matrixdb", "*", "xml25")

        """
        names = [x.lower() for x in self.registry_names]
        try:
            index = names.index(service)
        except ValueError:
            print("The service you gave (%s) is not registered. See self.registery_names" % service)
            raise ValueError
        resturl = self.registry_resturls[index]


        url = resturl  + 'query/' + query + "?format="+output
        if firstResult:
           url+="&firstResult=%s" % str(firstResult)
        if maxResults:
           url+="&maxResults=%s" % str(maxResults)
        if "xml" in output:
            res = self.request(url, format="xml")
        else:
            res = self.request(url, format="txt")
        return res


