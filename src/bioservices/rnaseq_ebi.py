#
#  This file is part of bioservices software
#
#  Copyright (c) 2016 - EBI-EMBL
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
"""Interface to web service that analysed 200,000 RNA-seq runs in 185 organisms
provided by EMBL-EBI Gene Expression Team.

.. topic:: RNASEQ_EBI ?

    :URL: http://www.ebi.ac.uk/~rpetry/geteam/rnaseq/apispec.pdf
    :Citation: http://www.ebi.ac.uk/~rpetry/geteam/rnaseq/apispec.pdf

    .. highlights::



"""
import types
import io
from bioservices.services import REST

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    import pandas as pd

    def tsv_parser(data):
        return pd.read_csv(StringIO(data), sep="\t")

except:

    def tsv_parser(data):
        """return a list of list"""
        print("pandas library is not installed. ")
        print("TSV results will not be interpreted  with Pandas.")
        try:
            data = data.split("\n")
            data = [this.split("\t") for this in data]
        except:
            pass
        return data


__all__ = ["RNASEQ_EBI"]


class RNASEQ_EBI(REST):
    """Interface to the `RNA-SEQ ANALYSIS API <http://www.ebi.ac.uk/fg/rnaseq/api>`_ service

    Example ::

        >>> from bioservices import RNASEQ_EBI
        >>> r = RNASEQ_EBI()
        >>> r.organisms
        >>> r.get_run_by_organism('homo_sapiens')

    See http://www.ebi.ac.uk/~rpetry/geteam/rnaseq/apispec.pdf for the original
    documentation

    """

    def __init__(self, verbose=False, cache=False):
        """**Constructor**

        :param verbose: set to False to prevent informative messages
        """
        print("This service is deprecated")

        # super(RNASEQ_EBI, self).__init__(name="UniProt",
        #        url="http://www.ebi.ac.uk/fg/rnaseq/api",
        #        verbose=verbose, cache=cache)
        # self._organisms = None


'''
    def get_run_by_organism(self, organism, frmt="json", mapping_quality=70,
        condition=None):
        """

        :param organism: Check the :attr:`organism` attributes for valid names
        :param frmt: json or tsv
        :param mapping_quality: Min. percentage of reads mapped to genome reference
        :param condition: check if it exists in EFO (e.g. cancer)
            ( http://www.ebi.ac.uk/efo)

        :return: If Pandas is installed and frmt is set to *tsv*, the
            returned object is a Pandas DataFrame. If Pandas is not available,
            a list of list is returned. The first element being the names of the
            field, and each sub list an entry. If *frmt* is set to json, a list
            of entries is returned, each of them being a dictionary.

        Examples::

            from bioservices import RNASEQ_EBI
            r = RNASEQ_EBI()
            results = r.get_run_by_organism('oryza_longistaminata', frmt='tsv')
            results = r.get_run_by_organism('homo_sapiens', frmt='tsv',
                            condition="central nervous system")


        .. csv-table:: Returned fields
            :header: "name", "description"
            :widths: 30,70

            ASSEMBLY_USED ,      Genome reference assembly name
            BIOREP_ID,           ENA Run ID or a unique label for tech. replicates in RUN_IDS
            ENA_LAST_UPDATED ,   Date ENA record for was last updated
            FTP_LOCATION,        FTP location of the CRAM file
            LAST_PROCESSED_DATE, Date the run(s) were last analysed
            ORGANISM,            Organism of samples in SAMPLE_IDS
            MAPPING_QUALITY ,    Percentage of reads mapped to the genome reference
            REFERENCE_ORGANISM,  Genome reference organism
            RUN_IDS,             List of ENA Run ID's corresponding to BIOREP_ID
            SAMPLE_ATTRIBUTE_TYPE, Matched sample attribute type
            SAMPLE_ATTRIBUTE_VALUE, Matched sample attribute value
            SAMPLE_IDS,         List of BioSamples DB ID's corresponding to BIOREP_ID
            STATUS,             Processing status
            STUDY_ID,           ENA Study ID


        """
        assert frmt in ["tsv", "json"]
        assert mapping_quality >0 and mapping_quality <100
        assert organism in self.organisms

        if condition is None:
            results = self.http_get("%s/%s/getRunsByOrganism/%s" %
                (frmt, mapping_quality, organism), frmt=frmt)
        else:
            results = self.http_get("%s/%s/getRunsByOrganismCondition/%s/%s" %
                (frmt, mapping_quality, organism, condition), frmt=frmt)

        if frmt == 'tsv':
            results = tsv_parser(results)

        return results

    def get_run(self, run_id, frmt="json", mapping_quality=70):
        """

        :param run_id: a valid run identifier (e.g., SRR1042759)
        :param frmt: json or tsv
        :param mapping_quality: Min. percentage of reads mapped to genome reference

        """
        assert frmt in ["tsv", "json"]
        assert mapping_quality >0 and mapping_quality <100
        results = self.http_get("%s/%s/getRun/%s" %
            (frmt, mapping_quality, run_id), frmt=frmt)
        if frmt == 'tsv':
            results = tsv_parser(results)

        return results


    def get_run_by_study(self, study, frmt="json", mapping_quality=70):
        """Access to the RUNS for a given study


        :param study: a valid study name eg SRP1042759
        :param frmt: json or tsv
        :param mapping_quality: Min. percentage of reads mapped to genome reference


        :return: See :meth:`get_run_by_organism`


        Example::

            r.get_run_by_study("SRP033494", mapping_quality=90, frmt='tsv')

        """


        assert frmt in ["tsv", "json"]
        assert mapping_quality >0 and mapping_quality <100

        results = self.http_get("%s/%s/getRunsByStudy/%s" %
                    (frmt, mapping_quality, study), frmt=frmt)

        if frmt == 'tsv':
            results = tsv_parser(results)

        return results

    def get_study(self, study, frmt="json"):
        """Retrieve a study data

        :param study: valid study name (see :meth:`get_studies_by_organism`)
        :return: a dictionary if frmt is set to jsonwith fields as described in
            :meth:`get_studies_by_organism`

        Example::

            r.get_study("SRP033494")


        """
        assert frmt in ["tsv", "json"]
        results = self.http_get("%s/getStudy/%s" %
                    (frmt, study), frmt=frmt)
        if frmt == 'tsv':
            results = tsv_parser(results)

        return results


    def get_studies_by_organism(self, organism, frmt='json'):
        """

        :param organism: Check the :attr:`organism` attributes for valid names
        :param frmt: json or tsv


        If you have Pandas install this code will return the list of valid
        studies for a given orgnanism::

            res = r.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
            studies = res['STUDY_ID'].values

        Otherwise, if you use the *tsv* format and do not have Pandas
        installed::

            res = r.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
            studies = [x[0] for x in res[1:]]

        Of with json output::

            res = r.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
            studies = [x['STUDY_ID'] for x in res]


        Note that in addition to study names, each study stores a set of fields
        as follows:

        .. csv-table:: Returned fields
            :header: "name", "description"
            :widths: 30,70


            ASSEMBLY_USED,                  Genome reference assembly name
            EXONS_FPKM_COUNTS_FTP_LOCATION, FTP location of exon FPKM counts
            EXONS_RAW_COUNTS_FTP_LOCATION,  FTP location of exon raw counts
            GENES_FPKM_COUNTS_FTP_LOCATION, FTP location of gene FPKM counts
            GENES_RAW_COUNTS_FTP_LOCATION,  FTP location of genes raw counts
            GTF_USED,                       Ensembl GTF file used for quantification
            LAST_PROCESSED_DATE,            Date the run(s) were last analysed
            ORGANISM,                       Organism studied in STUDY_ID
            REFERENCE_ORGANISM,             Genome reference organism
            SOFTWARE_VERSIONS_FTP_LOCATION,  FTP location of pipeline tools info
            STATUS,                         processing status
            STUDY_ID,                       ENA Study I

        """
        assert frmt in ["tsv", "json"]
        assert organism in self.organisms, "invalid organism"

        results = self.http_get("%s/getStudiesByOrganism/%s" %
                    (frmt, organism), frmt=frmt)

        if frmt == 'tsv':
            results = tsv_parser(results)

        return results

    def _get_organism(self):
        if self._organisms is None:
            self.logging.info("Fetching all organisms once for all")
            frmt = 'tsv'
            res1 = self.http_get("%s/0/getOrganisms/ensembl" % frmt, frmt)
            res1 = res1.split("\n")

            res2 = self.http_get("%s/0/getOrganisms/plants" % frmt, frmt)
            res2 = res2.split("\n")

            res3 = self.http_get("%s/0/getOrganisms/fungi" % frmt, frmt)
            res3 = res3.split("\n")

            res4 = self.http_get("%s/0/getOrganisms/fungi" % frmt, frmt)
            res4 = res4.split("\n")

            res = res1 + res2 + res3 + res4
            res = sorted(list(set(res)))

            res = [this.split('\t')[0] for this in res]
            res.remove("ORGANISM")

            self._organisms = res
        return self._organisms
    organisms = property(_get_organism, doc="return list of valid organisms")

    def get_sample_attribute_per_run(self, run_id, frmt='json'):
        """Return attributes of a given RUN ID

        :param: a run ID
        :param frmt: tsv or json
        :return: list of entries with the following fields

        .. csv-table:: Returned fields
            :header: "name", "description"
            :widths: 30,70

            FO_URL,     URL of EFO term matching VALUE
            RUN_ID,     ENA Run ID
            STUDY_ID,   ENA Study ID
            TYPE,       Sample Attribute Type
            VALUE,      Sample Attribute Value
            NUM_OF_RUNS, Number of runs annotated with TYPE/VALUE
            PCT_OF_ALL_RUNS, Runs annotated with TYPE/VALUE as a percentage of all runs

        Example::

            r.get_sample_attribute_per_run("SRR805786")

        """
        assert frmt in ["tsv", "json"]

        results = self.http_get("%s/getSampleAttributesByRun/%s" %
                    (frmt, run_id), frmt=frmt)

        if frmt == 'tsv':
            results = tsv_parser(results)
        return results

    def get_sample_attribute_per_study(self, study_id, frmt='json'):
        """Return attributes of a given RUN ID

        :param: a run ID
        :param frmt: tsv or json
        :return: list of entries with the fields as described in
            :meth:`get_sample_attribute_per_run`


        Example::

            r.get_sample_attribute_per_study("SRP020492")

        """
        assert frmt in ["tsv", "json"]

        results = self.http_get("%s/getSampleAttributesPerRunByStudy/%s" %
                    (frmt, study_id), frmt=frmt)

        if frmt == 'tsv':
            results = tsv_parser(results)
        return results

    def get_sample_attribute_coverage_per_study(self, study_id, frmt='json'):
        """Return attributes of a given RUN ID

        :param: a run ID
        :param frmt: tsv or json
        :return: list of entries with the fields as described in
            :meth:`get_sample_attribute_per_run`


        Example::

            r.get_sample_attribute_per_study("SRP020492")

        """
        assert frmt in ["tsv", "json"]

        results = self.http_get("%s/getSampleAttributesCoverageByStudy/%s" %
                    (frmt, study_id), frmt=frmt)

        if frmt == 'tsv':
            results = tsv_parser(results)
        return results

'''
