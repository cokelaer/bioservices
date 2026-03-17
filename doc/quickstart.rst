.. _quickstart:

Quick Start
###########

Introduction
============

**BioServices** lets you query biological databases from Python with no manual
HTTP requests, no XML parsing, and no API key juggling. You import a class,
call a method, and get back a Python object (usually a dictionary or a
:class:`pandas.DataFrame`).

The pattern is always the same::

    from bioservices import UniProt       # import the service class
    u = UniProt()                         # create an instance (opens no connection yet)
    result = u.search("ZAP70_HUMAN")     # call a method — data comes back as Python objects

The sections below walk through a handful of services to give you a feel for
what is possible.  The :doc:`reference guide <references>` documents every
class and method in full detail, and the :doc:`tutorials <tutorials>` go deeper
on KEGG, BioModels, and compound look-up workflows.


UniProt
=======

:class:`~bioservices.uniprot.UniProt` gives you programmatic access to the
UniProt Knowledgebase: full-text search, sequence retrieval, and cross-database
ID mapping.

**Map an accession to another database**

.. doctest::

    >>> from bioservices import UniProt
    >>> u = UniProt(verbose=False)
    >>> u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
    {'results': [{'from': 'P43403', 'to': 'hsa:7535'}]}

**Retrieve a FASTA sequence**::

    >>> fasta = u.retrieve("P09958", frmt="fasta")
    >>> print(fasta[:60])
    >sp|P09958|FURIN_HUMAN Furin OS=Homo sapiens OX=9606 GN=FURIN

**Search and get a DataFrame**::

    >>> df = u.search("ZAP70+AND+organism_id:9606", frmt="tsv",
    ...               columns="accession,gene_names,length", limit=5)

.. seealso:: :class:`bioservices.uniprot.UniProt`


KEGG
====

:class:`~bioservices.kegg.KEGG` wraps the KEGG REST API, giving access to
pathways, genes, compounds, reactions, and more across hundreds of organisms.

::

    from bioservices import KEGG
    k = KEGG(verbose=False)

Set the organism to human and explore pathways::

    k.organism = "hsa"            # Homo sapiens
    print(k.pathwayIds[:5])       # first five human pathway IDs

Retrieve the full entry for a gene or pathway::

    print(k.get("hsa:3586"))          # IL6 gene
    print(k.get("path:hsa05416"))     # Viral myocarditis pathway

Convert between KEGG and UniProt IDs:

.. doctest:: kegg

    >>> from bioservices import KEGG
    >>> k = KEGG(verbose=False)
    >>> k.code2Tnumber("hsa")
    'T01001'

.. seealso:: :class:`bioservices.kegg.KEGG`, :class:`bioservices.kegg.KEGGParser`,
             :ref:`kegg_tutorial`


QuickGO
=======

:class:`~bioservices.quickgo.QuickGO` provides access to Gene Ontology terms
and annotations from the EBI QuickGO browser.

**Look up a GO term**::

    from bioservices import QuickGO
    g = QuickGO(verbose=False)
    res = g.get_go_terms("GO:0003824")
    print(res[0]["name"])              # catalytic activity

**Search GO terms by keyword**::

    hits = g.go_search("apoptosis")
    for term in hits[:3]:
        print(term["id"], term["name"])

**Retrieve annotations for a gene product**::

    ann = g.Annotation(geneProductId="UniProtKB:P12345", limit=10)

.. seealso:: :class:`bioservices.quickgo.QuickGO`


BioModels
=========

:class:`~bioservices.biomodels.BioModels` provides access to the EBI BioModels
database of curated mathematical models of biological processes.

::

    from bioservices import BioModels
    b = BioModels()
    model = b.get_model("BIOMD0000000299")   # retrieve a curated SBML model

List all available model IDs and search by keyword::

    ids = b.get_models_by_search("glucose", offset=0, numResults=10)

.. seealso:: :class:`bioservices.biomodels.BioModels`, :ref:`biomodels_tutorial`


Rhea
====

:class:`~bioservices.rhea.Rhea` is a reaction database where all participants
are linked to ChEBI, with cross-references to KEGG, MetaCyc, and Reactome.

**Search by keyword** (wildcards supported)::

    from bioservices import Rhea
    r = Rhea()
    df = r.search("caffeine")          # returns a pandas DataFrame
    print(df[["RHEA ID", "Equation"]].head())

**Retrieve a specific reaction**::

    df = r.query("RHEA:10280", columns="rhea-id,equation")

.. seealso:: :class:`bioservices.rhea.Rhea`


Other services
==============

BioServices wraps many more databases — ChEMBL, ChEBI, Reactome, PDB, PDBe,
EUtils, Ensembl, STRING, GEO, PRIDE, WikiPathways, and others. Each follows the
same pattern: import, instantiate, call a method.

The :doc:`reference guide <references>` lists every available service with full
API documentation.  If you need a service that is not yet wrapped, the
:ref:`developer` section shows how to add one in a few lines using the
:class:`~bioservices.services.REST` base class.
