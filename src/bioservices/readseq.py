#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2015 - EBI-EMBL
#  Copyright (c) 2016-2017 - Institut Pasteur
#
#  File author(s): thomas cokelaer
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""This module provides a class :class:`~Seqret` to access to Seqret WS.


.. topic:: What is Seqret ?

    :URL: http://www.ebi.ac.uk/Tools/services/rest/seqret/
    :Service:
    :Citations: http://www.ncbi.nlm.nih.gov/pubmed/18428689

    .. highlights::

        EMBOSS seqret reads and converts biosequences between a selection of common
        biological sequence formats, including EMBL, GenBank and fasta sequence
        formats.

        Seqret homepage -- Sep 2017


"""
import copy
from bioservices.services import REST


__all__ = ["Seqret"]



class Seqret(REST):
    """Interface to the `Seqret <http://www.ebi.ac.uk/readseq>`_ service

    ::

        >>> from bioservices import *
        >>> s = Seqret()

    The ReadSeq service was replaced by the Seqret services (2015).

    .. versionchanged:: 0.15

    """
    _url = "https://www.ebi.ac.uk/Tools/services/rest/emboss_seqret"
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(Seqret, self).__init__(name="seqret", url=Seqret._url, verbose=verbose)
        self._parameters = None

    def _get_parameter(self):
        if self._parameters is None:
            self._parameters = self._get_parameters()
        return self._parameters
    parameters = property(_get_parameter, doc="Get list of parameter names")

    def _get_parameters(self):
        """Get a list of the parameter names.

        :returns: a list of strings giving the names of the parameters.

        """
        parameters = self.http_get("parameters", frmt="xml")
        res = self.easyXML(parameters)
        parameters = [x.text for x in res.findAll("id")]
        return parameters

    def get_parameter_details(self, parameter):
        """Get details of a specific parameter.

        :param str parameter: identifier/name of the parameter to fetch details of.
        :return: a data structure describing the parameter and its values.

        ::

            rs = ReadSeq()
            print(rs.get_parameter_details("stype"))

        """
        parameters = self.http_get("parameterdetails/{}".format(parameter), frmt="xml")
        res = self.easyXML(parameters)

        results = []
        for value in res.findAll('values')[0].findAll("value"):
            items = value.findAll()
            if len(items):
                results.append({
                    "text": items[0].text,
                    "value": items[1].text,
                    "defaultvalue": items[2].text})

        return results

    def run(self, email, title, **kargs):
        """Submit a job to the service.

        :param str email: user e-mail address.
        :param str title: job title.
        :param params: parameters for the tool as returned by :meth:`get_parameter_details`.
        :return: string containing the job identifier (jobId).

        Deprecated (olf readseq service)::

            Format Name     Value
            Auto-detected   0
            EMBL            4
            GenBank         2
            Fasta(Pearson)  8
            Clustal/ALN     22
            ACEDB           25
            BLAST           20
            DNAStrider      6
            FlatFeat/FFF    23
            GCG             5
            GFF             24
            IG/Stanford     1
            MSF             15
            NBRF            3
            PAUP/NEXUS      17
            Phylip(Phylip4)     12
            Phylip3.2       11
            PIR/CODATA      14
            Plain/Raw       13
            SCF             21
            XML             19

        As output, you also have

        Pretty 18

        ::

            s = readseq.Seqret()
            jobid = s.run("cokelaer@test.co.uk", "test", sequence=fasta, inputformat=8,
                outputformat=2)
            genbank = s.get_result(s._jobid)


        """
        for k in kargs.keys():
            self.devtools.check_param_in_list(k, self.parameters)

        assert "sequence" in kargs.keys()
        params = {"email":email, "title":title}

        for k in ['stype', 'inputformat','outputformat', "feature", "firstonly",
                  "reverse", 'outputcase', 'seqrange']:
            if k in kargs.keys():
                value = kargs.get(k)

                details = self.get_parameter_details(k)
                valid_values = [x['value'] for x in details]

                self.devtools.check_param_in_list(str(value), valid_values)
                params[k] = value
        #r = requests.post(url + "/run?", data={"sequence":fasta, "stype": "protein",
        #"inputformat":"raw", "outputformat":"fasta", "email":"thomas.cokelaer@pasteur.fr",
        #"title":"test"})

        params['sequence'] = kargs['sequence']

        jobid = self.http_post("run", frmt="txt", data=params)
        self._jobid = jobid
        return jobid

    def get_status(self, jobid=None):
        """Get the status of a submitted job.

        :param str jobid: job identifier.
        :return: string containing the status.

        The values for the status are:

        - RUNNING: the job is currently being processed.
        - FINISHED: job has finished, and the results can then be retrieved.
        - ERROR: an error occurred attempting to get the job status.
        - FAILURE: the job failed.
        - NOT_FOUND: the job cannot be found.

        """
        res = self.http_get("status/{}".format(jobid))
        return res.content.decode()

    def get_result_types(self, jobid):
        """Get the available result types for a finished job.

        :param str jobid: job identifier.
        :return: a list of wsResultType data structures describing the available result types.
        """
        res = self.http_get("resulttypes/{}".format(jobid))

        res = self.easyXML(res.content.decode())
        this = res.findAll("types")[0].findAll("type")[0].findAll('identifier')
        return this[0].text

    def get_result(self, jobid, parameters=None):
        """Get the result of a job of the specified type.

        :param str jobid: job identifier.
        :param parameters: optional list of wsRawOutputParameter used to
            provide additional parameters for derived result types.
        :return: the result data for the specified type, base64 encoded.
            Depending on the SOAP library and programming language used the
            result may be returned in decoded form. For some result types
            (e.g. images) this will be binary data rather than a text string.
        """
        if self.get_status(jobid) != 'FINISHED':
            self.logging.warning("Your job is not finished yet. Try again later.")
            return

        result_types = self.get_result_types(jobid)

        res = self.http_get("result/{}/{}".format(jobid, result_types))
        res = res.content.decode()

        try:
            import base64
            res = base64.b64decode(res).decode()
        except:
            pass
        return res

