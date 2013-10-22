FAQS
########


.. _troubleshootings:

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

How to convert ID from one database to another ?
-----------------------------------------------------

Many web services provides convertors. In BioServices, you can access to Kegg
and UniProt that both provides convertor. For instance with Kegg, you can
convert all human (hsa) Kegg Id to uniprot Id with::

    from bioservices import *
    kegg_ids, uniprot_ids = s.conv("hsa", "uniprot")

Or you can use the uniprot mapping function::

    from bioservices import *
    u = UniProt()
    u.mapping(to="KEGG_ID", fr="ACC", query="ZAP70_HUMAN")

.. seealso:: :ref:`mapping`

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
