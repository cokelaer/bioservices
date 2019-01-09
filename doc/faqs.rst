FAQS
########


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


Installation issues
=======================

ValueError: unknown locale: UTF-8  under Mac OS X 10.7 - Lion
-----------------------------------------------------------------

The installation with PIP is succesful but I get a *"ValueError: unknown locale: UTF-8"* under Mac OS X 10.7 - Lion when typing **from bioservices import ***.

On solution is to fix your environment by typing the following code in a shell::

    export LANG="it_IT.UTF-8"
    export LC_COLLATE="it_IT.UTF-8"
    export LC_CTYPE="it_IT.UTF-8"
    export LC_MESSAGES="it_IT.UTF-8"
    export LC_MONETARY="it_IT.UTF-8"
    export LC_NUMERIC="it_IT.UTF-8"
    export LC_TIME="it_IT.UTF-8"
    export LC_ALL=


You can check if it works by typing ::

    python -c 'import locale; print(locale.getdefaultlocale());'

If this works without error, then it is fixed and you should be able to import
bioservices. If so, make this solution persistent by adding the
code into your environment. For that, just copy and paste the code in a file called
.bashrc_profile (or .bashrc)

:reference: `blog entry <http://patrick.arminio.info/blog/2012/02/fix-valueerror-unknown-locale-utf8/>`_


General questions
=====================

How can I figure out the taxonomy identifier of the mouse ?
-------------------------------------------------------------

You can use the Taxon class that uses Ensembl/UniProt/Eutils depending on the
tasks. Here, we do not know the scientific name of taxonomy identifier of the
mouse. We can use the search_by_name fuction:

.. warning:: Taxon class is not part of BioServices but some 
    utilities have been added to BioKit (github.com/biokit)

.. versionchanged:: 1.3

In earlier version of BioServices, you could use::

    >>> from bioservices import Taxon
    >>> t = Taxon()
    >>> t.search_by_name("mouse")
    u'10090'

But this is now in BioKit::

    >>> from biokit import Taxonomy
    >>> t = Taxonomy()
    >>> results = t.fetch_by_name('mouse')
    >>> results[0]['id']
    u'10090'


How to convert ID from one database to another ?
-----------------------------------------------------

Many web services provides convertors. In BioServices, you can access to Kegg
and UniProt that both provides convertor. For instance with Kegg, you can
convert all human (hsa) Kegg Id to uniprot Id with::

    from bioservices import *
    s = KEGG()
    kegg_ids, uniprot_ids = s.conv("hsa", "uniprot")

Or you can use the uniprot mapping function::

    from bioservices import *
    u = UniProt()
    u.mapping(to="KEGG_ID", fr="ACC", query="ZAP70_HUMAN")


Specific Usage
===================

Why my uniprot request takes forever ?
-----------------------------------------

This may happen. Consider::

    from bioservices import *
    u = UniProt()
    u.search("P53")

This request performed on UniProt web sites is actually pretty fast but there
are 386 pages of results. In BioServices, the search commands reads the 386
pages of results and then stores the result in a variable. So it may take a while. 

More generally if a request returns a very long result, it may take a while.
You can use the socket module::

    import socket
    socket.setdefaulttimeout(5.)

After 5 seconds, the read() call will stop returning whatever has been read so
far.


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


Interest of the BioServices classes REST and WSDL ?
====================================================

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


