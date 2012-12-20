import urllib2
from services import RESTService



class PICR(RESTService):
    """Interface to the `PICR (Protein Identifier Cross reference ) <http://www.ebi.ac.uk/Tools/picr/>`_ service


    """
    def __init__(self):
        super(PICR, self).__init__(name="PICR")

    def getMappedDatabaseNames(self):
        url = "http://www.ebi.ac.uk/Tools/picr/rest/getMappedDatabaseNames"
        res = urllib2.urlopen(url).read()
        return res


    def getUPIForSequence(self, sequence, database, taxid=None,
        onlyactive=True, includeattributes=False):
        """

        :param sequence : the sequence to map [required]
        :param database:  the database to map to. At least one database is required, but
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

        Example:
            sequence=MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS
            database=[IPI, ENSEMBL, SWISSPROT] 
        """
        url = "http://www.ebi.ac.uk/Tools/picr/rest/getUPIForSequence"

        url += "?sequence=" + sequence
        if isinstance(database,str):
            url+= "&database=" + database
        elif isinstance(database,list):
            for d in database:
                url+="&database=" + d
        #if taxid !=None:
        #    url+=
        #if onlyactive

        print url

        res = urllib2.urlopen(url).read()

        return res

    def getUPIForAccession(self):
        #example:
        url = "http://www.ebi.ac.uk/Tools/picr/rest/getUPIForAccession?accession=P29375&database=IPI&database=ENSEMBL&database=KEGG"
        raise NotImplementedError
    def getUPIForBLAST(self):
        raise NotImplementedError



"""
<S-Insert>Method: getUPIForAccession
Base URL: http://www.ebi.ac.uk/Tools/picr/rest/getUPIForAccession
Parameters:

    accession - the accession to map [required]
    version - the version of accession to map [optional]
    database - the database to map to. At least one database is required, but multiple databases can be queried at once.
    taxid - the NEWT taxon ID to limit the mappings [optional]
    onlyactive - if true, only active mappings will be returned. If false, results may include deleted mappings. [optional, default is true]
    includeattributes - if true, extra attributes such as sequence and taxon IDs will be returned if available. If false, no extra information returned. [optional, default is false]

Notes:

Parameter names are case sensitive.

If version is not specified but the accession is of the form P29375.1, the accession and version will automatically be split to accession=P29375 and version-1.

If a taxid is submitted, includeattributes will be true.
Example: http://www.ebi.ac.uk/Tools/picr/rest/getUPIForAccession?accession=P29375&database=IPI&database=ENSEMBL
Method: getUPIForBLAST
Base URL: http://www.ebi.ac.uk/Tools/picr/rest/getUPIForBLAST
Parameters:

    blastfrag - the AA fragment to map to map [required]
    database - the database to map to. At least one database is required, but multiple databases can be queried at once.
    taxid - the NEWT taxon ID to limit the mappings [optional]
    onlyactive - if true, only active mappings will be returned. If false, results may include deleted mappings. [optional, default is true]
    includeattributes - if true, extra attributes such as sequence and taxon IDs will be returned if available. If false, no extra information returned. [optional, default is false]
    BLAST search parameters: These should not be changed unless you are sure that you know what you are doing.
        filtertype - which parameters should the BLAST results be filtered by, valid values are ORGANISM, IDENTITY, ORGANISM_AND_IDENTITY, and NONE. [optional, defaults to NONE]
            identityvalue - the minimum score to accept as a BLAST hit. [required if filtertype is IDENTITY or ORGANISM_AND_IDENTITY]
            identitytaxon - the target organism that BLAST is filtering for. [required if filtertype is ORGANISM or ORGANISM_AND_IDENTITY]
        program - which BLAST program to use for mapping [optional, defaults to blastp]
        matrix - specifies which protein scoring matrix to use. [optional, defaults to BLOSUM62]
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

Notes:

Parameter names are case sensitive.

If a taxid is submitted, includeattributes will be true.
Example:
http://www.ebi.ac.uk/Tools/picr/rest/getUPIForBLAST?blastfrag=MSVMYKKILYPTDFSETAEIALKHVKAFKTLKAEEVILLHVIDEREIKKRDIFSLLLGVAGLNKSVEEFENELKNKLTEEAKNKMENIKKELEDVGFKVKDIIVVGIPHEEIVKIAEDEGVDIIIMGSHGKTNLKEILLGSVTENVIKKSNKPVLVVKRKNS&database=SWISSPROT
"""
