from bioservices import RNASEQ_EBI


r = RNASEQ_EBI(cache=True)
assert 'homo_sapiens' in r.organisms


def test1():

    r.get_run_by_organism("homo_sapiens", "tsv")
    r.get_run_by_organism("homo_sapiens", "json")

def test2():

    r.get_run_by_study("SRP033494", mapping_quality=90, frmt='tsv')

def test3():
    res = r.get_study("SRP033494")

    assert res[0]['STUDY_ID'] == "SRP033494"

def test4():
    try:
        import pandas
        res = r.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
        studies = res['STUDY_ID'].values
    except:
        res = r.get_studies_by_organism("arabidopsis_thaliana", frmt='tsv')
        studies = [x['STUDY_ID'] for x in res]

def test5():
    r.get_sample_attribute_per_run("SRR805786")
    r.get_sample_attribute_per_study("SRP020492")
    r.get_sample_attribute_per_study("SRP020492")

