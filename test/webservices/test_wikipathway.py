import os

import pytest
from easydev import TempFile

from bioservices.wikipathway import WikiPathways


@pytest.fixture
def wikipath():
    return WikiPathways(verbose=False)


def test_organism(wikipath):
    assert "Homo sapiens" in wikipath.organisms
    wikipath.organism = "Homo sapiens"
    assert wikipath.organism == "Homo sapiens"

    try:
        wikipath.organism = "Homo sapi"
        assert False
    except ValueError:
        assert True

    assert len(wikipath.organisms) > 2  # check it is not empty


def test_showPathwayInBrowser(wikipath):
    wikipath.showPathwayInBrowser("WP232")


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(30)
def test_listPathways(wikipath):
    l = wikipath.listPathways()
    try:
        # FIXME pandas needed on travis. to do in v2
        assert len(l) > 40
        l = wikipath.listPathways("Homo sapiens")
        assert len(l) > 40
    except:
        pass


def test_getPathway(wikipath):
    wikipath.getPathway("WP232")


def test_getPathwayInfo(wikipath):
    wikipath.getPathwayInfo("WP232")


def test_getPathwayAs(wikipath):
    res = wikipath._getPathwayAs("WP4", filetype="png")


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(30)
def test_findPathwaysByText(wikipath):
    res = wikipath.findPathwaysByText(query="p53")
    res = wikipath.findPathwaysByText(query="p53", species="Homo sapiens")
    assert len(wikipath.findPathwaysByText(query="p53 OR mapk", species="Homo sapiens")) > 0


def test_getOntologyTersmByPathway(wikipath):
    res = wikipath.getOntologyTermsByPathway("WP4")


def _test_getCurationTags(wikipath):
    wikipath.getCurationTags("WP4")


def _test_getcurationTagByNames(wikipath):
    wikipath.getCurationTagsByName("Curation:Tutorial")


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(30)
def test_findInteractions(wikipath):
    assert len(wikipath.findInteractions("P53").species) > 10


@pytest.mark.xfail(reason="too slow", method="thread")
@pytest.mark.timeout(30)
def test_getRecentChanges(wikipath):
    wikipath.getRecentChanges(20120101000000)


# does not seem to work
def test_findPathwayByXref(wikipath):
    df = wikipath.findPathwaysByXref("P45985")
    assert len(df)


def test_findPathwaysByLitterature(wikipath):
    wikipath.findPathwaysByLiterature(18651794)


def test_savePathwayAs(wikipath):
    # Note that not all WP have the PDF format available.
    # WP4 has not (march 2018)
    with TempFile(suffix=".png") as fout:
        wikipath.savePathwayAs("WP232", fout.name, display=False)


def test_getPathwaysByParentOntologyTerm(wikipath):
    wikipath.getPathwaysByParentOntologyTerm("DOID:344")


def test_createPathway(wikipath):
    try:
        wikipath.createPathway("", "")
        assert False
    except NotImplementedError:
        assert True


def test_updatePathwa(wikipath):
    try:
        wikipath.updatePathway("", "", "")
        assert False
    except NotImplementedError:
        assert True


def test_saveCurationTag(wikipath):
    try:
        wikipath.saveCurationTag("", "", "")
        assert False
    except NotImplementedError:
        assert True


def test_login(wikipath):
    try:
        wikipath.login("dummy", "dummy")
        assert False
    except NotImplementedError:
        assert True


def test_remoceCurationTag(wikipath):
    try:
        wikipath.removeCurationTag("dummy", "dummy")
        assert False
    except NotImplementedError:
        assert True


# FIXME SLOW
def _test_getPathwayHistory(wikipath):
    _ = wikipath.getPathwayHistory("WP455", "20100101000000")


def test_coloredPathway(wikipath):
    wikipath.getColoredPathway("WP4", revision=0)
