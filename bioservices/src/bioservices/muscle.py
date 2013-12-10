#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EMBL-EBI
#
#  File author(s): 
#      Sven-Maurice Althoff, Christian Knauth
#      https://www.assembla.com/spaces/bioservices/team
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the MUSCLE web service

.. topic:: What is MUSCLE ?

    :URL: http://www.drive5.com/muscle/
    :service: http://www.ebi.ac.uk/Tools/webservices/services/msa/muscle_rest

    .. highlights::

        "MUSCLE - (MUltiple Sequence Comparison by Log-Expectation) 1)

        is claimed to achieve both better average accuracy and better speed than 
        ClustalW or T-Coffee, depending on the chosen options. Multiple alignments 
        of protein sequences are important in many applications, including 
        phylogenetic tree estimation, secondary structure prediction and critical 
        residue identification."

        -- from EMBL-EBI web page

"""
import sys
import time
from bioservices.services import RESTService

__all__ = ["MUSCLE"]


class MUSCLE(RESTService):
    """Interface to the `MUSCLE <http://www.ebi.ac.uk/Tools/webservices/services/msa/muscle_rest>`_ service.

    ::

        >>> from bioservices import *
        >>> m = MUSCLE(verbose=False)
        >>> sequencesFasta = open('filename','r')
        >>> jobid = n.run(format="fasta", sequence=sequencesFasta.read(),
                        email="name@provider")
        >>> s.getResult(jobid, "out")

    .. warning:: It is very important to provide a real e-mail address as your
        job otherwise very likely will be killed and your IP, Organisation or
        entire domain black-listed.


    Here is another similar example but we use :class:`~bioservices.uniprot.UniProt` 
    class provided in bioservices to fetch the FASTA sequences::

 
        >>> from bioservices import UniProt, MUSCLE
        >>> u = UniProt(verbose=False)
        >>> f1 = u.get_fasta("P18413")
        >>> f2 = u.get_fasta("P18412")
        >>> m = MUSCLE(verbose=False)
        >>> jobid = m.run(format="fasta", sequence=f1+f2, email="name@provider")
        >>> m.getResult(jobid, "out")

    """

    _url = "http://www.ebi.ac.uk/Tools/services/rest/muscle"
    def __init__(self, verbose=True):
        super(MUSCLE, self).__init__(name='MUSCLE', url=MUSCLE._url, verbose=verbose )
        self._parameters = None
        self._parametersDetails = {}

    def getParameters(self):
        """List parameter names.

         :returns: An XML document containing a list of parameter names.

         ::

             >>> from bioservices import muscle 
             >>> n = muscle.Muscle()
             >>> res = n.getParameters()
             >>> [x.text for x in res.findAll("id")]

         .. seealso:: :attr:`parameters` to get a list of the parameters without
            need to process the XML output.
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
    parameters = property(_get_parameters, doc=r"""Read-only attribute that returns a list of parameters. See :meth:`getParameters`.""")

    def getParametersDetails(self, parameterId):
        """Get detailed information about a parameter.
  
          :returns: An XML document providing details about the parameter or a list
              of values that can take the parameters if the XML could be parsed.
  
          For example::
  
              >>> n.getParametersDetails("format")
  
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
      
    def run(self, format=None, sequence=None, tree="none", email=None):
        """ Submit a job with the specified parameters.

        .. python ncbiblast_urllib2.py -D ENSEMBL --email "test@yahoo.com" --sequence
        .. MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS
        .. --program blastp --database uniprotkb


        .. rubric:: Compulsary arguments

        :param str format: input format (e.g., fasta)
        :param str sequence: query sequence. The use of fasta formatted sequence is recommended.
        :param str tree: tree type ('none','tree1','tree2')
        :param str email: a valid email address. Will be checked by the service itself.

        :return: A jobid that can be analysed with :meth:`getResult`,
            :meth:`getStatus`, ...

        The up to data values accepted for each of these parameters can be
        retrieved from the :meth:`parametersDetails`.

        For instance,::

            from bioservices import MUSCLE
            m = MUSCLE()
            m.parameterDetails("tree")

        Example::

            jobid = m.run(format="fasta",
                 sequence=sequence_example,
                 email="test@yahoo.fr")

        format can be a list of formats::

            format=['fasta','clw','clwstrict','html','msf','phyi','phys']

        The returned object is a jobid, which status can be checked. It must be
        finished before analysing/geeting the results.

        .. seealso:: :meth:`getResult`

        """

        # There are compulsary arguments:
        if format==None or sequence==None  or email==None:
            raise ValueError("format, sequence and email must be provided")


        # Here, we will check the arguments values (not the type)
        # Arguments will be checked by the service itself but if we can
        # catch some before, it is better

        # FIXME: return parameters from server are not valid
        self.checkParam(format, ['fasta','clw','clwstrict','html','msf','phyi','phys'])

        self.checkParam(tree, ['none','tree1','tree2'])

        # parameter structure
        params = {
            'format': format,
            'sequence': sequence,
            'email': email}
      
        request = self.url + "/run/"
        res = self.requestPost(request, params)
        return res

    def getStatus(self, jobid):
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
      requestUrl = self.url + '/status/' + jobid
      res = self.request(requestUrl, format="txt")
      return res

    def getResultTypes(self, jobid):
      """ Get available result types for a finished job.

      :param str jobid: a job identifier returned by :meth:`run`.
      :param bool verbose: print the identifiers together with their label,
            mediaTypes, description and filesuffix.

      :return: A dictionary, which keys correspond to the identifiers. Each
            identifier is itself a dictionary containing the label, description,
            file suffix and mediaType of the identifier.
      """
      if self.getStatus(jobid)!='FINISHED':
          self.logging.warning("waiting for the job to be finished. May take a while")
          self.wait(jobid, verbose=False)
      requestUrl = self.url + '/resulttypes/' + jobid
      res = self.request(requestUrl, format="xml")
      print res
      output = {}
    
      def myf(x):
          if len(x)==0: return ""
          else: return x[0].text

      descriptions = [myf(x.findall("description")) for x in res.getchildren()]
      identifiers = [myf(x.findall("identifier")) for x in res.getchildren()]
      mediaTypes = [myf(x.findall("mediaType")) for x in res.getchildren()]
      labels = [myf(x.findall("label")) for x in res.getchildren()]
      suffixes = [myf(x.findall("fileSuffix")) for x in res.getchildren()]

      for i, ident in enumerate(identifiers):
          output[ident] = {'label':labels[i], 'mediaType': mediaTypes[i],
                       'description':descriptions[i], 'fileSuffix':suffixes[i]}
      return output

    def getResult(self, jobid, resultType):
      """ Get the job result of the specified type.


      :param str jobid: a job identifier returned by :meth:`run`.
      :param str  resultType: type of result to retrieve. See :meth:`getResultTypes`.

      """
      if self.getStatus(jobid)!='FINISHED':
          self.logging.warning("waiting for the job to be finished. May take a while")
          self.wait(jobid, verbose=False)
      if self.getStatus(jobid) != "FINISHED":
          raise ValueError("job is not finished")
      requestUrl = self.url + '/result/' + jobid + '/' + resultType
      res = self.request(requestUrl, format=resultType)

      return res

    def wait(self, jobId, checkInterval=5, verbose=True):
      """This function checks the status of a jobid while it is running

      :param str jobid: a job identifier returned by :meth:`run`.
      :param int checkInterval: interval between requests in seconds.

      """

      if checkInterval<1:
          raise ValueError("checkInterval must be positive and less than minute")
      result = 'PENDING'
      while result == 'RUNNING' or result == 'PENDING':
          result = self.getStatus(jobId)
          if verbose:
              print >> sys.stderr, jobId, " is ", result
          if result == 'RUNNING' or result == 'PENDING':
              time.sleep(checkInterval)
      return result


