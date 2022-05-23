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
# $Id$
"""Interface to some part of the Panther web service

.. topic:: What is Panther ?

    :URL: http://www.panther.org
    :Citation:

    .. highlights::


        The PANTHER (Protein ANalysis THrough Evolutionary Relationships)
        Classification System was designed to classify proteins (and
        their genes) in order to facilitate high-throughput analysis.
        Proteins have been classified according to:

            * Family and subfamily: families are groups of evolutionarily related
              proteins; subfamilies are related proteins that also have the same function
            * Molecular function: the function of the protein by itself or with directly
              interacting proteins at a biochemical level, e.g. a protein kinase
            * Biological process: the function of the protein in the context of a larger
              network of proteins that interact to accomplish a process at the level of the
              cell or organism, e.g. mitosis.
            * Pathway: similar to biological process, but a pathway also explicitly
              specifies the relationships between the interacting molecules.

        -- From PantherDB (about) , Feb 2020

"""
from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["Panther"]


class Panther:
    """Interface to `Panther <http://www.pantherdb.org/services/oai/pantherdb>`_ pages


    ::

        >>> from bioservics import Panther
        >>> p = Panther()
        >>> p.get_supported_genomes()
        >>> p.get_ortholog("zap70", 9606)


        >>> from bioservics import Panther
        >>> p = Panther()
        >>> taxon = [x[0]['taxon_id'] for x in p.get_supported_genomes() if "coli" in x['name'].lower()]
        >>> # you may also use our method called search_organism
        >>> taxon = p.get_taxon_id(pattern="coli")
        >>> res = p.get_mapping("abrB,ackA,acuI", taxon)

    The get_mapping returns for each gene ID the GO terms corresponding to each
    ID. Those go terms may belong to different categories (see
    meth:`get_annotation_datasets`):

    - MF for molecular function
    - BP for biological process
    - PC for Protein class
    - CC Cellular location
    - Pathway

    Note that results from the website application http://pantherdb.org/
    do not agree with the oupput of the get_mapping service... Try out the dgt
    gene from ecoli for example




    """

    _url = "http://www.pantherdb.org/services/oai/pantherdb"

    def __init__(self, verbose=True, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        # super(Panther, self).__init__(name="Panther", url=Panther._url,
        #       verbose=verbose, cache=cache)
        self.services = REST(
            name="Panther",
            url=Panther._url,
            verbose=verbose,
            cache=cache,
            url_defined_later=True,
        )

        self._allPathwaysURL = "http://www.pantherdb.org/pathway/pathwayList.jsp"

    def get_pathways(self):
        """Returns all pathways from pantherdb"""
        return self.services.http_get("supportedpantherpathways")

    def get_supported_genomes(self, type=None):
        """Returns list of supported organisms.

        :param type: can be chrLoc to restrict the search


        """
        if type is not None:
            params = {"type": type}
        else:
            params = {}
        res = self.services.http_get("supportedgenomes", params=params)
        res = [x for x in res["search"]["output"]["genomes"]["genome"]]
        return res

    def get_taxon_id(self, pattern=None):
        """return all taxons supported by the service

        If pattern is provided, we filter the name to keep those that contain
        the filter. If only one is found, we return the name itself, otherwise a
        list of candidates

        """
        res = self.get_supported_genomes()
        if pattern:
            taxon = [x["taxon_id"] for x in res if pattern.lower() in x["name"].lower()]
            if len(taxon) == 1:
                return taxon[0]
            else:
                return taxon
        else:
            taxon = [x["taxon_id"] for x in res]
            return taxon

    def get_mapping(self, gene_list, taxon):
        """Map identifiers

        Each identifier to be delimited by comma i.e. ',. Maximum of 1000 Identifiers
        can be any of the following: Ensemble gene identifier, Ensemble protein
        identifier, Ensemble transcript identifier, Entrez gene id, gene symbol, NCBI
        GI, HGNC Id, International protein index id, NCBI UniGene id, UniProt accession
        and UniProt id

        :param gene_list: see above
        :param taxon: one taxon ID. See supported
            :meth:`~bioservices.panther.Panther.get_supported_genomes`

        If an identifier is not found, information can be found in the
        unmapped_genes key while found identifiers are in the mapped_genes key.

        .. warning:: found and not found identifiers are dispatched into
            unmapped and mapped genes. If there are not found identifiers,
            the input gene list and the mapped genes list do not have the same
            length. The input names are not stored in the output.
            Developpers should be aware of that feature.

        """
        params = {"geneInputList": gene_list, "organism": taxon}
        res = self.services.http_post("geneinfo", params=params, frmt="json")

        if "mapped_genes" in res["search"]:
            mapped_genes = res["search"]["mapped_genes"]["gene"]
            # if only one identifier, retuns a dictionary.
            # if several identifiers, returns a list of dictionary.
            # We will be consistent and return a list
            if "accession" in mapped_genes:
                mapped_genes = [mapped_genes]
        else:
            mapped_genes = [{}]

        if "unmapped_list" in res["search"]:
            unmapped_genes = res["search"]["unmapped_list"]["unmapped"]
            if isinstance(unmapped_genes, list):
                pass
            else:
                unmapped_genes = [unmapped_genes]
        else:
            unmapped_genes = []

        logger.warning("Some identifiers were not found")
        return {"unmapped": unmapped_genes, "mapped": mapped_genes}

    def get_enrichment(
        self,
        gene_list,
        organism,
        annotation,
        enrichment_test="Fisher",
        correction="FDR",
        ref_gene_list=None,
    ):
        """Returns over represented genes

        Compares a test gene list to a reference gene list,
        and determines whether a particular class (e.g. molecular function,
        biological process, cellular component, PANTHER protein class, the
        PANTHER pathway or Reactome pathway) of genes is overrepresented
        or underrepresented.

        :param organism: a valid taxon ID
        :param enrichment_test: either **Fisher** or **Binomial** test
        :param correction: correction for multiple testing. Either **FDR**,
            **Bonferonni**, or **None**.
        :param annotation: one of the supported PANTHER annotation data types.
            See :meth:`~bioservices.panther.Panther.get_annotation_datasets` to retrieve a list of
            supported annotation data types
        :param ref_gene_list: if not specified, the system will use all the genes
            for the specified organism. Otherwise, a list delimited by
            comma. Maximum of 100000 Identifiers can be any of the
            following: Ensemble gene identifier, Ensemble protein
            identifier, Ensemble transcript identifier, Entrez gene id,
            gene symbol, NCBI GI, HGNC Id, International protein index id,
            NCBI UniGene id, UniProt accession andUniProt id.

        :return: a dictionary with the following keys. 'reference' contains the
            orgnaism, 'input_list' is the input gene list with unmapped genes.
            'result' contains the list of candidates.

        ::

            >>> from bioservices import Panther
            >>> p = Panther()
            >>> res = p.get_enrichment('zap70,mek1,erk', 9606, "GO:0008150")
            >>> For molecular function, use :
            >>> res = p.get_enrichment('zap70,mek1,erk', 9606,
                    "ANNOT_TYPE_ID_PANTHER_GO_SLIM_MF")

        """
        assert enrichment_test.lower() in ["fisher", "binomial"]
        if correction is None:
            correction = "none"

        assert correction.lower() in ["fdr", "bonferroni", "none"]

        # This is a bug in panther DB where they used bonferonni . should be
        # bonferroni...
        if correction.lower() == "bonferroni":
            correction = "bonferonni"
        assert annotation in [x["id"] for x in self.get_annotation_datasets()]

        params = {"enrichmentTestType": enrichment_test.upper()}
        params["organism"] = organism
        if gene_list:
            params["geneInputList"] = gene_list
        if ref_gene_list:
            params["refInputList"] = ref_gene_list
        params["annotDataSet"] = annotation
        params["correction"] = correction.upper()
        try:
            res = self.services.http_post("enrich/overrep", params=params, frmt="json")
            try:
                return res["results"]
            except:
                return res
        except:
            return res

    def get_annotation_datasets(self):
        """Retrieve the list of supported annotation data sets"""
        res = self.services.http_get("supportedannotdatasets")
        res = res["search"]["annotation_data_sets"]["annotation_data_type"]
        return res

    def get_ortholog(self, gene_list, organism, target_organism=None, ortholog_type="all"):
        """search for matching orthologs in target organisms.

        Searches for matching orthologs in the gene family that contains
        the search gene associated with the search terms. Returns
        ortholog genes in target organisms given a search organism,
        the search terms and a list of target organisms.

        :param gene_list:
        :param organism: a valid taxon ID
        :param target_organism: zero or more taxon IDs separated by ','. See
            :meth:`~bioservices.panther.Panther.get_supported_genomes`
        :param ortholog_type: optional parameter to specify ortholog type of target organism
        :return: a dictionary with "mapped" and "unmapped" keys, each of them
            being a list. For each unmapped gene, a dictionary with id and
            organism is is returned. For the mapped gene, a list of ortholog is
            returned.

        """
        assert ortholog_type in ["LDO", "all"]
        params = {
            "geneInputList": gene_list,
            "organism": organism,
            "targetOrganism": target_organism,
            "orthologType": ortholog_type,
        }
        if params["targetOrganism"] is None:
            del params["targetOrganism"]
        res = self.services.http_get("ortholog/matchortho", frmt="json", params=params)
        res = res["search"]["mapping"]
        mapped = res["mapped"]

        try:
            unmapped = res["unmapped_ids"]["unmapped"]
            # make sure we always have a list
            if isinstance(unmapped, dict):
                unmapped = [unmapped]
        except:
            unmapped = []
        res = {"unmapped": unmapped, "mapped": mapped}

        return res

    def get_homolog_position(self, gene, organism, position, ortholog_type="all"):
        """

        :param gene: Can be any of the following: Ensemble gene identifier,
            Ensemble protein identifier, Ensemble transcript identifier, Entrez gene id,
            gene symbol, NCBI GI, HGNC Id, International protein index id, NCBI UniGene id,
            UniProt accession andUniProt id
        :param organism: a valid taxon ID
        :param ortholog_type: optional parameter to specify ortholog type of target organism
        """
        if "," in gene:
            logger.warning("did not expect a comma. Please provide only one gene name")
        assert ortholog_type in ["LDO", "all"]
        assert position >= 1
        params = {
            "gene": gene,
            "organism": organism,
            "pos": position,
            "orthologType": ortholog_type,
        }
        res = self.services.http_get("ortholog/homologpos", params=params, frmt="json")
        res = res["search"]["mapping"]
        if "mapped" in res.keys():
            res = res["mapped"]
            return res
        elif "unmapped_ids" in res.keys():
            logger.warning("did not find any match for {}".format(gene))
            return res["unmapped_ids"]

    def get_supported_families(self, N=1000, progress=True):
        """Returns the list of supported PANTHER family IDs

        This services returns only 1000 items per request. This is defined by
        the index. For instance index set to 1 returns the first 1000 families.
        Index set to 2 returns families between index 1000 and 2000 and so on.
        As of 20 Feb 2020, there was about 15,000 families.

        This function simplifies your life by calling the service as many times
        as required. Therefore it returns all families in one go.

        """
        from easydev import Progress

        params = {"startIndex": 1}
        res = self.services.http_get("supportedpantherfamilies", params=params)
        results = res["search"]["panther_family_subfam_list"]["family"]
        if len(results) != N:
            msg = "looks like the services changed. Call this function with N={}"
            msg = msg.format(len(results))
            raise ValueError(msg)

        number_of_families = res["search"]["number_of_families"]
        pb = Progress(int(number_of_families / N))
        pb.animate(1)
        for i in range(1, int(number_of_families / N) + 1):
            params = {"startIndex": i * N + 1}
            res = self.services.http_get("supportedpantherfamilies", params=params)
            data = res["search"]["panther_family_subfam_list"]["family"]
            results.extend(data)
            if progress:
                pb.animate(i)
        return results

    def get_family_ortholog(self, family, taxon_list=None):
        """Search for matching orthologs in target organisms

        Also return the corresponding position in the target
        organism sequence. The system searches for matching
        orthologs in the gene family that contains the search
        gene associated with the search term.

        :param family: Family ID
        :param taxon_list: Zero or more taxon IDs separated by ','.
        """

        params = {"family": family}
        if taxon_list:
            params["taxonFltr"] = taxon_list
        res = self.services.http_get("familyortholog", params=params, frmt="json")
        return res["search"]["ortholog_list"]["ortholog"]

    def get_family_msa(self, family, taxon_list=None):
        """Returns MSA information for the specified family.

        :param family: family ID
        :param taxon_list: Zero or more taxon IDs separated by ','.

        """
        params = {"family": family}
        if taxon_list:
            params["taxonFltr"] = taxon_list
        res = self.services.http_get("familymsa", params=params, frmt="json")
        return res["search"]["MSA_list"]["sequence_info"]

    def get_tree_info(self, family, taxon_list=None):
        """Returns tree topology information and node attributes for the specified family.

        :param family: Family ID
        :param taxon_list: Zero or more taxon IDs separated by ','.
        """
        params = {"family": family}
        if taxon_list:
            params["taxonFltr"] = taxon_list
        res = self.services.http_get("treeinfo", params=params, frmt="json")
        return res["search"]  # ['tree_topology']['annotation_node']
