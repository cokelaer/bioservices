#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the Rhea web services

.. topic:: What is Rhea ?

    :URL: http://www.ebi.ac.uk/rhea/
    :Citations: See http://www.ebi.ac.uk/rhea/about.xhtml

    .. highlights::

        Rhea is a reaction database, where all reaction participants (reactants
        and products) are linked to the ChEBI database (Chemical Entities of
        Biological Interest) which provides detailed information about structure,
        formula and charge. Rhea provides built-in validations that ensure both
        elemental and charge balance of the reactions... While the main focus of
        Rhea is enzyme-catalysed reactions, other biochemical reactions are also
        are included.

        The database is extensively cross-referenced. Reactions are currently linked
        to the EC list, KEGG and MetaCyc, and the reactions will be used in the
        IntEnz database and in all relevant UniProtKB entries. Furthermore, the
        reactions will also be used in the UniPathway database to generate
        pathways and metabolic networks.

        -- from Rhea Home page, Dec 2012 (http://www.ebi.ac.uk/rhea/about.xhtml)

"""
from collections import defaultdict

from bioservices.services import REST
from bioservices import logger

logger.name = __name__


__all__ = ["Rhea"]


class Rhea:
    """Interface to the `Rhea <http://www.ebi.ac.uk/rhea/rest/1.0/>`_ service

    You can search by compound name, ChEBI ID, reaction ID, cross reference
    (e.g., EC number) or citation (author name, title, abstract text, publication ID).
    You can use double quotes - to match an exact phrase - and the following
    wildcards:

        * ? (question mark = one character),
        * `*` (asterisk = several characters).

    Searching for caffe* will find reactions with participants such as caffeine,
    trans-caffeic acid or caffeoyl-CoA::

        from bioservices import Rhea
        r = Rhea()
        response = r.search("caffe*")

    Searching for a?e?o* will find reactions with participants such as acetoin,
    acetone or adenosine.::

        from bioservices import Rhea
        r = Rhea()
        response = r.search("a?e?o*")

    The :meth:`search` :meth:`entry` methods require a list of valid columns.
    By default all columns are used but you can restrict to only a few. Here is
    the description of the columns::

        rhea-id	:   reaction identifier (with prefix RHEA)
        equation :  textual description of the reaction equation
        chebi :	    comma-separated list of ChEBI names used as reaction participants
        chebi-id :  comma-separated list of ChEBI identifiers used as reaction participants
        ec :        comma-separated list of EC numbers (with prefix EC)
        uniprot :   number of proteins (UniProtKB entries) annotated with the Rhea reaction
        pubmed :    comma-separated list of PubMed identifiers (without prefix)

    and 5 cross-references::

        reaction-xref(EcoCyc)
        reaction-xref(MetaCyc)
        reaction-xref(KEGG)
        reaction-xref(Reactome)
        reaction-xref(M-CSA)
    """

    _url = "https://www.rhea-db.org"

    _valid_columns = [
        "rhea-id",
        "equation",
        "chebi",
        "chebi-id",
        "ec",
        "uniprot",
        "pubmed",
        "reaction-xref(EcoCyc)",
        "reaction-xref(MetaCyc)",
        "reaction-xref(KEGG)",
        "reaction-xref(Reactome)",
        "reaction-ref(M-CSA)",
    ]

    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Rhea constructor

        :param bool verbose: True by default

        ::

            >>> from bioservices import Rhea
            >>> r = Rhea()
        """
        self.services = REST(name="Rhea", url=Rhea._url, verbose=verbose, cache=cache)

    def search(self, query, columns=None, limit=None, frmt="tsv"):
        """Search for Rhea (mimics https://www.rhea-db.org/)

        :param str query: the search term using format parameter
        :param str format: the biopax2 or cmlreact format (default)

        :Returns: A pandas DataFrame.

        ::

            >>> r = Rhea()
            >>> df = r.search("caffeine")
            >>> df = r.search("caffeine", columns='rhea-id,equation')


        """
        params = {}
        if limit:
            params["limit"] = limit
        if columns:
            params["columns"] = columns
        params["format"] = frmt
        if columns is None:
            params["columns"] = ",".join(self._valid_columns)

        response = self.services.http_get("rhea/?query={}".format(query), frmt="txt", params=params)

        try:
            import pandas as pd
            import io

            df = pd.read_csv(io.StringIO(response), sep="\t")
            return df
        except Exception as err:
            return response

    def query(self, query, columns=None, frmt="tsv", limit=None):
        """Retrieve a concrete reaction for the given id in a given format

        :param str query: the entry to retrieve
        :param str frmt: the result format (tsv); only tsv accepted for now (Nov
            2020).
        :param int limit: maximum number of results to retrieve
        :Returns: dataframe


        Retrieve Rhea reaction identifiers and equation text::

            r.query("", columns="rhea-id,equation", limit=10)

        Retrieve Rhea reactions with enzymes curated in UniProtKB (only first 10
        entries)::

            r.query("uniprot:*", columns="rhea-id,equation", limit=10)

        To retrieve a specific entry::

            df = r.get_entry("rhea:10661")


        .. versionchanged:: 1.8.0 (entry() method renamed in query() and no
            more format required. Must be given in the entry name e.g.
            query("10281.rxn") instead of entry(10281, format="rxn")
            the option *frmt* is now related to the result format

        """

        params = {"query": query}
        if limit:
            params["limit"] = limit
        if columns:
            params["columns"] = columns
        params["format"] = frmt
        if columns is None:
            params["columns"] = ",".join(self._valid_columns)

        response = self.services.http_get("rhea?".format(query), frmt="txt", params=params)
        try:
            import pandas as pd
            import io

            df = pd.read_csv(io.StringIO(response), sep="\t")
            return df
        except Exception as err:
            return response

    def get_metabolites(self, rxn_id):
        """Given a Rhea (http://www.rhea-db.org/) reaction id,
        returns its participant metabolites as a dict: {metabolite: stoichiometry},

        e.g. '2 H + 1 O2 = 1 H2O' would be represented ad {'H': -2, 'O2': -1, 'H2O': 1}.

        :param rxn_id: Rhea reaction id
        :return: dict of participant metabolites.
        """
        response = self.entry(rxn_id, frmt="cmlreact")

        reactants = [xx.attrs["title"] for xx in response.findAll("reactant")]
        products = [xx.attrs["title"] for xx in response.findAll("product")]
        return {"reactants": reactants, "products": products}
