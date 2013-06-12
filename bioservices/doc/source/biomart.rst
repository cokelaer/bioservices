BioMart service
====================

BioMart provides a uniformed interface to many services such as Cosmic, Ensembl
and many more. In BioMart terminology a service is called a **mart**. As an 
example, we will consider the COSMIC interface provided by
BioMart (see `COSMIC <http://cancer.sanger.ac.uk/biomart/martview/>`_). You 
can play with the interface itself to get an idea of what can be selected (e.g.,
datasets, filters, attributes) but let us use BioServices to access to the
Cosmic mart programmatically. 

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
    ['COSMIC60', 'COSMIC61', 'COSMIC59']

The are lots of entries in such datasets and we want to restrict our request
using filters and attributes. Let us use the "COSMIC60" dataset. The following
commands can help you in figuring out what are the valid names of attributes and
filters to be used::

    >>> s.attributes("COSMIC60")
    >>> s.filters("COSMIC60")

They  return list of dictionaries that provide the identifiers (keys of the
dictionary) and information about the identifier (e.g. descriptive name).

For instance, if you want to add the gene name in the list of attributes, you will need to know its
identifier. If you look at the dictionary you will find the "gene_name" key that contains::

    >>> b.attributes("COSMIC60")["gene_name"]
    ['Gene Name',
     '',
     'naive_attributes',
     'html,txt,csv,tsv,xls',
     'COSMIC60__MART__MAIN',
     'gene_name']

So if you want to add the **Gene Name** attribute, you must use the
**gene_name** identifier. Similarly for filters. In order to use a filter you
must use the identifier as well as a value. Values are contained in the
dictionary returned by filters(). For instance, the "Mutated Sample" filter
given by the "samp_gene_mutated" identifier returns a list, which second element
contains the list of valid values (here y or n character)::

    >>> s.filters("COSMIC60")
    ['Mutated Sample',
     '[y,n]',
     '',
     'naive_filters',
     'list',
     '=',
     'COSMIC60__MART__MAIN',
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
    >>> s.add_dataset_to_xml("COSMIC60")

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
    >>> s.add_filter_to_xml("validation_status", "verified"


You can create the XML request that will be send::

    >>> xml = s.get_xml()

And finally send the request:: 

    >>> res = s.query(xml)






