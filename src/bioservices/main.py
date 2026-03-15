#
#  This file is part of bioservices software
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://bioservices.readthedocs.io
#
##############################################################################
import functools
import glob
import os
import subprocess
from pathlib import Path

import colorlog
import rich_click as click

logger = colorlog.getLogger(__name__)

__all__ = ["main"]


# This can be used by all commands as a simple decorator
def common_logger(func):
    @click.option(
        "--logger",
        default="INFO",
        type=click.Choice(["INFO", "DEBUG", "WARNING", "CRITICAL", "ERROR"]),
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


from bioservices import version


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version)
def main(**kwargs):
    """This is the main entry point for a set of BioServices applications"""
    pass


@main.command()
@click.option("--accession", type=click.STRING, required=True, help="A valid accession number (e.g., FN433596.1)")
@click.option(
    "--prefix",
    type=click.STRING,
    default=None,
    help="""By default, output FastA file is name after the accession number
            but you can rename it using this --prefix name""",
)
@click.option("--method", type=click.Choice(["ENA", "EUtils"]), default="EUtils")
@click.option("--with-gff3", is_flag=True, default=False)
@click.option("--with-gbk", is_flag=True, default=False)
def download_accession(**kwargs):
    """Download Fasta related to an accession and possibly other type (e.g gff)

    Input file can be gzipped or not. The --output-file

        bioservices download-accession FN433596.1
    """
    from bioservices.apps.download_fasta import download_fasta
    from bioservices.apps.download_gbk import download_gbk
    from bioservices.apps.download_gff3 import download_gff3

    prefix = kwargs["prefix"]

    logger.info("Downloading FastA file")
    download_fasta(kwargs["accession"], output_filename=f"{prefix}.fa" if prefix else prefix, method=kwargs["method"])

    if kwargs["with_gff3"]:
        logger.info("Downloading GFF file")
        download_gff3(
            kwargs["accession"], output_filename=f"{prefix}.gff" if prefix else prefix, method=kwargs["method"]
        )

    if kwargs["with_gbk"]:
        logger.info("Downloading Genbank file")
        download_gbk(
            kwargs["accession"], output_filename=f"{prefix}.gbk" if prefix else prefix, method=kwargs["method"]
        )


@main.command()
# @click.option("--name", type=click.STRING, help="A valid accession number (e.g., FN433596.1)")
@click.option("--id", type=click.STRING, help="A valid taxon ID (e.g., 9606)")
@click.option(
    "--method", type=click.STRING, default="EUtils", help="A method. EUtils only option implemented right now"
)
def taxonomy(**kwargs):
    """Download information related to a taxid

    bioservices taxonomy --id 9606
    """

    if kwargs["method"] == "EUtils":
        from bioservices import EUtils

        eu = EUtils(email="bioservices")
        ret = eu.ESummary("taxonomy", kwargs["id"])
        for uid in ret["uids"]:
            print(ret[uid])


# ---------------------------------------------------------------------------
# protein command group
# ---------------------------------------------------------------------------

# Map user-friendly database names to UniProt ID-mapping identifiers
_PROTEIN_ID_MAP_NAMES = {
    "uniprot": "UniProtKB_AC-ID",
    "kegg": "KEGG",
    "pdb": "PDB",
    "ensembl": "Ensembl",
    "refseq": "RefSeq_NT",
    "genename": "Gene_Name",
    "uniparc": "UniParc",
    "uniref50": "UniRef50",
    "uniref90": "UniRef90",
    "uniref100": "UniRef100",
}

# Common organism name to taxonomy ID shortcuts
_ORGANISM_NAME_TO_TAXID = {
    "human": "9606",
    "mouse": "10090",
    "rat": "10116",
    "zebrafish": "7955",
    "yeast": "559292",
    "arabidopsis": "3702",
    "fly": "7227",
    "worm": "6239",
    "ecoli": "83333",
}


@main.group()
def protein(**kwargs):
    """Commands for querying protein data across multiple databases

    \b
    Examples:
        bioservices protein search --query ZAP70 --organism human
        bioservices protein sequence --uniprot-id P43403
        bioservices protein structure --uniprot-id P43403
        bioservices protein annotation --uniprot-id P43403
        bioservices protein interaction --gene ZAP70 --taxid 9606
        bioservices protein map-id --from uniprot --to kegg --id P43403
    """
    pass


@protein.command()
@click.option("--query", required=True, type=click.STRING, help="Search query (e.g. gene name like ZAP70)")
@click.option(
    "--organism",
    default=None,
    type=click.STRING,
    help="Organism name (e.g. human, mouse) or NCBI taxonomy ID (e.g. 9606)",
)
@click.option(
    "--format",
    "frmt",
    default="tsv",
    type=click.Choice(["tsv", "fasta", "json"]),
    help="Output format (default: tsv)",
)
def search(**kwargs):
    """Search for proteins in UniProt.

    \b
    Examples:
        bioservices protein search --query ZAP70
        bioservices protein search --query ZAP70 --organism human --format tsv
    """
    from bioservices import UniProt

    u = UniProt(verbose=False)
    query = kwargs["query"]
    if kwargs["organism"]:
        org = kwargs["organism"]
        taxid = _ORGANISM_NAME_TO_TAXID.get(org.lower(), org)
        query = f"{query} AND organism_id:{taxid}"
    result = u.search(query, frmt=kwargs["frmt"])
    if result:
        print(result)


@protein.command()
@click.option("--uniprot-id", required=True, type=click.STRING, help="UniProt accession ID (e.g. P43403)")
def sequence(**kwargs):
    """Fetch the FASTA sequence for a protein from UniProt.

    \b
    Example:
        bioservices protein sequence --uniprot-id P43403
    """
    from bioservices import UniProt

    u = UniProt(verbose=False)
    result = u.get_fasta(kwargs["uniprot_id"])
    if result:
        print(result)


@protein.command()
@click.option("--uniprot-id", required=True, type=click.STRING, help="UniProt accession ID (e.g. P43403)")
def structure(**kwargs):
    """Find PDB 3D structures for a protein given its UniProt accession ID.

    \b
    Example:
        bioservices protein structure --uniprot-id P43403
    """
    from bioservices import PDB

    p = PDB()
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": (
                    "rcsb_polymer_entity_container_identifiers" ".reference_sequence_identifiers.database_accession"
                ),
                "operator": "in",
                "value": [kwargs["uniprot_id"]],
            },
        },
        "return_type": "entry",
    }
    result = p.search(query)
    if isinstance(result, dict) and "result_set" in result:
        for entry in result["result_set"]:
            print(entry["identifier"])
    else:
        logger.warning("No PDB structures found for %s", kwargs["uniprot_id"])


@protein.command()
@click.option("--uniprot-id", required=True, type=click.STRING, help="UniProt accession ID (e.g. P43403)")
@click.option(
    "--format",
    "frmt",
    default="json",
    type=click.Choice(["json", "txt", "fasta", "gff"]),
    help="Output format (default: json)",
)
def annotation(**kwargs):
    """Fetch UniProt annotations for a protein.

    \b
    Example:
        bioservices protein annotation --uniprot-id P43403
        bioservices protein annotation --uniprot-id P43403 --format txt
    """
    import json as _json

    from bioservices import UniProt

    u = UniProt(verbose=False)
    result = u.retrieve(kwargs["uniprot_id"], frmt=kwargs["frmt"])
    if result:
        if kwargs["frmt"] == "json":
            print(_json.dumps(result, indent=2))
        else:
            print(result)


@protein.command()
@click.option("--gene", required=True, type=click.STRING, help="Gene or protein name (e.g. ZAP70)")
@click.option(
    "--taxid",
    default=9606,
    type=click.INT,
    help="NCBI taxonomy ID (default: 9606 for Homo sapiens)",
)
def interaction(**kwargs):
    """Fetch protein-protein interactions from the STRING database.

    \b
    Example:
        bioservices protein interaction --gene ZAP70 --taxid 9606
    """
    import json as _json

    from bioservices import STRING

    s = STRING(verbose=False)
    result = s.get_interactions(kwargs["gene"], species=kwargs["taxid"])
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No interactions found for %s (taxid=%s)", kwargs["gene"], kwargs["taxid"])


@protein.command(name="map-id")
@click.option(
    "--from",
    "from_db",
    required=True,
    type=click.STRING,
    help="Source database (e.g. uniprot, kegg, pdb, ensembl)",
)
@click.option(
    "--to",
    "to_db",
    required=True,
    type=click.STRING,
    help="Target database (e.g. uniprot, kegg, pdb, ensembl)",
)
@click.option("--id", "identifier", required=True, type=click.STRING, help="Identifier to convert (e.g. P43403)")
def map_id(**kwargs):
    """Convert protein identifiers between databases via UniProt ID mapping.

    \b
    Examples:
        bioservices protein map-id --from uniprot --to kegg --id P43403
        bioservices protein map-id --from pdb --to uniprot --id 1ATP
    """
    import json as _json

    from bioservices import UniProt

    from_db = kwargs["from_db"].lower()
    to_db = kwargs["to_db"].lower()
    identifier = kwargs["identifier"]

    fr = _PROTEIN_ID_MAP_NAMES.get(from_db, from_db)
    to = _PROTEIN_ID_MAP_NAMES.get(to_db, to_db)

    u = UniProt(verbose=False)
    result = u.mapping(fr=fr, to=to, query=identifier)
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No mapping found for %s (%s -> %s)", identifier, from_db, to_db)


# ---------------------------------------------------------------------------
# gene command group
# ---------------------------------------------------------------------------

# Map user-friendly database names to UniProt ID-mapping identifiers for genes
_GENE_ID_MAP_NAMES = {
    "uniprot": "UniProtKB_AC-ID",
    "kegg": "KEGG",
    "ensembl": "Ensembl",
    "refseq": "RefSeq_NT",
    "genename": "Gene_Name",
    "entrez": "GeneID",
    "ncbi-geneid": "GeneID",
}


@main.group()
def gene(**kwargs):
    """Commands for querying gene data across multiple databases

    \b
    Examples:
        bioservices gene info --gene-id 1017
        bioservices gene name --symbol BRAF
        bioservices gene ontology --query GO:0003824
        bioservices gene expression --query cancer
        bioservices gene pathway --query TP53
        bioservices gene ortholog --gene zap70 --taxid 9606
        bioservices gene map-id --from uniprot --to kegg --id P43403
    """
    pass


@gene.command()
@click.option("--gene-id", required=True, type=click.STRING, help="Gene ID to look up (e.g. 1017 for CDK2)")
@click.option(
    "--fields",
    default="symbol,name,taxid,entrezgene,ensemblgene",
    type=click.STRING,
    help="Comma-separated fields to return (default: symbol,name,taxid,entrezgene,ensemblgene)",
)
def info(**kwargs):
    """Retrieve gene information from MyGene.info.

    \b
    Examples:
        bioservices gene info --gene-id 1017
        bioservices gene info --gene-id 1017 --fields symbol,name,taxid
    """
    import json as _json

    from bioservices import MyGeneInfo

    mgi = MyGeneInfo(verbose=False)
    result = mgi.get_one_gene(kwargs["gene_id"], fields=kwargs["fields"])
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No gene found for ID %s", kwargs["gene_id"])


@gene.command()
@click.option("--symbol", required=True, type=click.STRING, help="Gene symbol to look up (e.g. BRAF, ZNF3)")
def name(**kwargs):
    """Look up HGNC-approved gene names and symbols.

    \b
    Examples:
        bioservices gene name --symbol BRAF
        bioservices gene name --symbol ZNF3
    """
    import json as _json

    from bioservices import HGNC

    h = HGNC(verbose=False)
    result = h.fetch("symbol", kwargs["symbol"])
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No HGNC entry found for symbol %s", kwargs["symbol"])


@gene.command()
@click.option(
    "--query",
    required=True,
    type=click.STRING,
    help="GO term ID (e.g. GO:0003824) or free-text search term (e.g. kinase)",
)
def ontology(**kwargs):
    """Retrieve Gene Ontology annotations from QuickGO.

    Provide a GO term ID (e.g. GO:0003824) to fetch term details, or a
    free-text query (e.g. kinase) to search for matching GO terms.

    \b
    Examples:
        bioservices gene ontology --query GO:0003824
        bioservices gene ontology --query kinase
    """
    import json as _json

    from bioservices import QuickGO

    go = QuickGO(verbose=False)
    query = kwargs["query"]
    if query.upper().startswith("GO:"):
        result = go.get_go_terms(query.upper())
    else:
        result = go.go_search(query)
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No GO terms found for %s", query)


@gene.command()
@click.option("--query", required=True, type=click.STRING, help="Search keywords (e.g. cancer, TP53)")
@click.option(
    "--species",
    default=None,
    type=click.STRING,
    help="Organism filter (e.g. homo sapiens)",
)
def expression(**kwargs):
    """Search ArrayExpress for gene expression experiments.

    \b
    Examples:
        bioservices gene expression --query cancer
        bioservices gene expression --query TP53 --species homo sapiens
    """
    import json as _json

    from bioservices import ArrayExpress

    ae = ArrayExpress(verbose=False)
    query_params = {"keywords": kwargs["query"]}
    if kwargs["species"]:
        query_params["species"] = kwargs["species"]
    result = ae.queryAE(**query_params)
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No ArrayExpress experiments found for %s", kwargs["query"])


@gene.command()
@click.option("--query", required=True, type=click.STRING, help="Gene name or pathway search term (e.g. TP53)")
@click.option(
    "--source",
    default="reactome",
    type=click.Choice(["reactome", "kegg"]),
    help="Pathway database to query (default: reactome)",
)
def pathway(**kwargs):
    """Find pathways associated with a gene using Reactome or KEGG.

    \b
    Examples:
        bioservices gene pathway --query TP53
        bioservices gene pathway --query TP53 --source kegg
    """
    import json as _json

    source = kwargs["source"]
    query = kwargs["query"]

    if source == "reactome":
        from bioservices import Reactome

        r = Reactome(verbose=False)
        result = r.search_query(query)
        if result:
            print(_json.dumps(result, indent=2))
        else:
            logger.warning("No Reactome pathways found for %s", query)
    else:
        from bioservices import KEGG

        k = KEGG(verbose=False)
        result = k.find("pathway", query)
        if result:
            print(result)
        else:
            logger.warning("No KEGG pathways found for %s", query)


@gene.command()
@click.option("--gene", "gene_name", required=True, type=click.STRING, help="Gene name or ID (e.g. zap70)")
@click.option(
    "--taxid",
    default=9606,
    type=click.INT,
    help="NCBI taxonomy ID of the query organism (default: 9606 for Homo sapiens)",
)
def ortholog(**kwargs):
    """Search for orthologs of a gene using the Panther database.

    \b
    Examples:
        bioservices gene ortholog --gene zap70
        bioservices gene ortholog --gene zap70 --taxid 9606
    """
    import json as _json

    from bioservices import Panther

    p = Panther(verbose=False)
    result = p.get_mapping(kwargs["gene_name"], kwargs["taxid"])
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No orthologs found for %s (taxid=%s)", kwargs["gene_name"], kwargs["taxid"])


@gene.command(name="map-id")
@click.option(
    "--from",
    "from_db",
    required=True,
    type=click.STRING,
    help="Source database (e.g. uniprot, ncbi-geneid, ensembl)",
)
@click.option(
    "--to",
    "to_db",
    required=True,
    type=click.STRING,
    help="Target database (e.g. kegg, uniprot, ensembl)",
)
@click.option("--id", "identifier", required=True, type=click.STRING, help="Identifier to convert (e.g. P43403)")
def gene_map_id(**kwargs):
    """Convert gene identifiers between databases via UniProt ID mapping.

    \b
    Examples:
        bioservices gene map-id --from uniprot --to kegg --id P43403
        bioservices gene map-id --from ncbi-geneid --to uniprot --id 7535
        bioservices gene map-id --from ensembl --to uniprot --id ENSG00000145675
    """
    import json as _json

    from bioservices import UniProt

    from_db = kwargs["from_db"].lower()
    to_db = kwargs["to_db"].lower()
    identifier = kwargs["identifier"]

    fr = _GENE_ID_MAP_NAMES.get(from_db, from_db)
    to = _GENE_ID_MAP_NAMES.get(to_db, to_db)

    u = UniProt(verbose=False)
    result = u.mapping(fr=fr, to=to, query=identifier)
    if result:
        print(_json.dumps(result, indent=2))
    else:
        logger.warning("No mapping found for %s (%s -> %s)", identifier, from_db, to_db)
