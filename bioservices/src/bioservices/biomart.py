"""

http://www.biomart.org/martservice.html

SOAP could not be used directly, so we used REST instead.
"""


from bioservices import RESTService, BioServicesError

__all__ = ["BioMart"]

class BioMart(RESTService):
    """Interface to the `BioMart <http://www.biomart.org>`_ database


        >>> s = BioMart()
        >>> s.registry() # to get information about existing services
        >>> s.names      # alias to list of valid service names from registry
        >>> "unimart" in s.names
        True
        >>> s.datasets("unimart")  # retrieve datasets available for this mart

    .. rubric:: terminology

        * a **mart* is a service associated to biomart. For instance **ensembl**.

    """
        

    _xml_example = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
			
	<Dataset name = "pathway" interface = "default" >
		<Filter name = "referencepeptidesequence_uniprot_id_list" value = "P43403"/>
		<Attribute name = "stableidentifier_identifier" />
		<Attribute name = "pathway_db_id" />
	</Dataset>
</Query>
</xml>
    """


    def __init__(self):
        """.. rubric:: Constructor"""
        url = "http://www.biomart.org/biomart/martservice"
        super(BioMart, self).__init__("BioMart", url=url)
        self._names = None
        self._databases = None
        self._display_names = None
        self._valid_attributes = None
        self._hosts = None

        self._init()

    def _init(self):
        self.logging.info("Initialisation %s" % self.name)
        temp = self.debugLevel
        self.debugLevel = "ERROR"
        res = self.lookfor("uniprot", verbose=False)
        res = self.valid_attributes
        self.debugLevel = temp

        self.biomartQuery = BioMartQuery()

    def registry(self):
        """to retrieve registry information

         the XML contains list of children called MartURLLocation made 
         of attributes. We parse the xml to return a list of dictionary.
         each dictionary correspond to one MART.

        aliases to some keys are provided: names, databases, displayNames

	"""
        ret = self.request("?type=registry")
        # the XML contains list of children called MartURLLocation made 
        # of attributes. We parse the xml to return a list of dictionary.
        # each dictionary correspond to one MART.
        ret = [x.attrib for x in ret.getchildren()]
        return ret

    def datasets(self, mart, raw=False):
        """to retrieve datasets available for a mart: 

        :param str mart: e.g. ensembl. see :attr:`names` for a list of valid MART names 
            the mart is the database. see lookfor method or databases attributes
       
        >>> s = BioMart(verbose=False)
        >>> s.datasets("prod-intermart_1")
        ['Protein Matches', 'InterPro Entry Annotation', 'UniParc Protein Matches']
 
        """
        if mart not in self.names:
            raise BioServicesError("Provided mart name (%s) is not valid. see 'names' attribute" % mart)
        ret = self.request("?type=datasets&mart=%s" %mart, format="txt")
        if raw==False:
            try:
                ret2 = [x.split("\t") for x in ret.split("\n") if len(x.strip())]
                ret = [x[1] for x in ret2]
            except:
                ret = ["?"]
                
        return ret

    def attributes(self, dataset):
        """to retrieve attributes available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        #assert dataset in self.names
        if dataset not in [x for k in self.valid_attributes.keys() for x in self.valid_attributes[k]]:
            raise ValueError("provided dataset (%s) is not found. see valid_attributes" % dataset)
        ret = self.request("?type=attributes&dataset=%s" %dataset, format='txt')

        ret = [x for x in ret.split("\n") if len(x)]
        results = {}
        for line in ret:
            key = line.split("\t")[0]
            results[key] = line.split("\t")[1:]
        return results

    def filters(self, dataset):
        """to retrieve filters available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        s.filters("uniprot").split("\n")[1].split("\t")

        """
        if dataset not in [x for k in self.valid_attributes.keys() for x in self.valid_attributes[k]]:
            raise ValueError("provided dataset (%s) is not found. see valid_attributes" % dataset)
        ret = self.request("?type=filters&dataset=%s" %dataset, format='txt')
        ret = [x for x in ret.split("\n") if len(x)]
        results = {}
        for line in ret:
            key = line.split("\t")[0]
            results[key] = line.split("\t")[1:]
        return results

    def configuration(self, dataset):
        """to retrieve configuration available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        ret = self.request("?type=configuration&dataset=%s" %dataset)
        return ret


    def version(self, mart):
        """Returns version of a **mart**

        :param str mart: e.g. ensembl

        """
        ret = self.request("?type=version&mart=%s" % mart)
        return ret




    def query(self, xmlq):
        """Send a query to biomart

	The query must be formatted in a XML format which looks like::

            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE Query>
            <Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
			
                <Dataset name = "pathway" interface = "default" >
		    <Filter name = "referencepeptidesequence_uniprot_id_list" value = "P43403"/>
    	            <Attribute name = "stableidentifier_identifier" />
               	    <Attribute name = "pathway_db_id" />
                </Dataset>
            </Query>
        
        """

        ret = self.requestPost(self.url, params={"query":xmlq})
        return ret

    def create_filter(self, name, value, dataset=None):
        if dataset:
            valid_filters = self.filters(dataset).keys()
            if name not in valid_filters:
                raise BioServicesError("Invalid filter name. ")

        _filter = """        <Filter name = "%s" value = "%s"/>""" % (name, value)
        return _filter

    def create_attribute(self, name, dataset=None):
        #s.attributes(dataset)
        # valid dataset
        if dataset:
            valid_attributes = self.attributes(dataset).keys()
            if name not in valid_attributes:
                raise BioServicesError("Invalid attribute name. ")
        attrib = """        <Attribute name = "%s" />""" % name
        return attrib

    def _get_names(self):
        if self._names == None:
            ret = self.registry()
            names = [x["name"] for x in ret]
            self._names = names[:]
        return self._names
    names = property(_get_names, doc="list of valid datasets")

    def _get_displayNames(self):
        if self._display_names == None:
            ret = self.registry()
            names = [x["displayName"] for x in ret]
            self._display_names = names[:]
        return self._display_names
    displayNames = property(_get_displayNames, doc="list of valid datasets")

    def _get_databases(self):
        if self._databases == None:
            ret = self.registry()
            names = [x.get("database", "?") for x in ret]
            self._databases = names[:]
        return self._databases
    databases = property(_get_databases, doc="list of valid datasets")

    def _get_hosts(self):
        if self._hosts == None:
            ret = self.registry()
            names = [x.get("host", "?") for x in ret]
            self._hosts = names[:]
        return self._hosts
    hosts = property(_get_hosts, doc="list of valid hosts")


    def _get_valid_attributes(self,):
        res = {}
        if self._valid_attributes == None:
            for name in self.names:
                datasets = self.datasets(name, raw=False)
                res[name] = [x for x in datasets if len(x)>1]
                for x in datasets:
                    if len(x)<=1:
                        print("Not available within bioservice: ",name)
            self._valid_attributes = res.copy()
        return self._valid_attributes
    valid_attributes = property(_get_valid_attributes, doc="list of valid datasets")


    def lookfor(self, pattern, verbose=True):
        for a,x,y,z in zip(self.hosts, self.databases, self.names, self.displayNames):
            found = False
            if pattern.lower() in x.lower():
                found = True
            if pattern.lower() in y.lower():
                found = True
            if pattern.lower() in z.lower():
                found = True
            if found == True and verbose==True:
                print("Candidate:")
                print("     database: %s " %x)
                print("    MART name: %s " %y)
                print("  displayName: %s " %z)
                print("        hosts: %s " %a)


class BioMartQuery(object):
    def __init__(self, version="1.0", virtualScheme="default"):

        params = {
            "version": version, 
            "virtualSchemaName": virtualScheme,
            "formatter": "TSV",
            "header":0,
            "uniqueRows":0,
            "configVersion":"0.6"

        }

        self.header = """<?xml version="%(version)s" encoding="UTF-8"?>
            <!DOCTYPE Query>
            <Query  virtualSchemaName = "%(virtualSchemaName)s" formatter = "%(formatter)s" header = "%(header)s" uniqueRows = "%(uniqueRows)s" count = "" datasetConfigVersion = "%(configVersion)s" >""" % params


        self.footer = "    </Dataset>\n</Query>"
        self.attributes = []
        self.filters = []

    def add_filter(self, filter):
        self.filters.append(filter)

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def add_dataset(self, dataset):
	self.dataset = "<Dataset name = "%s" interface = "default" >" % dataset

    def reset(self):
        self.attributes = []
        self.filters = []

    def get_xml(self):
        xml = self.header
        xml += self.dataset
        xml += "\n"
        for line in self.filters:
            xml += line +"\n"
        for line in self.filters:
            xml += line + "\n"
        xml += self.footer
        return xml


