"""Interface to the NCBIBLAST web service

.. topic:: What is NCBIBLAST ?

    :URL:
    :service: http://www.ebi.ac.uk/Tools/webservices/services/sss/ncbi_blast_rest

    NCBI BLAST - Protein Database Query

    The emphasis of this tool is to find regions of sequence similarity, 
    which will yield functional and evolutionary clues about the structure
    and function of your novel sequence.

    Rapid sequence database search programs utilizing the BLAST algorithm. For more information 
    on NCBI BLAST refer to http://www.ebi.ac.uk/Tools/sss/ncbiblast

"""

from bioservices.services import RESTService
import xmltools


__all__ = ["NCBIblast"]

class NCBIblast(RESTService):
    """


    """

    _url = "http://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
    _sequence_example = "MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"
    def __init__(self, verbose=True):
        """NCBIblast constructor"""
        super(NCBIblast, self).__init__(name="NCBIblast", url=NCBIblast._url, verbose=verbose)
        self._parameters = None
        self._parametersDetails = {}

    def getParameters(self):
        """List parameter names. 

         :returns: An XML document containing a list of parameter names.

            >>> n = ncbiblast.NCBIBlast()
            >>> res = n.getParameters()

        .. seealso:: :attr:`parameters` to get a list of the parameters.
        """
        request = self.url + "/parameters/"
        res = self.request(request)
        return res

    def _get_parameters(self):
        if self._parameters:
            return self._parameters
        else:
            res = self.getParameters()
            parameters = [x.text for x in res.getchildren()]
            self._parameters = parameters
        return self._parameters
    parameters = property(_get_parameters, doc="return list of parameters")

    def parametersDetails(self, parameterId):
        """Get detailed information about a parameter. 

        :returns: An XML document providing details about the parameter or a list
            of values that can take the parameters if the XML could be parsed. 

        For example::

            >>> ivalues = n.parametersDetails("matrix") 
            [u'BLOSUM45',
             u'BLOSUM50',
             u'BLOSUM62',
             u'BLOSUM80',
             u'BLOSUM90',
             u'PAM30',
             u'PAM70',
             u'PAM250']

        """
        if parameterId not in self.parameters:
            raise ValueError("Invalid parameterId provided(%s). See parameters attribute" % parameterId)

        if parameterId not in self._parametersDetails.keys():

            request = self.url + "/parameterdetails/" + parameterId 
            res = self.request(request)
            self._parametersDetails[parameterId] = res

        try:
            # try to interpret the content to return a list of values instead of the XML
            res = [x for x in self._parametersDetails[parameterId].findAll("value")]
            res = [y[0].text for y in [x.findAll('label') for x in res] if len(y)]
        except:
            pass

        return res



    def run(self, program=None, database=None, sequence=None,stype="protein", email=None, **kargs):
        """



python ncbiblast_urllib2.py -D ENSEMBL --email "test@yahoo.com" --sequence MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS --program blastp --database uniprotkb

        email     User e-mail address.
        title     an optional title for the job.

        .. rubric:: Compulsary arguments

        :param str program: BLAST program to use to perform the search (e.g., blastp)
        :param str type: Query sequence type. One of: dna, rna or protein.
        :param str sequence: Query sequence. The use of fasta formatted sequence is recommended.
        :param list database: List of database names for search. 
        :param str email: a valid email address

        .. rubric:: optional arguments. If not provided, a default value will be used

        :param str matrix: Scoring matrix to be used in the search. (e.g., BLOSUM45)
        :param bool gapalign:  Perform gapped alignments.
        :param int alignments:     Maximum number of alignments displayed in the output.
        :param exp:     E-value threshold.
        :param bool filter:  Low complexity sequence filter to process the query 
            sequence before performing the search.
        :param int scores:     Maximum number of scores displayed in the output.
        :param int dropoff:     Amount score must drop before extension of hits is halted.
        :param match_scores:     Match/miss-match scores to generate a scoring matrix for nucleotide searches.
        :param int gapopen:     Penalty for the initiation of a gap.
        :param int gapext:     Penalty for each base/residue in a gap.
        :param seqrange: Region of the query sequence to use for the search. Default: whole sequence.

	The up to data values accepted for each of these parameters can be 
        retrieved from the :meth:`parametersDetails`.

        For instance,:: 

            n = NCBIblast()
            n.parameterDetails("program")

            n.run(program="blastp", 
                 sequence=n._sequence_example, 
                 stype="protein", 
                 database="uniprotkb", 
                 email="test@yahoo.fr")

            database=["uniprotkb", "uniprotkb_swissprot"]

        Cases are not important. Spaces in the database case should be replaced by underscore.

        """
        # There are compulsary arguments:
        if program==None or sequence==None or database==None:
            raise ValueError("program, sequence and database must be provided")

        from easydev import checkParam

        # Here, we will check the arguments values (not the type)
        # Arguments will be checked by the service itself but if we can 
        # catch some before, it is better
        checkParam(program, self.parametersDetails("program"))
        checkParam(stype, ["protein", "dna", "rna"])

        # So far, we have these parameters
        params = {
            'program': program, 
            'sequence': sequence, 
            'email': email,
            'stype': stype}

        # all others are optional (actually type is also optional)
        # We can check all of the optional argument provided automatically.
        # this is fine for now but note for instance that stype could not be put 
        # here because what is returned by parametersDetails is not exactly what 
        # is expected.
        for k,v in kargs.iteritems():
             print k,v
             checkParam(v,self.parametersDetails(k))
             params[k] = v

        # similarly for the database, we must process it by hand because ther
        # can be more than one database
        print params
        #checkParam(database.lower(), [str(x.replace(" ", "_").lower()) 
        #    for x in self.parametersDetails("database")])
        if isinstance(database, list):
            databases = database[:]
        elif isinstance(database, str):
            databases = [database]
        else:
            raise TypeError("database must be a string or a list of strings")
        DBs = "&database=" + "&database=".join(databases)

        """
parser.add_option('-E', '--exp', help='E-value threshold')
parser.add_option('-f', '--filter', action="store_true", help='low complexity sequence filter')
parser.add_option('-n', '--alignments', type='int', help='maximum number of alignments')
parser.add_option('-s', '--scores', type='int', help='maximum number of scores')
parser.add_option('-d', '--dropoff', type='int', help='dropoff score')
parser.add_option('--match_score', help='match/missmatch score')
parser.add_option('-o', '--gapopen', type='int', help='open gap penalty')
parser.add_option('-x', '--gapext', type='int', help='extend gap penalty')
parser.add_option('-g', '--gapalign', action="store_true", help='optimise gap alignments')
parser.add_option('--seqrange', help='region within input to use as query')
# General options
parser.add_option('--title', help='job title')
parser.add_option('--outfile', help='file name for results')
parser.add_option('--outformat', help='output format for results')
parser.add_option('--async', action='store_true', help='asynchronous mode')
parser.add_option('--jobid', help='job identifier')
parser.add_option('--polljob', action="store_true", help='get job result')
parser.add_option('--status', action="store_true", help='get job status')
parser.add_option('--resultTypes', action='store_true', help='get result types')
    """
       
         

        print DBs
        res = self.requestPost("http://www.ebi.ac.uk/Tools/services/rest/ncbiblast/run/", 
            params, extra=DBs)
        
        return res


    def getStatus(self, jobid):
        """Return status of a nbciblast jobID 

        :param str jobid:
        :return: FINISHED, RUNNING, NOT_FOUND

        """
        requestUrl = self.url + '/status/' + jobid
        res = self.request(requestUrl, format="txt")
        return res


    def getResultTypes(self, jobid, verbose=True):
        """

        """
        requestUrl = self.url + '/resulttypes/' + jobid
        res = self.request(requestUrl, format="xml")


        identifiers = [x.findAll('identifier')[0].text for x in res['type']]
        labels = [[y.text for y in x.findAll('label')] for x in res['type']]
        mediaTypes = [[y.text for y in x.findAll('mediaTypes')] for x in res['type']]
        descriptions = [[y.text for y in x.findAll('description')] for x in res['type']]
        fileSuffix = [[y.text for y in x.findAll('fileSuffix')] for x in res['type']]

        if verbose==True:
            for i, ident in enumerate(identifiers):
                print(" ".join([ident, str(descriptions[i]), 
                    str(labels[i]), str(mediaTypes[i]), str(fileSuffix[i])]))
        return res

    #def save(self, jobId, identifier, fileSuffix):
    #    filename = jobId + '.' + str(resultType['identifier']) + '.' + \ 
    #        str(resultType['fileSuffix'])




    # TODO need to check that jobid is finished
    def getResult(self, jobid, type):
        """
        """
        requestUrl = self.url + '/result/' + jobid + '/' + type
        res = self.request(requestUrl, format=type)

        #todo
        #create filename and save
        #fh = open(filename, 'w');
        #fh.write(result)
        #fh.close()

        return res


    def clientPoll(self, jobId, checkInterval=1):
        import sys
        result = 'PENDING'
        while result == 'RUNNING' or result == 'PENDING':
            result = self.getStatus(jobId)
            print >> sys.stderr, result
            if result == 'RUNNING' or result == 'PENDING':
                time.sleep(checkInterval)



