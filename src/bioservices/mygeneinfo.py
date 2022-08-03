#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2020 - EBI-EMBL - Institut Pasteur
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://bioservices.readthedocs.io
#
##############################################################################
"""Interface to the mygeneinfo web Service.

.. topic:: What is MyGeneInfo ?

    :URL: https://mygene.info
    :REST: https://mygeneinfo/v3.api/

    .. highlights::

        MyGene.info provides simple-to-use REST web services to query/retrieve gene
        annotation data. It’s designed with simplicity and performance emphasized. You
        can use it to power a web application which requires querying genes and
        obtaining common gene annotations. For example, MyGene.info services are used to
        power BioGPS; or use it in an analysis pipeline to retrieve always up-to-date
        gene annotations.

        -- mygene.info home page, June 2020

"""

from bioservices.services import REST

__all__ = ["MyGeneInfo"]


class MyGeneInfo:
    """Interface to `mygene.infoe <http://mygene.info>`_ service

    .. doctest::

        >>> from bioservices import MyGeneInfo
        >>> s = MyGeneInfo()

    """

    def __init__(self, verbose=False, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: prints informative messages (default is off)

        """
        url = "https://mygene.info/v3"
        self.services = REST(name="PDBe", url=url, verbose=verbose, cache=cache)

    def get_genes(
        self,
        ids,
        fields="symbol,name,taxid,entrezgene,ensemblgene",
        species=None,
        dotfield=True,
        email=None,
    ):
        """Get matching gene objects for a list of gene ids


        :param ids: list of geneinfo IDs
        :param str fields: a comma-separated fields to limit the fields returned
            from the matching gene hits. The supported field names can be found from any
            gene object (e.g. http://mygene.info/v3/gene/1017). Note that it supports dot
            notation as well, e.g., you can pass "refseq.rna". If "fields=all", all
            available fields will be returned. Default:
            "symbol,name,taxid,entrezgene,ensemblgene".
        :param str species:  can be used to limit the gene hits from given
            species. You can use "common names" for nine common species (human, mouse, rat,
            fruitfly, nematode, zebrafish, thale-cress, frog and pig). All other species,
            you can provide their taxonomy ids. Multiple species can be passed using comma
            as a separator. Default: human,mouse,rat.
        :param dotfield: control the format of the returned fields when passed
            "fields" parameter contains dot notation, e.g. "fields=refseq.rna". If True
            the returned data object contains a single "refseq.rna" field, otherwise
            (False), a single "refseq" field with a sub-field of "rna". Default:
            True.
        :param str email": If you are regular users of this services, the
            mygeneinfo maintainers/authors encourage you to provide an email,
            so that we can better track the usage or follow up with you.

        ::

            mgi = MyGeneInfoe()
            mgi.get_genes(("301345,22637"))
            # first one is rat, second is mouse. This will return a 'notfound'
            # entry and the second entry as expected.
            mgi.get_genes("301345,22637", species="mouse")

        """
        params = {"ids": ids, "fields": fields}
        if email:  # pragma: no cover
            params["email"] = email

        assert dotfield in [True, False]
        params["dotfield"] = dotfield

        if species:
            params["species"] = species

        res = self.services.http_post(
            "gene",  # params=params,
            data=params,
            frmt="json",
            headers={
                "User-Agent": self.services.getUserAgent(),
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return res

    def get_one_gene(
        self,
        geneid,
        fields="symbol,name,taxid,entrezgene,ensemblgene",
        dotfield=True,
        email=None,
    ):
        """Get matching gene objects for one gene id

        :param geneid: a valid gene ID
        :param str fields: a comma-separated fields to limit the fields returned
            from the matching gene hits. The supported field names can be found from any
            gene object (e.g. http://mygene.info/v3/gene/1017). Note that it supports dot
            notation as well, e.g., you can pass "refseq.rna". If "fields=all", all
            available fields will be returned. Default:
            "symbol,name,taxid,entrezgene,ensemblgene".
        :param dotfield: control the format of the returned fields when passed
            "fields" parameter contains dot notation, e.g. "fields=refseq.rna". If True
            the returned data object contains a single "refseq.rna" field, otherwise
            (False), a single "refseq" field with a sub-field of "rna". Default:
            True.
        :param str email": If you are regular users of this services, the
            mygeneinfo maintainers/authors encourage you to provide an email,
            so that we can better track the usage or follow up with you.

        ::

            mgi = MyGeneInfoe()
            mgi.get_genes("301345")
        """
        params = {"ids": geneid, "fields": fields}
        if email:  # pragma: no cover
            params["email"] = email

        assert dotfield in [True, False]
        params["dotfield"] = dotfield

        res = self.services.http_get(f"gene/{geneid}", params=params, frmt="json")
        return res

    def get_one_query(
        self,
        query,
        email=None,
        dotfield=True,
        fields="symbol,name,taxid,entrezgene,ensemblgene",
        species="human,mouse,rat",
        size=10,
        _from=0,
        sort=None,
        facets=None,
        entrezonly=False,
        ensemblonly=False,
    ):
        """Make gene query and return matching gene list. Support JSONP and CORS as well.

        :param str query: Query string. Examples "CDK2", "NM_052827", "204639_at",
            "chr1:151,073,054-151,383,976", "hg19.chr1:151073054-151383976". The detailed
            query syntax can be found from our docs.
        :param str fields: a comma-separated fields to limit the fields returned
            from the matching gene hits. The supported field names can be found from any
            gene object (e.g. http://mygene.info/v3/gene/1017). Note that it supports dot
            notation as well, e.g., you can pass "refseq.rna". If "fields=all", all
            available fields will be returned. Default:
            "symbol,name,taxid,entrezgene,ensemblgene".
        :param str species: can be used to limit the gene hits from given species. You can use
            "common names" for nine common species (human, mouse, rat, fruitfly, nematode,
            zebrafish, thale-cress, frog and pig). All other species, you can provide their
            taxonomy ids. Multiple species can be passed using comma as a separator.
            Default: human,mouse,rat.
        :param int size: the maximum number of matching gene hits to return
            (with a cap of 1000 at the moment). Default: 10.
        :param int _from: the number of matching gene hits to skip, starting
            from 0. Combining with "size" parameter, this can be useful for paging. Default:
            0.
        :param sort: the comma-separated fields to sort on. Prefix with "-" for
            descending order, otherwise in ascending order. Default: sort by matching scores
            in decending order.
        :param str facets: a single field or comma-separated fields to return
            facets, for example, "facets=taxid", "facets=taxid,type_of_gene".
        :param bool entrezonly: when passed as True, the query returns only the hits
            with valid Entrez gene ids. Default: False.
        :param bool ensembleonly: when passed as True, the query returns only the hits
            with valid Ensembl gene ids. Default: False.
        :param dotfield: control the format of the returned fields when passed
            "fields" parameter contains dot notation, e.g. "fields=refseq.rna". If True
            the returned data object contains a single "refseq.rna" field, otherwise
            (False), a single "refseq" field with a sub-field of "rna". Default:
            True.
        :param str email": If you are regular users of this services, the
            mygeneinfo maintainers/authors encourage you to provide an email,
            so that we can better track the usage or follow up with you.




        """
        params = {"fields": fields, "size": size, "from": _from}
        if email:  # pragma: no cover
            params["email"] = email

        assert dotfield in [True, False]
        params["dotfield"] = dotfield

        if sort:
            params["sort"] = sort
        if facets:  # pragma: no cover
            params["facets"] = sort
        assert entrezonly in [True, False]
        params["entrezonly"] = entrezonly
        assert ensemblonly in [True, False]
        params["ensemblonly"] = entrezonly

        res = self.services.http_get(f"query?q={query}", params=params, frmt="json")
        return res

    def get_queries(
        self,
        query,
        email=None,
        dotfield=True,
        scopes="all",
        species="human,mouse,rat",
        fields="symbol,name,taxid,entrezgene,ensemblgene",
    ):
        """Make gene query and return matching gene list. Support JSONP and CORS as well.

        :param str query: Query string. Examples "CDK2", "NM_052827", "204639_at",
            "chr1:151,073,054-151,383,976", "hg19.chr1:151073054-151383976". The detailed
            query syntax can be found from our docs.
        :param str fields: a comma-separated fields to limit the fields returned
            from the matching gene hits. The supported field names can be found from any
            gene object (e.g. http://mygene.info/v3/gene/1017). Note that it supports dot
            notation as well, e.g., you can pass "refseq.rna". If "fields=all", all
            available fields will be returned. Default:
            "symbol,name,taxid,entrezgene,ensemblgene".
        :param str species: can be used to limit the gene hits from given species. You can use
            "common names" for nine common species (human, mouse, rat, fruitfly, nematode,
            zebrafish, thale-cress, frog and pig). All other species, you can provide their
            taxonomy ids. Multiple species can be passed using comma as a separator.
            Default: human,mouse,rat.
        :param dotfield: control the format of the returned fields when passed
             "fields" parameter contains dot notation, e.g. "fields=refseq.rna". If True
             the returned data object contains a single "refseq.rna" field, otherwise
             (False), a single "refseq" field with a sub-field of "rna". Default:
             True.
        :param str email": If you are regular users of this services, the
            mygeneinfo maintainers/authors encourage you to provide an email,
            so that we can better track the usage or follow up with you.
        :param str scopes: not documented. Set to 'all'

        """
        params = {"q": query, "fields": fields, "scopes": scopes}
        if email:  # pragma: no cover
            params["email"] = email
        assert dotfield in [True, False]
        params["dotfield"] = dotfield

        res = self.services.http_post(
            "query",
            params=params,
            frmt="json",
            headers={
                "User-Agent": self.services.getUserAgent(),
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return res

    def get_metadata(self):
        res = self.services.http_get(f"metadata", frmt="json")
        return res

    def get_taxonomy(self):
        res = self.services.http_get(f"metadata", frmt="json")
        return res["taxonomy"]
