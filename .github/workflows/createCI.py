




services = [
    'arrayexpress',
    'bigg',
    'biocarta',
    'biodbnet',
    'biogrid',
    'biomart',
    'biomodels',
    'chebi',
    'chembl',
    'chemspider',
    'clinvitae',
    'cog',
    'dbfetch',
    'ena',
    'ensembl',
    'eutils',
    'eva',
    'hgnc',
    'intact_complex',
    'kegg',
    'muscle',
    'mygeneinfo',
    'ncbiblast',
    'omicsdi',
    'omnipath',
    'panther',
    'pathwaycommons',
    'pdbe',
    'pdb',
    'pfam',
    'picr',
    'pride',
    'psicquic',
    'pubchem',
    'quickgo',
    'reactome',
    'rhea',
    'rnaseq_ebi',
    'seqret',
    'unichem',
    'uniprot',
    'wikipathway']


with open("template.txt", "r") as fin:
    template = fin.read()

for service in services:
    with open(f'{service}.yml', 'w') as fout:
        code = template.replace("__name__", service)
        fout.write(code)



