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
"""This module provides a class :class:`~GeneProf`

.. topic:: What is GeneProf ?

    :URL: http://www.geneprof.org
    :REST: http://ww.geneprof.org/GeneProf/api
    :Citations:  Halbritter F, Kousa AI, Tomlinson SR. GeneProf data: a resource
        of curated, integrated and reusable high-throughput genomics experiments.
        Nucleic Acids Research (2013). PubMed ID:
        `24174536 <http://www.ncbi.nlm.nih.gov/pubmed/24174536>`_, Full
        Article @ NAR.


    .. highlights::

        GeneProf is a web-based, graphical software suite that allows users to
        analyse data produced using high-throughput sequencing platforms
        (RNA-seq and ChIP-seq; "Next-Generation Sequencing" or NGS): Next-gen
        analysis for next-gen data!

       -- GeneProf home page, Nov 2013


.. versionadded:: 1.2.0

Data is freely available, under the license terms of each contributing database.

"""
from __future__ import print_function

from bioservices.services import REST, BioServicesError


__all__ = ["GeneProf"]



class GeneProf(REST):
    """Interface to the `GeneProf <http://www.geneprof.org/>`_ service


    Here are some GeneProf terminology used throughout the web service
    interface:

    * Experiments are what GeneProf calls each individual data analysis project.
      An experiment typically consists of a set of input data (e.g. raw
      high-throughput sequencing reads), some experimental sample annotation, an
      analysis workflow and a selection of main outputs. More information here
      in the `Experiments section <http://www.geneprof.org/GeneProf/help_conceptsexplained.jsp#concept:Experiments>`_
    * Datasets, in GeneProf, are collections of data of the
      same type generated as the output of a component of an data analysis
      workflow. There are six generic types of datasets: FILE, SEQUENCES,
      GENOMIC_REGIONS, FEATURES, REFERENCE and SPECIAL.
      More information in `Datasets section
      <http://www.geneprof.org/GeneProf/help_conceptsexplained.jsp#concept:Datasets>`_.


    .. warning:: some of the GeneProf services requires registration.
        More about the API key registration on
        `GeneProf API page <http://www.geneprof.org/GeneProf/webapi.jsp>`_

    .. warning:: there may be a limitation on the number of request per day


    .. versionadded:: 1.2.0
    """

    _valid_format = ["json", "txt", "xml", "rdata"]
    valid_species = ["arabidopsis", "at", "ce", "celegans", "chick", "chicken",
    "danio", "dm", "dmel", "dr", "drosphila", "ef", "fruitfly", "gg", "hs",
    "hsapiens", "human", "mm", "mmusculus", "mouse", "os", "pig", "rat", "rice",
    "rn", "ss", "sscrofa", "tair", "yeast", "zebrafish"]


    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages

        Most of the time, outputs are returned in one of the following format:
        JSON, XML, TXT or RData (R data set). The default within bioservices is
        set to JSON format. You can change the default behaviour by changing the
        attribute :attr:`default_extension`.

        .. doctest::

            >>> from bioservices import GeneProf
            >>> g = GeneProf(verbose=False)
            >>> exp = g.get_list_experiments()

        Some functionalities expect the ID of a GeneProf reference dataset as
        one input parameter (e.g., pub_hs_ens59_grch37) but aliases are
        available. The list of species alias is available in the
        :attr:`valid_species` attribute.

        """
        super(GeneProf, self).__init__(name="GeneProf",
                url="http://www.geneprof.org/GeneProf/api", verbose=verbose)

        self.TIMEOUT = 100

        # why is it set to False ?
        self.easyXMLConversion = False
        self._default_extension = "json"

        # buffering the ids for the experiments and datasets
        self._ids_exp = None
        self._rigid_ids_exp = None
        self._ids_ds = None
        self._rigid_ids_ds = None

    # just a get/set to the default extension
    def _set_default_ext(self, ext):
        self.devtools.check_param_in_list(ext, ["json","xml", "txt", "rdata"])
        self._default_extension = ext
    def _get_default_ext(self):
        return self._default_extension
    default_extension = property(_get_default_ext, _set_default_ext,
             doc="""set extension of the requests (default is json). Can be
                'json' or 'xml', 'txt', 'rdata'.""")

    # buffering the ids from the experiments
    def _get_ids_exp(self):
        if self._ids_exp is None:
            self.logging.info("Fetchin ids...")
            res = self.get_list_experiments(frmt="json")
            self._ids_exp = [x['id'] for x in res]
            self._rigid_ids_exp = [x['rigid_id'] for x in res]
        return self._ids_exp
    ids_exp = property(_get_ids_exp)

    def _get_rigid_ids_exp(self):
        if self._rigid_ids_exp is None:
            self.logging.info("Fetchin ids...")
            res = self.get_list_experiments(frmt="json")
            self._rigid_ids_exp = [x['rigid_id'] for x in res]
            self._ids_exp = [x['id'] for x in res]
        return self._rigid_ids_exp
    rigid_ids_exp = property(_get_rigid_ids_exp)

    # buffering the ids from the datasets
    def _get_ids_ds(self):
        if self._ids_ds is None:
            self.logging.info("Fetchin ids...")
            res = self.get_list_reference_datasets(frmt="json")
            self._ids_ds = [x['id'] for x in res]
        return self._ids_ds
    ids_ds = property(_get_ids_ds)


    def get_list_experiments(self, frmt="json", **kargs):
        """Retrieves a list of GeneProf experiments.

        :param str frmt: format of the output
        :param bool with-ats: Include descriptions for all datasets'
            annotation types (data columns).
        :param bool with-samples: Include information about the sample
            annotation per experiment.
        :param bool with-inputs: Include a listing of all input datasets per
            experiment.
        :param bool with-outputs: Include a listing of the main output datasets
            per  experiment.
        :param bool with-workflow: Include the analysis workflow per experiment.
        :param bool with-all-data: Include ALL datasets linked with the
            experiment (large response!)
        :param bool only-user-experiments:  List only experiments owned by the
            user identified by the WebAPI key.
        :param bool key:  An optional WebAPI key, required to access
            non-public data.

        :return: if json format is requested, the output is a list of
            dictionaries. Each dictionary corresponds to one experiment.

        .. doctest::

            from bioservices import GeneProf
            g = GeneProf(verbose=False)
            experiments = g.get_list_experiments(with_outputs=True)

        """
        frmt = self._check_format(frmt)
        params = {}
        for key in kargs.keys():
            if key not in ["with_ats", "with_samples", "with_inputs",
                    "with_outputs", "with_workflow", "with_all_data",
                    "only_user_experiments", "key"]:
                raise BioServicesError("invalid parameter (%s) provided" % key)
            params[key] = kargs.get(key)

        params = self._clean_parameters(params)

        res =self.http_get("exp/list." + frmt, frmt=frmt, params=params)
        if frmt == "json":
            try:
                res = res['experiments']
            except:
                pass
        return res

    def _check_format(self, frmt):
        if frmt is None:
            frmt_ = self.default_extension
        self.devtools.check_param_in_list(frmt, self._valid_format)
        return frmt

    def _check_id(self, Id):
        try:
            Id = int(Id)
        except:
            pass
        if Id not in self.ids_exp and Id not in self.rigid_ids_exp:
            raise BioServicesError("Incorrect ids provides. See ids and rigid_ids attributes.")

    def _check_reference(self, ref):
        if ref not in self.valid_species:
            raise BioServicesError("Incorrect reference. check attribute :attr:`valid_species`.")

    def _check_kargs(self, kargs, valid_keys):
        for key in kargs.keys():
            if key not in valid_keys:
                raise BioServicesError("invalid parameter (%s) provided" % key)

    def _clean_parameters(self, params):
        # some parametesr in geneprof have dash character, which
        # cannot be usd in python so we use underscore. Consequently,
        # we must revert to a dash when encoding the URL
        for k,v in params.items():
            if "with_" in k:
                params[k.replace("with_", "with-")]=v
                del params[k]
        return params

    def get_metadata_experiment(self, Id, frmt="json", **kargs):
        """Retrieves metadata (names, descriptions, IDs, etc) about experiments.

        An experiment typically consists of a set of input data (e.g. raw
        high-throughput sequencing reads), some experimental sample
        annotation, an analysis workflow and a selection of main outputs.

        :param str Id: accession ID (a string of the form gpXP_XXXXXX or a
            numeric part (e.g., 3)).

        Other parameters like in :meth:`get_list_experiments` are also available
        :return: dictionary with metadata

        Retrieve basic metadata about experiment gpXP_000385 including
        workflow::

            >>> g.get_metadata_experiment(Id="385", with_workflow=True)

        """
        frmt = self._check_format(frmt)
        self._check_id(Id)
        self._check_kargs(kargs, ["with_ats", "with_samples", "with_inputs",
                    "with_outputs", "with_workflow", "with_all_data", "key"])
        params = self._clean_parameters(kargs)
        #    params = params.replace("only_user_ex", "only-user-ex")
        res = self.http_get('exp/%s.' %Id+frmt, frmt=frmt, params=params)
        return res

    def get_metadata_dataset(self, Id, frmt="json", **kargs):
        """Get metadata about geneprof dataset

        This method retrieves metadata about a specific GeneProf dataset
        given the dataset's accession ID (a string of the form
        gpDS_XXX_XXX_XXX_XXX).

        :param str Id: The identifier of the dataset of interest. Either the
            entire accession ID (e.g. gpDS_11_385_44_1) or just the
            dataset-specific part (e.g. 11_385_44_1).
        :param str frmt: one of json, xml, txt, rdata

        Retrieve metadata about the dataset gpDS_11_12_122_1 as JSON::

            g.get_metadata_dataset("11_12_122_1", with_ats=True)

        """
        frmt = self._check_format(frmt)
        self._check_kargs(kargs, ["with_ats", "key"])
        params = self._clean_parameters(kargs)
        res = self.http_get("ds/%s." % Id + frmt, frmt=frmt)
        return res

    def get_list_reference_datasets(self, frmt="json"):
        """Retrieves a list of public reference datasets.

        GeneProf provides a number of recommended reference datasets
        for several organisms (human, mouse, etc.). These reference datasets
        provide genomic sequence assemblies and genic annotations that serve
        as a scaffold for GeneProf's analyses, so most of GeneProf's datasets
        are based on one of these reference datasets. This web service simply
        retrieves a list of all the public, recommended reference datasets
        currently available in the database.

        :param str frmt: format in one of: json, xml, txt, rdata.

        .. note:: the txt and rdata format versions of the output reports a
            flattened version of the dataset metadata and misses out some
            information available in the other formats!

        Retrieve a list of all reference datasets as JSON::

            >>> g.get_list_reference_datasets()

        """
        frmt = self._check_format(frmt)
        url = "ds/pubref." + frmt
        res = self.http_get(url, frmt=frmt)
        #if frmt == "json":
        #    res = res['references']
        return res

    def get_list_experiment_samples(self, ref, frmt="json"):
        """Returns list of Public Experiment Samples for a reference dataset.

        All public data in the GeneProf databases has been annotated
        with the biological sample of origin, described in terms of
        cell type, tissue, treatment, and so on. This web service simply
        retrieves a list of all the public sample annotations in the database
        for a specific reference dataset (see the List Public Reference
        Datasets service).


        :param str ref: identifier of a public GeneProf reference dataset.
            you may use aliases here. Check the list public references
            service for all available reference datasets.
        :param str format: The file format requests, one of: json, xml, txt, rdata.

        Retrieve a list of all samples for mouse as XML::

            >>> g.get_list_experiment_samples("mouse")
            >>> g.get_list_experiment_samples("human", frmt="txt")
            >>> g.get_list_experiment_samples("human", frmt="rdata")

        """
        frmt = self._check_format(frmt)
        url = "gene.info/list.samples/%s." % ref + frmt
        res = self.http_get(url, frmt=frmt)
        #if frmt == "json":
        #    res = res['samples']
        return res

    def search_genes(self, query, taxons=None, frmt="json"):
        """Search genes using genes' description, name and accession IDs.

         use sets of gene annotations
         based on those from Ensembl. You can search for
         genes of interest using arbitrarily complex search queries against the
         names and identifiers (from Ensembl, RefSeq and more) of those genes.
         The search results are categorised by the reference dataset the genes
         belong to (also see the List Public Reference Datasets service).

        :param str query: The search term to look for, e.g. a gene name or paper
             title. You can narrow down the fields to be search by prefixing the
             query with a field name. Valid fields for genes are: Valid search
             fields are: id, label, description, type and reference. You can
             also use boolean logic in your queries using the keywords AND and
             OR, brackets and quotes (") for exact matches of whole phrases.
        :param str frmt: file format requests, one of: json, xml, txt, rdata.
        :param str taxons: Only return matches from experiments
                     dealing with organisms matching these NCBI taxonomy IDs
                     (comma-separated list).


        (1) Search for all genes matching the query 'sox2' (in json
            format), (2) same  but only in human (taxon 9606) (3) same bu only
            in human and 10090 (4)  query "brca2 AND cancer AND reference" in
            mouse

        >>> g.search_genes("sox2")['total_results']
        8
        >>> g.search_genes("sox2", taxons="9606")['total_results']
        2
        >>> g.search_genes("sox2", taxons="9606, 10090")['total_results']
        3
        >>> res = g.search_genes("brca2 AND cancer AND reference", taxons="mouse")


        XML output example::

        >>> g.search_genes("sox2", taxons="9606", frmt="xml")
        >>> geneIds = [x.find('numeric_id').text for x in res.findAll("genes")]

        >>> g.search_genes("sox2", taxons="9606")
        >>> geneIds = [x["numeric_id"] for x in res[0]['genes']]


        .. seealso:: search_gene_ids
        """
        frmt = self._check_format(frmt)
        query = query.replace(" ", "+")
        url = "search/gene/%s." % query + frmt
        params = {'taxons': taxons}
        res = self.http_get(url, frmt=frmt, params=params)
        #if frmt == "json":
        #    res = res['matches_per_dataset']
        return res

    def search_gene_ids(self, query, taxons):
        """This is an alias to :meth:`search_genes` to retrieve Ids

        geneIds = g.seqrch_gene_ids("nanog", "mouse")
        """
        results = self.search_genes(query, taxons)
        geneIds = {}
        for res in results:
            ids = [x["numeric_id"] for x in res['genes']]
            taxon = res["reference"]["taxon"]
            geneIds[taxon] = ids
        return geneIds

    def search_experiments(self, query, taxons=None, frmt="json"):
        """Search Experiments using  name, description and citations.

        Experiments are what GeneProf calls each individual data  analysis
        project. An experiment typically consists of a set of input data (e.g.
        raw high-throughput sequencing reads), some experimental sample
        annotation, an analysis workflow and a selection of main outputs. Please
        check the manual for further information about experiments. Using this
        web service, you can search for experiments of interest using
        arbitrarily complex search queries against the names, descriptions,
        linked citations, linked reference dataset, and so on of those
        experiments. The search results are categorised by the reference dataset
        the experiments belong to (also see the List Public Reference Datasets
        service).

        :param str query: The search term to look for, e.g. a gene name or paper
            title. You can narrow down the fields to be search by prefixing the
            query with a field name. Valid fields for experiments are: Valid
            search fields are: id, label, description, type, reference, user,
            dataset, citation, platform and sample. You can also use boolean
            logic in your queries using the keywords AND and OR, brackets and
            quotes (") for exact matches of whole phrases. Advanced search
            options and examples are documents on GeneProf's search
            page.
        :param str frmt: The file format requests, one of: json, xml, txt, rdata.
        :param str taxons: Only return matches from experiments dealing with
            organisms matching these NCBI taxonomy IDs (comma-separated list).

        Search for experiments mentioning 'sox2' anywhere (in XML format)::

            >>> g.search_experiments("sox2")

        Search for experiments mentioning 'cancer' in their description (in JSON
            format):

            >>> g.search_experiments("citation:cancer")

        Search for experiments mentioning 'cell stem cell' in a linked citation (in
        plain text format):

            >>> g.search_experiments("citation:'stem cell'")

        """
        frmt = self._check_format(frmt)
        query = query.replace(" ", "+")
        url = "search/experiment/%s." % query + frmt
        params = {}
        if taxons:
            params['taxons'] = taxons
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def search_datasets(self, query, taxons=None, frmt="json"):
        """search for datasets

        Using this web service, you can search for experiments of interest
        using arbitrarily complex search queries against the names and types
        of these datasets.

        :param str query: The search term to look for, e.g. a gene name
            or cell type. You can narrow down the fields to be search by
            prefixing the query with a field name. Valid fields for samples
            are: id, label, description, datatype, user, experiment .You can
            also use boolean logic in your queries using the keywords AND
            and OR, brackets and quotes (") for exact matches of whole phrases.
            Advanced search options and examples are documents on GeneProf's
            search page.
        :param str frmt: file format in: json, xml, txt, rdata.
        :param str taxons: Only return matches from experiments dealing
             with organisms matching these NCBI taxonomy IDs (comma-separated
             list).

         Search for datasets mentioning 'sox2'::

             >>> g.search_datasets('sox2')

         Search for datasets mentioning 'gene expression':

            >>> g.search_datasets('gene expression')

        Search for genomic data for 'sox2' in plain text format:

            >>> g.search_datasets("datatype:GENOMIC_REGIONS AND sox2")

        """
        frmt = self._check_format(frmt)
        query = query.replace(" ", "+")
        url = "search/dataset/%s." % query + frmt
        params = {}
        if taxons:
            params['taxons'] = taxons
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def search_samples(self, query, taxons=None, frmt="json"):
        """search for public experiment samples using search terms against their annotations.


        All public data in the GeneProf databases has been
        annotated with the biological sample of origin, described in terms of
        cell type, tissue, treatment, and so on. Using this web service, you can
        search for samples of interest using arbitrarily complex search queries
        against the annotations of these samples.

        :param str query: search term to look for, e.g. a gene name or cell type.
            You can narrow down the fields to be search by prefixing the
            query with a field name. Valid fields for samples are: Valid
            search fields are: id, label, description , Age, Antibody,
            Cell_Line, Cell_Type, Description, Developmental_Stage, Gender,
            Gene, Label, Organism, Platform, Sample_Group, SRA_Accession,
            Strain, Time, Tissue, Treatment. You can also use boolean logic
            in your queries using the keywords AND and OR, brackets and
            quotes (") for exact matches of whole phrases. Advanced
            search options and examples are documents on GeneProf's search
            page.
        :param bool frmt: file format requests, one of: json, xml, txt, rdata.
        :param str taxons: Only return matches from experiments dealing with
            organisms matching these NCBI taxonomy IDs (comma-separated list).

        Search for samples annotated 'ChIP' in any of the default search fields
        (in XML format):

            >>> g.search_samples("ChIP")

        Search for samples annotated with the gene 'sox2':

            >>> g.search_samples("Gene:sox2")

        Search for samples annotated 'human' in any of the default search fields
        in plain text format:

            >>> g.search_samples("human")

        """
        frmt = self._check_format(frmt)
        query = query.replace(" ", "+")
        url = "search/sample/%s." % query + frmt
        params = {}
        if taxons:
            params['taxons'] = taxons
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_gene_id(self, ref, idtype, Id, frmt="json"):
        """Get the GeneProf ID of a Gene

        GeneProf uses well-defined sets of gene annotations
        based on those from `Ensembl <http://www.ensembl.org/>`_. you can get
        the :meth:`get_gene_id` of any gene in the reference annotation by
        matching it against an external name (official gene symbol) or one of
        the supported accession ID types (e.g. Ensembl Gene IDs, RefSeq IDs,
        etc. -- use the :meth:`get_list_idtypes` to find out which types
        are supported for a dataset).

        :param str ref: The identifier of a public GeneProf reference
            dataset. You may use aliases here. Check the list public
            references service for all available reference datasets.
        :param str idtype: The identifier of an annotation column storing IDs or
            the term any to use any available identifier type. Use
            :meth:`get_list_idtypes` to find out which types are supported for a
            dataset.
        :param str Id: The GeneProf ID of a gene (an integer number).
        :param str frmt: output format in json, txt, xml, rdata.

        Get the GeneProf ID of the mouse gene with Ensembl ID ENSMUSG00000059552

            >>> g.get_gene_id("mouse", "C_ENSG", "ENSMUSG00000059552")


        Get the GeneProf IDs of all human genes with RefSeq ID NM_005657,
        as JSON::

            >>> g.get_gene_id("human", "C_RSEQ", "NM_005657")

        Get the GeneProf IDs of all human genes with any ID matching
        "NM_005657" (should, in this case, be same as the previous query)::

            >>> g.get_gene_id("human", "any", "NM_005657")
        """
        frmt = self._check_format(frmt)
        url = "gene.info/gp.id/%s/%s/%s." % (ref, idtype, Id)
        url += frmt
        res = self.http_get(url, frmt=frmt)
        return res


    def get_external_gene_id(self, ref, idtype, Id, frmt="json"):
        """Translates a GeneProf gene ID into an external identifier or name.

        GeneProf uses sets of gene annotations based on those from Ensembl.
        With this method, you can look up an external name (official gene
        symbol) or one of the supported accession ID types (e.g. Ensembl
        Gene IDs, RefSeq IDs, etc. -- use the :meth:`get_list_idtypes` service
        to find out which types are supported for a dataset) for any given
        internal GeneProf gene ID.

        :param str Id:   The GeneProf ID of a gene (an integer number).
        :param str ref:  The identifier of a public GeneProf reference
            dataset. You may use aliases here. Check the
            :meth:`get_list_reference_datasets`
            service for all  available reference datasets.
        :param str idtype:   The identifier an annotation column storing
            IDs. Check the :meth:`get_list_idtypes` to find out which types
            are supported for a  dataset.
        :param str frmt:  format requests, one of: json, txt, xml, rdata.

        Get the Ensembl Gene ID(s) of the mouse gene #715, as plain text:

             >>> g.get_external_gene_id("mouse","715", "C_ENSG")

         Get the RefSeq ID(s) of the human gene #2981, as JSON:

             >>> g.get_external_gene_id("mouse","2981", "C_RSEQ")

         Get the name(s) of the human gene #2981, as XML:

             >>> g.get_external_gene_id("mouse","2981", "C_NAME")
        """
        frmt = self._check_format(frmt)
        url = "gene.info/external.id/%s/%s/%s." % (ref, idtype, Id)
        url += frmt
        res = self.http_get(url, frmt=frmt)
        return res

    def get_list_idtypes(self, ref, frmt="json"):
        """list all the ID types available for a dataset.

        GeneProf reference datasets provide a number of alternative ID annotations (e.g.
        Ensembl Gene IDs, RefSeq IDs, UniGene IDs, etc.) for each of the genes
        in the reference annotation. This service simply lists all the ID types
        available for a dataset.

        :param str ref: identifier of a public GeneProf reference dataset (e.g.
            human)
        :param str frmt: format, one of: json, txt, xml, rdata.


        ::

            >>> g.get_list_idtypes("mouse")
            >>> g.get_list_idtypes("human")

        """
        frmt = self._check_format(frmt)
        url = "gene.info/list.id.types/%s." % ref
        url += frmt
        res = self.http_get(url, frmt=frmt)
        return res

    def get_expression(self, ref, Id, frmt="json", with_sample_info=False,
            output="RPKM"):
        """Alias to :meth:`get_gene_expression`




        """
        return self.get_gene_expression(ref, Id, frmt=frmt,
                with_sample_info=with_sample_info, output=output)


    def get_gene_expression(self, ref, Id, frmt="json",
            with_sample_info=False,  output="RPKM"):
        """Get Gene Expression Values for a Gene

        Retrieves gene expression values for a gene based on public RNA-seq data
        in the GeneProf databases.

        GeneProf's databases contain many
        pre-calculated gene expression values stemming from a reanalyses of a
        large collection of RNA-seq (and similar) experiments. Use this web
        service to retrieve all the expression values for a single gene of
        interest by giving the name of the **reference** dataset the gene
        belongs to and its internal GeneProf gene **Id** -- use the
        :meth:`get_list_reference_datasets`, :meth:`get_gene_id`  and/or
        :meth:`search_genes` methods to look up these identifiers. You may
        retrieve the values either as raw read counts (the
        total number of short reads that were aligned to the gene's locus), RPM
        (reads per million -- the raw counts rescaled to account for differences
        in library size) or RPKM (reads per kilobase million -- like RPM, but
        also accounting for transcript length bias). All gene expression values
        have been calculated using the
        `Calculate Gene Expression module
        <http://www.geneprof.org/GeneProf/help_modules.jsp#module:org.stembio.geneprof.workflow.module.rna.CalculateGeneExpression>`_.
        Full details for the analysis pipeline that was used to calculate each
        value are available from the individual experiments the values come
        from (the JSON and XML output contain a link to the experiment of
        origin).

        :param str Id: GeneProf ID of a gene (an integer number).
        :param str ref: identifier of a public GeneProf reference dataset. You
            may use aliases here. Check the list public references service for
            all available reference datasets.
        :param str frmt: format requests, one of: json, txt, xml, rdata.
        :param str type: type of values to obtain, one of: RAW | RPM | RPKM
        :param str with_sample_info: Include additional annotations about the
            tissue, cell type, etc. of the expression values.

        Retrieve gene expression values for the mouse gene #715, including additional annotation data:

            >>> g.get_gene_expression("mouse", "715", with_sample_info=True)

        Retrieve raw read count values for the mouse gene #715

            >>> g.get_gene_expression("mouse", "715", type="RAW")

        Retrieve gene expression values for the mouse gene #715 as a tab-delimited text file, including additional annotation data:

            >>> g.get_gene_expression("mouse", "715", frmt="txt", with_sample_info=True)

        Retrieve gene expression values for the mouse gene #715 as an
        RData file, including additional annotation data:

            >>> g.get_gene_expression("mouse", "715", frmt="rdata", with_sample_info=True)


        .. plot::
            :include-source:
            :width: 80%

            >>> from bioservices import GeneProf
            >>> import math
            >>> from pylab import hist, title, xlabel, clf, show, ylabel
            >>> g = GeneProf()
            >>> res = g.get_gene_expression("mouse", "715")
            >>> rpkmValues = [x["RPKM"] for x in res]
            >>> logValues = [math.log(x+1,2.) for x in rpkmValues]
            >>> hist(logValues)
            >>> xlabel('RPKM'); ylabel('Count')
            >>> title( 'Histogram: 715')
            >>> show()

        """
        frmt = self._check_format(frmt)
        self.devtools.check_param_in_list(output, ["RAW", "RPM", "RPKM"])

        url = "gene.info/expression/%s/%s." % (ref, Id)
        url += frmt

        #TODO: params
        params = {}
        params['with-sample-info'] = with_sample_info
        params['type'] = output

        res = self.http_get(url, frmt=frmt, params=params)

        #if frmt == "json":
        #    res = res['values']
        return res

    def get_targets_tf(self,ref,Id,frmt="json", ats="C_NAME",
            include_unbound=False):
        """Retrieve putative target genes for a transcription factor

        Retrieve putative target genes for a transcription factor
        (or other transcriptional regulator) based on public
        ChIP-seq data in the GeneProf databases by querying for the
        targets discovered in all available ChIP-seq experiments
        (identified by the ID of a gene).

        GeneProf's databases contain lots of information about putative
        gene regulatory interactions from a reanalyses of a large
        collection of ChIP-seq experiments.

        Give the name of the reference
        dataset the TF gene belongs to and its internal GeneProf gene ID -- use
        the :meth:`get_list_reference_datasets`, :meth:`get_gene_id` or
        :meth:`search_genes` or :meth:`get_gene_id` methods to look up these
        identifiers. The assignment of putative
        target genes to TFs has been done by calling enriched binding peaks on
        the aligned ChIP-seq reads using MACS and subsequently assigning the
        peaks to target genes if they were within a permissible window of the
        transcription start site (as by current wizard default: 20kb up- and
        1kb down-stream of the TSS; in an upcoming release of the web service,
        you will be able to redefine these threshold dynamically, so watch this
        space!). The GeneProf workflow modules corresponding to these two steps
        are documented in `Find Peaks with MACS
        <http://www.geneprof.org/GeneProf/help_modules.jsp#module:org.stembio.geneprof.workflow.module.chipseq.MACS14withFDRFilter>`_
        and `Map Regions to Genes
        <http://www.geneprof.org/GeneProf/help_modules.jsp#module:org.stembio.geneprof.workflow.module.chipseq.MapRegionsToGenes>`_.
        Full details for the analysis pipeline that was used to calculate each
        value are available from the individual experiments the values come
        from (the JSON and XML output contain a link to the experiment of
        origin). For some TFs there might be more than one dataset available,
        in which case the output returned by the web service will contain the
        status in all availabledatasets (distinguished by the experimental
        sample they belong to, see :meth:`get_list_experiment_samples`.

        :param str Id: The GeneProf ID of a gene/feature (an integer number).
        :param str ref: identifier of a public GeneProf reference dataset.
            Check the list public references service for all available reference
            datasets.
        :param str frmt: format requests, one of: json, txt, xml, rdata.
        :param str ats: (default C_NAME)  A selection of column IDs (from the
            reference) to be included in the output.
        :param bool include_unbound: include not only putative target genes in
           the output, but also those genes that show now evidence of regulation.


        Get all the putative targets of the mouse TF Smad1 in JSON format::

            >>> g.get_targets_tf("mouse", "9885")

        Get all the putative targets of the human TF MEIS1, also include
        unbound genes for comparison::

            >>> g.get_targets_tf("human", "36958", include_unbound=True)

        Get all the putative targets of the mouse TF Nanog as
        include a column for gene name and Ensembl ID (there are TWO ChIP-seq
        datasets available for this TF!)::

            >>> g.get_targets_tf("mouse", "14899", ats="C_NAME,C_ENSG")

        Get all the putative targets of the human TF MEIS1 as an RData file::

            >>> g.get_targets_tf("human", "36958", frmt="rdata")


        """
        frmt = self._check_format(frmt)
        url =  "gene.info/regulation/binary/by.gene/%s/%s." % (ref, Id)
        url += frmt
        params = {}
        params['ats'] = ats
        params['include-unbound'] = include_unbound

        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_targets_by_experiment_sample(self, ref, Id, frmt="json",
            ats="C_NAME", include_unbound=False):
        """Get Targets by Experiment Sample

        Retrieve putative target genes for a transcription factor (or other
        transcriptional regulator) based on public ChIP-seq data in the GeneProf
        databases by querying for the targets discovered in a specific ChIP-seq
        experiment (identified by the ID of a public sample).

        GeneProf's databases contain lots of information about putative gene
        regulatory interactions from a reanalyses of a large collection of
        ChIP-seq experiments. You use this web service to retrieve a list of
        putative target genes for a transcription factor (TF) or other
        DNA-binding protein (incl. histone modifications), by giving the
        identifier of a public GeneProf sample -- use the
        :meth:`get_list_experiment_samples` or
        the :meth:`search_samples` method to look up these identifiers. The
        assignment of putative target genes to TFs has been done by calling
        enriched binding peaks on the aligned ChIP-seq reads using MACS and
        subsequently assigning the peaks to target genes if they were within a
        permissible window of the transcription start site (as by current wizard
        default: 20kb up- and 1kb down-stream of the TSS; in an upcoming release
        of the web service, you will be able to redefine these threshold
        dynamically, so watch this space!). The GeneProf workflow modules
        corresponding to these two steps are documented here: Find Peaks with
        MACS and Map Regions to Genes. Full details for the analysis pipeline
        that was used to calculate each value are available from the individual
        experiments the values come from (the JSON and XML output contain a link
        to the experiment of origin).

        :param str Id: the GeneProf ID of a public sample (an integer number).
        :param str ref: The identifier of a public GeneProf reference dataset.
            You may use aliases here. Check the list public references service
            for all available reference datasets.
        :param str frmt: format requests, one of: json, txt, xml, rdata.
        :param str ats: (default C_NAME)  A selection of column IDs (from the
            reference) to be included in the output.
        :param bool include_unbound: default False. Include not only putative
            target genes in the output, but also those genes that show now
            evidence of regulation.

        Get all the putative targets of the mouse TF Smad1 in JSON format::

            >>> g.get_targets_by_experiment_sample("mouse", "541")

        Get all the putative targets of the human TF MEIS1 in XML
        format, also include unbound genes for comparison::

            >>> g.get_targets_by_experiment_sample("human", "784", include_unbound=True)

        Get all the putative targets of the mouse TF Smad1 as
        tab-delimited text and include a column for gene name and
        Ensembl ID::

            >>> g.get_targets_by_experiment_sample("mouse", "541", ats="C_NAME,C_ENSG")

        Get all the putative targets of the human TF MEIS1 as an RData file::

            >>> g.get_targets_by_experiment_sample("human", "784", frmt="rdata")


        """
        frmt = self._check_format(frmt)
        url = "gene.info/regulation/binary/by.sample/%s/%s." % (ref, Id)
        url += frmt
        params = {}
        params['ats'] = ats
        params['include-unbound'] = include_unbound
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_tfas_by_gene(self, ref, Id, frmt="json", ats="C_NAME",
            include_unbound=False):
        """Get TFAS of a Transcription Factor

        Retrieve transcription factor association strength (TFAS)
        scores for a transcription factor (or other
        transcriptional regulator) based on public ChIP-seq data in the GeneProf
        databases by querying for the data in all available ChIP-seq experiments
        (identified by the ID of a gene).

        Full description:   GeneProf's databases contain lots of information
        about putative gene regulatory interactions from a reanalyses of a large
        collection of ChIP-seq experiments. You use this web service to retrieve
        a list of TFAS scores for a transcription factor (TF) or other
        DNA-binding protein, by giving the name of the reference dataset the TF
        gene belongs to and its internal GeneProf gene ID -- use the list
        reference datasets, get GeneProf ID and/or search genes services to look
        up these identifiers. 'TFAS' (= transcription factor association
        strength) scores are continuous values that give an indication of how
        strongly a transcription factor (or other DNA-binding protein) is
        associated with a target gene. The TFAS is calculated as a function of
        the intensity and the distance of all binding sites (ChIP-seq peaks)
        near a gene, for details, please refer to the publication by Ouyang et
        al. (PubMed: 19995984). We use as an intensity score the fold-change
        enrichment of the ChIP-seq signal over the control background as
        calculated by MACS in conjunction with calling peaks for the input
        ChIP-seq data. The GeneProf workflow modules corresponding to these two
        steps are documented here: Find Peaks with MACS and Calculate TFAS. Full
        details for the analysis pipeline that was used to calculate each value
        are available from the individual experiments the values come from (the
        JSON and XML output contain a link to the experiment of origin). For
        some TFs there might be more than one dataset available, in which case
        the output returned by the web service will contain the status in all
        available datasets (distinguished by the experimental sample they belong
        to, see list public samples service).

        :param str Id:  The GeneProf ID of a gene/feature (an integer number).
        :param str Ref: The identifier of a public GeneProf reference dataset.
            You may use aliases here. Check the list public references service
            for all available reference datasets.
        :param str frmt: format requests, one of: json, txt, xml, rdata.
        :param str ats: (default C_NAME) a selection of column IDs (from
            the reference) to be included in the output.

        Get all TFAS scores for the mouse TF Smad1 in JSON format:

            >>> g.get_tfas_by_gene("mouse", "9885")

        Get all TFAS scores for the human TF MEIS1 in XML format, also include
        unbound genes for comparison:

            >>> g.get_tfas_by_gene("human", "36958", frmt="xml",
                    include_unbound=True)

        Get all TFAS scores the mouse TF Nanog as tab-delimited text and include
        a column for gene name and Ensembl ID (there are TWO ChIP-seq datasets
        available for this TF!):

            >>> g.get_tfas_by_gene("mouse", "14899", frmt="txt",
                    ats="C_NAME,C_ENSG")

        Get all TFAS scores for the human TF MEIS1 as an RData file:

            >>> g.get_tfas_by_gene("human", "36958", frmt="rdata")

        """
        frmt = self._check_format(frmt)
        url = "gene.info/regulation/tfas/by.gene/%s/%s." % (ref, Id)
        url += frmt
        params = {}
        params['ats'] = ats
        params['include-unbound'] = include_unbound
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_tfas_by_sample(self, ref, Id, frmt="json", ats="C_NAME",
            include_unbound=False):
        """Get TFAS by Experiment Sample

        Retrieve a list of TFAS scores for a transcription factor (TF) or
        other DNA-binding protein, by giving the identifier of a public GeneProf
        sample -- use the list public samples or the :meth:`search_samples`
        to look up these identifiers. TFAS (transcription factor association
        strength) scores are continuous values that give an indication of how
        strongly a transcription factor (or other DNA-binding protein) is
        associated with a target gene. The TFAS is calculated as a function of
        the intensity and the distance of all binding sites (ChIP-seq peaks)
        near a gene, for details, please refer to the publication by Ouyang et
        al. (PubMed: 19995984). We use as an intensity score the fold-change
        enrichment of the ChIP-seq signal over the control background as
        calculated by MACS in conjunction with calling peaks for the input
        ChIP-seq data. The GeneProf workflow modules corresponding to these two
        steps are documented here: Find Peaks with MACS and Calculate TFAS. Full
        details for the analysis pipeline that was used to calculate each value
        are available from the individual experiments the values come from (the
        JSON and XML output contain a link to the experiment of origin).

        :param str Id: The GeneProf ID of a public sample (an integer number).
        :param str ref: identifier of a public GeneProf reference dataset.
            You may use aliases here. Check the list public references service
            for all available reference datasets.
        :param str frmt: format requests, one of: json, txt, xml, rdata.
        :param str ats: (default C_NAME) a selection of column IDs (from the
            reference) to be included in the output.

        Get TFAS scores for the mouse TF Smad1 in JSON format:

            >>> g.get_tfas_by_sample("mouse", 541)

        Get TFAS scores for the human TF MEIS1 in XML format, also include
        unbound genes for comparison:

            >>> g.get_tfas_by_sample("human", "784", frmt="xml",
                    >>> include_unbound=True)

        Get TFAS scores for the mouse TF Smad1 as tab-delimited text and include
        a column for gene name and Ensembl ID:

            >>> g.get_tfas_by_sample("mouse", "541", frmt="txt",
                ats="C_NAME,C_ENSG")

        Get TFAS scores for the human TF MEIS1 as an RData file:

            >>> g.get_tfas_by_sample("human", "784")

        """
        frmt = self._check_format(frmt)
        url = "gene.info/regulation/tfas/by.sample/%s/%s." % (ref, Id)
        url += frmt
        params = {}
        params['ats'] = ats
        params['include-unbound'] = include_unbound
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_tf_by_target_gene(self, ref, Id, frmt="json", ats="C_NAME",
            with_sample_info=False):
        """Get Transcription Factors by Target Gene

        Retrieve transcription factors (and other regulatory inputs) putatively
        targeting a specific gene, based on public ChIP-seq data in the GeneProf
        databases.

        GeneProf's databases contain lots of information about putative gene
        regulatory interactions from a reanalyses of a large collection of
        ChIP-seq experiments. You use this web service to retrieve a list of
        transcription factors and other DNA-binding proteins that might possible
        be regulating a gene of interest, by giving the name of the reference
        dataset the gene belongs to and its internal GeneProf gene ID -- use the
        :meth:`get_list_reference_datasets`, :meth:`get_gene_id` or
        :meth:`search_genes` to look up these identifiers. The assignment
        of putative target genes to
        TFs has been done by calling enriched binding peaks on the aligned
        ChIP-seq reads using MACS and subsequently assigning the peaks to target
        genes if they were within a permissible window of the transcription
        start site (as by current wizard default: 20kb up- and 1kb
        down-stream of the TSS; in an upcoming release  of the web service, you
        will be able to redefine these threshold dynamically, so watch
        this space!). The GeneProf workflow modules corresponding to these two
        steps are documented here: Find Peaks with MACS and Map Regions to
        Genes. Full details for the analysis pipeline that was used to calculate
        each value are available from the individual experiments the values come
        from (the JSON and XML output contain a link to the experiment of
        origin).

        :param str Id: GeneProf ID of a gene (an integer number).
        :param str ref: The identifier of a public GeneProf reference dataset.
            see :meth:`get_list_reference_datasets` and :attr:`valid_species`
            for list of public references.
        :param bool frmt: format requests, one of: json, txt, xml, rdata.
        :param bool with_sample_info: default false. Include additional
            annotations about the  tissue, cell type, etc. of the expression
            values.

        Get information about factors putatively targeting gene #715 in JSON
            format, including additional annotation data::

            >>> g.get_tf_by_target_gene("mouse", "715", with_sample_info=True)

        Get information about factors putatively targeting gene #715 in
        XML format, including additional annotation data::

            >>> g.get_tf_by_target_gene("mouse", "715", frmt="xml",
                    with_sample_info=True)

        Get information about factors putatively targeting gene #715
        as a tab-delimited text file::

            >>> g.get_tf_by_target_gene("mouse", "715", frmt="txt")

        Get information about factors putatively targeting gene
        715 as an RData file, including additional annotation
        data::

            >>> g.get_tf_by_target_gene("mouse", "715", frmt="rdata",
                    with_sample_info=True)

        """
        frmt = self._check_format(frmt)
        url = "gene.info/regulation/binary/by.target/%s/%s." % (ref, Id)
        url += frmt
        params = {}
        params['with-sample-info'] = with_sample_info
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_tfas_scores_by_target(self, ref, Id, frmt="json",
            with_sample_info=False):
        """Get TFAS Scores by Target Gene

        Rerieve a list of Transcription Factor Association Strength scores
        quantitating  the association between transcription factors
        (TFs) and other DNA-binding proteins and a gene of interest, by giving
        the name of the reference dataset the gene belongs to and its internal
        GeneProf gene ID -- use the :meth:`get_list_reference_datasets`,
        :meth:`get_gene_id`, :meth:`search_genes` to look up these identifiers.

        TFAS scores are continuous values that give an indication of how
        strongly a transcription factor (or other
        DNA-binding protein) is associated with a target gene. The TFAS is
        calculated as a function of the intensity and the distance of all
        binding sites (ChIP-seq peaks) near a gene, for details, please refer to
        the publication by Ouyang et al. (PubMed: 19995984). We use as an
        intensity score the fold-change enrichment of the ChIP-seq signal over
        the control background as calculated by MACS in conjunction with calling
        peaks for the input ChIP-seq data. The GeneProf workflow modules
        corresponding to these two steps are documented here:
        `Find Peaks with MACS <http://www.geneprof.org/GeneProf/help_modules.jsp#module:org.stembio.geneprof.workflow.module.chipseq.MACS14withFDRFilter>`_ and `Calculate TFAS <http://www.geneprof.org/GeneProf/help_modules.jsp#module:org.stembio.geneprof.workflow.module.chipseq.TranscriptionFactorAssociationStrength>`_

        Full details for the analysis pipeline that was  used to calculate each
        value are available from the individual experiments the values come from
        (the JSON and XML output contain a link to the experiment of origin).

        :param str Id: The GeneProf ID of a gene (an integer number).
        :param str ref:   The identifier of a public GeneProf reference
            dataset. You may use aliases here. Check the list public references
            service for all available reference datasets.
        :param str frmt: format requests, one of: json, txt, xml, rdata.
        :param bool with-sample-info: (default false) Include additional
            annotations about the tissue, cell type, etc. of the expression values.

        Get TFAS scores to gene #715 in JSON format, including additional
        annotation data::

            >>> g.get_tfas_scores_by_target("mouse", "715", with_sample_info=True)

        Get TFAS scores to gene #715 in XML format, including additional
        annotation data::

            >>> g.get_tfas_scores_by_target("mouse", 715, with_sample_info=True)


        Get TFAS scores to gene #715 as a tab-delimited text file::

            >>> g.get_tfas_scores_by_target("mouse", 715, frmt="txt")

        Get TFAS scores to gene #715 as an RData file, including additional
        annotation data::

            >>> g.get_tfas_scores_by_target("mouse", "715", frmt="rdata",
                with_sample_info=True)
        """
        frmt = self._check_format(frmt)
        url = "gene.info/regulation/tfas/by.target/%s/%s." % (ref, Id)
        url += frmt
        params = {}
        params['with-sample-info'] = with_sample_info
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_metadata_usr(self):
        """Metadata about a User


        """
        raise NotImplementedError

    def get_data(self, Id, frmt=None, sep="\t", gz=False, ats=None, key=None):
        """Retrieves data as Plain Text Files (TXT)

        Retrieve data from a GeneProf dataset as plain
        text (optionailly compressed as GZIP). Retrieves the entire contents
        of an arbitrary GeneProf dataset as a tab-delimited, plain text file.
        The dataset of interest is identified by its GeneProf accession ID
        (something of the form gpDS_XXX_XXX_XXX_X). You can get a list of
        datasets belonging to a certain experiment of interest using the
        :meth:`get_metadata_experiment` method, or you can use the
        :meth:`search_datasets` method to query datasets globally.

        :param str id: identifier of the dataset of interest. Either the entire
            accession ID (e.g. gpDS_11_385_44_1) or just the dataset-specific
            part (e.g. 11_385_44_1).
        :param str gz: compressed the data (if format is not rdata).
        :param str ats: (default displayed columns) A selection of column IDs
            to be included in the output.
        :param str sep: (default is tabulation \t) symbol to be used as
            a column separator.
        :param str key: optional WebAPI key, required to access non-public data.

        Retrieve data from all visible columns of the dataset gpDS_11_119_18_1
        (example RNA-seq data):

            >>> g.get_data("11_119_18_1", frmt="txt", gz=True)

        Retrieve only the Ensembl Gene IDs and RPKM values from the same
        dataset:

            >>> g.get_data("11_119_18_1", frmt="txt", gz=True,
                    ats="C_ENSG,C_11_119_16_1_RPKM0,C_11_119_16_1_RPKM1,C_11_119_16_1_RPKM2,C_11_119_16_1_RPKM3")

        """
        frmt = frmt
        if frmt not in ["txt", "xls", "xml", "rdata"]:
            raise ValueError("frmt must be txt,xls,xml,rdata")
        url = "data/%s." % (Id) + frmt
        if gz:
            if frmt == "rdata":
                raise ValueError("rdata and gz cannot be combined.")
            url += ".gz"
        params = {}
        if ats:
            params['ats'] = ats
        if key:
            params['key'] = key
        if sep!="\t":
            params['sep'] = sep
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_chromosome_names(self, Id, frmt="json", key=None):
        """Get Chromosome Names

        Retrieve the IDs and names of all chromosomes in a genomic dataset. This
        service can only be used for genomic datasets, i.e. for datasets with
        type GENOMIC_REGIONS or REFERENCE.

        The names in genome databases use to refer to chromosomes, even
        of well-known organisms, are not always the same. For example, the
        mitochondrial (pseudo-)chromosome is usally called 'chrMT' in Ensembl,
        but 'chrM' in the UCSC databases. The data as :meth:`get_bed_files`
        or as `WIG <get_wig_files>`_ might therefore require you to rename
        the experiments in the
        output, before using them with other applications.

        :param str Id: The identifier of the dataset of interest. Either the
            entire accession ID (e.g. gpDS_11_385_44_1) or just the
            dataset-specific part (e.g. 11_385_44_1).
        :param str key: optional WebAPI key, required to access non-public data.

        Get all chromosomes for the mouse reference dataset in plain text
        format::

            >>> g.get_chromosome_names("pub_mm_ens58_ncbim37", frmt="txt")

        Get all chromosomes for the human reference dataset in JSON format::

            >>> g.get_chromosome_names("pub_hs_ens59_grch37")

        Get the chromosome names from the ChIP-seq peaks dataset gpDS_11_3_7_2
        in  XML format::

            >>> g.get_chromosome_names("11_3_7_2", frmt="xml")

        """
        frmt = self._check_format(frmt)
        url = "data/chromosome.names/%s." % (Id) + frmt
        params = {}
        if key:
            params['key'] = key
        res = self.http_get(url, frmt=frmt, params=params)
        return res

    def get_bed_files(self, Id, chromosome=None, key=None, filter_column=None,
            with_track_description=True, only_distinct=False):
        """Retrieve Genomic Data as compressed BED Files (gzipped)

        Retrieves genomic data as `BED <http://genome.ucsc.edu/FAQ/FAQformat.html#format1>`_
        files in compressed gzipped format. It works only for datasets with type
        GENOMIC_REGIONS  i.e. those containing genomic data! The dataset of
        interest is identified by its GeneProf accession ID (something of the
        form  gpDS_XXX_XXX_XXX_X). You can get a list of datasets belonging to a
        certain experiment of interest using the metadata for an experiment
        service :meth:`get_metadata_experiment`, or you can use the search
        datasets service to query datasets globally. The maximum size of
        datasets retrieved without an
        API key is restricted to 10,000,000 entries.

        .. note:: chromosomes in the output BED can be
            dynamically renamed in order to make the names compatible with other
            applications (that's because, unfortunately, not all genome
            databases use the same names, see also the
            :meth:`get_chromosome_names` method).

        :param str Id: The identifier of the dataset of interest. Either
            the entire  accession ID (e.g. gpDS_11_385_44_1) or just the
            dataset-specific part (e.g. 11_385_44_1).
        :param str chromosome:  An optional parameter that may be used to rename
            chromosomes in the output. The value should be comma-separated map
            from  chromosome ID to its name in the output, where key and value
            are to be  separated with a hyphen (-), e.g. 1-chr1,2-chr2,3-chr12.
            Any chromosome  not mentioned in the map will not be exported, so
            you can use this as a  filtering mechanism, too. Use the Get
            Chromosome Names service to get a  list of all the available
            chromosome in a dataset with their default  names.
        :param bool filter_column: The ID of a column / annotation type
            holding  boolean flags. Only entries for which this boolean flag
            is true will be  exported.
        :param bool bool with-track-description: Include a track description
            header.
        :param bool only_distinct: Export only one entry if there are
            multiple with the same coordinates.
        :param str key:  An optional WebAPI key, required to access non-public
            data.

        Retrieve ChIP-seq peaks for FoxA1 from dataset gpDS_11_3_7_2:

            >>> g.get_bed_files("11_3_7_2")

        Retrieve only the ChIP-seq peaks on chromosome 3 for FoxA1 from dataset
        gpDS_11_3_7_2:

            >>> g.get_bed_files("11_3_7_2", chromosome="3-chr3")

        Retrieve gene coordinates from the zebrafish reference dataset without a
        track header:

            >>> g.get_bed_files("zebrafish", with_track_description=False)

        Retrieve only the ChIP-seq peaks for Stat3 (identified by the column
        $C_11_12_125_2_14_TFBS) from a dataset containing peaks for many
        different factors (gpDS_11_12_125_2):

            >>> g.get_bed_files("11_12_125_2",
                    filter_column="C_11_12_125_2_14_TFBS")

        """
        url =  "data/"
        if chromosome:
            url += chromosome + "/"
        url += "%s.bed.gz" % (Id)

        params = {}
        if with_track_description is False:
            params['with-track-description'] = False
        if filter_column is not None:
            params['filter-column'] = filter_column
        if only_distinct is True:
            params['only-distinct'] = only_distinct
        if key:
            params['key'] = key
        res = self.http_get(url, frmt="txt", params=params)
        return res

    def get_wig_files(self, Id, chromosome=None, key=None, frag_length=-1,
            with_track_description=True, only_distinct=False, bin_size=25):
        """Genomic Data as WIG Files (WIG)

        Retrieves the entire contents of a genomic GeneProf
        dataset in WIG file format. This will only work for dataset of type
        GENOMIC_REGIONS, i.e. those containing genomic data! The dataset of
        interest is identified by its GeneProf accession ID (something of the
        form     gpDS_XXX_XXX_XXX_X). You can get a list of datasets belonging
        to a certain experiment of interest using the
        :meth:`get_metadata_experiment` service, or you can use the
        :meth:`search_datasets` method to query datasets globally. The maximum
        size of datasets retrieved without an API key is restricted to
        10,000,000 entries. With an API key, the maximum size is unlimited.

        .. note:: chromosomes in the output BED can be
            dynamically renamed in order to make the names compatible with other
            applications (because not all genome databases
            use the same names, see also the get chromosome names service).

        :param str Id: The identifier of the dataset of interest. Either
            the entire accession ID (e.g. gpDS_11_385_44_1) or just the
            dataset-specific part (e.g. 11_385_44_1).
        :param str chromosome: An optional parameter that may be used to
            rename chromosomes in the output. The value should be
            comma-separated map from chromosome ID to its name in the
            output, where key and value are to be separated with a
            hyphen (-), e.g. 1-chr1,2-chr2,3-chr12. Any chromosome not
            mentioned inthe map will not be exported, so you can use
            this as a filtering mech anism, too. Use the Get Chromosome
            Names service to get a list of all the available chromosome
            in a dataset with their default names.
        :param bool with-track-description: (default True) Include a track
            description header.
        :param bool only_distinct: Include only one entry in the
            coverage count if there are multiple with the same
            coordinates. (default False)
        :param int frag-length: (default -1)  The "fragment length" to
            calculate the  coverage with, use -1 to use the actual size
            of the regions.
        :param int bin-size: (default 25)  The bin size / resolution
            of the tracks.
        :param str key: An optional WebAPI key, required to access
            non-public data.

        Retrieve genomic coverage data from a RNA-seq assay of gene
        expression in human liver gpDS_11_58_16_2:

            >>> g.get_wig_files("11_58_16_2")

        Retrieve genomic coverage data from a ChIP-seq experiment for
        Smad1 (gpDS_11_12_112_2), using only distinct alignments:

            >>> g.get_wig_files("11_12_112_2", with_track_description=False,
                only_distinct=True, frag_length=200)
        """
        url = "data/"
        if chromosome:
            url += chromosome + "/"
        url += "%s.wig.gz" % (Id)

        params = {}
        if with_track_description is False:
            params['with-track-description'] = False
        if frag_length != -1:
            params['frag-length'] = frag_length
        if bin_size != -1:
            params['bin-size'] = bin_size
        if only_distinct is True:
            params['only-distinct'] = only_distinct
        if key:
            params['key'] = key
        res = self.http_get(url, frmt="txt", params=params)
        return res

    def get_fasta(self, Id, key=None):
        """Sequence Data as FASTA Files (FASTA, gzipped)

        Retrieves the entire contents of a nucleotide sequence dataset in
        `FASTA <http://en.wikipedia.org/wiki/FASTA_format>`_
        format. This will only work for dataset of type SEQUENCES, i.e. those
        containing sequence data! The dataset of interest is identified by its
        GeneProf accession ID (something of the form
        gpDS_XXX_XXX_XXX_X). You can get a list of datasets belonging to a
        certain experiment of interest using the :meth:`get_metadata_experiment`
        service, or you can use the :meth:`search_datasets` method to query
        datasets  globally. The maximum size of datasets retrieved
        without an API key is restricted to 10,000,000 entries. With an
        API key, the maximum size is unlimited.

        :param str Id: The identifier of the dataset of interest. Either the
            entire accession ID (e.g. gpDS_11_385_44_1) or just the
            dataset-specific part (e.g.11_385_44_1).
        :param str key: optional WebAPI key, required to access non-public data.

        Retrieve unprocessed Tag-seq sequence data from gpDS_11_385_6_1:

            >>> g.get_fasta("11_385_6_1")

        """
        url = "data/%s.fasta.gz" % (Id)
        params = {}
        if key:
            params['key'] = key
        res = self.http_get(url, frmt=None, params=params)
        return res

    def get_fastq(self, Id, key=None):
        """Sequence Data as FASTQ Files (FASTQ)

        Same as :meth:`get_fasta` but for FASTQ format.

        Retrieve unprocessed Tag-seq sequence data from gpDS_11_385_6_1:

            >>> g.get_fastq("11_385_6_1")

        """
        url = self.url + "/data/%s.fastq.gz" % (Id)
        params = {'key':key}
        res = self.http_get(url, None, params=params)

        return res

