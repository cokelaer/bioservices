from bioservices import biomart



def test_registry():
    s = biomart.BioMart()
    s.registry()
    s.datasets("ensembl")
    s.attributes("oanatinus_gene_ensembl")
    s.filters("oanatinus_gene_ensembl")
    s.configuration("oanatinus_gene_ensembl")


    xmlq = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
                        
        <Dataset name = "pathway" interface = "default" >
                <Filter name = "referencepeptidesequence_uniprot_id_list" value = "P43403"/>
                <Attribute name = "stableidentifier_identifier" />
                <Attribute name = "pathway_db_id" />
        </Dataset>
</Query>
"""
    s.query(s._xml_example)


