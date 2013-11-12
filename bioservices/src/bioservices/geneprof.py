# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
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
#$Id: kegg.py 226 2013-07-08 07:05:14Z cokelaer $
"""This module provides a class :class:`~GeneProf`

.. topic:: What is GeneProf ?

    :URL: http://www.geneprof.org
    :REST: http://ww.geneprof.org/GeneProf/api

    .. highlights::


       -- GeneProf home page, Nov 2013



Data is freely available, under the license terms of each contributing database.

"""
from __future__ import print_function

from bioservices.services import RESTService, BioServicesError

import json

__all__ = ["GeneProf"]



class GeneProf(RESTService):
    """Interface to the `GeneProf <http://www.pathwaycommons.org/pc2>`_ service



    .. warning:: some of the GeneProf services requires registration. This class
        only provides access to the services that do not require registration.
        More about the API key registration on
        `http://www.geneprof.org/GeneProf/webapi.jsp`_

    .. warning:: there is a limitation on the number of request per day that is
        <250 (Nov 2013)

    """

    _valid_format = ["json", "txt", "xml", "rdata"]
    _valid_species = ["arabidopsis", "at", "ce", "celegans", "chick", "chicken",
    "danio", "dm", "dmel", "dr", "drosphila", "ef", "fruitfly", "gg", "hs",
    "hsapiens", "human", "mm", "mmusculus", "mouse", "os", "pig", "rat", "rice",
    "rn", "ss", "sscrofa", "tair", "yeast", "zebrafish"]


    def __init__(self, verbose=True):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages

        """
        super(GeneProf, self).__init__(name="GeneProf",
                url="http://www.geneprof.org/GeneProf/api", verbose=verbose)
        self.easyXMLConversion = False
        self._default_extension = "json"

        # buffering the ids for the experiments and datasets
        self._ids_exp = None
        self._rigid_ids_exp = None
        self._ids_ds = None
        self._rigid_ids_ds = None

    # just a get/set to the default extension
    def _set_default_ext(self, ext):
        self.checkParam(ext, ["json","xml", "txt", "rdata"])
        self._default_extension = ext
    def _get_default_ext(self):
        return self._default_extension
    default_extension = property(_get_default_ext, _set_default_ext,
             doc="set extension of the requests (default is json). Can be 'json' or 'xml'")

    # buffering the ids from the experiments
    def _get_ids_exp(self):
        if self._ids_exp == None: 
            self.logging.info("Fetchin ids...")
            res = self.list_experiments(format="json")
            self._ids_exp = [x['id'] for x in res]
            self._rigid_ids_exp = [x['rigid_id'] for x in res]
        return self._ids_exp
    ids_exp = property(_get_ids_exp)

    def _get_rigid_ids_exp(self):
        if self._rigid_ids_exp == None: 
            self.logging.info("Fetchin ids...")
            res = self.list_experiments(format="json")
            self._rigid_ids_exp = [x['rigid_id'] for x in res]
            self._ids_exp = [x['id'] for x in res]
        return self._rigid_ids_exp
    rigid_ids_exp = property(_get_rigid_ids_exp)

    # buffering the ids from the datasets
    def _get_ids_ds(self):
        if self._ids_ds == None: 
            self.logging.info("Fetchin ids...")
            res = self.list_datasets(format="json")
            self._ids_ds = [x['id'] for x in res]
        return self._ids_ds
    ids_ds = property(_get_ids_ds)


    def list_experiments(self, format="json", **kargs):
        """Use this web service to retrieve a list of GeneProf experiments.


        'Experiments' are what GeneProf calls each individual data analysis
        project. An experiment typically consists of a set of input data 
        (e.g. raw high-throughput sequencing reads), some experimental sample 
        annotation, an analysis workflow and a selection of main outputs. 
        Please check the manual for further information
        about experiments. This web service simply retrieves a list of all the
        experiments available in the database along with a range of metadata.

        :param str format: format of the output

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

        :return: if json output is requested, the output is a list of
            dictionaries. Each dictionary corresponds to one experiment

        .. doctest::

            from bioservices import GeneProf
            g = GeneProf(verbose=False)
            experiments = g.list_experiments(with_outputs=True)

        """

        if format == None:
            format = self.default_extension
        self.checkParam(format, self._valid_format)
        url = self.url + "/exp/list." + format

        for key in kargs.keys():
            if key not in ["with_ats", "with_samples", "with_inputs",
                    "with_outputs", "with_workflow", "with_all_data",
                    "only_user_experiments", "key"]:
                raise BioServicesError("invalid parameter (%s) provided" % key)
        params = self.urlencode(kargs)
        if len(params):
            params = params.replace("with_", "with-")
            url += "?"+ params
        res = self.request(url)
        if format == "json":
            res = json.loads(res)
            res = res['experiments']
        return res

    def _check_format(self, format_):
        if format_ == None:
            format_ = self.default_extension
        self.checkParam(format_, self._valid_format)
        return format_

    def _check_id(self, Id):
        if Id not in self.ids_exp and Id not in self.rigid_ids_exp:
            raise BioServicesError("Incorrect ids provides. See ids and rigid_ids attributes.")

    def _check_kargs(kargs, valid_keys):
        for key in kargs.keys():
            if key not in valid_keys:
                raise BioServicesError("invalid parameter (%s) provided" % key)

    def metadata_experiment(self, Id, format="json", **kargs):
        """Retrieves metadata (names, descriptions, IDs, etc) about experiments.


        An experiment typically consists of a set of input data (e.g. raw 
        high-throughput sequencing reads), some experimental sample 
        annotation, an analysis workflow and a selection of main outputs. 

        :param str Id: accession ID (a string of the form gpXP_XXXXXX or a
            numeric part (e.g., 3)).
        Other parameters from :meth:`list_experiments` are also available 
        except only_user_experiments.
        :return: dictionary with metadata

        Retrieve basic metadata about experiment gpXP_000385 including 
        workflow::

            g.metadata(Id="385", with_workflow=True)

        """
        format_ = self._check_format(format)
        self._check_id(Id)
        self._check_kargs(kargs, ["with_ats", "with_samples", "with_inputs",
                    "with_outputs", "with_workflow", "with_all_data", "key"])

        url = self.url + "/exp/%d." % Id + format_
        params = self.urlencode(kargs)
        if len(params):
            params = params.replace("with_", "with-")
            params = params.replace("only_user_ex", "only-user-ex")
            url += "?"+ params
        res = self.request(url)
        if format == "json":
            res = json.loads(res)
        return res

    def metadata_dataset(self, Id, format="json", **kargs):
        """


        :param str Id: The identifier of the dataset of interest. Either the
            entire accession ID (e.g. gpDS_11_385_44_1) or just the 
            dataset-specific part (e.g. 11_385_44_1).

        Retrieve metadata about the dataset gpDS_11_12_122_1 as JSON::

            g.metadata_dataset("11_12_122_1", with_ats=True)

        """
        format_ = self._check_format(format)
        self._check_id_ds(Id)
        self._check_kargs(kargs, ["with_ats", "key"])

        url = self.url + "/ds/%d." % Id + format_
        params = self.urlencode(kargs)
        if len(params):
            params = params.replace("with_", "with-")
            url += "?"+ params
        res = self.request(url)
        if format == "json":
            res = json.loads(res)
        return res



    def list_pubref_datasets(self, format="json"):
        """Retrieves a list of public reference datasets.

        GeneProf provides a number of recommended reference datasets
        for several organisms (human, mouse, rat, etc.). These reference datasets
        provide genomic sequence assemblies and genic annotations that serve as a
        scaffold for GeneProf's analyses, so most of GeneProf's datasets 
        are based on one of these reference datasets. This web service simply 
        retrieves a list of all the public, recommended reference datasets 
        currently available in the database.


        :param str format: the file format requests, one of: json, xml, 
            txt, rdata. 

        .. note:: the txt and rdata format versions of the output reports a 
            flattened version of the dataset metadata and misses out some 
            information available in the other formats!

        Examples:

        Retrieve a list of all reference datasets as JSON::

            >>> g.list_datasets()


        """
        format_ = self._check_format(format)
        url = self.url + "/ds/pubref." + format_
        res = self.request(url)
        if format_ == "json":
            res = json.loads(res)
            res = res['references']
        return res


    def list_samples(self, ref, format="json"):
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

        :Examples:
        Retrieve a list of all samples for mouse as XML:

            >>> g.list_samples("mouse")
            >>> g.list_samples("human.txt")
            >>> g.list_samples("human.rdata")

        """
        format_ = self._check_format(format)
        url = self.url + "/gene.info/list.samples/%s." % ref + format_
        res = self.request(url)

        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
            res = res['samples']
        return res


    def search_genes(self, query, taxons=None, format="json"):
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
        :param str format: file format requests, one of: json, xml, txt, rdata.
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



        """
        format_ = self._check_format(format)
        query = query.replace(" ", "+")
        url = self.url + "/search/gene/%s." % query + format_
        params = {}
        if taxons:
            params['taxons'] = taxons
        params = self.urlencode(params)
        if len(params):
            url += "?" +  params
        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res


    def search_experiment(self, query, taxons=None, format="json"):
        """Search Experiments using  name, description and citations.

        'Experiments' are what GeneProf calls each individual data
        analysis project. An experiment typically consists of a set of input data (e.g.
         raw high-throughput sequencing reads), some experimental sample
 annotation, an analysis workflow and a selection of main outputs. Please check
 the manual for further information about experiments. Using this web service,
 you can search for experiments of interest using arbitrarily complex search
 queries against the names, descriptions, linked citations, linked reference
 dataset, and so on of those experiments. The search results are categorised by
 the reference dataset the experiments belong to (also see the List Public
         Reference Datasets service).

     :param str query: The search term to look for, e.g. a gene name or paper 
        title. You can narrow down the fields to be search by prefixing the 
        query with a field name. Valid fields for experiments are: Valid 
        search fields are: id, label, description, type, reference, user, 
        dataset, citation, platform and sample. You can also use boolean 
        logic in your queries using the keywords AND and OR, brackets and 
        quotes (") for exact matches of whole phrases. Advanced search 
        options and examples are documents on GeneProf's search
        page.
     :param str format: The file format requests, one of: json, xml, txt, rdata.
     :param str taxons: Only return matches from experiments dealing with
         organisms matching these NCBI taxonomy IDs (comma-separated list).

     Search for experiments mentioning 'sox2' anywhere (in XML format):

        g.search_experiment("sox2")

     Search for experiments mentioning 'cancer' in their description (in JSON
         format):

        g.search_experiment("citation:cancer")

    Search for experiments mentioning 'cell stem cell' in a linked citation (in
    plain text format):

        g.search_experiment("citation:'stem cell'")

        """
        format_ = self._check_format(format)
        query = query.replace(" ", "+")
        url = self.url + "/search/experiment/%s." % query + format_
        params = {}
        if taxons:
            params['taxons'] = taxons
        params = self.urlencode(params)
        if len(params):
            url += "?" +  params
        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res

    def search_datasets(self, query, taxons=None, format=None):
        """search for datasets

        'Datasets', in GeneProf, are collections of data of the
        same type generated as the output of a component of an data analysis
        workflow. There are six generic types of datasets: FILE, SEQUENCES,
        GENOMIC_REGIONS, FEATURES, REFERENCE and SPECIAL. Please check the manual
        for further information about datasets. Using this web service, you can
        search for experiments of interest using arbitrarily complex search queries
        against the names and types of these datasets.

        :param str query: The search term to look for, e.g. a gene name 
            or cell type. You can narrow down the fields to be search by 
            prefixing the query with a field name. Valid fields for samples 
            are: id, label, description, datatype, user, experiment .You can 
            also use boolean logic in your queries using the keywords AND and OR,
            brackets and quotes (") for exact matches of whole phrases.
            Advanced search options and examples are documents on GeneProf's
            search page.
        :param str format: file format in: json, xml, txt, rdata.
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
        format_ = self._check_format(format)
        query = query.replace(" ", "+")
        url = self.url + "/search/dataset/%s." % query + format_
        params = {}
        if taxons:
            params['taxons'] = taxons
        params = self.urlencode(params)
        if len(params):
            url += "?" +  params
        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res


    def search_samples(self, query, taxons=None, format=None):
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
        :param bool format: file format requests, one of: json, xml, txt, rdata.
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
        format_ = self._check_format(format)
        query = query.replace(" ", "+")
        url = self.url + "/search/sample/%s." % query + format_
        params = {}
        if taxons:
            params['taxons'] = taxons
        params = self.urlencode(params)
        if len(params):
            url += "?" +  params
        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res


    def get_gene_id(self, ref, idtype, Id, format="json"):
        """Get the GeneProf ID of a Gene 

        GeneProf uses well-defined sets of gene annotations
        based on those from Ensembl. you can get the
        GeneProf-internal ID of any gene in the reference annotation by
        matching it against an external name (official gene symbol) or one of
        the supported accession ID types (e.g. Ensembl Gene IDs, RefSeq IDs,
        etc. -- use the list ID types service to find out which types
        are supported for a dataset).

        :param str Id: The GeneProf ID of a gene (an integer number).
        :param str ref: The identifier of a public GeneProf reference 
            dataset. You may use aliases here. Check the list public 
            references service for all available reference datasets.
        :param str IDTYPE: The identifier of an annotation column storing IDs or
            the term any to use any available identifier type. Check the list
            ID types service to find out which types are supported for a
            dataset.
        :param str format: format, one of: json, txt, xml, rdata.

        Get the GeneProf ID of the mouse gene with Ensembl ID ENSMUSG00000059552

            >>> g.get_gene_id("mouse", "C_ENSG", "ENSMUSG00000059552")


        Get the GeneProf IDs of all human genes with RefSeq ID NM_005657, 
        as JSON::

            >>> g.get_gene_id("human", "C_RSEQ", "NM_005657")

        Get the GeneProf IDs of all human genes with any ID matching 
        "NM_005657" (should, in this case, be same as the previous query)::

            >>> g.get_gene_id("human", "any", "NM_005657")
        """
        format_ = self._check_format(format)

        url = self.url + "/gene.info/gp.id/%s/%s/%s." % (ref, idtype, Id) 
        url += format_

        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res


    def get_external_gene_id(self, ref, idtype, Id, format="json"):
        """translates a GeneProf gene ID into an  external identifier or name.


        Using this web service, you can look up an
        external name (official gene symbol) or one of the supported accession ID
        types (e.g. Ensembl Gene IDs, RefSeq IDs, etc. -- use the list ID types
        service to find out which types are supported for a dataset) for
        any given internal GeneProf gene ID.

        :param str Id:   The GeneProf ID of a gene (an integer number).
        :param str ref:  The identifier of a public GeneProf reference 
            dataset. You may use aliases here. Check the list public references 
            service for all  available reference datasets.
        :param str idtype:   The identifier an annotation column storing 
            IDs. Check the list ID types service to find out which types 
            are supported for a  dataset.
        :param str format:  format requests, one of: json, txt, xml, rdata.

        Get the Ensembl Gene ID(s) of the mouse gene #715, as plain text:

             >>> g.get_external_gene_id("mouse","715", "C_ENSG")

         Get the RefSeq ID(s) of the human gene #2981, as JSON:

             >>> g.get_external_gene_id("mouse","2981", "C_RSEQ")

         Get the name(s) of the human gene #2981, as XML:

             >>> g.get_external_gene_id("mouse","2981", "C_NAME")
        """
        format_ = self._check_format(format)
        url = self.url + "/gene.info/external.id/%s/%s/%s." % (ref, idtype, Id) 
        url += format_
        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res

    def get_idtypes(self, ref, format="json"):
        """list all the ID types available for a dataset.

Full Description:   GeneProf reference datasets provide a number of alternative ID annotations (e.g. Ensembl Gene IDs, RefSeq IDs, UniGene IDs, etc.) for each of the genes in the reference annotation. This service simply lists all the ID types available for a dataset.

    :param str ref: identifier of a public GeneProf reference dataset. 
    :param str format: format, one of: json, txt, xml, rdata.


        >>> g.get_idtypes("mouse")
        >>> g.get_idtypes("human")

        """
        format_ = self._check_format(format)
        url = self.url + "/gene.info/list.id.types/%s." % ref
        url += format_
        res = self.request(url)
        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res


    def get_expression(self, red, Id, format="json", with_sample_info=False,
        type=None):
        """Get Gene Expression Values for a Gene

        retrieve gene expression values for a gene based on public RNA-seq data in the GeneProf databases. GeneProf's databases contain many pre-calculated gene expression values stemming from a reanalyses of a large collection of RNA-seq (and similar) experiments. You use this web service to retrieve all the expression values for a single gene of interest by giving the name of the reference dataset the gene belongs to and its internal GeneProf gene ID -- use the list reference datasets, get GeneProf ID and/or search genes services to look up these identifiers. You may retrieve the values either as raw read counts (the total number of short reads that were aligned to the gene's locus), RPM (reads per million -- the raw counts rescaled to account for differences in library size) or RPKM (reads per kilobase million -- like RPM, but also accounting for transcript length bias). All gene expression values have been calculated using the Calculate Gene Expression module. Full details for the analysis pipeline that was used to calculate each value are available from the individual experiments the values come from (the JSON and XML output contain a link to the experiment of origin).

        :param str Id: GeneProf ID of a gene (an integer number).
        :param str ref: identifier of a public GeneProf reference dataset. You may use aliases here. Check the list public references service for all available reference datasets.
        :param str format: format requests, one of: json, txt, xml, rdata.
        :param str type: type of values to obtain, one of: RAW | RPM | RPKM
        :param str with_sample_info: Include additional annotations about the 
            tissue, cell type, etc. of the expression values.

        Retrieve gene expression values for the mouse gene #715, including additional annotation data: 

            >>> g.get_expression("mouse", "715", with_sample_info=True)

        Retrieve raw read count values for the mouse gene #715

            >>> g.get_expression("mouse", "715", type="RAW")

        Retrieve gene expression values for the mouse gene #715 as a tab-delimited text file, including additional annotation data: 

            >>> g.get_expression("mouse", "715", format="txt", with_sample_info=True)
    
        Retrieve gene expression values for the mouse gene #715 as an 
        RData file, including additional annotation data: 

            >>> g.get_expression("mouse", "715", format="rdata", with_sample_info=True)

        """
        format_ = self._check_format(format)
        url = self.url + "/gene.info/expression/%s/%s." % (ref, Id)
        url += format_
        res = self.request(url)

        params = {}
        
        if len(params):
            params = params.replace("with_", "with-")
            url += "?"+ params
        res = self.request(url)

        if format_ == "json":
            # TODO: special characters to be removed.
            res = json.loads(res.replace("\\", ""))
        return res



    def get_targets_tf(self,ref,Id,format="json"):
        """Get Targets of a Transcription Factor (TXT, XML, JSON, RDATA)
URL(s):     
http://www.geneprof.org/api/gene.info/regulation/binary/by.gene/{REF}/{ID}.{FORMAT}
Summary:    Use this web service to retrieve putative target genes for a transcription factor (or other transcriptional regulator) based on public ChIP-seq data in the GeneProf databases by querying for the targets discovered in all available ChIP-seq experiments (identified by the ID of a gene).
        """
        raise NotImplementedError

    def get_targets_bysample(self):
        """Get Targets by Experiment Sample (TXT, XML, JSON, RDATA)
URL(s):     
http://www.geneprof.org/api/gene.info/regulation/binary/by.sample/{REF}/{ID}.{FORMAT}
Summary:    Use this web service to retrieve putative target genes for a transcription factor (or other transcriptional regulator) based on public ChIP-seq data in the GeneProf databases by querying for the targets discovered in a specific ChIP-seq experiment (identified by the ID of a public sample).
        """
        raise NotImplementedError

    def get_tfas_bygene(self, ref, Id, format="json"):
        """Get TFAS of a Transcription Factor (TXT, XML, JSON, RDATA)
URL(s):     
http://www.geneprof.org/api/gene.info/regulation/tfas/by.gene/{REF}/{ID}.{FORMAT}
Summary:    Use this web service to retrieve transcription factor association strength (TFAS) scores for a transcription factor (or other transcriptional regulator) based on public ChIP-seq data in the GeneProf databases by querying for the data in all available ChIP-seq experiments (identified by the ID of a gene).
        """
        raise NotImplementedError


    def get_tfas_bysample(self):
        """
Get TFAS by Experiment Sample (TXT, XML, JSON, RDATA)
URL(s):     
http://www.geneprof.org/api/gene.info/regulation/tfas/by.sample/{REF}/{ID}.{FORMAT}
Summary:    Use this web service to retrieve transcription factor association strength (TFAS) scores for a transcription factor (or other transcriptional regulator) based on public ChIP-seq data in the GeneProf databases by querying for data in a specific ChIP-seq experiment (identified by the ID of a public sample).
        """
        raise NotImplementedError
        
    def get_tf_bytarget(self):
        """Get Transcription Factors by Target Gene (TXT, XML, JSON, RDATA)
URL(s):     
http://www.geneprof.org/api/gene.info/regulation/binary/by.target/{REF}/{ID}.{FORMAT}
Summary:    Use this web service to retrieve transcription factors (and other regulatory inputs) putatively targeting a specific gene, based on public ChIP-seq data in the GeneProf databases.
        """
        raise NotImplementedError

    def get_tfas_bytarget(self):
        """Get TFAS Scores by Target Gene (TXT, XML, JSON, RDATA)
URL(s):     
http://www.geneprof.org/api/gene.info/regulation/tfas/by.target/{REF}/{ID}.{FORMAT}
Summary:    Use this web service to retrieve transcription factors association scores between transcription factors (and other regulatory inputs) and a specific target gene of interest, based on public ChIP-seq data in the GeneProf databases.
        """
        raise NotImplementedError

    def get_metadata_usr(self):
        """Metadata about a User (XML, JSON)
URL(s):     http://www.geneprof.org/api/usr/{ID}.{FORMAT}
Summary:    Use this web service to retrieve metadata about a GeneProf user (name, email, user experiments, etc.). In the interest of privacy, the service can only be used to retrieve information about yourself.
        """
        raise NotImplementedError

    def get_data(self, Id):
        """Data as Plain Text Files (TXT)
URL(s):     
http://www.geneprof.org/api/data/{ID}.txt
http://www.geneprof.org/api/data/{ID}.txt.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as plain text (optionally compressed as GZIP). Maximum size of datasets without API key = 1,000,000, with API key = unlimited.

        """
        raise NotImplementedError

    def get_data_xls(self, Id):
        """Data as Spreadsheets (XLS)
URL(s):     
http://www.geneprof.org/api/data/{ID}.xls
http://www.geneprof.org/api/data/{ID}.xls.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as Excel-compatible spreadsheets (optionally compressed as GZIP). Maximum size of datasets without API key = 50,000, with API key = 50,000.
        """
        raise NotImplementedError

    def get_data(self, Id):
        """Data as XML 

http://www.geneprof.org/api/data/{ID}.xml
http://www.geneprof.org/api/data/{ID}.xml.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as XML (compressed as GZIP). Maximum size of datasets without API key = 1,000,000, with API key = unlimited.

        """
        raise NotImplementedError

    def get_rdata(self, Id):
        """Data as R Binary Files (RData)

URL(s):     http://www.geneprof.org/api/data/{ID}.rdata
Summary:    Use this web service to retrieve data from a GeneProf dataset as binary files that can be loaded into R. Maximum size of datasets without API key = 1,000,000, with API key = 1,000,000.
        """
        raise NotImplementedError

    def get_chromosome(self, Id, format="json"):
        """
Get Chromosome Names (XML, JSON, TXT, RDATA)
URL(s):     http://www.geneprof.org/api/data/chromosome.names/{ID}.{FORMAT}
Summary:    Use this web service to retrieve the IDs and names of all chromosomes in a genomic dataset. This service can only be used for genomic datasets, i.e. for datasets with type GENOMIC_REGIONS or REFERENCE.
        """
        raise NotImplementedError

    def get_bed(self, Id):
        """Genomic Data as BED Files (BED)
URL(s):     
http://www.geneprof.org/api/data/{ID}.bed.gz
http://www.geneprof.org/api/data/{CHROMNAMES}/{ID}.bed.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as BED (compressed as GZIP). Maximum size of datasets without API key = 10,000,000, with API key = unlimited. This service can only be used for genomic datasets, i.e. for datasets with type GENOMIC_REGIONS.
        """
        raise NotImplementedError

    def get_wig(self, Id):
        """
Genomic Data as WIG Files (WIG)
URL(s):     
http://www.geneprof.org/api/data/{ID}.wig.gz
http://www.geneprof.org/api/data/{CHROMNAMES}/{ID}.wig.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as WIG (compressed as GZIP). Maximum size of datasets without API key = 10,000,000, with API key = unlimited. This service can only be used for genomic datasets, i.e. for datasets with type GENOMIC_REGIONS.
        """
        raise NotImplementedError

    def get_fasta(self, Id):
        """
Sequence Data as FASTA Files (FASTA)
URL(s):     http://www.geneprof.org/api/data/{ID}.fasta.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as FASTA (compressed as GZIP). Maximum size of datasets without API key = 10,000,000, with API key = unlimited. This service can only be used for nucleotide sequence datasets, i.e. for datasets with type SEQUENCES.
        """
        raise NotImplementedError

    def get_fastq(self, Id):
        """
Sequence Data as FASTQ Files (FASTQ)
URL(s):     http://www.geneprof.org/api/data/{ID}.fastq.gz
Summary:    Use this web service to retrieve data from a GeneProf dataset as FASTA (compressed as GZIP). Maximum size of datasets without API key = 10,000,000, with API key = unlimited. This service can only be used for nucleotide sequence datasets, i.e. for datasets with type SEQUENCES.
        """
        raise NotImplementedError

