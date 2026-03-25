import pytest

from bioservices import NCBIBlastAPI


@pytest.fixture
def ncbi():
    return NCBIBlastAPI()


# ------------------------------------------------------------------
# Unit-level tests (no network)
# ------------------------------------------------------------------


def test_parse_submission_ok():
    html = """
    <pre>
    QBlastInfoBegin
        RID = ABCD1234EF
        RTOE = 22
    QBlastInfoEnd
    </pre>
    """
    rid, rtoe = NCBIBlastAPI._parse_submission(html)
    assert rid == "ABCD1234EF"
    assert rtoe == 22


def test_parse_submission_missing_rid():
    with pytest.raises(RuntimeError, match="Could not extract RID"):
        NCBIBlastAPI._parse_submission("<html>no rid here</html>")


def test_parse_status_waiting():
    html = "    Status=WAITING\n"
    assert NCBIBlastAPI._parse_status(html) == "WAITING"


def test_parse_status_ready():
    html = "    Status=READY\n    ThereAreHits=yes\n"
    assert NCBIBlastAPI._parse_status(html) == "READY"


def test_parse_status_unknown():
    assert NCBIBlastAPI._parse_status("<html>nothing here</html>") == "UNKNOWN"


def test_invalid_program(ncbi):
    with pytest.raises(ValueError, match="Invalid program"):
        ncbi.run(
            program="badblast",
            database="nt",
            sequence="ATGC",
            email="test@example.org",
        )


# ------------------------------------------------------------------
# Network tests — marked xfail / slow
# ------------------------------------------------------------------


@pytest.mark.xfail(reason="requires network and NCBI availability")
@pytest.mark.timeout(120)
def test_run_and_retrieve(ncbi):
    rid, rtoe = ncbi.run(
        program="blastn",
        database="nt",
        sequence=NCBIBlastAPI._nucleotide_example,
        email="test@example.org",
        hitlist_size=5,
    )
    assert rid
    assert isinstance(rtoe, int)

    status = ncbi.wait(rid, rtoe)
    assert status == "READY"

    xml = ncbi.get_result(rid, format_type="XML")
    assert "BlastOutput" in xml or "BlastXML" in xml


@pytest.mark.xfail(reason="requires network and NCBI availability")
@pytest.mark.timeout(30)
def test_get_result_before_ready_raises(ncbi):
    # Submit a job but do not wait — status should be WAITING immediately
    rid, _ = ncbi.run(
        program="blastn",
        database="nt",
        sequence=NCBIBlastAPI._nucleotide_example,
        email="test@example.org",
    )
    # If NCBI hasn't finished yet, get_result should raise
    if ncbi.get_status(rid) == "WAITING":
        with pytest.raises(RuntimeError, match="still running"):
            ncbi.get_result(rid)
