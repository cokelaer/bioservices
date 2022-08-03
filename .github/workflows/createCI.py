




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


print("==================== ================================================================================================")
print("Service              CI testing")
print("==================== ================================================================================================")
for service in sorted(services):
    service_name = f"{service}".ljust(14)
    print(f'{service_name}        .. image:: https://github.com/cokelaer/bioservices/actions/workflows/{service}.yml/badge.svg')
    print(f"                         :target: https://github.com/cokelaer/bioservices/actions/workflows/{service}.yml")

print("==================== ================================================================================================")









