#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EMBL-EBI
#
#  File author(s):
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the NCBIBLAST web service

.. topic:: What is NCBIBLAST ?

    :URL: http://blast.ncbi.nlm.nih.gov/
    :service: http://www.ebi.ac.uk/Tools/webservices/services/sss/ncbi_blast_rest

    .. highlights::

        "NCBI BLAST - Protein Database Query

        The emphasis of this tool is to find regions of sequence similarity,
        which will yield functional and evolutionary clues about the structure
        and function of your novel sequence."

        -- from NCBIblast web page


"""
import sys
import time

from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["NCBIblast"]


class NCBIblast:
    """Interface to the `NCBIblast <http://blast.ncbi.nlm.nih.gov/>`_ service.

    ::

        >>> from bioservices import *
        >>> s = NCBIblast(verbose=False)
        >>> jobid = s.run(program="blastp", sequence=s._sequence_example,
            stype="protein", database="uniprotkb", email="name@provider")
        >>> s.getResult(jobid, "out")

    .. warning:: It is very important to provide a real e-mail address as your
        job otherwise very likely will be killed and your IP, Organisation or
        entire domain black-listed.

    When running a blast request, a program is required. You can obtain the
    list using::

        >>> s.parametersDetails("program")
        [u'blastp', u'blastx', u'blastn', u'tblastx', u'tblastn']

    * blastn: Search a nucleotide database using a nucleotide query
    * blastp: Search protein database using a protein query
    * blastx: Search protein database using a translated nucleotide query
    * tblastn     Search translated nucleotide database using a protein query
    * tblastx     Search translated nucleotide database using a translated nucleotide query

    """

    _sequence_example = "MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"

    def __init__(self, verbose=False):
        """.. rubric:: NCBIblast constructor

        :param bool verbose: prints informative messages

        """
        url = "http://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
        self.services = REST(name="NCBIblast", url=url, verbose=verbose)
        self._parameters = None
        self._parametersDetails = {}
        self.checkInterval = 2

    def get_parameters(self):
        """List parameter names.

        :returns: An XML document containing a list of parameter names.

        ::

            >>> from bioservices import ncbiblast
            >>> n = ncbiblast.NCBIblast()
            >>> res = n.get_parameters()
            >>> [x.text for x in res.findAll("id")]

        .. seealso:: :attr:`parameters` to get a list of the parameters without
            need to process the XML output.
        """

        res = self.services.http_get(
            "parameters",
            frmt="json",
            headers={
                "User-Agent": self.services.getUserAgent(),
                "Accept": "application/json",
            },
        )
        return res["parameters"]

    def _get_parameters(self):
        if self._parameters:
            return self._parameters
        else:
            # on 2 lines in case it fails, self._parameters remaisn None
            res = self.get_parameters()
            self._parameters = res
        return self._parameters

    parameters = property(_get_parameters)

    def get_parameter_details(self, parameterId):
        """Get detailed information about a parameter.

        :returns: An XML document providing details about the parameter or a list
            of values that can take the parameters if the XML could be parsed.

        For example::

            >>> s.parameter_details("matrix")
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
            request = "parameterdetails/" + parameterId
            res = self.services.http_get(
                request,
                frmt="json",
                headers={
                    "User-Agent": self.services.getUserAgent(),
                    "Accept": "application/json",
                },
            )

            try:
                data = [x["value"] for x in res["values"]["values"]]
            except:
                data = res
            self._parametersDetails[parameterId] = data
        return self._parametersDetails[parameterId]

    def run(self, program=None, database=None, sequence=None, stype="protein", email=None, **kargs):
        """Submit a job with the specified parameters.

        .. python ncbiblast_urllib2.py -D ENSEMBL --email "test@yahoo.com" --sequence
        .. MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS
        .. --program blastp --database uniprotkb


        .. rubric:: Compulsary arguments

        :param str program: BLAST program to use to perform the search (e.g., blastp)
        :param str sequence: query sequence. The use of fasta formatted sequence is recommended.
        :param list database: list of database names for search or possible a single string (for one database).
            There are some mismatch between the output of parametersDetails("database") and
            the accepted values. For instance UniProt Knowledgebase should be
            given as "uniprotkb".
        :param str email: a valid email address. Will be checked by the service itself.

        .. rubric:: Optional arguments. If not provided, a default value will be used

        :param str type: query sequence type in 'dna', 'rna' or 'protein' (default is protein).
        :param str matrix: scoring matrix to be used in the search (e.g., BLOSUM45).
        :param bool gapalign:  perform gapped alignments.
        :param int alignments:     maximum number of alignments displayed in the output.
        :param exp:     E-value threshold.
        :param bool filter:  low complexity sequence filter to process the query
            sequence before performing the search.
        :param int scores:     maximum number of scores displayed in the output.
        :param int dropoff:     amount score must drop before extension of hits is halted.
        :param match_scores:     match/miss-match scores to generate a scoring matrix
            for nucleotide searches.
        :param int gapopen:     penalty for the initiation of a gap.
        :param int gapext:     penalty for each base/residue in a gap.
        :param seqrange: region of the query sequence to use for the search.
            Default: whole sequence.
        :return: A jobid that can be analysed with :meth:`getResult`,
            :meth:`getStatus`, ...

        The up to data values accepted for each of these parameters can be
        retrieved from the :meth:`get_parameter_details`.

        For instance,::

            from bioservices import NCBIblast
            n = NCBIblast()
            n.get_parameter_details("program")

        Example::

            jobid = n.run(program="blastp",
                 sequence=n._sequence_example,
                 stype="protein",
                 database="uniprotkb",
                 email="test@yahoo.fr")

        Database can be a list of databases::

            database=["uniprotkb", "uniprotkb_swissprot"]

        The returned object is a jobid, which status can be checked. It must be
        finished before analysing/geeting the results.

        .. seealso:: :meth:`getResult`

        .. warning:: Cases are not important. Spaces in the database case should
            be replaced by underscore.

        .. note:: database returned by the server have meaningless names since
            they do not map to the expected names. An example is "ENA Sequence Release"
            that should be provided as em_rel

        http://www.ebi.ac.uk/Tools/sss/ncbiblast/help/index-nucleotide.html

        """
        # There are compulsary arguments:
        if program is None or sequence is None or database is None or email is None:
            raise ValueError("program, sequence, email  and database must be provided")

        checkParam = self.services.devtools.check_param_in_list

        # Here, we will check the arguments values (not the type)
        # Arguments will be checked by the service itself but if we can
        # catch some before, it is better
        checkParam(program, self.get_parameter_details("program"))
        checkParam(stype, ["protein", "dna", "rna"])

        # So far, we have these parameters
        params = {
            "program": program,
            "sequence": sequence,
            "email": email,
            "stype": stype,
        }

        # all others are optional (actually type is also optional)
        # We can check all of the optional argument provided automatically.
        # this is fine for now but note for instance that stype could not be put
        # here because what is returned by parametersDetails is not exactly what
        # is expected.
        for k, v in kargs.items():
            # print(k, v)
            checkParam(v, self.get_parameter_details(k))
            params[k] = v

        # similarly for the database, we must process it by hand because ther
        # can be more than one database
        # checkParam(database.lower(), [str(x.replace(" ", "_").lower())
        #    for x in self.parametersDetails("database")])
        if isinstance(database, list):
            databases = database[:]
        elif isinstance(database, str):
            databases = [database]
        else:
            raise TypeError("database must be a string or a list of strings")
        params["database"] = databases

        """
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
        # IMPORTANT: use data parameter, not params !!!
        res = self.services.http_post(
            "run",
            frmt=None,
            data=params,
            headers={
                "User-Agent": self.services.getUserAgent(),
                "accept": "text/plain",
            },
        )

        return res

    def get_status(self, jobid):
        """Get status of a submitted job

        :param str jobid:
        :param str jobid: a job identifier returned by :meth:`run`.
        :return: A string giving the jobid status (e.g. FINISHED).

         The values for the status are:

         *   RUNNING: the job is currently being processed.
         *   FINISHED: job has finished, and the results can then be retrieved.
         *   ERROR: an error occurred attempting to get the job status.
         *   FAILURE: the job failed.
         *   NOT_FOUND: the job cannot be found.


        """
        res = self.services.http_get(
            "status/{}".format(jobid),
            frmt="txt",
            headers={
                "User-Agent": self.services.getUserAgent(),
                "accept": "text/plain",
            },
        )
        return res

    def get_result_types(self, jobid):
        """Get available result types for a finished job.

        :param str jobid: a job identifier returned by :meth:`run`.
        :param bool verbose: print the identifiers together with their label,
            mediaTypes, description and filesuffix.

        :return: A dictionary, which keys correspond to the identifiers. Each
            identifier is itself a dictionary containing the label, description,
            file suffix and mediaType of the identifier.
        """
        if self.get_status(jobid) != "FINISHED":
            self.services.logging.warning("waiting for the job to be finished. May take a while")
            self.wait(jobid, verbose=False)
        url = "resulttypes/" + jobid
        res = self.services.http_get(
            url,
            frmt="json",
            headers={
                "User-Agent": self.services.getUserAgent(),
                "accept": "application/json",
            },
        )
        return [x["identifier"] for x in res["types"]]

    def get_result(self, jobid, result_type):
        """Get the job result of the specified type.


          :param str jobid: a job identifier returned by :meth:`run`.
          :param str  result_type: type of result to retrieve. See :meth:`getResultTypes`.

          The output from the tool itself.
          Use the 'format' parameter to retireve the output in different formats,
          the 'compressed' parameter to retrieve the xml output in compressed form.
          Format options::

             0 = pairwise,
             1 = query-anchored showing identities,
             2 = query-anchored no identities,
             3 = flat query-anchored showing identities,
             4 = flat query-anchored no identities,
             5 = XML Blast output,
             6 = tabular,
             7 = tabular with comment lines,
             8 = Text ASN.1,
             9 = Binary ASN.1,
             10 = Comma-separated values,
             11 = BLAST archive format (ASN.1).

        See NCBI Blast documentation for details.
        Use the 'compressed' parameter to return the XML output in compressed form.
        e.g. '?format=5&compressed=true'.


        """
        if self.get_status(jobid) != "FINISHED":
            self.services.logging.warning("waiting for the job to be finished. May take a while")
            self.wait(jobid)
        if self.get_status(jobid) != "FINISHED":
            raise ValueError("job is not finished")
        url = "result/" + jobid + "/" + result_type

        if result_type in ["out", "error", "sequence", "ids"]:
            res = self.services.http_get(
                url,
                frmt="txt",
                headers={
                    "User-Agent": self.services.getUserAgent(),
                    "accept": "text/plain",
                },
            )
        elif result_type in ["xml"]:
            res = self.services.http_get(
                url,
                frmt="xml",
                headers={
                    "User-Agent": self.services.getUserAgent(),
                    "accept": "text/plain",
                },
            )
        return res

    def wait(self, jobId):
        """This function checks the status of a jobid while it is running

        :param str jobid: a job identifier returned by :meth:`run`.
        :param int checkInterval: interval between requests in seconds.

        """

        if self.checkInterval < 1:
            raise ValueError("checkInterval must be positive and less than a second")
        result = "PENDING"
        while result == "RUNNING" or result == "PENDING":
            result = self.get_status(jobId)
            if result == "RUNNING" or result == "PENDING":
                time.sleep(self.checkInterval)
        return result

    def _get_database(self):
        return self.get_parameter_details("database")

    databases = property(_get_database, doc=r"""Returns accepted databases.""")
