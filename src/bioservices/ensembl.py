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
"""Interface to some part of the UniProt web service

.. topic:: What is UniProt ?

    :URL:
    :URL: https://github.com/Ensembl/ensembl-rest/wiki/Output-formats
    :Citation:

    .. highlights::


        -- From Uniprot web site (help/about) , Dec 2012


"""
from bioservices.services import REST

__all__ = ["Ensembl"]

"""
if e.code == 429:
    if 'Retry-After' in e.headers:
        retry = e.headers['Retry-After']
        time.sleep(float(retry))
        self.perform_rest_action(endpoint, hdrs, params)
    else:
        sys.stderr.write('Request failed for {0}: Status code: {1.code} Reason: {1.reason}\n'.format(endpoint, e))
"""


class Ensembl(REST):
    """Interface to the `Ensembl <http://rest.ensembl.org>`_ service


    """
    _url = "http://rest.ensembl.org"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        super(Ensembl, self).__init__(name="Ensembl", url=Ensembl._url,
                verbose=verbose, cache=cache)

    def _check_frmt(self, frmt):
        self.devtools.check_param_in_list(frmt, ['json', 'xml', 'jsonp',
        'phyloxml'])

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
    def post_archive(self, identifiers, frmt='json', callback=None):
        """Retrieve the archived sequence for a set of identifiers"""
        raise NotImplementedError

    def get_archive(self, identifier, frmt='json', callback=None):
        """Uses the given identifier to return the archived sequence


        :param str identifier: An Ensembl stable ID


        ::

            >>> from bioservices import Ensembl
            >>> s = Ensembl()
            >>> res = s.get_archive("ENSG00000157764")

        """
        # TODO, jsonp needs example
        # :param str callback: Name of the callback subroutine to be returned by the requested JSONP
        #     response. Required ONLY when using JSONP as the serialisation method.

        # If one identifier, use get. If a list, use post.
        # We can simplify the interface by transforming input string into a list and therefore
        # always call the POST
        self._check_frmt(frmt)
        self._check_id(identifier)
        res = self.http_get("archive/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':callback})

        #FIXME: could not find a way to make this to work with POST method.
        #identifiers = self.devtools.tolist(identifier)
        #res = self.http_post("archive/id", frmt=frmt,
        #        data={'id':identifiers},
        #        headers=self.get_headers(content=frmt))

        if frmt == 'xml':
            res = self.easyXML(res)
        return res


    # COMPARATIVE GENOMICS
    # ------------------------------------------------------------------

    def get_genetree_by_member_symbol(self, species, symbol, frmt='json',
            aligned=False, db_type='core', object_type=None,
            nh_format='simple', sequence='protein',
            callback='randomlygeneratedname', compara='multi'):
        """ Retrieves a gene tree containing the gene identified by a symbol"""
        self._check_frmt(frmt)
        frmt = self.nh_format_to_frmt(nh_format)
        aligned = int(aligned)
        self.check_sequence(sequence)
        self.check_nh_format(nh_format)

        res = self.http_get("genetree/member/symbol/%s/%s" %(species, symbol),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence, 
                    'aligned':aligned, 'compara':compara, 
                    'db_type':db_type}
                )

        return res

    def get_genetree_by_member_id(self, identifier, frmt='json',
            aligned=False, db_type='core', object_type=None,
            nh_format='simple', sequence='protein', species='homo_sapiens',
            callback='randomlygeneratedname', compara='multi'):
        """GET genetree/member/symbol/:species/:symbol     
        Retrieves a gene tree containing the gene identified by a symbol

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
        self._check_frmt(frmt)
        self.check_nh_format(nh_format)
        frmt = self.nh_format_to_frmt(nh_format)
        if aligned is True:
            aligned = 1
        elif aligned is False:
            aligned = 0

        self.check_sequence(sequence)

        res = self.http_get("genetree/member/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence, 
                    'aligned':aligned, 'compara':compara, 
                    'db_type':db_type, 'species':species}
                )
        return res

    def get_genetree_by_id(self, identifier, aligned=False, frmt='json',
            nh_format='simple', sequence='protein', 
            callback='randomlygeneratedname', compara='multi'):
        """Retrieves a gene tree dump for a gene tree stable identifier

        :param str identifier: An Ensembl genetree ID
        :param str frmt: response formats: json, jsonp, nh, phyloxml
        :param bool aligned: if true, return the aligned string otherwise, i
            return the original
            sequence (no insertions). Can be True/1 or False/0 and defaults to 0
        :param str callback: use if frmt is 'json' only. Name of the callback subroutine to be
            returned by the requested JSONP response.
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
        #self.devtools.ckeck_param_in_list(frmt, ['nh', 'phyloxml', 'josn', 
        #    'jsonp'])
        self.check_nh_format(nh_format)
        aligned = int(aligned)
        self.check_sequence(sequence)

        res = self.http_get("genetree/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence, 'aligned':aligned}
                )
        return res


    def get_alignment_by_region(self, species, region, frmt='json'):
        """Retrieves genomic alignments as separate blocks based on a region and
        species"""
        raise NotImplementedError


    def get_homology_by_id(self, identifier, frmt='json'):
        """Retrieves homology information (orthologs) by Ensembl gene id"""
        raise NotImplementedError
        # d(id='ENSG00000157764'

    def get_homology_by_symbol(self, species, symbol, frmt='json'):
        """Retrieves homology information (orthologs) by symbol"""
        raise NotImplementedError
        # species='human', symbol='BRCA2'


    # CROSS REFERENCES
    # -------------------------------

    def get_xrefs_by_id(self, identifier, frmt='json'):
        """Perform lookups of Ensembl Identifiers and retrieve their external
        references in other databases"""
        # '/xrefs/id/{id}'
        raise NotImplementedError

    def get_xrefs_by_name(self, species, name, frmt='json'):
        """Performs a lookup based upon the primary accession or display label
        of an external reference and returning the information we hold about the
        entry"""
        #  '/xrefs/name/{species}/{name}'
        raise NotImplementedError

    def get_xrefs_by_symbol(self, species, symbol, frmt='json'): 
        """Looks up an external symbol and returns all Ensembl objects linked to
        it. This can be a display name for a gene/transcript/translation, a
        synonym or an externally linked reference. If a gene's transcript is
        linked to the supplied symbol the service will return both gene and
        transcript (it supports transient links)."""
        #
        raise NotImplementedError

        # '/xrefs/symbol/{species}/{symbol}'

    # INFORMATION 
    # ---------------------------------------------------------------------------
    def get_info_analysis(self, species, frmt='json'):
        """List the names of analyses involved in generating Ensembl data."""
        raise NotImplementedError
        # /info/analysis/{species}


    def get_info_assembly(self, species, frmt='json'): 
        """List the currently available assemblies for a species."""
        raise NotImplementedError
        # 'info/assembly/{species}

    def get_info_assembly_by_region(self, species, region, frmt='json'):
        """Returns information about the specified toplevel sequence region for the
            given species."""
        # info/assembly/:species/:region_name
        raise NotImplementedError

    def get_info_biotypes(self, species, frmt='json'):
        """List the functional classifications of gene models that Ensembl associates
        with a particular species. Useful for restricting the type of genes/transcripts
        retrieved by other endpoints."""
        # GET info/biotypes/:species 
        raise NotImplementedError

    def get_info_compara_methods(self, frmt='json'):
        """List all compara analyses available (an analysis defines the type of
        comparative data)."""
        # info/compara/methods  
        raise NotImplementedError

    def get_info_compara_by_method(self, species, frmt='json'):
        """List all collections of species analysed with the specified compara
        method."""
        raise NotImplementedError
        # GET info/compara/species_sets/:method  

    def get_info_comparas(self, frmt='json'):
        """Lists all available comparative genomics databases and their data release."""
        raise NotImplementedError
        # GET info/comparas   Lists all available comparative genomics databases and their data release.

    def get_info_data(self, frmt='json'):
        """Shows the data releases available on this REST server. May return more than
        one release (unfrequent non-standard Ensembl configuration)."""
        raise NotImplementedError
        # GET info/data  

    def get_info_external_dbs(self, species, frmt='json'):
        """Lists all available external sources for a species."""
        raise NotImplementedError
        # GET info/external_dbs/:species  Lists all available external sources for a species.

    def get_info_ping(self, frmt='json'):
        """Checks if the service is alive."""
        res = self.http_get('info/ping/', frmt=frmt,
                headers=self.get_headers(content=frmt))
        try:
            return res['ping']
        except:
            return res

    def get_info_rest(self, frmt='json'):
        """Shows the current version of the Ensembl REST API."""
        res = self.http_get('info/rest/', frmt=frmt,
                headers=self.get_headers(content=frmt))
        try:
            return res['release']
        except:
            return res

    def get_info_software(self, frmt='json'):
        """Shows the current version of the Ensembl API used by the REST server."""
        res = self.http_get('info/software/', frmt=frmt,
                headers=self.get_headers(content=frmt))
        try:
            return res['software']
        except:
            return res

    def get_info_species(self, frmt='json'):
        """Lists all available species, their aliases, available adaptor groups and data
        release."""
        res = self.http_get('info/species/', frmt=frmt,
                headers=self.get_headers(content=frmt))
        try:
            return res['species']
        except:
            return res



    # LOOKUP 
    # -------------------------------------------------------------------
    def get_lookup_by_id(self, identifier, frmt='json',
            callback='randomlygeneratedname', db_type=None, expand=False,
            format='full', species=None):
        """Find the species and database for a single identifier

        :param str identifier: An ontology term identifier (e.g., GO:0005667)
        :param str frmt: response formats in json, xml, jsonp
        :param str callback: see class documentation
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
        self._check_frmt(frmt)
        expand = int(expand)
        res = self.http_get("lookup/id/" + identifier, frmt=frmt,
                headers = self.get_headers(content=frmt),
                params = {'db_type': db_type, 'expand': expand, 'format': format,
                    'callback': callback, 'species': species})
        return res

    def post_lookup_by_id(self, identifiers, frmt='json',
            callback='randomlygeneratedname', db_type=None, expand=False,
            format='full', object_type=None, species=None):
        """Find the species and database for a single identifier

        :param str identifier: An ontology term identifier (e.g., GO:0005667)
        :param str frmt: response formats in json, xml, jsonp
        :param str callback: see class documentation
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
        identifiers = self.devtools.tolist(identifiers)
        self._check_frmt(frmt)
        expand = int(expand)
        res = self.http_post("lookup/id/", frmt=frmt,
                headers = self.get_headers(content=frmt),
                data =self.devtools.to_json({'ids':identifiers}),
                params={'db_type': db_type, 'expand': expand, 'format': format,
                    'callback': callback, 'species': species})
        return res

    def get_lookup_by_symbol(self, species, symbol, frmt='json',
            callback='randomlygeneratedname', expand=False,
            format='full',):
        """Find the species and database for a single identifier

        :param str species: Species name/alias (e.g., human)
        :param str symbol: A name or symbol from an annotation source has been
            linked to a genetic feature. e.g., BRCA2
        :param str frmt: response formats in json, xml, jsonp
        :param str callback: see class documentation
        :param str expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param str format: Specify the formats to emit from this endpoint

        :: 

            get_lookup_by_symbol('homo_sapiens', 'BRCA2', expand=True)

        """
        self._check_frmt(frmt)
        expand = int(expand)
        res = self.http_get("lookup/symbol/{0}/{1}".format(species, symbol), 
                frmt=frmt,
                headers = self.get_headers(content=frmt),
                params = {'format': format,
                    'callback': callback, 'expand':expand})
        return res

    def post_lookup_by_symbol(self, species, symbols, frmt='json',
            callback='randomlygeneratedname', expand=False,
            format='full',):
        """Find the species and database for a set of symbols

        :param str species: Species name/alias (e.g., human)
        :param list symbols: A list of names or symbols from an annotation source has been
            linked to a genetic feature. e.g., BRCA2
        :param str frmt: response formats in json, xml, jsonp
        :param str callback: see class documentation
        :param str expand: Expands the search to include any connected features.
            e.g. If the object is a gene, its transcripts, translations and exons
            will be returned as well.
        :param str format: Specify the formats to emit from this endpoint

        :: 

            post_lookup_by_symbol('homo_sapiens', ['BRCA2', 'BRAF'], expand=True)

        """
        symbols = self.devtools.tolist(symbols)
        self._check_frmt(frmt)
        expand = int(expand)
        res = self.http_post("lookup/symbol/{0}".format(species),
                frmt=frmt,
                headers = self.get_headers(content=frmt),
                data = self.devtools.to_json({'symbols':symbols}),
                params = {'format': format,
                    'callback': callback, 'expand':expand})
        return res




    # MAPPING
    # --------------------------------------------------------------------

    def get_map_cds_to_region(self, identifier, region, frmt='json',
            callback='randomlygeneratedname', species=None):
        """

            get_map_cds_to_region('ENST00000288602', '1..1000')
        """
        self._check_frmt(frmt)
        res = self.http_get("map/cds/{0}/{1}".format(identifier, region),
                frmt=frmt,  headers=self.get_headers(content=frmt),
        #        params={'callback':callback, 'species':species})
        )
        return res

    def get_map_cdna_to_region(self, identifier, region, frmt='json',
            callback='randomlygeneratedname', species=None):
        """ Convert from cDNA coordinates to genomic coordinates. 

        :param str first: version of the input assembly
        :param str first: version of the output assembly
        :param str region:  query region (see example)
        :param str species: default to human 

        Output reflects forward orientation coordinates as returned from the Ensembl API.


        ::

            get_map_cdna_to_region('ENST00000288602', '100..300')

        """
        self._check_frmt(frmt)
        res = self.http_get("map/cdna/{0}/{1}".format(identifier, region),
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={'callback':callback, 'species':species})
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
        self._check_frmt(frmt)
        res = self.http_get("map/{0}/{1}/{2}/{3}".format(species, first, region, second ), 
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={})
        return res

    def get_map_translation_to_region(self, identifier, region, frmt='json',
            callback='randomlygeneratedname', species=None):
        """Convert from protein (translation) coordinates to genomic coordinates.

        Output reflects forward orientation coordinates as returned from the
        Ensembl API.

        :param identifier: a stable Ensembl ID
        :param str query: a query region
        :param str callback: see class documentation
        :param str species: Species name/alias (e.g., homo_sapiens)


        :m

            get_map_translation_to_region('ENSP00000288602', '100..300')
        """

        self._check_frmt(frmt)
        res = self.http_get("map/translation/{0}/{1}".format(identifier, region), 
                frmt=frmt,  headers=self.get_headers(content=frmt),
                params={'callback':callback})
        return res


    # ONTOLOGY and Taxonomy
    # -------------------------------------------------------------------------

    def get_ontology_by_id(self, identifier, frmt='json', callback=None, relation=None, simple=False):
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
        simple = int(simple)
        identifier = str(identifier)
        res = self.http_get("ontology/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'simple':simple, 'relation':relation, 'callback':callback})
        return res

    def get_ontology_by_name(self, name, frmt='json', callback=None,
            ontology=None, relation=None, simple=False):
        """Search for a list of ontological terms by their name

        :param str name: An ontology name. SQL wildcards are supported (e.g.,
            transcription factor complex)
        :param str frmt: response formats in json, xml, yaml, jsonp
        :param str simple: If set the API will avoid the fetching of parent and child terms
        :param str relation: The types of relationships to include in the output. Fetches
            all relations by default (e.g., is_a, part_of)
        :param str ontology: Filter by ontology. Used to disambiguate terms which are
            shared between ontologies such as GO and EFO (e.g., GO)


        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_ontology_name('transcription factor')
            400
            >>> res = e.get_ontology_name('transcription factor complex')
            >>> res[0]['children']

        """
        simple = int(simple)

        res = self.http_get("ontology/name/" + name, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'simple':simple, 'relation':relation,
                    'callback':callback, 'ontology':ontology})
        return res

    def get_taxonomy_by_id(self, identifier, frmt='json', simple=False):
        """Search for a taxonomic term by its identifier or name

        :param str identifier: A taxon identifier. Can be a NCBI taxon id or
            a name (e.g., 9606 or Homo sapiens)
        :param bool simple: If set the API will avoid the fetching of parent and child terms
        :param str frmt: response formats in json, xml, yaml, jsonp
        """
        simple = int(simple)
        identifier = str(identifier)
        res = self.http_get("taxonomy/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'simple':simple})
        return res

    def get_taxonomy_by_name(self, name, frmt='json', callback=None):
        """Search for a taxonomic id by a non-scientific name

        :param str name: A non-scientific species name. Can include SQL wildcards
        :param str frmt: response formats in json, xml, yaml, jsonp
        :param str callback: not used

        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_taxonomy_name('homo')


        """
        res = self.http_get("taxonomy/name/" + name, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':callback})
        return res

    def get_taxonomy_classification_by_id(self, identifier, frmt='json', callback=None):
        """Return the taxonomic classification of a taxon node


        :param str identifier: A taxon identifier. Can be a NCBI taxon id or a name
            (e.g., 9606, Homo sapiens)
        :param str frmt: json, xml, yaml, jsonp
        :param str callback: see class documentation

        ::

            >>> from bioservices imoprt Ensembl
            >>> e = Ensembl()
            >>> res = e.get_taxonomy_classification('9606')

        """
        res = self.http_get("taxonomy/classification/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'callback':callback})
        return res

    def get_ontology_ancestors_by_id(self, identifier):
        """Reconstruct the entire ancestry of a term from is_a and part_of
        relationships"""
         #'url': '/ontology/ancestors/{{id}}',
        raise NotImplementeError


    def get_ontology_ancestors_by_id(self, identifier):
        """Reconstruct the entire ancestry of a term from is_a and part_of
        relationships."""
        raise NotImplementeError
        #'getAncestorsChartById': {'url': '/ontology/ancestors/chart/{{id}}',
    def get_ontology_ancestors_by_id(self, identifier):
        """ Find all the terms descended from a given term. By default searches
        are conducted within the namespace of the given identifier"""
        raise NotImplementeError
        #'getDescendentsById': { 'url': '/ontology/descendents/{{id}}',

    # OVERLAP
    # -----------------------------------------------------


    def get_overlap_by_id(self, identifier):
        #GET overlap/id/:id  Retrieves features (e.g. genes, transcripts, variations etc.) that overlap a region defined by the given identifier.
        raise NotImplementeError

    def get_overlapby_region(self, species, region):
        # GET overlap/region/:species/:region     Retrieves multiple types of features for a given region.
        raise NotImplementeError

    def get_overlap_by_translation(self, identifier):
        # GET overlap/translation/:id     Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variations).
        raise NotImplementeError

    # REGULATION
    # --------------------------------------
    def get_regulatory_by_id(self, species, identifier):
        raise NotImplementeError


    # SEQUENCE
    # -----------------------------
    def get_sequence_by_id(self, identifier, frmt='fasta', type='genomic', species='',
            db_type='', object_type='', multiple_sequences=False, expand_3prime='',
            expand_5prime=''):
        """Request multiple types of sequence by stable identifier.

        :param str frmt: response formats: fasta, json, text, yam, jsonp
        :param str db_type: core
        :param str format: fasta
        :param str object_type: (defaults to gene)
        :param str type:. could be genomic, cds, cdna, protein (homo_sapiens). Requesting
            a gene and kind not equal to genomic may result in multiple sequence, which
            required the parameter multi_sequences to be set to True
        :param str species: genomic, cds, cdna, protein (defaults to cds)


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
        multiple_sequences = int(multiple_sequences)
        #identifier = self.devtools.tolist(identifier)
        res = self.http_get('sequence/id/' + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'type':type,
                'db_type': db_type, 'object_type':object_type,
                'multiple_sequences':multiple_sequences,  'species':species,
                'expand_3prime':expand_3prime,
                'expand_5prime':expand_5prime}
                )
        return res

    def get_sequence_by_region(self, species, region):
        # GET sequence/region/:species/:region    Returns the genomic sequence of the specified region of the given species.
        raise NotImplementeError


    # VARIATION
    # -----------------------------------------------------
    def get_variation_by_id(self, identifier, species, frmt='json', genotypes=False, phenotypes=False,
            pops=False):
        """

        :param str identifier: variation identifier (e.g., rs56116432)
        :param str species: Species name/alias (e.g., homo_sapiens)
        :param str frmt: response format (json, xml, jsonp)
        :param str callback: Name of the callback subroutine to be returned if
            requested JSONP response.
        :param bool genotypes: Include genotypes
        :param bool phenotypes: Include phenotypes
        :param bool pops: Include populations

        """
        genotypes = int(genotypes)
        phenotypes = int(phenotypes)
        pops = int(pops)
        res = self.http_get('variation/{0}/{1}'.format(species, identifier),
                frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'genotypes':genotypes, 'phenotypes':phenotypes, 'pops':pops}
                )
        return res

    def get_vep_by_id(self, species, identifier):
        raise NotImplementeError
        #GET vep/:species/id/:id     Fetch variant consequences based on a variation identifier


    def post_vep_by_id(self, species, identifiers):
        #POST vep/:species/id/   Fetch variant consequences for multiple ids
        raise NotImplementeError
    def get_vep_by_region(self, species, region, allele):
        #GET vep/:species/region/:region/:allele/    Fetch variant consequences
        raise NotImplementeError

    def post_vep_by_region(self, species, region):
        #POST vep/:species/region/   Fetch variant consequences for multiple regions
        raise NotImplementeError


# old API ????
"""
        'getFeatureById': {
            'url': '/feature/id/{{id}}?feature={{feature}}',
            'method': 'GET',
            'content_type': 'application/json'
            },
        'getFeatureByRegion': {
            'url': '/feature/region/{{species}}/{{region}}?feature={{feature}}',
            'method': 'GET',
            'content_type': 'application/json'
            },
        'getVariantConsequencesByRegion': {
                'url': '/vep/{{species}}/{{region}}/{{allele}}/consequences',
                'method': 'GET',
                'content_type': 'application/json'
                },
        'getVariantConsequencesById': {
                'url': '/vep/{{species}}/id/{{id}}/consequences',
                'method': 'GET',
                'content_type': 'application/json'
                },
        }
"""
