.. _quickstart:

Quick Start
#################

Introduction
================

**BioServices** provides access to several Web Services. Each service requires some expertise on its own. 
In this Quick Start section, we will neither cover all the services nor all their functionalities. However,
it should give you a good overview of what you can do with **BioServices** (both from the user and developer point of views).

Before starting, let us remind what are Web Services. There provide an access to databases or applications via a web interface based on the SOAP/WSDL or the REST technologies. These technologies allow a programmatic access, which we take advantage in **BioServices**.

The REST technology uses URLs so there is no external dependency. 
You simply need to build a well-formatted URL and you will retrieve
an XML document that you can consume with your preferred technology
platform.

The SOAP/WSDL technology combines SOAP (Simple Object Access Protocol), which is
a messaging protocol for transporting information and the WSDL (Web Services
Description Language), which is a method for describing Web Services and their
capabilities.

What methods are available for a given service 
------------------------------------------------

Usually most of the service functionalities have been wrapped and we try to keep
the names as close as possible to the API. On top of the service methods, each
class inherits from the BioService class (REST or WSDL). For instance REST
service have the useful request method. Another nice function is the onWeb. 

.. seealso:: :class:`~bioservices.services.REST`, :class:`~bioservices.services.WSDLService`

What about the output ?
------------------------

Outputs depend on the service and functionalities of the service. It can be
heteregeneous. However, output are mostly XML formatted or in tabulated
separated column format (TSV). When XML is returned, it is usually parsed via the
BeautilSoup package (for instance you can get all children using getchildren() function).
Sometimes, we also convert output into dictionaries. So, it really depends on
the service/functionality you are using.



Let us look at some of the Web Services wrapped in **BioServices**.





UniProt service
================

Let us start with the :class:`~bioservices.uniprot.UniProt` class. With this 
class, you can access to uniprot services. In particular, you can map an ID 
from a database to another one. For instance to convert the UniProtKB ID into KEGG ID, use:

.. doctest::

    >>> from bioservices.uniprot import UniProt
    >>> u = UniProt(verbose=False)
    >>> u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query='P43403')
    {'results': [{'from': 'P43403', 'to': 'hsa:7535'}]}

Note that the returned response from uniprot web service is a dictionary with a key called **results**, which needs to be selected. Then, a list of identifiers is provided. 

You can also search for a specific UniProtKB ID to get exhaustive information::

    >>> print(u.search("P43403", frmt="txt"))
    ID   ZAP70_HUMAN             Reviewed;         619 AA.
    AC   P43403; A6NFP4; Q6PIA4; Q8IXD6; Q9UBS6;
    DT   01-NOV-1995, integrated into UniProtKB/Swiss-Prot.
    DT   01-NOV-1995, sequence version 1.
    ...

To obtain the FASTA sequence, you can use :meth:`~bioservices.uniprot.UniProt.searchUniProtId`::

    >>> print(u.searchUniProtId("P09958", frmt="fasta"))
    sp|P09958|FURIN_HUMAN Furin OS=Homo sapiens GN=FURIN PE=1 SV=2
    MELRPWLLWVVAATGTLVLLAADAQGQKVFTNTWAVRIPGGPAVANSVARKHGFLNLGQI
    FGDYYHFWHRGVTKRSLSPHRPRHSRLQREPQVQWLEQQVAKRRTKRDVYQEPTDPKFPQ
    QWYLSGVTQRDLNVKAAWAQGYTGHGIVVSILDDGIEKNHPDLAGNYDPGASFDVNDQDP
    DPQPRYTQMNDNRHGTRCAGEVAAVANNGVCGVGVAYNARIGGVRMLDGEVTDAVEARSL
    GLNPNHIHIYSASWGPEDDGKTVDGPARLAEEAFFRGVSQGRGGLGSIFVWASGNGGREH
    DSCNCDGYTNSIYTLSISSATQFGNVPWYSEACSSTLATTYSSGNQNEKQIVTTDLRQKC
    TESHTGTSASAPLAAGIIALTLEANKNLTWRDMQHLVVQTSKPAHLNANDWATNGVGRKV
    SHSYGYGLLDAGAMVALAQNWTTVAPQRKCIIDILTEPKDIGKRLEVRKTVTACLGEPNH
    ITRLEHAQARLTLSYNRRGDLAIHLVSPMGTRSTLLAARPHDYSADGFNDWAFMTTHSWD
    EDPSGEWVLEIENTSEANNYGTLTKFTLVLYGTAPEGLPVPPESSGCKTLTSSQACVVCE
    EGFSLHQKSCVQHCPPGFAPQVLDTHYSTENDVETIRASVCAPCHASCATCQGPALTDCL
    SCPSHASLDPVEQTCSRQSQSSRESPPQQQPPRLPPEVEAGQRLRAGLLPSHLPEVVAGL
    SCAFIVLVFVTVFLVLQLRSGFSFRGVKVYTMDRGLISYKGLPPEAWQEECPSDSEEDEG
    RGERTAFIKDQSAL

.. seealso:: Reference guide of :class:`bioservices.uniprot.UniProt` for more details

KEGG service
=============

.. testsetup:: kegg

    from bioservices import KEGG
    k = KEGG(verbose=False)

The KEGG interface is similar but contains more methods. The tutorial presents
the KEGG itnerface in details, but let us have a quick overview. First, let us start a KEGG instance::

    from bioservices import KEGG
    k = KEGG(verbose=False)

KEGG contains biological data for many organisms. By default, no organism is
set, which can be checked in the following attribute ::

    k.organism

We can set it to human using KEGG terminology for homo sapiens::

    k.organis = 'hsa'

You can use the :meth:`~bioservices.kegg.KEGG.dbinfo` to obtain statistics 
on the **pathway** database::

    >>> print(k.info("pathway"))
    pathway          KEGG Pathway Database
    path             Release 65.0+/01-15, Jan 13
                     Kanehisa Laboratories
                     218,277 entries

You can see the list of valid databases using the databases attribute. Each of the
database entry can also be listed using the :meth:`~bioservices.kegg.KEGG.list`
method. For instance, the organisms can be retrieved with::

    k.list("organism")

However, to extract the Ids extra processing is required. So, we provide aliases 
to retrieve the organism Ids easily::

    k.organismIds

The human organism is coded as "hsa". You can also get its T number instead:

.. doctest:: kegg

    >>> k.code2Tnumber("hsa")
    'T01001'


Every elements is referred to with a KEGG ID, which may be difficult to handle
at first. There are methods to retrieve the IDs though. For instance, get the list of 
pathways iIs for the current organism as follows::

    k.pathwayIds

For a given gene, you can get the full information related to that gene by using
the method :meth:`~bioservices.kegg.KEGG.get`::

    print(k.get("hsa:3586"))

or a pathway::

    print(k.get("path:hsa05416"))

.. seealso:: Reference guide of :class:`bioservices.kegg.KEGG` for more details
.. seealso:: :ref:`kegg_tutorial` for more details
.. seealso:: Reference guide of :class:`bioservices.kegg.KEGGParser` to parse a KEGG entry into a dictionary

.. WSDbfetch service
   ==================
   There is a uniprot module that allows to access to the uniprot WSDL. However,
   there are really few services and the only relevant method returns raw data that
   the user will need to scan. For instance::

..    >>> from bioservices import WSDbfetch
    >>> w = WSDbfetch()
    >>> data = w.fetchBatch("uniprot", "zap70_human", "xml", "raw")

.. .. seealso:: Reference guide of :class:`bioservices.dbfetch.DBFetch` for more details



QuickGO
=========

To acces to the GO interface, simply create an instance and look for a entry
using the :meth:`bioservices.quickgo.QuickGO.Term` method:

.. doctest::
    :options: +SKIP

    >>> from bioservices import QuickGO
    >>> g = QuickGO(verbose=False)
    >>> print(g.Term("GO:0003824", frmt="obo"))
    [Term]
    id: GO:0003824
    name: catalytic activity
    def: "Catalysis of a biochemical reaction at physiological temperatures. In
    biologically catalyzed reactions, the reactants are known as substrates, and the
    catalysts are naturally occurring macromolecular substances known as enzymes.
    Enzymes possess specific binding sites for substrates, and are usually composed
    wholly or largely of protein, but RNA that has catalytic activity (ribozyme) is
    often also regarded as enzymatic."
    synonym: "enzyme activity" exact
    xref: InterPro:IPR000183
    ...


.. seealso:: Reference guide of :class:`bioservices.quickgo.QuickGO` for more details

PICR service
=============


PICR, the Protein Identifier Cross Reference service provides 2 services
in WSDL and REST protocols. When it is the case, we arbitrary chose one of the
available protocol. In the PICR case, we implemented only the REST interface. The
methods available in the REST service are very similar to those available
via SOAP except for one major difference: only one accession or sequence
can be mapped per request.

The following example returns a XML document containing information about the
protein P29375 found in two specific databases::

    >>> from bioservices.picr import PICR
    >>> p = PICR()
    >>> res = p.getUPIForAccession("P29375", ["IPI", "ENSEMBL"])


.. seealso:: Reference guide of :class:`bioservices.picr.PICR` for more details


BioModels service
===================

You can access the biomodels service and obtain a model as follows::


    >>> from bioservices import biomodels
    >>> b = biomodels.BioModels()
    >>> model = b.get_model('BIOMD0000000299')

Then you can play with the SBML file with your favorite SBML tool.

In order to get the model IDs, you can look at the full list::

    >>> b.get_models()

.. seealso:: Reference guide of :class:`bioservices.biomodels.BioModels` for more details
.. seealso:: :ref:`biomodels_tutorial` for more details

Rhea service 
==============

Create a :class:`~bioservices.rhea.Rhea` instance as follows:

.. doctest::

    from bioservices import Rhea
    r = Rhea()

Rhea provides only 2 type of requests with a REST interface that are available with the :meth:`~bioservices.rhea.Rhea.search` and :meth:`~bioservices.rhea.Rhea.query` methods. 
Let us first find information about the chemical product **caffein** using the :meth:`search` method::

    response = r.search("caffein*")

The output is a JSON file that we convert in BioServices into a Pandas dataframe. 


The previous request returns more than 10,000 entries. Here are the first two
entries::

      Reaction identifier                                           Equation             ChEBI name           Cross-reference (KEGG)  Cross-reference (Reactome)
  0   RHEA:47148              a ubiquinone + caffeine + H2O = 1,3,7-trimethy...          MetaCyc:RXN-11523           KEGG:R07980                         NaN
  1   RHEA:10280              1,7-dimethylxanthine + S-adenosyl-L-methionine...          MetaCyc:RXN-7601            KEGG:R07921                         NaN


The second method provided is the :meth:`query` method. Given an Id, 
you can query the Rhea database using Id found earlier (e.g., 10280). This is
finally a filtering method as compared to the search method. If you kow what
your are looking for (the rhea-id) use this method instead of the search method::

    info = r.query("10280", columns="rhea-id,equation", limit=10)


.. seealso:: Reference guide of :class:`bioservices.rhea.Rhea` for more details


Other services
==================

There are many other services provided within **BioServices** and the reference
guide should give you all the information available with examples to start to
play with any of them. The home page of the services themselves is usually a
good starting point as well.

Services that are not available in **BioServices** can still be accesssed to quite
easily as demonstrated in the  :ref:`developer` section.





