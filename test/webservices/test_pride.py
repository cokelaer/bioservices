import os

import pytest

from bioservices import PRIDE

p = PRIDE()


def test_pride_project():
    res = p.get_project("PRD000001")
    assert res["title"] == "COFRADIC proteome of unstimulated human blood platelets"

    assert p.get_project("dummy") == {}


def test_get_projects():
    res = p.get_projects(max_pages=2)
    assert len(res)


def test_get_project_files():
    res = p.get_project_files("PRD000001", pageSize=100)
    assert res["page"]["size"] == 100


def _test_pride_protein():
    res = p.get_protein_evidences()
    assert "_embedded" in res
    assert "proteinevidences" in res["_embedded"]

    p.get_protein_evidences(project_accession="PXD019473")


def test_stats():
    assert "SUBMISSIONS_PER_YEAR" in p.get_stats()
    p.get_stats("SUBMISSIONS_PER_YEAR")


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(30)
def test_peptide():
    res = p.get_peptide_evidence("PXD016700")
    assert res["_embedded"]

    res = p.get_peptide_evidence(protein_accession="Q8IX30")
    assert res["_embedded"]
