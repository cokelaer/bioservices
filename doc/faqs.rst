Help & Credits
##############


.. _troubleshootings:

General Errors
================

The most common errors come from

#. The web service that you are trying to access is down (temporarily or not)
#. The web service API has changed
#. A request inside bioservices is incorrect
#. A timeout occured.

For the first problem, we cannot do anything except wait for the service to be
up again.

For the second, you are trying to update bioservices to reflect those changes.

For the two other issues, which are really bioservices problems, we recommend to
rerun your code setting the logging level to debug and send the code and errors
you see.

To set the debug level on on a web service::

    u = UniProt(verbose=True)
    u.logging.level = 'DEBUG'




General questions
=====================

How can I figure out the taxonomy identifier of the mouse ?
-------------------------------------------------------------

You can use the `EUtils` class to search the NCBI taxonomy database. Here is how
to find the taxonomy identifier of the mouse ("mouse")::

    >>> from bioservices import EUtils
    >>> e = EUtils()
    >>> res = e.ESearch(db="taxonomy", term="mouse")
    >>> res['idlist']
    ['10090']

This returns the identifiers, where `10090` is the taxon ID for *Mus musculus*.


How to convert ID from one database to another ?
-----------------------------------------------------

Many web services provides convertors. In BioServices, you can access to Kegg
and UniProt that both provides convertor. For instance with Kegg, you can
convert all human (hsa) Kegg Id to uniprot Id with::

    from bioservices import KEGG
    s = KEGG()
    kegg_ids, uniprot_ids = s.conv("hsa", "uniprot")

Or you can use the uniprot mapping function::

    from bioservices import UniProt
    u = UniProt()
    u.mapping(to="KEGG_ID", fr="ACC", query="ZAP70_HUMAN")


Specific Usage
===================

Why my uniprot request takes forever ?
-----------------------------------------

This may happen. Consider::

    from bioservices import UniProt
    u = UniProt()
    u.search("P53")

This request performed on UniProt web sites is actually pretty fast but there
may be hundreds of pages of results. In BioServices, the search command reads all
pages and stores the result in a variable. So it may take a while.

More generally, if a request takes too long, you can configure a timeout for the
underlying REST service rather than for the whole python environment::

    from bioservices import UniProt
    u = UniProt()
    u.services.TIMEOUT = 5.0 # seconds

After 5 seconds, the request will raise a Timeout error if it hasn't completed.


KEGG service
----------------

Is it possible to get the pathway information for multiple proteins ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently there is no such function. You can only retrieve pathways  given a
single protein Id. However, you can easily write such a function. Here is the
code for 2 proteins::

    >>> p1 = k.get_pathway_by_gene("7535", "hsa")   # correspond to ZAP70
    >>> p2 = k.get_pathway_by_gene("6885", "hsa")   # 6885 correspond to MAP3K7
    >>> [k1 for k1 in p1.keys() if k1 in p2.keys()]
    ['hsa04660', 'hsa04064']


There are 2 pathways containing the proteins 7535 and 6885.


Interest of the BioServices REST base class
============================================

There are a few technical aspects covered by BioServices to ease our life when
adding new modules such as timeout, long request, headers, and so on.


What is the difference between GET and POST
-----------------------------------------------

When the user enters information in a form and clicks Submit , there are two
ways the information can be sent from the browser to the server: in the URL, or
within the body of the HTTP request.

The alternative to the GET method is the POST method. This method packages the
name/value pairs inside the body of the HTTP request, which makes for a cleaner
URL and imposes no size limitations on the forms output. It is also more
secure.


.. _contributors:

Credits
=======

Contributors are the authors who started the development of BioServices
(and authors of this reference on `BioInformatics <http://bioinformatics.oxfordjournals.org/content/29/24/3241>`_).

In addition to the main authors of the papers the following developers have
implemented modules now available in BioServices:

 * Achilles Rasquinha implemented the BiGG models service :class:`bioservices.bigg` module
 * Sven-Maurice Althoff, Christian Knauth implemented the :class:`bioservices.muscle` module.
 * Patrick Short implemented the :class:`bioservices.clinvitae` module

And thank you also to the contributions from users who have sent communication
via emails or via the `ticket system <https://github.com/cokelaer/bioservices/issues>`_.

Special thanks to Thoba Lose (https://github.com/thobalose) and
https://github.com/jsmusach for various pull requests.

Note that originally code (and earlier tickets) were hosted `elsewhere <https://www.assembla.com/spaces/bioservices/tickets>`_.
