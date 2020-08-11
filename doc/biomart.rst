BioMart service
====================

BioMart provides a uniform interface to many services such as Cosmic, Ensembl
and many more. In BioMart terminology a service is called a **mart**. As an 
example, we will consider the COSMIC interface provided by
BioMart (see `COSMIC <http://cancer.sanger.ac.uk/biomart/martview/>`_). You 
can play with the interface itself to get an idea of what can be selected (e.g.,
datasets, filters, attributes). To help you, let us give a simple example that
consists in converting the ensemble identifiers into entrez identifiers. 

First you create an instance. There are lots of services behind the scene. The
ENSEMBL_MART_ENSEMBL provides the conversion we are looking for. 
::


    from bioservices import BioMart
    b = BioMart()
    datasets = b.get_datasets("ENSEMBL_MART_ENSEMBL")

In datasets, there is a hsapiens_gene_ensembl database. Let us add it to the
request that will be send::
 
    b.add_dataset_to_xml(dataset)

We want to extract only the to following attributes::

    b.add_attribute_to_xml("ensemble_gene_id")
    b.add_attribute_to_xml("entrezgene_id")

If you are interested in a set of identifiers, provide it as a list (here below
the queries::

    queries = ["", ""]
    b.add_filter_to_xml("ensemble_gene_id", queries)

and finally do the query itself::

    xml = b.get_xml()
    res = b.query(xml)

You can obtain the attributes and filters of a dataset as follows::

    dataset = 'hsapiens_gene_ensembl'
    attributes = b.attributes(dataset)
    filters = b.filters(dataset)

Here is another example with cosmic.

.. note:: the cosmic mart was available at the time of 1.0 but not during
    release 1.4.1 . This is not a BioServices issue but the COSMIC mart being 
    down. Hopefully, it will be available again soon. meanwhile this
    example should help you get a feeling of what can be done with a MART.

In **BioServices**, you can create a biomart request (which is a XML document) but first 
we need to figure out what are the datasets associated with the COSMIC mart. The tricky part is to know
the names of the datasets/attributes/filters. BioServices provides a function
that ease this task. First let create an instance of BioMart::

    >>> from bioservices import *
    >>> s = BioMart()

Then, let us use the :meth:`~bioservices.biomart.BioMart.lookfor` as follows::

    >>> s.lookfor("cosmic")
    Candidate:
         database: cosp 
        MART name: CosmicMart 
      displayName: COSMIC (SANGER UK) 
            hosts: www.sanger.ac.uk 

From the previous command, only one mart has been found. It is called
CosmicMart, from which we can retrieve the datasets::

    >>> s.datasets("CosmicMart")
    ['COSMIC67', 'COSMIC68', 'COSMIC66']

The are lots of entries in such datasets and we want to restrict our request
using filters and attributes. Let us use the "COSMIC60" dataset. The following
commands can help you in figuring out what are the valid names of attributes and
filters to be used::

    >>> s.attributes("COSMIC67")
    >>> s.filters("COSMIC67")

They  return list of dictionaries that provide the identifiers (keys of the
dictionary) and information about the identifier (e.g. descriptive name).

For instance, if you want to add the gene name in the list of attributes, you will need to know its
identifier. If you look at the dictionary you will find the "gene_name" key that contains::

    >>> s.attributes("COSMIC67")["gene_name"]
    ['Gene Name',
     '',
     'naive_attributes',
     'html,txt,csv,tsv,xls',
     'COSMIC67__MART__MAIN',
     'gene_name']

So if you want to add the **Gene Name** attribute, you must use the
**gene_name** identifier. Similarly for filters. In order to use a filter you
must use the identifier as well as a value. Values are contained in the
dictionary returned by filters(). For instance, the "Mutated Sample" filter
given by the "samp_gene_mutated" identifier returns a list, which second element
contains the list of valid values (here y or n character)::

    >>> s.filters("COSMIC67")
    ['Mutated Sample',
     '[y,n]',
     '',
     'naive_filters',
     'list',
     '=',
     'COSMIC67__MART__MAIN',
     'samp_gene_mutated']


So, there is a little bit of work for the user to figure out the identifiers of the attributes and filters. This could be a good exercice but let us give the list of relevant identifiers and there names that we want to use in this tutorial:

=========== =================== ==============================
category    name                identifier
=========== =================== ==============================
filter      Mutated Sample      samp_gene_mutated (y)
filter      Primary Site        site_primary (breast)
filter      Validation Status   validation_status (verified)
Attribute   Cosmic Sample ID    id_sample
Attribute   Sample Name         sample_name
Attribute   Sample Source       sample_source
Attribute   Tumour source       tumour_source
Attribute   Gene Name           gene_name
Attribute   Accession Number    accession_number
Attribute   Cosmi Mutation ID   id_mutation
Attribute   Gene ID             id_gene
=========== =================== ==============================

It is now time to create the XML request by adding attributes/filters and the
dataset::

    >>> # add the dataset
    >>> s.add_dataset_to_xml("COSMIC67")

    >>> # add the attributes
    >>> s.add_attribute_to_xml("id_sample")
    >>> s.add_attribute_to_xml("sample_name")
    >>> s.add_attribute_to_xml("sample_source")
    >>> s.add_attribute_to_xml("tumour_source")
    >>> s.add_attribute_to_xml("gene_name")
    >>> s.add_attribute_to_xml("accession_number")
    >>> s.add_attribute_to_xml("id_mutation")
    >>> s.add_attribute_to_xml("id_gene")

    >>> # add the filters
    >>> s.add_filter_to_xml("samp_gene_mutated", "y")
    >>> s.add_filter_to_xml("site_primary", "breast")
    >>> s.add_filter_to_xml("validation_status", "verified")


You can create the XML request that will be send::

    >>> xml = s.get_xml()

And finally send the request:: 

    >>> res = s.query(xml)






