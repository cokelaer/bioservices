# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
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
"""Interface to the ArrayExpress web Service.

.. topic:: What is ArrayExpress ?

    :URL: http://www.ebi.ac.uk/arrayexpress/
    :REST: http://www.ebi.ac.uk/arrayexpress/xml/v2/experiments

    .. highlights::

        ArrayExpress is a database of functional genomics experiments that can be queried and the data downloaded. It includes gene expression data from microarray and high throughput sequencing studies. Data is collected to MIAME and MINSEQE standards. Experiments are submitted directly to ArrayExpress or are imported from the NCBI GEO database.

        -- ArrayExpress home page, Jan 2013

"""
from __future__ import print_function

from bioservices.services import REST


__all__ = ["ArrayExpress"]


class ArrayExpress(REST):
    """Interface to the `ArrayExpress <http://www.ebi.ac.uk/arrayexpress>`_ service

    ArrayExpress allows to retrieve data sets used in various experiments.

    **QuickStart** Given an experiment name (e.g., E-MEXP-31), type::

        s = ArrayExpress()
        s.getEA('E-MEXP-31')

    You can also quickyl retrieve experiments matching some search queries as
    follows::

        a.queryAE(keywords="pneumonia", species='homo+sapiens')

    Now let us look at other methods.If you know the file and experiment
    name, you can retrieve a specific file as follows::

        >>> from bioservices import ArrayExpress
        >>> s = ArrayExpress()
        >>> # retrieve a specific file from a experiment
        >>> res = s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")

    The main issue is that you may not know the experiment you are looking for.
    You can query experiments by keyword::

        >>> # Search for experiments
        >>> res = s.queryExperiments(keywords="cancer+breast", wholewords=True)

    keywords used in queries follows these rules:

    * Accession number and keyword searches are case insensitive
    * More than one keyword can be searched for using the + sign (e.g. keywords="cancer+breast")
    * Use an asterisk as a multiple character wild card (e.g. keywords="colo*")
    * use a question mark ? as a single character wild card (e.g. keywords="te?t")

    More complex queries can be constructed using the operators AND, OR or NOT.
    AND is the default if no operator is specified. Either experiments or
    files can be searched for. Examples are::

        keywords="prostate+AND+breast"
        keywords="prostate+breast"      # same as above
        keywords="prostate+OR+breast"
        keywords="prostate+NOT+breast "

    The returned objects are XML parsed with beautifulSoup. You can get all
    experiments using the getChildren method:

    .. doctest::
        :options: +SKIP

        >>> res = s.queryExperiments(keywords="breast+cancer")
        >>> len(res.getchildren())
        1487


    If you know what you are looking for, you can give the experiment name::

        >>> res = s.retrieveExperiment("E-MEXP-31")
        >>> exp = res.getchildren()[0]   # it contains only one experiment
        >>> [x.text for x in exp.getchildren() if x.tag == "name"]
        ['Transcription profiling of mammalian male germ cells undergoing mitotic
        growth, meiosis and gametogenesis in highly enriched cell populations']

    Using the same example, you can retrieve the names of the files related to
    the experiment::


        >>> files = [x.getchildren() for x in exp.getchildren() if x.tag == "files"]
        >>> [x.get("name") for x in files[0]]
        ['E-MEXP-31.raw.1.zip',
         'E-MEXP-31.processed.1.zip',
         'E-MEXP-31.idf.txt',
         'E-MEXP-31.sdrf.txt']

    Nnew in version 1.3.7 you can use the method :meth:`getEA`


    Then, you may want to download a particular file::

        >>> s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")


    You can get json file instead of XML by setting the format to "json"::

        >>> a.format = "json"

    .. seealso:: :meth:`queryFiles` for more details about the parameters to be
        used in queries.

    .. warning:: supports only new style (v2). You can still use the old style by
        setting the request manually using the :meth:`version`.

    .. warning:: some syntax requires the + character, which is a special character
        for http requests. It is replaced internally by spaces if found
    .. warning:: filtering is not implemented (e.g., assaycount:[x TO y]syntax.)
    """
    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages

        """
        super(ArrayExpress, self).__init__(name="ArrayExpress",
            url="http://www.ebi.ac.uk/arrayexpress", cache=cache,
            verbose=verbose)

        self.easyXMLConversion = True
        self._format = "xml"
        self.version = "v2"

    def _set_format(self, f):
        self.devtools.check_param_in_list(f, ["json", "xml"])
        self._format = f
    def _get_format(self):
        return self._format
    format = property(_get_format, _set_format,
        doc="Read/Write access to specify the output format (json or xml)")

    def _search(self, mode, **kargs):
        """common function to search for files or experiments"""
        assert mode in ["experiments", "files"]
        url = "{0}/{1}/{2}".format(self.format, self.version, mode)


        defaults = {
            "accession":None, #ex: E-MEXP-31
            "keywords":None,
            "species": None,
            "wholewords": "on",
            "expdesign":  None,
            "exptype": None,
            "gxa": "true",
            "pmid": None,
            "sa": None,
            "ef": None,         # e.g., CellType
            "efv": None,         # e.g., HeLa
            "array":None,       # ex: A-AFFY-33
            "expandfo": "on",
            "directsub": "true",
            "sortby": ["accession", "name", "assays", "species", "releasedate", "fgem", "raw", "atlas"],
            "sortorder": ["ascending", "descending"],
        }

        for k in kargs.keys():
            self.devtools.check_param_in_list(k, list(defaults.keys()))

        #if len(kargs.keys()):
        #    url += "?"
        params = {}

        for k, v in kargs.items():
            if k in ["expandfo", "wholewords"]:
                if v in ["on", True, "true", "TRUE", "True"]:
                    #params.append(k + "=on")
                    params[k] = "on"
            elif k in ["gxa", "directsub"]:
                if v in ["on", True, "true", "TRUE", "True"]:
                    #params.append(k + "=true")
                    params[k] = "true"
                elif v in [False, "false", "False"]:
                    #params.append(k + "=false")
                    params[k] = "false"
                else:
                    raise ValueError("directsub must be true or false")
            else:
                if k in ["sortby", "sortorder"]:
                    self.devtools.check_param_in_list(v, defaults[k])
                #params.append(k + "=" + v)
                params[k] = v

        # NOTE: + is a special character that is replaced by %2B
        # The + character is the proper encoding for a space when quoting
        # GET or POST data. Thus, a literal + character needs to be escaped
        # as well, lest it be decoded to a space on the other end
        for k,v in params.items():
            params[k] = v.replace("+",  " ")

        self.logging.info(url)
        res = self.http_get(url, frmt=self.format, params=params)
        if self.format == "xml":
            res = self.easyXML(res)
        return res

    def queryFiles(self, **kargs):
        """Retrieve a list of files associated with a set of experiments

        The following parameters are used to search for experiments/files:

        :param str accession: experiment primary or secondary accession e.g. E-MEXP-31
        :param str array: array design accession or name e.g., A-AFFY-33
        :param str ef: Experimental factor, the name of the main variables in an
            experiment. (e.g., CellType)
        :param str efv:  Experimental factor value. Has EFO expansion. (e.g.,
            HeLa)
        :param str expdesign: Experiment design type  (e.g., "dose+response")
        :param str exptype:  Experiment type. Has EFO expansion. (e.g.,
            "RNA-seq")
        :param str gxa: Presence in the Gene Expression Atlas. Only value is gxa=true.
        :param str keywords: e.g. "cancer+breast"
        :param str pmid: PubMed identifier (e.g., 16553887)
        :param str sa: Sample attribute values. Has EFO expansion. fibroblast
        :param str species: Species of the samples.Has EFO expansion. (e.g., "homo+sapiens")
        :param bool wholewords:

        The following parameters can filter the experiments:

        :param str directsub: only experiments directly submitted to
            ArrayExpress (true) or only imported from GEO databae (false)


        The following parameters can sort the results:

        :param str sortby: sorting by grouping (can be accession, name, assays, species, releasedata,
            fgem, raw, atlas)
        :param str sortorder: sorting by orderering. Can be either ascending or descending (default)

        .. doctest::
            :options: +SKIP

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> res = s.queryFiles(keywords="cancer+breast", wholewords=True)
            >>> res = s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens")
            >>> res = s.queryExperiments(array="A-AFFY-33", species="Homo Sapiens", sortorder="releasedate")
            >>> res = s.queryExperiments(array="A-AFFY-33", species="Homo+Sapiens",
            ...     expdesign="dose response", sortby="releasedate", sortorder="ascending")
            >>> dates = [x.findall("releasedate")[0].text for x in res.getchildren()]

        """
        res = self._search("files", **kargs)
        return res

    def queryExperiments(self, **kargs):
        """Retrieve experiments

        .. seealso:: :meth:`~bioservices.arrayexpress.ArrayExpress.queryFiles` for
            all possible keywords

        .. doctest::
            :options: +SKIP

            >>> res = s.queryExperiments(keywords="cancer+breast", wholewords=True)

        """
        res = self._search("experiments", **kargs)
        return res

    def retrieveExperiment(self, experiment):
        """alias to queryExperiments if you know the experiment name


        ::

            >>> s.retrieveExperiment("E-MEXP-31")
            >>> # equivalent to
            >>> s.queryExperiments(accession="E-MEXP-31")


        """
        res = self.queryExperiments(keywords=experiment)
        return res

    def retrieveFile(self, experiment, filename, save=False):
        """Retrieve a specific file from an experiment

        :param str filename:

        ::

            >>> s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")
        """
        frmt = self.format[:]
        self.format = "xml"
        files = self.retrieveFilesFromExperiment(experiment)
        self.format = frmt[:]

        assert filename in files, """Error. Provided filename does not seem to be correct.
            Files available for %s experiment are %s """ % (experiment, files)

        url =  "files/" + experiment + "/" + filename

        if save:
            res = self.http_get(url, frmt="txt")
            f = open(filename,"w")
            f.write(res)
            f.close()
        else:
            res = self.http_get(url, frmt=None)
            return  res

    def retrieveFilesFromExperiment(self, experiment):
        """Given an experiment, returns the list of files found in its description


        :param str experiment: a valid experiment name
        :return: the experiment files

        .. doctest::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress(verbose=False)
            >>> s.retrieveFilesFromExperiment("E-MEXP-31")
            ['E-MEXP-31.raw.1.zip', 'E-MEXP-31.processed.1.zip', 'E-MEXP-31.idf.txt', 'E-MEXP-31.sdrf.txt']


        .. warning:: if format is json, filenames cannot be found so you
            must use format set to xml
        """
        if self.format != "xml":
            frmt = 'xml'
        try:
            res = self.queryExperiments(keywords=experiment)
            exp = res.getchildren()[0]
            files = [x.getchildren() for x in exp.getchildren() if x.tag == "files"]
            output = [x.get("name") for x in files[0]]
            if self.format != 'xml':
                self.format = frmt
        except Exception as err:
            if self.format != 'xml':
                self.format = frmt
            raise Exception(err)
        return output

    def queryAE(self, **kargs):
        """Returns list of experiments

        See :meth:`queryExperiments` for parameters and usage

        This is a wrapper around :meth:`queryExperiments` that returns only
        the accession values.

        ::

            a.queryAE(keywords="pneumonia", species='homo+sapiens')
        """
        frmt = self.format
        self.format = 'json'
        try:
            sets = self.queryExperiments(**kargs)
        except:
            pass
        self.format = frmt
        return [x['accession'] for x in sets['experiments']['experiment']]

    def getAE(self, accession, type='full'):
        """retrieve all files from an experiments and save them locally"""
        filenames = self.retrieveFilesFromExperiment(accession)
        self.info("Found %s files" % len(filenames))
        for i,filename in enumerate(filenames):
            res = self.retrieveFile(accession, filename)
            fh = open(filename, 'w')
            self.info("Downloading %s" % filename)
            fh.write(res)
            fh.close()
