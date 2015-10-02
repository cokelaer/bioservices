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
# $Id$
"""Interface to Ensembl web service

.. topic:: What is Ensembl ?

    :URL: http://www.ensembl.org/
    :URL: https://github.com/Ensembl/ensembl-rest/wiki/Output-formats

    .. highlights::

        The Ensembl project produces genome databases for vertebrates and
        other eukaryotic species, and makes this information freely available
        online.

        -- From Ensembl web site, Oct 2014


"""
from bioservices.services import REST

__all__ = ["Ensembl"]


class Ensembl(REST):
    """Interface to the `Ensembl <http://rest.ensembl.org>`_ service

    For the BioServices documentation see the documentation of
    each method for the list of parameters. The API was copied
    from the Ensemble API (http://rest.ensembl.org)

    All methods have been tests using this BioServices
    `notebook <http://nbviewer.ipython.org/github/bioservices/notebooks/blob/master/ensembl/Ensembl.ipynb>`_


    .. todo:: There are 3 methods out of 50 that are not implemented so far.
    .. todo:: some methods have a parameter called *feature*. The official
       Ensembl API allows one to provide several features at the same time.
       This is not yet implemented. Only one at a time is accepted.

    .. note:: Some function uses SQL wildcards. See e.g. http://www.w3schools.com/sql/sql_wildcards.asp
        In brief, "_" can be use to substitute a single character and '%' a set of characters.
    """
    _url = "http://rest.ensembl.org"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(Ensembl, self).__init__(name="Ensembl", url=Ensembl._url,
                verbose=verbose, cache=cache)
        self.callback = None #use in all methods

    def _check_frmt(self, frmt, values=[]):
        self.devtools.check_param_in_list(frmt, ['json','jsonp'] + values)

    def _check_id(self, identifier):
        pass

    def nh_format_to_frmt(self, value):
        if value == 'phylip':
            return 'phyloxml'
        elif value == 'simple':
            return 'nh'
        else:
            return 'json'

    def check_sequence(self, value):
        self.devtools.check_param_in_list(value,
                ['none', 'cdna', 'protein'])

    def check_nh_format(self, value):
        self.devtools.check_param_in_list(value,
                ['full', 'display_label_composite', 'simple', 'species',
                    'species_short_name', 'ncbi_taxon', 'ncbi_name', 'njtree',
                    'phylip'])

    # ARCHIVE
    # ---------------------------------------------------------------------
    def get_archive(self, identifier, frmt='json'):
        """Uses the given identifier to return the archived sequence

        :param str identifier: An Ensembl stable ID
        :param str frmt: output formart(json, xml or jsonp)

        ::

            >>> from bioservices import Ensembl
            >>> s = Ensembl()
            >>> res = s.get_archive("ENSG00000157764")

        """
        self._check_frmt(frmt, ['xml'])
        self._check_id(identifier)
        res = self.http_get("archive/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback})

        if frmt == 'xml':
            res = self.easyXML(res)
        return res

    def post_archive(self, identifiers, frmt='json'):
        """Retrieve the archived sequence for a set of identifiers

            returned by the requested JSONP response. Required ONLY when using
            JSONP as the serialisation method. Please see the user guide.

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_post("archive/id/", frmt=frmt,
                headers = self.get_headers(content=frmt),
                data =self.devtools.to_json({'id':identifiers}),
                params={'callback': self.callback})
        if frmt == 'xml':
            res = self.easyXML(res)
        return res

    # COMPARATIVE GENOMICS
    # ------------------------------------------------------------------

    def get_genetree_by_member_symbol(self, species, symbol, frmt='json',
            aligned=False, db_type='core', object_type=None,
            nh_format='simple', sequence='protein',
            compara='multi'):
        """ Retrieves a gene tree containing the gene identified by a symbol"""
        self._check_frmt(frmt, ['nh', 'phyloxml'])
        frmt = self.nh_format_to_frmt(nh_format)
        self.check_sequence(sequence)
        self.check_nh_format(nh_format)

        res = self.http_get("genetree/member/symbol/%s/%s" %(species, symbol),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence,
                    'aligned':int(aligned), 'compara':compara,
                    'db_type':db_type})
        return res

    def get_genetree_by_member_id(self, identifier, frmt='json',
            aligned=False, db_type='core', object_type=None,
            nh_format='simple', sequence='protein', species='homo_sapiens',
            compara='multi'):
        """Retrieves a gene tree containing the gene identified by a symbol

        :param str compara: Name of the compara database to use. Multiple
            comparas can exist on a server if you are accessing Ensembl
            Genomes data. Defautl to 'multi'
        :param db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core. Defaults
            to core
        :param object_type: Filter by feature type. Default to None
            examples are gene, transcript.

        :

            get_genetree_by_member_id('ENSG00000157764', frmt='phyloxml')


        """
        self._check_frmt(frmt, ['nh', 'phyloxml'])
        self._check_frmt(frmt)
        self.check_nh_format(nh_format)
        frmt = self.nh_format_to_frmt(nh_format)
        self.check_sequence(sequence)

        res = self.http_get("genetree/member/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence,
                    'aligned':int(aligned), 'compara':compara,
                    'db_type':db_type, 'species':species})
        return res

    def get_genetree_by_id(self, identifier, aligned=False, frmt='json',
            nh_format='simple', sequence='protein',
            compara='multi'):
        """Retrieves a gene tree dump for a gene tree stable identifier

        :param str identifier: An Ensembl genetree ID
        :param str frmt: response formats: json, jsonp, nh, phyloxml
        :param bool aligned: if true, return the aligned string otherwise, i
            return the original
            sequence (no insertions). Can be True/1 or False/0 and defaults to 0
        :param str compara: Name of the compara database to use. Multiple comparas can
            exist on a server if you are accessing Ensembl Genomes data
        :param nh_format: The format of a NH (New Hampshire) request.
            Valid values are 'full', 'display_label_composite', 'simple',
            'species', 'species_short_name', 'ncbi_taxon', 'ncbi_name',
            'njtree', 'phylip'
        :param sequence: The type of sequence to bring back. Setting it to none
            results in no sequence being returned.
            Valid values are 'none', 'cdna', 'protein'.

        ::

            >>> from bioservices import Ensembl
            >>> s = Ensembl()
            >>> s.get_genetree('ENSGT00390000003602', frmt='nh', nh_format='simple')
            >>> s.get_genetree('ENSGT00390000003602', frmt='phyloxml')
            >>> s.get_genetree('ENSGT00390000003602', frmt='phyloxml',aligned=True, sequence='cdna')
            >>> s.get_genetree('ENSGT00390000003602', frmt='phyloxml', sequence='none')

        """
        self._check_frmt(frmt, ['nh', 'phyloxml'])
        self.check_nh_format(nh_format)
        aligned = int(aligned)
        self.check_sequence(sequence)
        res = self.http_get("genetree/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence,
                    'aligned':aligned})
        return res

    def get_alignment_by_region(self, region, species, frmt='json', aligned=True,
            compact=True, compara='multi',
            display_species_set=None, mask=None, method='EPO', species_set=None,
            species_set_group='mammals'):
        """Retrieves genomic alignments as separate blocks based on a region and
        species

        :param str region: Query region. A maximum of 10Mb is allowed to be
            requested at any one time (e.g.,  'X:1000000..1000100:1',
            'X:1000000..1000100:-1',  'X:1000000..1000100')
        :param str species: Species name/alias (e.g., human)
        :param bool aligned: Return the aligned string if true. Otherwise,
            return the original sequence (no insertions)
        :param bool compact: Applicable to EPO_LOW_COVERAGE alignments.
            If true, concatenate the low coverage species sequences
            together to create a single sequence. Otherwise, separates
            out all sequences.
        :param str compara: Name of the compara database to use. Multiple
            comparas can exist on a server if you are accessing Ensembl
            Genomes data (defaults to multi)
        :param str display_species_set: Subset of species in the alignment
            to be displayed (multiple values). All the species in the alignment
            will be displayed if this is not set. Any valid alias may be
            used.. (e.g., human, chimp, gorilla)
        :param str mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters.
        :param str method:The alignment method amongst Enum(EPO,
            EPO_LOW_COVERAGE, PECAN, LASTZ_NET, BLASTZ_NET, TRANSLATED_BLAT_NET)
        :param str species_set: the set of species used to define the pairwise
            alignment (multiple values). Should not be used with the
            species_set_group parameter. Use :meth:`get_info_compara_by_method`
            with one of the methods listed above to obtain a valid list of
            species sets. Any valid alias may be used. (e.g., musc_musculus,
            homo_sapiens)
        :param str species_set_group: The species set group name of the multiple
            alignment. Should not be used with the species_set parameter.
            Use /info/compara/species_sets/:method with one of the methods
            listed above to obtain a valid list of group names. (Defaults to
            mammals. e.g. mammals, amniotes, fish, sauropsids)


        """
        self._check_frmt(frmt, ['xml', 'phyloxml'])
        res = self.http_get("alignment/region/{0}/{1}".format(species, region),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'aligned':int(aligned), 'callback':self.callback,
                    'compact':compact, 'compara':compara,
                    'display_species_set': display_species_set,
                    'mask':mask, 'method':method, 'species_set':species_set,
                    'species_set_group': species_set_group})
        return res


    def get_homology_by_id(self, identifier, frmt='json', aligned=True,
            compara='multi',
            format=None, sequence=None, species=None, target_species=None,
            target_taxon=None, type='all'):
        """Retrieves homology information (orthologs) by Ensembl gene id"""
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("homology/id/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'aligned':int(aligned), 'callback':self.callback,
                    'compara':compara, 'format':format,'sequence':sequence,
                    'species': species,
                    'target_species':target_species, 'target_taxon':target_taxon,
                    'type': type})
        return res

    def get_homology_by_symbol(self, species, symbol, frmt='json',
            aligned=True, compara=None):
        """Retrieves homology information (orthologs) by symbol"""
        raise NotImplementedError("Please fill an issue her https://github.com/cokelaer/bioservices")
        # species='human', symbol='BRCA2'


    # CROSS REFERENCES
    # -------------------------------

    def get_xrefs_by_id(self, identifier, frmt='json', all_levels=False,
            db_type='core', external_db=None, object_type=None,
            species=None):
        """Perform lookups of Ensembl Identifiers and retrieve their external
        references in other databases

        :param str identifier: An Ensembl Stable ID (ENSG00000157764)
        :param str frmt: response formats: json, jsonp, nh, phyloxml
        :param bool all_levels: Set to find all genetic features linked to
            the stable ID, and fetch all external references for them.
            Specifying this on a gene will also return values from its
            transcripts and translations.
        :param str db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core
        :param str external_db: Filter by external database (e.g., HGNC)
        :param str object_type: filter by feature type (e.g., gene, transcript)
        :param str species: Species name/alias (human)

        """
        self._check_frmt(frmt)
        res = self.http_get('xrefs/id/{0}'.format(identifier), frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'db_type': db_type, 'callback':self.callback,
                    'db_type':db_type, 'all_levels': int(all_levels),
                    'external_db':external_db, 'object_type':object_type,
                    'species':species})
        return res

    def get_xrefs_by_name(self, name, species, frmt='json',
            db_type='core',
            external_db=None):
        """Performs a lookup based upon the primary accession or display label
        of an external reference and returning the information we hold about the
        entry

        :param str name: Symbol or display name of a gene (e.g., BRCA2)
        :param str species: Species name/alias (e.g., human)
        :param str frmt: response formats: json, jsonp,xml
        :param str db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core
        :param str external_db: Filter by external database (e.g., HGNC)


        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('xrefs/name/{0}/{1}'.format(species, name), frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'db_type': db_type, 'callback':self.callback,
                    'external_db': external_db})
        return res

    def get_xrefs_by_symbol(self, symbol, species, frmt='json',
            db_type='core',
            external_db=None, object_type=None
            ):
        """Looks up an external symbol and returns all Ensembl objects linked to
        it. This can be a display name for a gene/transcript/translation, a
        synonym or an externally linked reference. If a gene's transcript is
        linked to the supplied symbol the service will return both gene and
        transcript (it supports transient links).

        :param str species: Species name/alias (e.g., human)
        :param str symbol: Symbol or display name of a gene (BRCA2)
        :param str frmt: response formats: json, jsonp,xml
        :param str db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core
        :param str external_db: Filter by external database (e.g., HGNC)
        :param str object_type: filter by feature type (e.g., gene, transcript)

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('xrefs/symbol/{0}/{1}'.format(species, symbol), frmt=frmt,
                headers=self.get_headers(content=frmt),
        #      params = {'db_type': db_type, 'callback':self.callback,
        #           'object_type':object_type, 'external_db': external_db}
        )
        return res


    # INFORMATION
    # ---------------------------------------------------------------------------
    def get_info_analysis(self, species, frmt='json'):
        """List the names of analyses involved in generating Ensembl data.

        :param str species: Species name/alias (e.g., homo_sapiens)
        :param str frmt: response formats: json, jsonp,xml

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/analysis/{0}'.format(species), frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    def get_info_assembly(self, species, frmt='json', bands=False):
        """List the currently available assemblies for a species.

        :param str species: Species name/alias (e.g., homo_sapiens)
        :param str frmt: response formats: json, jsonp,xml
        :param bool bands: if set to 1, include karyotype band information.
            Only display if band information is available

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/assembly/{0}'.format(species), frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'bands': bands,'callback':self.callback})
        return res

    def get_info_assembly_by_region(self, species, region, frmt='json',
            bands=0 ):
        """Returns information about the specified toplevel sequence region for the
            given species."""
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/assembly/{0}/{1}'.format(species,region),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'bands': bands, 'callback':self.callback
                    })
        return res

    def get_info_biotypes(self, species, frmt='json'):
        """List the functional classifications of gene models that Ensembl associates
        with a particular species. Useful for restricting the type of genes/transcripts
        retrieved by other endpoints.

        :param str species: Species name/alias (e.g., homo_sapiens)
        :param str frmt: response formats: json, jsonp,xml

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/biotypes/{0}'.format(species), frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    def get_info_compara_methods(self, frmt='json', compara='multi',
            method_class=None):
        """List all compara analyses available (an analysis defines the type of
        comparative data).

        :param str frmt: response formats: json, yaml, jsonp, xml
        :param str class: The class of the method to query for.
            Regular expression patterns are supported.
            (Defaults to  GenomicAlign)
        :param str compara: Name of the compara database to use.
            Multiple comparas may exist on a server when accessing Ensembl Genomes data.

        .. note:: API argument is class, renamed in method_class

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/compara/methods', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'class':method_class, 'compara':compara,
                    'callback':self.callback})
        return res

    def get_info_compara_by_method(self, method, frmt='json', compara='multi',
            ):
        """List all collections of species analysed with the specified compara
        method.

        :param str method: Filter by compara method. Use one the
            methods returned by /info/compara/methods endpoint.
            e.g., EPO
        :param str frmt: response formats: json, jsonp,xml
        :param str compara: Name of the compara database to use. Multiple
            comparas may exist on a server when accessing Ensembl Genomes data.
            defaults to 'multi'

        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get('info/compara/species_sets/{0}'.format(method),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'compara':compara, 'callback':self.callback})
        return res

    def get_info_comparas(self, frmt='json' ):
        """Lists all available comparative genomics databases and their data release.

        :param str frmt: response formats: json, jsonp,xml
        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get('info/comparas', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    def get_info_data(self, frmt='json'):
        """Shows the data releases available on this REST server. May return more than
        one release (unfrequent non-standard Ensembl configuration).

        :param str frmt: response formats: json, jsonp,xml


        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/data', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    def get_info_external_dbs(self, species, frmt='json',
            filter=None):
        """Lists all available external sources for a species.

        :param str frmt: response formats: json, jsonp,xml
        :param str species: Species name/alias
        :param str filter: Restrict external DB searches to a single
            source or pattern. SQL-LIKE patterns are supported.
            See :class:`Ensembl` doc.


        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/external_dbs/{0}'.format(species),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback, 'filter':filter})
        return res

    def get_info_ping(self, frmt='json'):
        """Checks if the service is alive."""
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/ping/', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res['ping']

    def get_info_rest(self, frmt='json'):
        """Shows the current version of the Ensembl REST API.

        :param str frmt: response formats: json, jsonp,xml

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/rest/', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    def get_info_software(self, frmt='json'):
        """Shows the current version of the Ensembl API used by the REST server.

        :param str frmt: response formats: json, jsonp,xml
        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/software/', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    def get_info_species(self, frmt='json'):
        """Lists all available species, their aliases, available adaptor groups and data
        release.

        :param str frmt: response formats: json, jsonp,xml

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('info/species/', frmt=frmt,
                headers=self.get_headers(content=frmt),
                params = {'callback':self.callback})
        return res

    # LOOKUP
    # -------------------------------------------------------------------
    def get_lookup_by_id(self, identifier, frmt='json',
            db_type=None, expand=False,
            format='full', species=None):
        """Find the species and database for a single identifier

        :param str identifier: An ontology term identifier (e.g., GO:0005667)
        :param str frmt: response formats in json, xml, jsonp
        :param str db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core. Defaults
            to core
        :param str expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param str format: Specify the formats to emit from this endpoint
        :param str species: Species name/alias (e.g., human)

        ::

            get_lookup_by_id('ENSG00000157764', expand=True)

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("lookup/id/" + identifier, frmt=frmt,
                headers = self.get_headers(content=frmt),
                params = {'db_type': db_type, 'expand': int(expand), 'format': format,
                    'callback': self.callback, 'species': species})
        return res

    def post_lookup_by_id(self, identifiers, frmt='json',
            db_type=None, expand=False,
            format='full', object_type=None, species=None):
        """Find the species and database for a single identifier

        :param str identifier: An ontology term identifier (e.g., GO:0005667)
        :param str frmt: response formats in json, xml, jsonp
        :param str db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core. Defaults
            to core
        :param str expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param str format: Specify the formats to emit from this endpoint
        :param str object_type: Filter by feature type (e.g., gene, transcript)
        :param str species: Species name/alias (e.g., human)

        ::

            post_lookup_by_id(["ENSG00000157764", "ENSG00000248378" ])

        .. todo: frmt can only be json or jsonp
        """
        self._check_frmt(frmt)
        identifiers = self.devtools.to_list(identifiers)
        expand = int(expand)
        res = self.http_post("lookup/id/", frmt=frmt,
                headers = self.get_headers(content=frmt),
                data =self.devtools.to_json({'ids':identifiers}),
                params={'db_type': db_type, 'expand': expand, 'format': format,
                    'callback': self.callback, 'species': species})
        return res

    def get_lookup_by_symbol(self, species, symbol, frmt='json',
            expand=False,
            format='full',):
        """Find the species and database for a single identifier

        :param str species: Species name/alias (e.g., human)
        :param str symbol: A name or symbol from an annotation source has been
            linked to a genetic feature. e.g., BRCA2
        :param str frmt: response formats in json, xml, jsonp
        :param str expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param str format: Specify the formats to emit from this endpoint

        ::

            get_lookup_by_symbol('homo_sapiens', 'BRCA2', expand=True)

        """
        self._check_frmt(frmt, ['xml'])
        expand = int(expand)
        res = self.http_get("lookup/symbol/{0}/{1}".format(species, symbol),
                frmt=frmt,
                headers = self.get_headers(content=frmt),
                params = {'format': format,
                    'callback': self.callback, 'expand':expand})
        return res

    def post_lookup_by_symbol(self, species, symbols, frmt='json',
            expand=False,
            format='full',):
        """Find the species and database for a set of symbols

        :param str species: Species name/alias (e.g., human)
        :param list symbols: A list of names or symbols from an annotation source has been
            linked to a genetic feature. e.g., BRCA2
        :param str frmt: response formats in json, xml, jsonp
        :param str expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param str format: Specify the formats to emit from this endpoint

        ::

            post_lookup_by_symbol('homo_sapiens', ['BRCA2', 'BRAF'], expand=True)

        """
        self._check_frmt(frmt, ['xml'])
        symbols = self.devtools.tolist(symbols)
        expand = int(expand)
        res = self.http_post("lookup/symbol/{0}".format(species),
                frmt=frmt,
                headers = self.get_headers(content=frmt),
                data = self.devtools.to_json({'symbols':symbols}),
                params = {'format': format,
                    'callback': self.callback, 'expand':expand})
        return res

    # MAPPING
    # --------------------------------------------------------------------

    def get_map_cds_to_region(self, identifier, region, frmt='json',
            species=None):
        """Convert from cDNA coordinates to genomic coordinates.

        :param identifier: Ensembl ID e.g. ENST00000288602
        :param region: Query region e.g., 100..300

        Output reflects forward orientation coordinates as returned from the Ensembl API.


            get_map_cds_to_region('ENST00000288602', '1..1000')
        """
        self._check_frmt(frmt, ['json'])
        res = self.http_get("map/cds/{0}/{1}".format(identifier, region),
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'species':species})

        return res

    def get_map_cdna_to_region(self, identifier, region, frmt='json',
            species=None):
        """ Convert from cDNA coordinates to genomic coordinates.

        :param str first: version of the input assembly
        :param str first: version of the output assembly
        :param str region:  query region (see example)
        :param str species: default to human

        Output reflects forward orientation coordinates as returned from the Ensembl API.


        ::

            get_map_cdna_to_region('ENST00000288602', '100..300')

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("map/cdna/{0}/{1}".format(identifier, region),
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'species':species})
        return res

    def get_map_assembly_one_to_two(self, first, second, region, species='human',
        frmt='json'):
        """Convert the co-ordinates of one assembly to another


        :param str first: version of the input assembly
        :param str first: version of the output assembly
        :param str region:  query region (see example)
        :param str species: default to human

        ::

            e.get_map_assembly_one_to_two(species='human',
                first='GRCh37', region='X:1000000..1000100:1', second='GRCh38')

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("map/{0}/{1}/{2}/{3}".format(species, first, region, second ),
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={})
        return res

    def get_map_translation_to_region(self, identifier, region, frmt='json',
            species=None):
        """Convert from protein (translation) coordinates to genomic coordinates.

        Output reflects forward orientation coordinates as returned from the
        Ensembl API.

        :param identifier: a stable Ensembl ID
        :param str query: a query region
        :param str species: Species name/alias (e.g., homo_sapiens)

        ::

            get_map_translation_to_region('ENSP00000288602', '100..300')
        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("map/translation/{0}/{1}".format(identifier, region),
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={'callback':self.callback})
        return res


    # ONTOLOGY and Taxonomy
    # -------------------------------------------------------------------------

    def get_ontology_by_id(self, identifier, frmt='json',
            relation=None, simple=False):
        """Search for an ontological  term by its namespaced identifier

        :param str identifier: An ontology term identifier (e.g., GO:0005667)
        :param bool simple: If set the API will avoid the fetching of parent and child terms
        :param str frmt: response formats in json, xml, yaml, jsonp
        :param str simple: If set the API will avoid the fetching of parent and child terms
        :param str relation: The types of relationships to include in the output. Fetches
            all relations by default (e.g., is_a, part_of)

        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_ontology('GO:0005667')

        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        identifier = str(identifier)
        res = self.http_get("ontology/id/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'simple': int(simple), 'relation':relation,
                    'callback':self.callback})
        return res

    def get_ontology_by_name(self, name, frmt='json',
            ontology=None, relation=None, simple=False):
        """Search for a list of ontological terms by their name

        :param str name: An ontology name. SQL wildcards See :class:`Ensembl` doc.
        :param str frmt: response formats in json, xml, yaml, jsonp
        :param str simple: If set the API will avoid the fetching of parent and child terms
        :param str relation: The types of relationships to include in the output. Fetches
            all relations by default (e.g., is_a, part_of)
        :param str ontology: Filter by ontology. Used to disambiguate terms which are
            shared between ontologies such as GO and EFO (e.g., GO)


        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_ontology_by_name('transcription factor')
            400
            >>> res = e.get_ontology_by_name('transcription factor complex')
            >>> res[0]['children']

        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("ontology/name/{0}".format(name), frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'simple':int(simple), 'relation':relation,
                    'callback':self.callback, 'ontology':ontology})
        return res

    def get_taxonomy_by_id(self, identifier, frmt='json', simple=False):
        """Search for a taxonomic term by its identifier or name

        :param str identifier: A taxon identifier. Can be a NCBI taxon id or
            a name (e.g., 9606 or Homo sapiens)
        :param bool simple: If set the API will avoid the fetching of parent and child terms
        :param str frmt: response formats in json, xml, yaml, jsonp
        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("taxonomy/id/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'simple':int(simple)})
        return res

    def get_taxonomy_by_name(self, name, frmt='json'):
        """Search for a taxonomic id by a non-scientific name

        :param str name: A non-scientific species name. Can include SQL wildcards
            See :class:`Ensembl` doc.
        :param str frmt: response formats in json, xml, yaml, jsonp

        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_taxonomy_by_name('homo')

        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("taxonomy/name/{0}".format(name),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback})
        return res

    def get_taxonomy_classification_by_id(self, identifier, frmt='json',
            ):
        """Return the taxonomic classification of a taxon node


        :param str identifier: A taxon identifier. Can be a NCBI taxon id or a name
            (e.g., 9606, Homo sapiens)
        :param str frmt: json, xml, yaml, jsonp

        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_taxonomy_classification_by_id('9606')

        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("taxonomy/classification/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback})
        return res

    def get_ontology_ancestors_by_id(self, identifier, frmt='json',
            ontology=None):
        """Reconstruct the entire ancestry of a term from is_a and part_of
        relationships

        :param str identifier: An ontology term identifier (e.g., GO:0005667)
        :param str frmt: json, xml, yaml, jsonp
        :param str ontology: Filter by ontology. Used to disambiguate
            terms which are shared between ontologies such as GO and EFO (e.g.,
            GO)


        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("ontology/ancestors/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'ontology':ontology})
        return res

    def get_ontology_ancestors_chart_by_id(self, identifier, frmt='json',
            ontology=None):
        """Reconstruct the entire ancestry of a term from is_a and part_of
        relationships.

        :param str identifier: an ontology term identifier (GO:0005667)
        :param str frmt: json, xml, yaml, jsonp
        :param str ontology: Filter by ontology. Used to disambiguate
            terms which are shared between ontologies such as GO and EFO

        """
        self._check_frmt(frmt, ['xml', 'yaml'])
        res = self.http_get("ontology/ancestors/chart/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'ontology':ontology})
        return res
        #'getAncestorsChartById': {'url': '/ontology/ancestors/chart/{{id}}',

    def get_ontology_descendants_by_id(self, identifier, frmt='json',
            closest_term=None, ontology=None, subset=None, zero_distance=None):
        """ Find all the terms descended from a given term. By default searches
        are conducted within the namespace of the given identifier

        :param str identifier: an ontology term identifier (GO:0005667)
        :param str frmt: json, xml, jsonp
        :param bool closest_term: If true return only the closest terms to the
            specified term
        :param str ontology: Filter by ontology. Used to disambiguate terms
            which are shared between ontologies such as GO and EFO
        :param str subset: Filter terms by the specified subset
        :param bool zero_distance: Return terms with a distance of 0

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("ontology/descendants/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'ontology':ontology,
                    'closest_term': closest_term, 'subset':subset,
                    'zero_distance': zero_distance})
        return res

    # OVERLAP
    # -----------------------------------------------------
    def get_overlap_by_id(self, identifier, feature=None, frmt='json',
            biotype=None, db_type=None, logic_name=None,
            misc_set=None, object_type=None, so_term=None, species=None,
            species_set='mammals'):
        """Retrieves features (e.g. genes, transcripts, variations etc.)
        that overlap a region defined by the given identifier.

        :param str identifier: An Ensemble stable ID
        :param str feature: The type of feature to retrieve. Multiple values
            are accepted. Value in Enum(gene, transcript, cds, exon, repeat,
            simple, misc, variation, somatic_variation, structural_variation,
            somatic_structural_variation, constrained, regulatory
        :param str biotype: The functional classification of the gene or
            transcript to fetch. Cannot be used in conjunction with logic_name
            when querying transcripts. (e.g., protein_coding)
        :param str db_type: Restrict the search to a database other than
            the default. Useful if you need to use a DB other than core
        :param str logic_name: Limit retrieval of genes, transcripts and
            exons by a given name of an analysis.
        :param str misc_set: Miscellaneous set which groups together
            feature entries. Consult the DB or returned data sets to discover
            what is available. (e.g., cloneset_30k
        :param str object_type: Filter by feature type (e.g., gene)
        :param str so_term: Sequence Ontology term to narrow down the
            possible variations returned. (e.g., SO:0001650)
        :param str species: Species name/alias.
        :param str species_set: Filter by species set for
            retrieving constrained elements. (e.g. mammals)

        """
        self._check_frmt(frmt, ['xml', 'gff3', 'bed'])
        res = self.http_get("overlap/id/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'biotype':biotype,
                    'db_type':  db_type, 'logic_name': logic_name,
                    'misc_set': misc_set, 'object_type': object_type,
                    'so_term': so_term, 'species': species,'feature':feature,
                    'species_set': species_set})
        return res

    def get_overlap_by_region(self, region, species, feature=None,
            frmt='json', biotype=None, cell_type=None,
            db_type=None, logic_name=None,
            misc_set=None, object_type=None, so_term=None,
            species_set=None, trim_downstream=False, trim_upstream=False):
        """Retrieves multiple types of features for a given region.

        :param str region: Query region. A maximum of 5Mb is allowed to
            be requested at any one time. e.g.,  X:1..1000:1, X:1..1000:-1,
            X:1..1000
        :param str species: Species name/alias.
        :param str feature: The type of feature to retrieve. Multiple
            values are accepted: gene, transcript, cds, exon, repeat,
            simple, misc, variation, somatic_variation, structural_variation,
            somatic_structural_variation, constrained, regulatory
        :param str biotype: The functional classification of the gene or
            transcript to fetch. Cannot be used in conjunction with logic_name
            when querying transcripts. (e.g., protein_coding)
        :param cell_type: Cell type name in Ensembl's Regulatory Build,
            required for segmentation feature, optional for regulatory elements.
            e.g., K562
        :param str db_type: Restrict the search to a database other than
            the default. Useful if you need to use a DB other than core
        :param str logic_name: Limit retrieval of genes, transcripts and
            exons by a given name of an analysis.
        :param str misc_set: Miscellaneous set which groups together
            feature entries. Consult the DB or returned data sets to discover
            what is available. (e.g., cloneset_30k)
        :param str so_term: Sequence Ontology term to narrow down the
            possible variations returned. (e.g., SO:0001650)
        :param str species_set: Filter by species set for
            retrieving constrained elements. (e.g. mammals)
        :param bool trim_downstream: Do not return features which overlap
            the downstream end of the region.
        :param bool trim_upstream: Do not return features which overlap
            upstream end of the region.

        .. todo:: feature can take several values. how can be do that.
        """
        self._check_frmt(frmt, ['xml', 'gff3', 'bed'])
        res = self.http_get("overlap/region/{0}/{1}".format(species, region),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'biotype':biotype,
                    'cell_type': cell_type, 'feature':feature,
                    'db_type':  db_type, 'logic_name': logic_name,
                    'misc_set': misc_set,
                    'so_term': so_term, 'species_set': species_set,
                    'trim_downstream': trim_downstream,
                    'trim_upstream': trim_upstream
                    })
        return res

    def get_overlap_by_translation(self, identifier, frmt='json',
            db_type=None, feature='protein_feature',
            so_term=None, species=None,type='none'):
        """Retrieve features related to a specific Translation as
        described by its stable ID (e.g. domains, variations).

        :param str identifier:
        :param str frmt:
        :param str db_type: Restrict the search to a database other
            than the default. Useful if you need to use a DB other than core
        :param str feature: requested feature in: transcript_variation,
            protein_feature, residue_overlap, translation_exon,
            somatic_transcript_variation
        :param str so_term: Sequence Ontology term to restrict the variations
            found. Its descendants are also included in the search. (e.g.,
            SO:0001650)
        :param str species: species name/alias
        :param str type: Type of data to filter by. By default, all
            features are returned. Can specify a domain or consequence
            type. (e.g.,  low_complexity)
        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("overlap/translation/{0}".format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback,
                    'db_type':  db_type, 'feature': feature,
                    'so_term': so_term, 'species': species,
                    'type': type})
        return res

    # REGULATION
    # --------------------------------------
    def get_regulatory_by_id(self, identifier, species, frmt='json',
            ):
        """Returns a RegulatoryFeature given its stable ID

        :param str identifier:
        :param str species:


        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get("regulatory/{0}/{1}".format(species, identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback})
        return res


    # SEQUENCE
    # -----------------------------
    def get_sequence_by_id(self, identifier, frmt='fasta',
            db_type=None, expand_3prime=None,
            expand_5prime=None, format=None, mask=None,
            mask_feature=False, multiple_sequences=False,
            object_type=None, species=None, type='genomic'):
        """Request multiple types of sequence by stable identifier.

        :param str identifier:
        :param str frmt: response formats: fasta, json, text, yam, jsonp
        :param str db_type: Restrict the search to a database other than the
            default. Useful if you need to use a DB other than core (e.g.,
            core)
        :param int expand_3prime: Expand the sequence downstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param int expand_5prime: Expand the sequence upstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param str format: Format of the data (e.g., fasta)
        :param str mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters. Only available when using genomic
            sequence type. (hard/soft)
        :param bool mask_feature: Mask features on the sequence. If sequence
            is genomic, mask introns. If sequence is cDNA, mask UTRs.
            Incompatible with the 'mask' option
        :param bool multiple_sequences: Allow the service to return more
            than 1 sequence per identifier. This is useful when querying
            for a gene but using a type such as protein.
        :param str object_type: Filter by feature type (e.g., gene)
        :param str species: Species name/alias (e.g., homo_sapiens)
        :param str type:. could be genomic, cds, cdna, protein (homo_sapiens).
            Requesting a gene and kind not equal to genomic may result in
            multiple sequence, which required the parameter multi_sequences
            to be set to True

        ::

            >>> # Default format is fasta, let us use parameter frmt to overwrite it
            >>> sequence = e.get_sequence('ENSG00000157764', frmt='text')
            >>> print(sequence[0:10])
            CGCCTCCCTTCCCCCTCCCC

            >>> # complex request for different database and kind
            >>> res = e.get_sequence('CCDS5863.1', frmt='fasta',
                    object_type='transcript', db_type='otherfeatures',
                    type='cds', species='human')
            >>> print(res[0:100])
            >CCDS5863.1
            ATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGGCTCTGTTCAAC
            GGGGACATGGAGCCCGAGGCCGGCGCC

            >>>


        """
        self._check_frmt(frmt, ['fasta', 'text', 'yaml', 'seqxml'])
        multiple_sequences = int(multiple_sequences)
        res = self.http_get('sequence/id/{0}'.format(identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={
                    'db_type': db_type, 'object_type':object_type,
                    'multiple_sequences':multiple_sequences,  'species':species,
                    'expand_3prime':expand_3prime,
                    'expand_5prime':expand_5prime,'format':format,'mask':mask,
                    'mask_feature':mask_feature, 'type':type,
                    'multiple_sequences':multiple_sequences,'species':species}
                )
        return res

    def get_sequence_by_region(self, region, species, frmt='json',
            coord_system=None, coord_system_version=None,
            expand_3prime=None,
            expand_5prime=None, format=None, mask=None,
            mask_feature=False):
        """Returns the genomic sequence of the specified region of the given species.

        :param str region: Query region. A maximum of 10Mb is allowed to be
            requested at any one time. e.g.,  X:1000000..1000100:1
        :param str species: Species name/alias
        :param str coord_system: Filter by coordinate system name (e.g., contig,
            seqlevel)
        :param str  coord_system_version: Filter by coordinate system version
            (e.g., GRCh37)
        :param int expand_3prime: Expand the sequence downstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param int expand_5prime: Expand the sequence upstream of the
            sequence by this many basepairs. Only available when using
            genomic sequence type.
        :param str format: Format of the data. (e.g., fasta)
        :param str mask: Request the sequence masked for repeat sequences.
            Hard will mask all repeats as N's and soft will mask repeats
            as lowercased characters. Only available when using genomic
            sequence type. (hard/soft)
        :param bool mask_feature: Mask features on the sequence. If sequence
            is genomic, mask introns. If sequence is cDNA, mask UTRs.
            Incompatible with the 'mask' option

        """
        self._check_frmt(frmt, ['fasta', 'text', 'yaml', 'seqxml'])
        res = self.http_get('sequence/region/{0}/{1}'.format(species, region),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={
                    'callback': self.callback, 'coord_system':coord_system,
                    'coord_system_version': coord_system_version,
                    'expand_3prime':expand_3prime,
                    'expand_5prime':expand_5prime,'format':format,'mask':mask,
                    'mask_feature':mask_feature}
                )
        return res


    # VARIATION
    # -----------------------------------------------------
    def get_variation_by_id(self, identifier, species, frmt='json',
            genotypes=False, phenotypes=False,
            pops=False):
        """

        :param str identifier: variation identifier (e.g., rs56116432)
        :param str species: Species name/alias (e.g., homo_sapiens)
        :param str frmt: response format (json, xml, jsonp)
        :param bool genotypes: Include genotypes
        :param bool phenotypes: Include phenotypes
        :param bool pops: Include populations

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('variation/{0}/{1}'.format(species, identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'genotypes':int(genotypes), 'phenotypes':int(phenotypes),
                    'pops': int(pops)}
                )
        return res

    def get_vep_by_id(self, identifier, species, frmt='json',
            canonical=False, ccds=False, domains=False,
            hgvs=False, numbers=False, protein=False, xref_refseq=False):
        """Fetch variant consequences based on a variation identifier

        :param str identifier: Query ID. Supports dbSNP, COSMIC and
            HGMD identifiers   (e.g.,    rs116035550, COSM476)
        :param str species: Species name/alias
        :param bool canonical: Include a flag indicating the canonical transcript for a gene
        :param bool ccds: Include CCDS transcript identifiers
        :param bool domains:Include names of overlapping protein domains
        :param bool hgvs: Include HGVS nomenclature based on Ensembl stable identifiers
        :param bool numbers: Include affected exon and intron positions within the transcript
        :param bool protein: Include Ensembl protein identifiers
        :param bool xref_refseq: Include aligned RefSeq mRNA identifiers for
            transcript. NB: theRefSeq and Ensembl transcripts aligned in this
            way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence,
            exon structure and protein product
        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('vep/{0}/id/{1}'.format(species, identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'canonical':canonical,
                    'ccds':ccds, 'domains':domains,
                    'hgvs': hgvs, 'numbers':numbers, 'protein': protein,
                    'xref_refseq': xref_refseq})
        return res


    def post_vep_by_id(self, species, identifiers):
        raise NotImplementedError
        #POST vep/:species/id/   Fetch variant consequences for multiple ids
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('variation/{0}/{1}'.format(species, identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'genotypes':int(genotypes), 'phenotypes':int(phenotypes),
                    'pops': int(pops)}
                )
        raise NotImplementeError

    def get_vep_by_region(self, region, allele, species, frmt='json',
            canonical=False, ccds=False, domains=False,
            hgvs=False, numbers=False, protein=False, xref_refseq=False):
        """Fetch variant consequences

        :param region: Query region e.g,  9:22125503-22125502:1
        :param str allele: Variation allele (e.g., C, DUP)
        :param str species: Species name/alias
        :param bool canonical: Include a flag indicating the canonical transcript for a gene
        :param bool ccds: Include CCDS transcript identifiers
        :param bool domains:Include names of overlapping protein domains
        :param bool hgvs: Include HGVS nomenclature based on Ensembl stable identifiers
        :param bool numbers: Include affected exon and intron positions within the transcript
        :param bool protein: Include Ensembl protein identifiers
        :param bool xref_refseq: Include aligned RefSeq mRNA identifiers for
            transcript. NB: theRefSeq and Ensembl transcripts aligned in this
            way MAY NOT, AND FREQUENTLY WILL NOT, match exactly in sequence,
            exon structure and protein product

        """
        self._check_frmt(frmt, ['xml'])
        res = self.http_get('vep/{0}/region/{1}/{2}'.format(species, region, allele),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':self.callback, 'canonical':canonical,
                    'ccds':ccds, 'domains':domains,
                    'hgvs': hgvs, 'numbers':numbers, 'protein': protein,
                    'xref_refseq': xref_refseq})
        return res

    def post_vep_by_region(self, species, region):
        #POST vep/:species/region/   Fetch variant consequences for multiple regions
        raise NotImplementeError


