from bioservices import RNASEQ_EBI
import os
import pytest

# This services is deprecated
'''
skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
     reason="in maintenance")


@skiptravis
@pytest.fixture
def rnaseq():
    r = RNASEQ_EBI(cache=False)
    assert 'homo_sapiens' in r.organisms
    return r


@skiptravis
def test1(rnaseq):
    rnaseq.get_run_by_organism("homo_sapiens", "tsv")
    rnaseq.get_run_by_organism("homo_sapiens", "json")
    rnaseq.get_run_by_organism("homo_sapiens",condition="central nervous system")


@skiptravis
def test2(rnaseq):
    rnaseq.get_run_by_study("SRP033494", mapping_quality=90, frmt='tsv')


@skiptravis
def test3(rnaseq):
    res = rnaseq.get_study("SRP033494", "tsv")
    res = rnaseq.get_study("SRP033494", frmt="json")
    assert res[0]['STUDY_ID'] == "SRP033494"


@skiptravis
def test4(rnaseq):
    try:
        import pandas
        res = rnaseq.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
        studies = res['STUDY_ID'].values
    except:
        res = rnaseq.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
        studies = [x[0] for x in res[1:]]


@skiptravis
def test5(rnaseq):
    rnaseq.get_sample_attribute_per_run("SRR805786")
    rnaseq.get_sample_attribute_per_run("SRR805786", frmt='tsv')

    rnaseq.get_sample_attribute_per_study("SRP020492")
    rnaseq.get_sample_attribute_per_study("SRP020492", frmt='tsv')

    rnaseq.get_sample_attribute_per_study("SRP020492")
    rnaseq.get_sample_attribute_per_study("SRP020492", frmt='tsv')


@skiptravis
def test_get_run(rnaseq):
    res = rnaseq.get_run("SRR1042759")
    assert res[0]['RUN_IDS'] == "SRR1042759"
'''
