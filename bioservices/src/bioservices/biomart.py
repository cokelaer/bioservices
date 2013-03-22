"""

http://www.biomart.org/martservice.html

SOAP could not be used directly, so we used REST instead.
"""


from bioservices import RESTService

__all__ = ["BioMart"]

class BioMart(RESTService):
    """Interface to the `BioMart <http://www.biomart.org>`_ database"""

    def __init__(self):
        """.. rubric:: Constructor"""

        url = "http://www.biomart.org/biomart/martservice"
        super(BioMart, self).__init__("BioMart", url=url)

    def registry(self):
        """to retrieve registry information"""
        ret = self.request("?type=registry")
        return ret

    def datasets(self, mart):
        """to retrieve datasets available for a mart: 

        :param str mart: e.g. ensembl
        """
        ret = self.request("?type=datasets&mart=%s" %mart, format="txt")
        ret = [x.split("\t") for x in ret.split("\n") if len(x.strip())]
        return ret

    def attributes(self, dataset):
        """to retrieve attributes available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        ret = self.request("?type=attributes&dataset=%s" %dataset)
        return ret

    def filters(self, dataset):
        """to retrieve filters available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        ret = self.request("?type=filters&dataset=%s" %dataset)
        return ret

    def configuration(self, dataset):
        """to retrieve configuration available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        ret = self.request("?type=configuration&dataset=%s" %dataset)
        return ret


    def version(self, mart):
        ret = self.request("?type=version&mart=%s" % mart)
        return ret


    def query(self):

        xmlq = """<?xml version="1.0" encoding="UTF-8"?>
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
