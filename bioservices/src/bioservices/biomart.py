"""

SOAP could not be used directly, so we used REST instead.
"""


"""Retrieving Meta Data

    to retrieve registry information: /biomart/martservice?type=registry
    to retrieve datasets available for a mart:
/biomart/martservice?type=datasets&mart=ensembl
    to retrieve attributes available for a dataset:
/biomart/martservice?type=attributes&dataset=oanatinus_gene_ensembl
    to retrieve filters available for a dataset:
/biomart/martservice?type=filters&dataset=oanatinus_gene_ensembl
    to retrieve configuration for a dataset:
/biomart/martservice?type=configuration&dataset=oanatinus_gene_ensembl
"""
