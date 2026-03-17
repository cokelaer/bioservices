#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
"""Interface to the BioDBNet REST web service.

.. topic:: What is BioDBNet?

    :URL: https://biodbnet-abcc.ncifcrf.gov/
    :Service: https://biodbnet-abcc.ncifcrf.gov/webServices
    :Citation: Mudunuri,U., Che,A., Yi,M. and Stephens,R.M. (2009)
        bioDBnet: the biological database network. Bioinformatics, 25, 555-556.

    .. highlights::

        BioDBNet is a biological database network that provides identifier
        conversion between a large number of biological databases (Ensembl,
        Entrez Gene, UniProt, KEGG, Reactome, and many more). It supports
        cross-species ortholog mapping and path-based database traversal.

        -- BioDBNet website, Dec. 2012

"""
import pandas as pd

from bioservices import logger
from bioservices.services import REST

logger.name = __name__


__all__ = ["BioDBNet"]


class BioDBNet:
    """Interface to the `BioDBNet <https://biodbnet-abcc.ncifcrf.gov/>`_ service.

    BioDBNet converts biological identifiers between databases (Ensembl,
    UniProt, Entrez Gene, KEGG, Reactome, and many more).

    Example::

        >>> from bioservices import BioDBNet
        >>> b = BioDBNet()
        >>> b.getInputs()[:5]
        >>> df = b.db2db("UniProt Accession", ["Gene ID", "Gene Symbol"], "P43403")

    Use :meth:`db2db` to convert identifiers from one database to others.
    Use :meth:`dbReport` to convert to all possible output databases at once.
    Use :meth:`dbOrtho` for cross-species identifier conversion.
    Use :meth:`dbFind` when the identifier type is unknown.
    Use :meth:`dbWalk` to follow a custom path through the database network.
    """

    _url = "https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json"

    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param bool verbose: set to False to suppress informative messages
        :param bool cache: use HTTP cache
        """
        self.services = REST(name="BioDBNet", url=BioDBNet._url, verbose=verbose, cache=cache)
        self._valid_inputs = self.getInputs()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _list_to_string(self, values):
        """Convert a list of values to a comma-separated string."""
        if isinstance(values, list):
            values = ",".join(str(v) for v in values)
        return values

    def _interpret_output_db(self, input_db, output_db):
        """Validate output databases against those available for *input_db*."""
        outputs = self._list_to_string(output_db)
        outputResult = self.getOutputsForInput(input_db)
        outputResult = [o.lower().replace(" ", "") for o in outputResult]
        for output in outputs.split(","):
            if output.lower().replace(" ", "") not in outputResult:
                raise ValueError("{} not found in valid outputs for {}".format(output, input_db))
        return outputs

    def _check_db(self, value):
        """Raise ValueError if *value* is not a recognised input database."""

        def _normalise(v):
            return v.lower().replace(" ", "")

        if _normalise(value) not in [_normalise(v) for v in self._valid_inputs]:
            raise ValueError("Invalid value '{}': not a known database".format(value))

    # ------------------------------------------------------------------
    # Core conversion methods
    # ------------------------------------------------------------------

    def db2db(self, input_db, output_db, input_values, taxon=9606):
        """Convert identifiers from one database to one or more output databases.

        :param str input_db: input database name (e.g., ``"UniProt Accession"``).
        :param output_db: output database name or list of names
            (e.g., ``["Gene ID", "Gene Symbol"]``).
        :param input_values: single identifier string or list of identifiers.
        :param int taxon: NCBI taxonomy ID (default: 9606 for human).
        :return: :class:`pandas.DataFrame` indexed by the input identifier,
            with one column per output database.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> df = b.db2db("UniProt Accession", ["Gene ID", "Gene Symbol"], "P43403")
            >>> df.loc["P43403", "Gene Symbol"]
            'ZAP70'
            >>> df = b.db2db("Ensembl Gene ID", ["Gene Symbol"],
            ...              ["ENSG00000121410", "ENSG00000171428"], taxon=9606)

        """
        self._check_db(input_db)
        outputs = self._interpret_output_db(input_db, output_db)

        params = {
            "method": "db2db",
            "input": input_db,
            "outputs": outputs,
            "inputValues": self._list_to_string(input_values),
            "taxonId": taxon,
            "format": "row",
        }
        request = self.services.http_get(None, params=params)
        try:
            df = pd.DataFrame(request)
            df.set_index("InputValue", inplace=True)
            df.index.name = input_db
            return df
        except Exception as err:
            self.services.logging.error(err)
            return request

    def dbFind(self, output_db, input_values, taxon="9606"):
        """Find identifiers of unknown type and convert to an output database.

        Use when you do not know the identifier type, or when you have a
        mixture of different identifier types. BioDBNet detects the type
        automatically and converts to *output_db*.

        :param str output_db: output database name (e.g., ``"Gene ID"``).
        :param input_values: single identifier string or list of identifiers.
        :param str taxon: NCBI taxonomy ID as string (default: ``"9606"``).
        :return: :class:`pandas.DataFrame` indexed by the input value, with
            columns ``output_db`` and ``Input Type``.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> df = b.dbFind("Gene ID", ["ZMYM6_HUMAN", "NP_710159", "ENSP00000305919"])
            >>> df.loc["ZMYM6_HUMAN", "Gene ID"]
            '9204'

        """
        self._check_db(output_db)
        params = {
            "method": "dbfind",
            "output": output_db,
            "inputValues": self._list_to_string(input_values),
            "taxonId": taxon,
            "format": "row",
        }
        request = self.services.http_get(None, params=params)
        try:
            return pd.DataFrame(request).set_index("InputValue")
        except Exception as err:
            self.services.logging.error(err)
            return request

    def dbOrtho(self, input_db, output_db, input_values, input_taxon, output_taxon):
        """Convert identifiers from one species to identifiers of another species.

        :param str input_db: input database name (e.g., ``"Gene Symbol"``).
        :param str output_db: output database name (e.g., ``"Gene ID"``).
        :param input_values: single identifier string or list of identifiers.
        :param int input_taxon: NCBI taxonomy ID for the input species
            (e.g., 9606 for human).
        :param int output_taxon: NCBI taxonomy ID for the output species
            (e.g., 10090 for mouse).
        :return: :class:`pandas.DataFrame` indexed by the input identifier
            with a column for the output database.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> df = b.dbOrtho("Gene Symbol", "Gene ID", ["MYC", "MTOR", "A1BG"],
            ...                input_taxon=9606, output_taxon=10090)
            >>> df.loc["MYC", "Gene ID"]
            '17869'

        """
        self._check_db(input_db)
        self._check_db(output_db)
        params = {
            "method": "dbortho",
            "input": input_db,
            "output": output_db,
            "inputValues": self._list_to_string(input_values),
            "inputTaxon": input_taxon,
            "outputTaxon": output_taxon,
            "format": "row",
        }
        request = self.services.http_get(None, params=params)
        try:
            df = pd.DataFrame(request).set_index("InputValue")
            df.index.name = input_db
            return df
        except Exception as err:
            self.services.logging.error(err)
            return request

    def dbReport(self, input_db, input_values, taxon=9606):
        """Convert identifiers to *all* available output databases at once.

        Same as :meth:`db2db` but automatically uses every output database
        reachable from *input_db*, making it convenient for exploratory
        mapping.

        :param str input_db: input database name (e.g., ``"Ensembl Gene ID"``).
        :param input_values: single identifier string or list of identifiers.
        :param int taxon: NCBI taxonomy ID (default: 9606 for human).
        :return: :class:`pandas.DataFrame` indexed by the input identifier,
            with one column per output database.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> df = b.dbReport("UniProt Accession", ["P43403"])
            >>> "Gene Symbol" in df.columns
            True

        """
        self._check_db(input_db)
        params = {
            "method": "dbreport",
            "input": input_db,
            "inputValues": self._list_to_string(input_values),
            "taxonId": taxon,
            "format": "row",
        }
        request = self.services.http_get(None, params=params)
        try:
            df = pd.DataFrame(request)
            df.set_index("InputValue", inplace=True)
            df.index.name = input_db
            return df
        except Exception as err:
            self.services.logging.error(err)
            return request

    def dbWalk(self, db_path, input_values, taxon=9606):
        """Walk through the biological database network along a custom path.

        Gives full control over the conversion path. Useful when the same
        database appears at both ends of the path (e.g., converting human
        Ensembl Gene IDs to mouse Ensembl Gene IDs via Homologene).

        :param str db_path: ``"->"`-separated path of database names
            (e.g., ``"Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID"``).
        :param input_values: single identifier string or list of identifiers.
        :param int taxon: NCBI taxonomy ID (default: 9606).
        :return: :class:`pandas.DataFrame` with columns corresponding to
            each node in the path.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> path = "Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID"
            >>> df = b.dbWalk(path, ["ENSG00000121410"])

        """
        params = {
            "method": "dbwalk",
            "inputValues": self._list_to_string(input_values),
            "dbPath": db_path,
            "taxonId": taxon,
            "format": "row",
        }
        request = self.services.http_get(None, params=params)
        try:
            return pd.DataFrame(request)
        except Exception as err:
            self.services.logging.error(err)
            return request

    # ------------------------------------------------------------------
    # Database-discovery methods
    # ------------------------------------------------------------------

    def getInputs(self):
        """Return the list of all valid input database names.

        :return: list of database name strings.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> inputs = b.getInputs()
            >>> "UniProt Accession" in inputs
            True

        """
        params = {"method": "getinputs"}
        request = self.services.http_get(None, params=params)
        try:
            return request["input"]
        except Exception:
            return request

    def getOutputsForInput(self, input_db):
        """Return all output databases reachable from a given input database.

        :param str input_db: input database name (e.g., ``"UniProt Accession"``).
        :return: list of output database name strings.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> outputs = b.getOutputsForInput("UniProt Accession")
            >>> "Gene Symbol" in outputs
            True

        """
        self._check_db(input_db)
        params = {"method": "getoutputsforinput", "input": input_db}
        request = self.services.http_get(None, params=params)
        try:
            return request["output"]
        except Exception:
            return request

    def getDirectOutputsForInput(self, input_db):
        """Return databases reachable from *input_db* by a single edge.

        Unlike :meth:`getOutputsForInput`, which returns all transitively
        reachable databases, this returns only those connected by a direct
        single-hop edge in the BioDBNet graph.

        :param str input_db: input database name or normalised alias
            (e.g., ``"Gene Symbol"`` or ``"genesymbol"``).
        :return: list of directly connected output database name strings.

        Example::

            >>> from bioservices import BioDBNet
            >>> b = BioDBNet()
            >>> b.getDirectOutputsForInput("Gene Symbol")  # doctest: +SKIP
            >>> b.getDirectOutputsForInput("genesymbol")   # normalised alias  # doctest: +SKIP

        """
        self._check_db(input_db)
        params = {"method": "getdirectoutputsforinput", "input": input_db, "directOutput": 1}
        request = self.services.http_get(None, params=params)
        try:
            return request["output"]
        except Exception:
            return request
