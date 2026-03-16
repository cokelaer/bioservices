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
"""Interface to the ArrayExpress web Service.

.. topic:: What is ArrayExpress ?

    :URL: https://www.ebi.ac.uk/biostudies/arrayexpress
    :REST: https://www.ebi.ac.uk/biostudies/api/v1/search?collection=arrayexpress

    .. highlights::

        ArrayExpress is a database of functional genomics experiments that can be
        queried and the data downloaded. It includes gene expression data from
        microarray and high throughput sequencing studies. Data is collected to
        MIAME and MINSEQE standards. Experiments are submitted directly to
        ArrayExpress or are imported from the NCBI GEO database.

        ArrayExpress data is now hosted on the BioStudies platform at EBI.

        -- ArrayExpress/BioStudies, EBI

"""

from bioservices import logger
from bioservices.services import REST

logger.name = __name__


__all__ = ["ArrayExpress"]


class ArrayExpress:
    """Interface to the `ArrayExpress <https://www.ebi.ac.uk/biostudies/arrayexpress>`_ service.

    ArrayExpress data is now hosted via the BioStudies platform at EBI.
    This class provides access to the ArrayExpress collection using the
    BioStudies REST API.

    **Quick start**::

        >>> from bioservices import ArrayExpress
        >>> s = ArrayExpress()
        >>> results = s.search("breast cancer")
        >>> results["totalHits"]  # total experiments found
        >>> study = s.get_study("E-MEXP-31")
        >>> files = s.get_files("E-MEXP-31")

    You can also search by keyword and retrieve accessions::

        >>> accessions = s.queryAE("pneumonia homo sapiens")

    .. note:: ArrayExpress was migrated from ``http://www.ebi.ac.uk/arrayexpress``
        to the BioStudies platform in 2021. The new API base URL is
        ``https://www.ebi.ac.uk/biostudies``.

    .. seealso:: :meth:`search` for the primary search method.
    """

    _SORT_BY_VALUES = ["relevance", "release_date", "views"]
    _SORT_ORDER_VALUES = ["ascending", "descending"]
    _COLLECTION = "arrayexpress"

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages
        :param bool cache: use HTTP cache

        """
        self.services = REST(
            name="ArrayExpress",
            url="https://www.ebi.ac.uk/biostudies",
            cache=cache,
            verbose=verbose,
        )

    # ------------------------------------------------------------------
    # Primary (new-style) methods
    # ------------------------------------------------------------------

    def search(self, query, page=1, page_size=20, sort_by="relevance", sort_order="descending"):
        """Search ArrayExpress experiments.

        :param str query: Free-text search query. Supports keywords, accession
            numbers, species names, and boolean operators (AND, OR, NOT).
        :param int page: Page number for paginated results (default: 1).
        :param int page_size: Number of results per page (default: 20).
        :param str sort_by: Field to sort by. One of: ``relevance``,
            ``release_date``, ``views`` (default: ``relevance``).
        :param str sort_order: Sort direction. One of: ``ascending``,
            ``descending`` (default: ``descending``).
        :return: dict with keys ``page``, ``pageSize``, ``totalHits``, ``hits``.

        Each entry in ``hits`` contains: ``accession``, ``title``, ``author``,
        ``release_date``, ``files`` (count), ``links`` (count).

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> res = s.search("breast cancer")
            >>> res["totalHits"]  # doctest: +SKIP
            1152
            >>> res["hits"][0]["accession"]  # doctest: +SKIP
            'E-GEOD-17155'
            >>> res2 = s.search("Homo sapiens", sort_by="release_date", sort_order="ascending")

        """
        if sort_by not in self._SORT_BY_VALUES:
            raise ValueError("sort_by must be one of {}".format(self._SORT_BY_VALUES))
        if sort_order not in self._SORT_ORDER_VALUES:
            raise ValueError("sort_order must be one of {}".format(self._SORT_ORDER_VALUES))

        params = {
            "query": query,
            "collection": self._COLLECTION,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self.services.http_get("api/v1/search", frmt="json", params=params)

    def get_study(self, accession):
        """Retrieve full metadata for a specific ArrayExpress study.

        :param str accession: Study accession number (e.g., ``"E-MEXP-31"``).
        :return: dict containing study metadata, sections, and file listings.

        The returned dict has keys ``accno``, ``attributes``, ``section``,
        and ``type``. Files are nested within ``section["subsections"]``.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> study = s.get_study("E-MEXP-31")
            >>> study["accno"]
            'E-MEXP-31'
            >>> # Get the study title
            >>> [a["value"] for a in study["attributes"] if a["name"] == "Title"][0]  # doctest: +SKIP
            'Transcription profiling of mammalian male germ cells...'

        """
        return self.services.http_get("api/v1/studies/{}".format(accession), frmt="json")

    def get_files(self, accession):
        """Retrieve the list of file paths for a specific study.

        :param str accession: Study accession number (e.g., ``"E-MEXP-31"``).
        :return: list of file path strings.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> files = s.get_files("E-MEXP-31")
            >>> "E-MEXP-31.idf.txt" in files  # doctest: +SKIP
            True

        """
        study = self.get_study(accession)
        return self._extract_files(study)

    def retrieve_file(self, accession, filename, save=False):
        """Download a specific file from an ArrayExpress study.

        Files are served via the BioStudies file store (redirecting to the EBI
        FTP). For large files such as ``.zip`` archives the content is returned
        as bytes; plain-text files are returned as strings.

        :param str accession: Study accession number (e.g., ``"E-MEXP-31"``).
        :param str filename: Name of the file to download (e.g., ``"E-MEXP-31.idf.txt"``).
        :param bool save: If ``True``, write the file to disk in the current
            working directory (default: ``False``).
        :return: file content (``str`` or ``bytes``), or ``None`` when *save* is ``True``.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> content = s.retrieve_file("E-MEXP-31", "E-MEXP-31.idf.txt")  # doctest: +SKIP

        """
        available = self.get_files(accession)
        if filename not in available:
            raise ValueError(
                "File '{}' not found for experiment '{}'. Available files: {}".format(filename, accession, available)
            )

        url = "files/{}/{}".format(accession, filename)
        res = self.services.http_get(url, frmt="txt")

        if save:
            mode = "wb" if isinstance(res, bytes) else "w"
            with open(filename, mode) as fout:
                fout.write(res)
            return None
        return res

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_files(self, study):
        """Recursively extract all file paths from a study dict.

        :param dict study: study dict as returned by :meth:`get_study`.
        :return: list of file path strings.
        """
        files = []

        def _recurse(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "file" and "path" in obj:
                    files.append(obj["path"])
                for v in obj.values():
                    _recurse(v)
            elif isinstance(obj, list):
                for item in obj:
                    _recurse(item)

        _recurse(study)
        return files

    def _build_query(self, kargs):
        """Build a search query string from legacy keyword arguments.

        :param dict kargs: keyword arguments as passed to legacy methods.
        :return: tuple (query_str, sort_by, sort_order, page_size).
        """
        valid_keys = {
            "accession",
            "keywords",
            "species",
            "wholewords",
            "expdesign",
            "exptype",
            "gxa",
            "pmid",
            "sa",
            "ef",
            "efv",
            "array",
            "expandfo",
            "directsub",
            "sortby",
            "sortorder",
            "pagesize",
        }
        for k in kargs:
            if k not in valid_keys:
                raise ValueError("Unknown parameter '{}'. Valid parameters are: {}".format(k, sorted(valid_keys)))

        # Map old sortby values to new API values
        sortby_map = {
            "accession": "relevance",
            "name": "relevance",
            "assays": "relevance",
            "species": "relevance",
            "releasedate": "release_date",
            "fgem": "relevance",
            "raw": "relevance",
            "atlas": "relevance",
        }

        sort_by = "relevance"
        sort_order = "descending"
        page_size = 20

        if "sortby" in kargs:
            sort_by = sortby_map.get(kargs["sortby"], "relevance")
        if "sortorder" in kargs:
            sort_order = kargs["sortorder"]
        if "pagesize" in kargs:
            page_size = int(kargs["pagesize"])

        # Build combined query string from search parameters
        query_parts = []
        for key in ("accession", "keywords", "species", "expdesign", "exptype", "pmid", "sa", "ef", "efv", "array"):
            if kargs.get(key):
                # Replace + with space (old API used + as separator)
                query_parts.append(kargs[key].replace("+", " "))

        query = " ".join(query_parts) if query_parts else "*"
        return query, sort_by, sort_order, page_size

    # ------------------------------------------------------------------
    # Backward-compatible methods (legacy names kept for compatibility)
    # ------------------------------------------------------------------

    def queryExperiments(self, **kargs):
        """Search ArrayExpress experiments.

        This method accepts the same keyword arguments as the original
        ArrayExpress v2 API for backward compatibility and maps them to the
        current BioStudies API.

        :param str accession: Experiment accession (e.g., ``"E-MEXP-31"``).
        :param str keywords: Search keywords (e.g., ``"cancer breast"``).
            Separate multiple terms with ``+`` or spaces.
        :param str species: Species filter (e.g., ``"homo sapiens"``).
        :param str expdesign: Experiment design type (e.g., ``"dose response"``).
        :param str exptype: Experiment type (e.g., ``"RNA-seq"``).
        :param str array: Array design accession (e.g., ``"A-AFFY-33"``).
        :param str pmid: PubMed identifier (e.g., ``"16553887"``).
        :param str sa: Sample attribute value (e.g., ``"fibroblast"``).
        :param str ef: Experimental factor name (e.g., ``"CellType"``).
        :param str efv: Experimental factor value (e.g., ``"HeLa"``).
        :param str sortby: Sort field. One of: ``accession``, ``name``,
            ``assays``, ``species``, ``releasedate``, ``fgem``, ``raw``,
            ``atlas``.
        :param str sortorder: Sort direction: ``ascending`` or ``descending``.
        :param int pagesize: Number of results per page (default: 20).
        :return: dict with keys ``page``, ``pageSize``, ``totalHits``, ``hits``.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> res = s.queryExperiments(keywords="breast cancer")  # doctest: +SKIP
            >>> res["totalHits"]  # doctest: +SKIP
            1152
            >>> res = s.queryExperiments(array="A-AFFY-33", species="Homo sapiens")  # doctest: +SKIP
            >>> res = s.queryExperiments(keywords="pneumonia", sortby="releasedate",
            ...                          sortorder="ascending")  # doctest: +SKIP

        .. seealso:: :meth:`search` for the primary search interface.
        """
        query, sort_by, sort_order, page_size = self._build_query(kargs)
        return self.search(query, page_size=page_size, sort_by=sort_by, sort_order=sort_order)

    def queryFiles(self, **kargs):
        """Search ArrayExpress experiments and return results including file counts.

        Accepts the same keyword arguments as :meth:`queryExperiments`.
        Each hit in the result includes a ``files`` field with the file count.
        Use :meth:`get_files` to retrieve the actual file paths for a specific
        experiment.

        :return: dict with keys ``page``, ``pageSize``, ``totalHits``, ``hits``.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> res = s.queryFiles(keywords="breast cancer")  # doctest: +SKIP
            >>> res["hits"][0]["files"]  # number of files in first hit  # doctest: +SKIP
            78

        .. seealso:: :meth:`get_files` to retrieve file paths for a study.
        """
        return self.queryExperiments(**kargs)

    def retrieveExperiment(self, experiment):
        """Retrieve metadata for a specific experiment by accession.

        This is an alias for :meth:`get_study`.

        :param str experiment: Experiment accession (e.g., ``"E-MEXP-31"``).
        :return: dict with full study metadata.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> study = s.retrieveExperiment("E-MEXP-31")  # doctest: +SKIP
            >>> study["accno"]  # doctest: +SKIP
            'E-MEXP-31'

        """
        return self.get_study(experiment)

    def retrieveFilesFromExperiment(self, experiment):
        """Return the list of file paths for a given experiment.

        This is an alias for :meth:`get_files`.

        :param str experiment: Experiment accession (e.g., ``"E-MEXP-31"``).
        :return: list of file path strings.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> files = s.retrieveFilesFromExperiment("E-MEXP-31")  # doctest: +SKIP
            >>> "E-MEXP-31.idf.txt" in files  # doctest: +SKIP
            True

        """
        return self.get_files(experiment)

    def retrieveFile(self, experiment, filename, save=False):
        """Download a specific file from an experiment.

        This is an alias for :meth:`retrieve_file`.

        :param str experiment: Experiment accession (e.g., ``"E-MEXP-31"``).
        :param str filename: Name of the file to download.
        :param bool save: If ``True``, save the file to disk.
        :return: file content as ``str`` or ``bytes``, or ``None`` if *save* is ``True``.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> content = s.retrieveFile("E-MEXP-31", "E-MEXP-31.idf.txt")  # doctest: +SKIP

        """
        return self.retrieve_file(experiment, filename, save=save)

    def queryAE(self, query, **kargs):
        """Search ArrayExpress and return a list of experiment accessions.

        :param str query: Search query (keywords, species, etc.).
        :param kargs: Additional arguments passed to :meth:`search`
            (``page``, ``page_size``, ``sort_by``, ``sort_order``).
        :return: list of accession strings.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> accessions = s.queryAE("pneumonia homo sapiens")  # doctest: +SKIP
            >>> accessions[:3]  # doctest: +SKIP
            ['E-GEOD-12345', 'E-MEXP-67890', 'E-MTAB-11111']

        """
        results = self.search(query, **kargs)
        return [hit["accession"] for hit in results.get("hits", [])]

    def getAE(self, accession):
        """Download all files from an experiment and save them locally.

        :param str accession: Experiment accession (e.g., ``"E-MEXP-31"``).

        Files are written to the current working directory. Binary files
        (e.g., ``.zip``) are written in binary mode; text files in text mode.

        Example::

            >>> from bioservices import ArrayExpress
            >>> s = ArrayExpress()
            >>> s.getAE("E-MEXP-31")  # doctest: +SKIP

        """
        filenames = self.get_files(accession)
        self.services.logging.info("Found %s files" % len(filenames))
        for filename in filenames:
            url = "files/{}/{}".format(accession, filename)
            res = self.services.http_get(url, frmt="txt")
            mode = "wb" if isinstance(res, bytes) else "w"
            with open(filename, mode) as fout:
                self.services.logging.info("Downloading %s" % filename)
                fout.write(res)
