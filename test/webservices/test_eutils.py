from bioservices.eutils import EUtilsParser, EUtils
import pytest

@pytest.fixture
def eutils():
    return EUtils(verbose=False)


def test_taxonomy(eutils):
    ret = eutils.taxonomy_summary("9606")
    assert ret['9606']['taxid'] == 9606


def test_snp(eutils):
    eutils.snp_summary("123")


def test_databases(eutils):
    assert "proteinclusters" in eutils.databases


def test_summary(eutils):
    ret = eutils.ESummary("taxonomy", "9606,9913")
    assert ret['9606']['taxid'] == 9606
    assert ret['9913']['taxid'] == 9913

    # test another database 
    ret = eutils.ESummary("structure", "10000")
    assert ret['10000']['pdbacc'] == '1CA4'


def test_espell(eutils):
    ret = eutils.ESpell(db="pubmed", term="aasthma+OR+alergy")
    ret = ret['eSpellResult']
    assert ret['Query'] == 'aasthma OR alergy'
    assert ret['CorrectedQuery'] == 'asthma or allergy'


def test_esearch(eutils):
    ret = eutils.ESearch('protein', 'human', RetMax=5)


def test_elink(eutils):
    ret = eutils.ELink(db="pubmed", dbfrom="pubmed", id="20210808",
                       cmd="neighbor_score")

    ret = eutils.ELink(db="pubmed", id="24064416")

    # assert len(ret.LinkSet[0].LinkSetDb[0].Link) > 10

    eutils.ELink(dbfrom="nucleotide", id="48819,7140345", db="protein")

def test_einfo(eutils):
    # Use XML
    dbinfo = eutils.EInfo("gtr")
    dbinfo = dbinfo[0]
    assert dbinfo['dbname'] == 'gtr'
    assert dbinfo['menuname'] == 'GTR'
    assert dbinfo['description'] == 'GTR Database'

    # use JSON
    ret = eutils.EInfo("taxonomy")[0]
    ret['count']

    alldbs = eutils.EInfo()
    for db in ['pubmed', 'genome', 'dbvar', 'gene']:
        assert db in alldbs
    assert len(alldbs) > 40  # 52 Aug 2014 but let us be on the safe side


def test_einfo_pubmed(eutils):
    ret = eutils.EInfo('pubmed')[0]
    assert ret['dbname'] == 'pubmed'
    assert ret['menuname'] == 'PubMed'
    assert ret['description'] == 'PubMed bibliographic record'
    assert int(ret['count']) > 17905967
    assert ret['lastupdate']
    assert len(ret['fieldlist']) >= 40
    assert ret['fieldlist'][0]['name'] == 'ALL'
    assert ret['fieldlist'][0]['fullname'], 'All Fields'


def test_gquery(eutils):
    ret = eutils.EGQuery("asthma")
    [(x.DbName, x.Count) for x in ret.eGQueryResult.ResultItem
     if x.Count != '0']

@pytest.mark.xfail
def test_efetch(eutils):
    ret = eutils.EFetch("omim", "269840")
    ret1 = eutils.EFetch("protein", "34577063",
                         retmode="text", rettype="fasta", stand=1)
    ret2 = eutils.EFetch("protein", "34577063",
                         retmode="text", rettype="fasta", stand=2)
    eutils.EFetch("protein", "34577063",
                  retmode="text", rettype="fasta", strand=2,
                  seq_start=10, seq_stop=20)

    ret = eutils.EFetch('pubmed', '12091962,9997',
                        retmode='xml', rettype='abstract')
    # sequences
    res1 = eutils.EFetch("protein", "352, 234",
                         retmode="text", rettype="fasta")
    res2 = eutils.EFetch("protein", ["352", "234"],
                         retmode="text", rettype="fasta")
    res3 = eutils.EFetch("protein", [352, 234],
                         retmode="text", rettype="fasta")

    assert res1 == res2
    assert res2 == res3
    assert res1 == res3

def test_efetch_gene(eutils):
    res = eutils.EFetch('gene', 4747, retmode="text")
    assert b'neurofilament' in res
    res = eutils.EFetch('gene', 4747, retmode="xml")


def test_epost(eutils):
    ret = eutils.EPost("pubmed", "20210808")
    assert ret['QueryKey']
    assert ret['WebEnv']
    print(ret)


def test_check_db(eutils):
    try:
        eutils._check_db('dummy')
        assert False
    except:
        assert True


def test_check_retmode(eutils):
    try:
        eutils._check_retmode('dummy')
        assert False
    except:
        assert True


def test_check_ids(eutils):
    assert eutils._check_ids(None) == None

    eutils._check_ids(",".join([str(x) for x in range(199)]))
    try:
        eutils._check_ids(",".join([str(x) for x in range(201)]))
        assert False
    except:
        assert True


def test_efetch_xml(eutils):
    xml = eutils.EFetch(db="nuccore",id="AP013055", rettype="docsum",
        retmode="xml")
    res = eutils.parse_xml(xml, "EUtilsParser")
    assert res['eSummaryResult']['DocSum']['Id'] == '578887486'
    assert res['eSummaryResult']['DocSum']['Item'][0] == 'AP013055'





