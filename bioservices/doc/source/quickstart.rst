.. _quickstart:

Quick Start
#################



Kegg
=====


Start a kegg interface (default organism is human, that is called hsa)::

    from bioservices.kegg import Kegg
    k = Kegg()


By default, the organism is human (hsa) but you can change it::

    k.organism = "dosa"
    k.organism = "hsa"

In order to get the list of valid organisms, type::

    print k.organisms

Every elements is referred to with a Kegg ID, which may be difficult to handle
at first. There are methods to retrieve the IDs though. For instance, get the list of 
pathways ids for the current organism as follows::

    k.pathways

Now, you can various requests but let us first open a pathway in a browser::

    k.color_pathway_by_elements('path:hsa04660')

Genes within a pathway can be retrieved with the method::

    k.get_genes_by_pathway("path:hsa04660")

For a given gene, you can get the full information related to that gene by using
the method :meth:`~bioservices.kegg.Kegg.bget`::

    k.bget("hsa:3586")

Commands shown so far are part of the Kegg WSDL service. Most of the Kegg
methods are directly available. To obtain all methods, type ::

    k.methods

If a method is not found, you can still directly access to the
service method via the attribute :meth:`~bioservices.kegg.Kegg.serv`.

In addition to the Kegg service, we implemented extra commands. 
The tutorial links here below provides more examples.

Uniprot
===========

There is a uniprot module that allows to access to the uniprot WSDL. However,
there are really few service and the only relevant method returns raw data that
the user will need to scan. For instance::



    >>> from bioservices import uniprot
    >>> u = uniprot.Uniprot()
    >>> data = u.fetchBatch("uniprot" ,"zap70_human", "xml", "raw")

Then, you need to scan it with xml standard python module::

    >>> import xml.etree.ElementTree as ET
    >>> root = ET.fromstring(data)

Biomodels
==============

You can access to the biomodels service and obtain a model as follows::


    >>> from bioservices import biomodels
    >>> b = biomodels.BioModels()
    >>> b.getModelSBMLById('BIOMD0000000299')



More Tutorials
=================

.. toctree::

    kegg_tutorial.rst
    biomodels.rst
