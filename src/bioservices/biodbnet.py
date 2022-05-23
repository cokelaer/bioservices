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
"""This module provides a class :class:`~BioDBNet` to access to BioDBNet WS.


.. topic:: What is BioDBNet ?

    :URL: http://biodbnet.abcc.ncifcrf.gov/
    :Service: http://biodbnet.abcc.ncifcrf.gov/webServices
    :Citations:  Mudunuri,U., Che,A., Yi,M. and Stephens,R.M. (2009) bioDBnet: the biological database network. Bioinformatics, 25, 555-556

    .. highlights::

        "BioDBNet Database is a repository hosting computational models of biological
        systems. A large number of the provided models are published in the
        peer-reviewed literature and manually curated. This resource allows biologists
        to store, search and retrieve mathematical models. In addition, those models can
        be used to generate sub-models, can be simulated online, and can be converted
        between different representational formats. "

        -- From BioDBNet website, Dec. 2012

    .. versionadded:: 1.2.3
    .. sectionauthor:: Thomas Cokelaer, Feb 2014

"""
import io
from bioservices.services import REST
from bioservices import logger

logger.name = __name__

try:
    import pandas as pd
except:
    pass

__all__ = ["BioDBNet"]


class BioDBNet:
    """Interface to the `BioDBNet <http://biodbnet.abcc.ncifcrf.gov/>`_ service

    ::

        >>> from bioservices import *
        >>> s = BioDBNet()

    Most of the BioDBNet WSDL are available. There are functions added to
    the original interface such as :meth:`extra_getReactomeIds`.

    Use :meth:`db2db` to convert from 1 database to some databases.
    Use :meth:`dbReport` to get the convertion from one database to all
    databases.

    """

    _url = "https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json"

    def __init__(self, verbose=True, cache=False):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        self.services = REST(name="BioDBNet", url=BioDBNet._url, verbose=verbose, cache=cache)
        self._valid_inputs = self.getInputs()

    def _list_to_string(self, values):
        if isinstance(values, list):
            values = ",".join(values)
        return values

    def _interpret_output_db(self, input_db, output_db):
        # in biodbnet, the database can be provided as
        # in the output of getInputs() that is with capitals and spaces
        # or with no spaces and no big caps.
        # Here, like in _check_db(), with convert everything to small caps and
        # remove spaces so as to compare the input/output databases with the
        # list of databases returned by getInputs
        outputs = self._list_to_string(output_db)
        inputResult = self.getInputs()
        # getOutputsForInput method
        outputResult = self.getOutputsForInput(input_db)
        outputResult = [this.lower().replace(" ", "") for this in outputResult]
        for output in outputs.split(","):
            if output.lower().replace(" ", "") not in outputResult:
                raise ValueError(output + " not found")
        return outputs

    def _check_db(self, value):
        def convert(value):
            return value.lower().replace(" ", "")

        if convert(value) not in [convert(this) for this in self._valid_inputs]:
            raise ValueError("Invalid value {} not a known database".format(value))

    def db2db(self, input_db, output_db, input_values, taxon=9606):
        """Retrieves models associated to the provided Taxonomy text.

        :param input_db: input database.
        :param output_db: list of databases to map to.
        :param input_values: list of identifiers to map to the output databases
        :return:  dataframe where index correspond to the input database
            identifiers. The columns contains the identifiers for each output
            database (see example here below).

        ::

            >>> from bioservices import BioDBNet
            >>> input_db = 'Ensembl Gene ID'
            >>> output_db = ['Gene Symbol']
            >>> input_values = ['ENSG00000121410', 'ENSG00000171428']
            >>> df = s.db2db(input_db, output_db, input_values, 9606)
                            Gene Symbol
            Ensembl Gene ID
            ENSG00000121410        A1BG
            ENSG00000171428        NAT1

        """
        self._check_db(input_db)
        # This also check that the outputs exist and are compatible with the
        # input.
        outputs = self._interpret_output_db(input_db, output_db)

        url = self._url + "?method=db2db"
        url += "&input={}".format(input_db)
        url += "&outputs={}".format(outputs)
        url += "&inputValues={}".format(self._list_to_string(input_values))
        url += "&taxonId={}".format(taxon)
        url += "&format={}".format("row")
        request = self.services.http_get(url)
        try:  # TODO can be removed in v2
            df = pd.DataFrame(request)
            df.set_index("InputValue", inplace=True)
            df.index.name = input_db
            return df
        except Exception as err:
            self.logging.error(err)
            return request

    def dbFind(self, output_db, input_values, taxon="9606"):
        """dbFind method

        dbFind can be used when you do not know the actual type of your identifiers or
        when you have a mixture of different types of identifiers. The tool finds the
        identifier type and converts them into the selected output if the identifiers
        are within the network.

        :param str output_db: valid database name
        :param list input_values: list of identifiers to look for
        :return: a dataframe with index set to the input values.


        ::

            >>> b.dbFind("Gene ID", ["ZMYM6_HUMAN", "NP_710159", "ENSP00000305919"])
                            Gene ID                Input Type
            InputValue
            ZMYM6_HUMAN        9204        UniProt Entry Name
            NP_710159        203100  RefSeq Protein Accession
            ENSP00000305919  203100        Ensembl Protein ID

        """
        self._check_db(output_db)

        url = self._url + "?method=dbfind"
        url += "&output={}".format(output_db)
        url += "&inputValues={}".format(self._list_to_string(input_values))
        url += "&taxonId={}".format(taxon)
        url += "&format={}".format("row")
        request = self.services.http_get(url)
        try:
            return pd.DataFrame(request).set_index("InputValue")
        except:
            return request

    def dbOrtho(self, input_db, output_db, input_values, input_taxon, output_taxon):
        """Convert identifiers from one species to identifiers of a different species

        :param input_db: input database
        :param output_db: output database
        :param input_values: list of identifiers to retrieve
        :param input_taxon: input taxon
        :param output_taxon: output taxon
        :return:  dataframe where index correspond to the input database
            identifiers. The columns contains the identifiers for each output
            database (see example here below)

        ::

            >>> df = b.dbOrtho("Gene Symbol", "Gene ID", ["MYC", "MTOR", "A1BG"],
            ...                    input_taxon=9606, output_taxon=10090)
                 Gene ID InputValue
            0   17869        MYC
            1   56717       MTOR
            2  117586       A1BG

        """
        self._check_db(input_db)
        self._check_db(output_db)
        url = self._url + "?method=dbortho"
        url += "&input={}".format(input_db)
        url += "&output={}".format(output_db)
        url += "&inputValues={}".format(self._list_to_string(input_values))
        url += "&inputTaxon={}".format(input_taxon)
        url += "&outputTaxon={}".format(output_taxon)
        url += "&format={}".format("row")
        request = self.services.http_get(url)

        try:
            df = pd.DataFrame(request).set_index("InputValue")
            df.index.name = input_db
            return df
        except:
            return request

    def dbReport(self, input_db, input_values, taxon=9606):
        """Same as :meth:`db2db` but returns results for all possible outputs.

        :param input_db: input database
        :param input_values: list of identifiers to retrieve
        :return:  dataframe where index correspond to the input database
            identifiers. The columns contains the identifiers for each output
            database (see example here below)

        ::

            df = s.dbReport("Ensembl Gene ID", ['ENSG00000121410', 'ENSG00000171428'])

        """
        self._check_db(input_db)
        # This also check that the outputs exist and are compatible with the
        # input.
        url = self._url + "?method=dbreport"
        url += "&input={}".format(input_db)
        url += "&inputValues={}".format(self._list_to_string(input_values))
        url += "&taxonId={}".format(taxon)
        url += "&format={}".format("row")
        request = self.services.http_get(url)
        try:  # TODO can be removed in v2
            df = pd.DataFrame(request)
            df.set_index("InputValue", inplace=True)
            df.index.name = input_db
            return df
        except Exception as err:
            self.logging.error(err)
            return request
        inputValues = self._interpret_input_db(inputValues)

        # df = pd.readcsv(io.StringIO(res.strip()), sep="\t")

    def dbWalk(self, db_path, input_values, taxon=9606):
        """Walk through biological database network

        dbWalk is a form of database to database conversion where the user has complete
        control on the path to follow while doing the conversion. When a input/node is
        added to the path the input selection gets updated with all the nodes that it
        can access directly.

        :param db_path: path to follow in the databases
        :param input_values: list of identifiers
        :return: a dataframe with columns corresponding to the path nodes

        A typical example is to get the Ensembl mouse homologs for
        Ensembl Gene ID's from human. This conversion is not possible
        through :meth:`db2db` as Homologene does not have
        Ensembl ID's and the input and output nodes to acheive this would both be
        'Ensembl Gene ID'. It can however be run by using dbWalk as follows.
        Add Ensembl Gene ID to the path, then add Gene Id, Homolog - Mouse Gene ID
        and Ensebml Gene ID to complete the path.

        ::

            db_path = "Ensembl Gene ID->Gene ID->Homolog - Mouse Gene ID->Ensembl Gene ID"
            s.dbWalk(db_path, ["ENSG00000175899"])

        .. todo:: check validity of the path

        """
        url = self._url + "?method=dbwalk"
        url += "&inputValues={}".format(self._list_to_string(input_values))
        url += "&dbPath={}".format(db_path)
        url += "&taxonId={}".format(taxon)
        url += "&format={}".format("row")
        request = self.services.http_get(url)
        try:
            return pd.DataFrame(request)
        except:
            return request

    def getDirectOutputsForInput(self, input_db):
        """Gets all the direct output nodes for a given input node

        Gets all the direct output nodes for a given input node
        Outputs reachable by single edge connection in the bioDBnet graph.

        ::

            b.getDirectOutputsForInput("genesymbol")
            b.getDirectOutputsForInput("Gene Symbol")
            b.getDirectOutputsForInput("pdbid")
            b.getDirectOutputsForInput("PDB ID")
        """
        self._check_db(input_db)

        url = self._url
        url += "?method=getdirectoutputsforinput"
        url += "&input={}&directOutput=1".format(input_db)
        request = self.services.http_get(url)
        try:
            return request["output"]
        except:
            return request

    def getInputs(self):
        """Return list of possible input database

        ::

            s.getInputs()
        """
        request = self.services.http_get(self._url + "?method=getinputs")
        try:
            return request["input"]
        except:
            return request

    def getOutputsForInput(self, input_db):
        """Return list of possible output database for a given input database

        ::

            s.getOutputsForInput("UniProt Accession")

        """
        self._check_db(input_db)
        url = self._url + "?method=getoutputsforinput"
        url += "&input={}".format(input_db)
        request = self.services.http_get(url)
        try:
            return request["output"]
        except:
            return request
