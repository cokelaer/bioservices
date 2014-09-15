#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
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
#$Id$
"""This module provides a class :class:`~Readseq` to access to Readseq WS.


.. topic:: What is Readseq ?

    :URL: http://www.ebi.ac.uk/Tools/sfc/readseq/
    :Service: 
    :Citations: http://www.ncbi.nlm.nih.gov/pubmed/18428689

    .. highlights::

        Readseq reads and converts biosequences between a selection of common 
        biological sequence formats, including EMBL, GenBank and fasta sequence 
        formats. 

        Readseq homepage -- Sep 2014



.. testsetup:: biomodels

    from bioservices import Readseq
    s = Readseq()


"""
import copy
from bioservices.services import WSDLService


__all__ = ["Readseq"]



class Readseq(WSDLService):
    """Interface to the `Readseq <http://www.ebi.ac.uk/readseq>`_ service

    ::

        >>> from bioservices import *
        >>> s = Readseq()


    """
    _url = "http://www.ebi.ac.uk/Tools/services/soap/readseq?wsdl"
    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(Readseq, self).__init__(name="Readseq", url=Readseq._url, verbose=verbose)
        self._parameters = None

    def _get_parameter(self):
        if self._parameters is None:
            self._parameters = self.get_parameters()
        return self._parameters
    parameters = property(_get_parameter, doc="Get list of parameter names")

    def get_parameters(self):
        """Get a list of the parameter names.

        :returns: a list of strings giving the names of the parameters.

        """
        parameters = self.serv.getParameters().id
        return parameters

    def get_parameter_details(self, parameter):
        """Get details of a specific parameter.

        :param str parameter: identifier/name of the parameter to fetch details of.
        :return: a data structure describing the parameter and its values.

        """
        self.devtools.check_param_in_list(parameter, self.parameters)
        return self.serv.getParameterDetails(parameter)

    def run(self, email, title, **kargs):
        """Submit a job to the service.

        :param str email: user e-mail address. 
        :param str title: job title.
        :param params: parameters for the tool as returned by :meth:`get_parameter_details`.
        :return: string containing the job identifier (jobId).
        """
        for k in kargs.keys():
            self.devtools.check_param_in_list(k, self.parameters)
        for k in ['inputformat','outputformat', 'outputcase', 'reverse', 'degap',
                'feature', 'fthandle']:
            if k in kargs.keys():
                value = kargs.get(k)

                valid_values = [x.value for x in self.get_parameter_details(k).values.value]

                self.devtools.check_param_in_list(str(value), valid_values)

        jobid = self.serv.run(email, title, kargs)
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
        return self.serv.getStatus(jobid)

    def get_result_types(self, jobid):
        """Get the available result types for a finished job.

        :param str jobid: job identifier.
        :return: a list of wsResultType data structures describing the available result types.
        """
        return self.serv.getResultTypes(jobid)

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
            self.logging.warning("Your job is not finished yet. Try again.")
            return
        type_ = self.get_result_types(jobid).type[0].identifier
        res = self.serv.getResult(jobid, type_)

        res = res.decode("base64")
        return res

"""
The input parameters for the job:

Attribute   Type    Description
inputformat     int     sequence format for input data
outputformat    int     sequence format for output data
outputcase  string  character case for output sequence data
reverse     boolean     output reverse complement of input nucleotide sequence
degap   string  remove gap symbols from sequence
transymbol  string  replace specified base/residue symbol(s) in input sequence with specified base/residue symbol(s)
feature     string  list of selected features to process
fthandle    string  action to perform on selected features
subrange    string  region of input sequence on which feature processing is performed
sequence    string  input sequence data to process

More detailed information about each parameter, including valid values can be obtained using the getParameterDetails(parameterId) operation.
wsParameterDetails

Descriptive information about a tool parameter. Returned by getParameterDetails(parameterId).
Attribute   Type    Description
name    string  Name of the parameter.
description     string  Description of the parameter, suitable for use in option help interfaces.
type    string  Data type of the parameter.
values  list of wsParameterValue    Optional list of valid values for the option.
wsParameterValue

Description of a tool parameter value. Used in wsParameterDetails.
Attribute   Type    Description
label   string  Display name of the value, for use in interfaces.
value   string  String representation of the value to be passed to the tool parameter.
defaultValue    boolean     Flag indicating if this value is the default.
properties  list of wsProperty  Optional list of key/value pairs providing further information.
wsProperty

Properties of a tool parameter value. Used in wsParameterValue.
Attribute   Type    Description
key     string  Property name.
value   string  Property value.
wsRawOutputParameter

Additional parameters passed when requesting a result. See getResult(jobId, type, parameters).
Attribute   Type    Description
name    string  Parameter name.
value   list of string  Parameter value.
wsResultType

Description of a result type. Returned by getResultTypes(jobId).
Attribute   Type    Description
identifier  string  Identifier for the result type. Passed as type to getResult(jobId, type, parameters).
label   string  Display name for use in user interfaces.
description     string  Description of the result type, for use in help interfaces.
mediaType   string  MIME type of the returned data.
fileSuffix  string  Suggested suffix for file name, if writing data to disk. 
"""
