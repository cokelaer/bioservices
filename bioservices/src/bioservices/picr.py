"""This module provides a class :class:`~bioservices.picr.PICR` that allows an 
access to the REST interface of the PICR web service. There is also a SOAP web service but we implemented only the REST interface since they both provide access to the same functionalities.

.. topic:: PICR description (from PICR website)

    The Protein Identifier Cross-Reference (PICR) service is a web application that provides interactive and programmatic (SOAP and REST) access to a mapping algorithm based on 100% sequence identity to proteins from over 98 distinct source databases. Mappings can be limited by source database, taxonomic ID and activity status in the source database. Users can copy/paste or upload files containing protein identifiers or sequences in FASTA format to obtain mappings using the interactive interface. Search results can be viewed in simple or detailed HTML tables or downloaded as comma-separated values (CSV) or Microsoft Excel (XLS) files suitable for use in a local database or a spreadsheet. Alternatively, a SOAP interface is available to integrate PICR functionality in other applications, as is a lightweight REST interface.

"""
from services import RESTService
import xmltools

#//the NEWT taxonomy ID to limit the mappings to
#//can be null or a number. Do not specify 0 for null.
#String taxonID = "9606";     //H. Sapiens

class PICR(RESTService):
    """Interface to the `PICR (Protein Identifier Cross reference) <http://www.ebi.ac.uk/Tools/picr/>`_ service

    .. doctest::

        p = PICR()
        p.getMappedDatabaseNames()

        sequence="MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"
        results = p.getUPIForSequence(self.sequence, ["IPI", "ENSEMBL", "SWISSPROT"])



    """
    _sequence_example="MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"
    _blastfrag_example="MSVMYKKILYPTDFSETAEIALKHVKAFKTLKAEEVILLHVIDEREIKKRDIFSLLLGVAGLNKSVEEFENELKNKLTEEAKNKMENIKKELEDVGFKVKDIIVVGIPHEEIVKIAEDEGVDIIIMGSHGKTNLKEILLGSVTENVIKKSNKPVLVVKRKNS"
    _accession_example = "P29375"
    _url = "http://www.ebi.ac.uk/Tools/picr/rest/"

    def __init__(self):
        super(PICR, self).__init__(name="PICR", url=PICR._url)

    def getMappedDatabaseNames(self):
        """Return the valid database names

        This method calls the getMappedDatabaseNames REST services from PICR website.

        :returns: a XML containing the databases available.

        .. seealso:: :attr:`databases` to obtain a human readable list
        """
        url = self.url + "/getMappedDatabaseNames"
	res = self.request(url)
        #x = xmltools.easyXML(res)
        return res

    def _get_databases(self):
        res = self.getMappedDatabaseNames()
        databases = [a.text for a in res.getchildren()]
        return databases
    databases = property(_get_databases, doc="get the list of databases (from XML returned by :meth:`getMappedDatabaseNames`)")

    def getUPIForSequence(self, sequence, database, taxid=None,
        onlyactive=True, includeattributes=False):
        """Get Protein identifier given an exact sequence

        :param sequence: the sequence to map [required]
        :param database: the database to map to. At least one database is required, but
            multiple databases can be queried at once.
        :param taxid: the NEWT taxon ID to limit the mappings [optional] 
        :param onlyactive: if true, only active mappings will be returned. 
            If false, results may include deleted mappings. [optional, default is true]
        :param includeattributes: if true, extra attributes such as sequence and taxon 
            IDs will be returned if available. If false, no extra information returned. 
            [optional, default is false]

        .. note:: Parameter names are case sensitive.

        Some servers, browsers and other clients may have restrictions on the length of
        the query string, so long sequences might cause errors. If this is the case, use
        a POST request rather than a GET.

        If a taxid is submitted, includeattributes will be true.

        .. doctest::

            >>> from bioservices import picr
            >>> p = picr.PICR()
            >>> sequence="MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"
            >>> databases = ["IPI", "ENSEMBL", "SWISSPROT"] 
            >>> results = p.getUPIForSequence(sequence, databases)

        """
        url = self._url + "getUPIForSequence"

        # check validity of the database provided

        url += "?sequence=" + sequence
        if isinstance(database,str):
            self._checkDBname(database)
            url+= "&database=" + database
        elif isinstance(database,list):
            for d in database:
                self._checkDBname(d)
                url+="&database=" + d
        #if taxid!=None or onlyactive==False or includeattributes==False:
        #    raise NotImplementedError
	if taxid:
            url += "&taxonid=" +taxid
        if includeattributes == False:
            url += "&includeattributes=false"
        if onlyactive == False:
            url += "&onlyactive=false"
        #if onlyactive

        #print url

        #res = urllib2.urlopen(url).read()
        res = self.request(url)
        #res = xmltools.easyXML(res)
        return res

    def _checkDBname(self, db):
        if db not in self.databases:
            raise ValueError("Provided database name (%s) is not valid. Use database attribute to check the valid names" % db)

    def getUPIForAccession(self, accession, database,
        taxid=None,
        version=None, 
        onlyactive=True, 
        includeattributes=True):
        """Get Protein identifier given an accession number

        :param str accession:  the accession to map [required]
        :param str version: the version of accession to map [optional]
        :param database: the database to map to (string). At least one database is 
            required, but multiple databases can be queried at once using a list.
        :param taxid: the NEWT taxon ID to limit the mappings [optional]
        :param bool onlyactive: if true, only active mappings will be returned. If false, 
            results may include deleted mappings. [optional, default is true]
        :param bool includeattributes: if true, extra attributes such as sequence 
            and taxon IDs will be returned if available. If false, no extra 
            information returned. [optional, default is false]

        .. note:: parameter names are case sensitive

        If version is not specified but the accession is of the form P29375.1, 
        the accession and version will automatically be split to accession=P29375 
        and version-1.

        If a taxid is submitted, includeattributes will be true.

        #example:
        url = "http://www.ebi.ac.uk/Tools/picr/rest/getUPIForAccession?accession=P29375&database=IPI&database=ENSEMBL&database=KEGG"
        """
        url = "http://www.ebi.ac.uk/Tools/picr/rest/getUPIForAccession"

        url += "?accession=" + accession
        if isinstance(database,str):
            self._checkDBname(database)
            url+= "&database=" + database
        elif isinstance(database,list):
            for d in database:
                self._checkDBname(d)
                url+="&database=" + d
	if taxid:
            url += "&taxonid=" +taxid
        if includeattributes == False:
            url += "&includeattributes=false"
        if onlyactive == False:
            url += "&onlyactive=false"
        res = self.request(url)
        #res = xmltools.easyXML(res)
        return res

    def getUPIForBLAST(self, blasfrag, database,
        taxid=None,
        version=None, 
        onlyactive=True, 
        includeattributes=True, **kargs):
        """Get Protein identifier given a sequence similarity (BLAST)

        :param str blastfrag:  the AA fragment to map to map [required]
        :param database: the database to map to (string). At least one database is 
            required, but multiple databases can be queried at once using a list.
        :param taxid: the NEWT taxon ID to limit the mappings [optional]
        :param bool onlyactive: if true, only active mappings will be returned. If false, 
            results may include deleted mappings. [optional, default is true]
        :param bool includeattributes: if true, extra attributes such as sequence 
            and taxon IDs will be returned if available. If false, no extra 
            information returned. [optional, default is false]


        Other options (related to BLAST analysis):

        See http://www.ebi.ac.uk/Tools/sss/ncbiblast/ for values.

        :param float scores: 
        :param str matrix: -specifies which protein scoring matrix to use. [optional, defaults to BLOSUM62]

        .. note:: parameter names are case sensitive

        ::

            res = p.getUPIForBLAST(p._blastfrag_example, "SWISSPROT",program="blastp",matrix="BLOSUM80")

        .. warning:: no sanity check performed on the optinal parameters
        """
        url = "http://www.ebi.ac.uk/Tools/picr/rest/getUPIForBLAST"
        url += "?blastfrag=" + blasfrag
        if isinstance(database,str):
            self._checkDBname(database)
            url+= "&database=" + database
        elif isinstance(database,list):
            for d in database:
                self._checkDBname(d)
                url+="&database=" + d
	if taxid:
            url += "&taxonid=" +taxid
        if includeattributes == False:
            url += "&includeattributes=false"
        if onlyactive == False:
            url += "&onlyactive=false"

        if kargs:
            postData = self.urlencode(kargs)
            res = self.request(url + "&" +postData)
        else:
            res = self.request(url)

        #res = xmltools.easyXML(res)
        return res



"""
Parameters:

    BLAST search parameters: These should not be changed unless you are sure that you know what you are doing.
        filtertype - which parameters should the BLAST results be filtered by, valid values are ORGANISM, IDENTITY, ORGANISM_AND_IDENTITY, and NONE. [optional, defaults to NONE]
            identityvalue - the minimum score to accept as a BLAST hit. [required if filtertype is IDENTITY or ORGANISM_AND_IDENTITY]
            identitytaxon - the target organism that BLAST is filtering for. [required if filtertype is ORGANISM or ORGANISM_AND_IDENTITY]
        program - which BLAST program to use for mapping [optional, defaults to blastp]
        alignments - specifies the number of alignments to find pre-filtering (there is probably no need to change this.) [optional, defaults to 100]
        scores - sets the maximum number of scores to display in output. [optional, defaults to 100]
        exp - sets the E-value cutoff. [optional, defaults to 10]
        dropoff - Amount score must drop before extension of hits is halted. [optional, defaults to 0]
        gapopen - sets the gap opening penalty. [optional, defaults to 11]
        gapext - sets the gap extension penalty [optional, defaults to 1]
        gapalign - perform gapped alignment. [optional, defaults to true]
        filter - specifies filters to be used to mask query sequence. See table 3.2.7 for details. [optional, defaults to F, ie none]
        align - sets the alignment view. [optional, defaults to 0]
        stype - sets the type of submission. [optional, defaults to protein]
        blastdb - set the database against which to query the protein fragments. [optional, defaults to uniprotkb]

"""
