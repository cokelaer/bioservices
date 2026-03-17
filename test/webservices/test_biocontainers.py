import pandas as pd
import pytest

from bioservices import Biocontainers


@pytest.fixture
def b():
    return Biocontainers(verbose=False)


def test_get_tools(b):
    df = b.get_tools(limit=5)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert "id" in df.columns
    assert "name" in df.columns


def test_get_tools_search(b):
    df = b.get_tools(limit=10, search="samtools")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_get_tool(b):
    tool = b.get_tool("samtools")
    assert isinstance(tool, dict)
    assert tool["id"] == "samtools"
    assert tool["name"] == "samtools"
    assert "versions" in tool
    assert "pulls" in tool


def test_get_tool_versions(b):
    df = b.get_tool_versions("samtools")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "id" in df.columns


def test_get_tool_version(b):
    v = b.get_tool_version("samtools", "samtools-1.17")
    assert isinstance(v, dict)
    assert v["id"] == "samtools-1.17"
    assert v["meta_version"] == "1.17"
    assert "images" in v
    image_types = [img["image_type"] for img in v["images"]]
    assert "Docker" in image_types


def test_get_tool_classes(b):
    classes = b.get_tool_classes()
    assert isinstance(classes, list)
    names = [c["name"] for c in classes]
    assert "CommandLineTool" in names
    assert "Workflow" in names


def test_get_versions_one_tool_alias(b):
    # backward-compatible alias
    df = b.get_versions_one_tool("samtools")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
