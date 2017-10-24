from bioservices import PRIDE
import pytest
import os

pytestmark = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
        reason="On travis")
   


p = PRIDE()


def test_pride_project():
    res = p.get_project("PRD000001")
    assert res["numPeptides"] == 6758

    projects = p.get_project_list(show=100)
    counter = p.get_project_count()
    assert counter > 1000


def test_pride_assay():
    res = p.get_assays(1643)
    assert res['proteinCount'] == 276

    assays = p.get_assay_list('PRD000001')
    count = p.get_assay_count('PRD000001')

    assert count == len(assays)


def test_pride_file():
    files = p.get_file_list("PRD000001")
    count = p.get_file_count("PRD000001")
    assert len(set([x['assayAccession'] for x in files])) == count

    files = p.get_file_list_assay(1643)
    count = p.get_file_count_assay(1643)
    assert len(set([x['assayAccession'] for x in files])) == count


def test_pride_protein():
    files = p.get_protein_list("PRD000001")
    count = p.get_protein_count("PRD000001")
    assert count == 1530
    assert len(files) == 10  # only a subset

    files = p.get_protein_list_assay(1643)
    count = p.get_protein_count_assay(1643)
    # assert len(files) == count
    assert count == 276
    assert len(files) == 10


def test_pride_peptide():
    # without sequence
    count = p.get_peptide_count('PRD000001')
    peptides = p.get_peptide_list('PRD000001', show=count)
    assert len(peptides) == count

    # with sequence
    peptides = p.get_peptide_list('PRD000001', sequence='PLIPIVVEQTGR')
    assert len(peptides) == 4
    count = p.get_peptide_count('PRD000001', sequence='PLIPIVVEQTGR')
    assert count == 4

    # with assay and sequence
    peptides = p.get_peptide_list_assay(1643, sequence='AAATQKKVER')
    assert len(peptides) == 5
    count = p.get_peptide_count_assay(1643, sequence='AAATQKKVER')
    assert count == 5

    # with assay no sequence
    count = p.get_peptide_count_assay(1643)
    assert count == 1696
    peptides = p.get_peptide_list_assay(1643)
    # FIXME this works in a shell but not via nosetests or pytest
    #assert len(peptides) == 10
