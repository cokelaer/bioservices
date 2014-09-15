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
        self.devtools.check_param_in_list(frmt, ['json', 'xml', 'jsonp'])

    def _check_id(self, identifier):
        pass

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

    def get_genetree(self, identifier, frmt='json', aligned=False, nh_format='simple',
            sequence='protein', callback='randomlygeneratedname', compara='multi'):
        """Retrieves a gene tree dump for a gene tree stable identifier

        :param str identifier: An Ensembl genetree ID
        :param bool aligned: if true, return the aligned string otherwise, return the original 
            sequence (no insertions). Can be True/1 or False/0 and defaults to 0
        :param str callback: use if frmt is 'json' only. Name of the callback subroutine to be 
            returned by the requested JSONP response. 
        :param str compara: Name of the compara database to use. Multiple comparas can 
            exist on a server if you are accessing Ensembl Genomes data
        :param nh_format: The format of a NH (New Hampshire) request.
            Valid values are 'full', 'display_label_composite', 'simple', 'species', 
            'species_short_name', 'ncbi_taxon', 'ncbi_name', 'njtree', 'phylip'
        :param sequence: The type of sequence to bring back. Setting it to none 
            results in no sequence being returned.
            Valid values are 'none', 'cdna', 'protein'.

        ::

            >>> from bioservices import Ensembl
            >>> s = Ensembl()
            >>> s.genetree('ENSGT00390000003602', frmt='nh', nh_format='simple')
            >>> s.genetree('ENSGT00390000003602', frmt='phyloxml')
            >>> s.genetree('ENSGT00390000003602', frmt='phyloxml',aligned=True, sequence='cdna')
            >>> s.genetree('ENSGT00390000003602', frmt='phyloxml', sequence='none')

        """
        if aligned is True:
            aligned = 1
        elif aligned is False:
            aligned = 0
        self.devtools.check_param_in_list(nh_format, 
                ['full', 'display_label_composite', 'simple', 'species', 
                    'species_short_name', 'ncbi_taxon', 'ncbi_name', 'njtree', 'phylip'])
        self.devtools.check_param_in_list(sequence, ['none', 'cdna', 'protein'])

        res = self.http_get("genetree/id/" + identifier, frmt=frmt,
                headers=self.get_headers(content=frmt),
                params={'nh_format':nh_format, 'sequence':sequence, 'aligned':aligned}
                )
        return res

    def get_sequence(self, identifier, frmt='fasta', type='genomic', species='',
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
        if multiple_sequences is False:
            multiple_sequences = 0
        else:
            multiple_sequences = 1
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

    def get_variation(self, identifier, species, frmt='json', genotypes=False, phenotypes=False,
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

    def get_taxonomy(self, identifier, frmt='json', simple=False):
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

    def get_taxonomy_name(self, name, frmt='json', callback=None):
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

    def get_taxonomy_classification(self, identifier, frmt='json', callback=None):
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

    def get_ontology(self, identifier, frmt='json', callback=None, relation=None, simple=False):
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

    def get_ontology_name(self, name, frmt='json', callback=None, 
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

    
"""

Resource    Description
POST archive/id/:id     Retrieve the archived sequence for a set of identifiers
Comparative Genomics
    
Resource    Description
GET genetree/member/id/:id  Retrieves a gene tree that contains the stable identifier
GET genetree/member/symbol/:species/:symbol     Retrieves a gene tree containing the gene identified by a symbol
GET alignment/region/:species/:region   Retrieves genomic alignments as separate blocks based on a region and species
GET homology/id/:id     Retrieves homology information (orthologs) by Ensembl gene id
GET homology/symbol/:species/:symbol    Retrieves homology information (orthologs) by symbol
Cross References
    
Resource    Description
GET xrefs/symbol/:species/:symbol   Looks up an external symbol and returns all Ensembl objects linked to it. This can be a display name for a gene/transcript/translation, a synonym or an externally linked reference. If a gene's transcript is linked to the supplied symbol the service will return both gene and transcript (it supports transient links).
GET xrefs/id/:id    Perform lookups of Ensembl Identifiers and retrieve their external references in other databases
GET xrefs/name/:species/:name   Performs a lookup based upon the primary accession or display label of an external reference and returning the information we hold about the entry
Information
    
Resource    Description
GET info/analysis/:species  List the names of analyses involved in generating Ensembl data.
GET info/assembly/:species  List the currently available assemblies for a species.
GET info/assembly/:species/:region_name     Returns information about the specified toplevel sequence region for the given species.
GET info/biotypes/:species  List the functional classifications of gene models that Ensembl associates with a particular species. Useful for restricting the type of genes/transcripts retrieved by other endpoints.
GET info/compara/methods    List all compara analyses available (an analysis defines the type of comparative data).
GET info/compara/species_sets/:method   List all collections of species analysed with the specified compara method.
GET info/comparas   Lists all available comparative genomics databases and their data release.
GET info/data   Shows the data releases available on this REST server. May return more than one release (unfrequent non-standard Ensembl configuration).
GET info/external_dbs/:species  Lists all available external sources for a species.
GET info/ping   Checks if the service is alive.
GET info/rest   Shows the current version of the Ensembl REST API.
GET info/software   Shows the current version of the Ensembl API used by the REST server.
GET info/species    Lists all available species, their aliases, available adaptor groups and data release.
Lookup
    
Resource    Description
GET lookup/id/:id   Find the species and database for a single identifier
GET lookup/symbol/:species/:symbol  Find the species and database for a symbol in a linked external database
Mapping
    
Resource    Description
GET map/cdna/:id/:region    Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.
GET map/cds/:id/:region     Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.
GET map/:species/:asm_one/:region/:asm_two  Convert the co-ordinates of one assembly to another
GET map/translation/:id/:region     Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.
Ontologies and Taxonomy
    
Resource    Description
GET ontology/ancestors/:id  Reconstruct the entire ancestry of a term from is_a and part_of relationships
GET ontology/ancestors/chart/:id    Reconstruct the entire ancestry of a term from is_a and part_of relationships.
GET ontology/descendants/:id    Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier
    
Resource    Description
GET overlap/id/:id  Retrieves features (e.g. genes, transcripts, variations etc.) that overlap a region defined by the given identifier.
GET overlap/region/:species/:region     Retrieves multiple types of features for a given region.
GET overlap/translation/:id     Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variations).
Sequences
    
Resource    Description
GET sequence/region/:species/:region    Returns the genomic sequence of the specified region of the given species.
Variation
    
Resource    Description
GET vep/:species/id/:id     Fetch variant consequences based on a variation identifier
POST vep/:species/id/   Fetch variant consequences for multiple ids
GET vep/:species/region/:region/:allele/    Fetch variant consequences
POST vep/:species/region/   Fetch variant consequences for multiple regions

"""



