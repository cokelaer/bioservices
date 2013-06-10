"""This is a draft module to convert chEBI to chembl easily




"""
from bioservices import WSDLService


class ChEBI(WSDLService):
    """

    """
    _url = "http://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl"
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(ChEBI, self).__init__(name="ChEBI", url=ChEBI._url, 
            verbose=verbose, lib="suds")


        """[x[0] for x in res.DatabaseLinks if x[1].startswith("chEMBL")]
        [x[0] for x in res.DatabaseLinks if x[1].startswith("ChEMBL")][116485]
        [x[0] for x in res.DatabaseLinks if x[1].startswith("KEGG")]
        [C07481, D00528]"""
        #res = ch.service.getCompleteEntity("CHEBI:27732")
        #ch = Client('http://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl')



