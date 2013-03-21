from bioservices import biomart



def test_registry():
    s = biomart.BioMart()
    s.registry()
    s.datasets("ensembl")
    s.attributes("oanatinus_gene_ensembl")
    s.filters("oanatinus_gene_ensembl")
    s.configuration("oanatinus_gene_ensembl")


