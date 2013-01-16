"""Interface to the NCIBLAST web service

.. topic:: What is NCIBLAST ?

    :URL:
    :service: http://www.ebi.ac.uk/Tools/webservices/services/sss/ncbi_blast_rest

    NCBI BLAST - Protein Database Query
    The emphasis of this tool is to find regions of sequence similarity, 
    which will yield functional and evolutionary clues about the structure
    and function of your novel sequence.

"""

from bioservices.services import RESTService
import xmltools


class NCIBlast(RESTService):
    """

python ncbiblast_urllib2.py -D ENSEMBL --email "test@yahoo.com" --sequence MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS --program blastp --database uniprotkb

    """

    _url = "http://www.ebi.ac.uk/Tools/services/rest/ncbiblast"

    def __init__(self, verbose=True):
        """NCIblast constructor"""
        super(NCIBlast, self).__init__(name="NCIBlast", url=NCIBlast._url, verbose=verbose)
        self._parameters = None

    def getParameters(self):
        """List parameter names. 

         :returns: An XML document containing a list of parameter names.

            >>> n = nciblast.NCIBlast()
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
            raise ValueError("Invalid parameterId provided(%s). " % parameterId)
        request = self.url + "/parameterdetails/" + parameterId 
        res = self.request(request)

        try:
            # try to interpret the content to return a list of values instead of the XML
            res = [x for x in res.findAll("value")]
            res = [y[0].text for y in [x.findAll('label') for x in res] if len(y)]
        except:
            pass

        return res



    def run(self, program, database, stype="protein"):
        """



python ncbiblast_urllib2.py -D ENSEMBL --email "test@yahoo.com" --sequence MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS --program blastp --database uniprotkb

        email     User e-mail address.
        title     an optional title for the job.
        program     BLAST program to use to perform the search.
        matrix     Scoring matrix to be used in the search.
        alignments     Maximum number of alignments displayed in the output.
        scores     Maximum number of scores displayed in the output.
        exp     E-value threshold.
        dropoff     Amount score must drop before extension of hits is halted.
        match_scores     Match/miss-match scores to generate a scoring matrix for for nucleotide searches.
        gapopen     Penalty for the initiation of a gap.
        gapext     Penalty for each base/residue in a gap.
        filter     Low complexity sequence filter to process the query sequence before performing the search.
        :param seqrange: Region of the query sequence to use for the search. Default: whole sequence.
        gapalign     Perform gapped alignments.
        align     Alignment format to use in output.
        stype     Query sequence type. One of: dna, rna or protein.
        sequence     Query sequence. The use of fasta formatted sequence is recommended.
        database     List of database names for search. 
        """
        from easydev import checkParam
        checkParam(program, [])

        

        """parser.add_option('-p', '--program', help='program to run')
parser.add_option('-D', '--database', help='database to search')
parser.add_option('--stype', default='protein', help='query sequence type')
parser.add_option('-m', '--matrix', help='scoring matrix')
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
parser.add_option('--sequence', help='input sequence file name')
# General options
parser.add_option('--email', help='e-mail address')
parser.add_option('--title', help='job title')
parser.add_option('--outfile', help='file name for results')
parser.add_option('--outformat', help='output format for results')
parser.add_option('--async', action='store_true', help='asynchronous mode')
parser.add_option('--jobid', help='job identifier')
parser.add_option('--polljob', action="store_true", help='get job result')
parser.add_option('--status', action="store_true", help='get job status')
parser.add_option('--resultTypes', action='store_true', help='get result types')
parser.add_option('--quiet', action='store_true', help='decrease output level')
parser.add_option('--verbose', action='store_true', help='increase output level')
parser.add_option('--baseURL', default=baseUrl, help='Base URL for service')
parser.add_option('--debugLevel', type='int', default=debugLevel, help='debug output level')
    """
        params = {
            'program': 'blastp', 
            'email':'test@yahoo.com', 
            'sequence': 'MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS', 
            'database':'uniprotkb', 
            'stype':'protein'}

        res = self.requestPost("http://www.ebi.ac.uk/Tools/services/rest/ncbiblast/run/", params)
        
        return res




