"""Unit tests for bioservices.xmltools — no network required."""
from unittest.mock import MagicMock, patch

import pytest

from bioservices.xmltools import XMLObjectify, easyXML, readXML

_VALID_XML = b"<root><child id='1'>alpha</child><child id='2'>beta</child></root>"
_INVALID_XML = b"not valid xml <<< >>>"


# ---------------------------------------------------------------------------
# easyXML — core behaviour
# ---------------------------------------------------------------------------


class TestEasyXML:
    def test_init_valid_xml_parses_root(self):
        import xml.etree.ElementTree as ET

        x = easyXML(_VALID_XML)
        assert isinstance(x.root, ET.Element)

    def test_init_invalid_xml_falls_back_to_data(self):
        x = easyXML(_INVALID_XML)
        assert x.root == _INVALID_XML

    def test_data_is_a_copy(self):
        data = b"<a/>"
        x = easyXML(data)
        assert x.data == data

    def test_getchildren_returns_child_elements(self):
        x = easyXML(_VALID_XML)
        children = x.getchildren()
        assert len(children) == 2

    def test_soup_property_returns_beautifulsoup(self):
        import bs4

        x = easyXML(_VALID_XML)
        assert isinstance(x.soup, bs4.BeautifulSoup)

    def test_soup_is_cached_on_repeated_access(self):
        x = easyXML(_VALID_XML)
        assert x.soup is x.soup

    def test_str_returns_prettified_xml(self):
        x = easyXML(_VALID_XML)
        s = str(x)
        assert "root" in s
        assert "child" in s

    def test_getitem_delegates_to_findall(self):
        x = easyXML(_VALID_XML)
        results = x["child"]
        assert len(results) == 2

    def test_findall_alias_is_callable(self):
        x = easyXML(_VALID_XML)
        assert callable(x.findAll)
        assert x.findAll("child") == x["child"]

    def test_prettify_alias_is_callable(self):
        x = easyXML(_VALID_XML)
        assert callable(x.prettify)


# ---------------------------------------------------------------------------
# easyXML — parametrize over various XML structures
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "xml_bytes,tag,expected_count",
    [
        (b"<root><item/><item/><item/></root>", "item", 3),
        (b"<root><a/></root>", "a", 1),
        (b"<root/>", "missing", 0),
    ],
)
def test_easyxml_getitem_count(xml_bytes, tag, expected_count):
    x = easyXML(xml_bytes)
    assert len(x[tag]) == expected_count


# ---------------------------------------------------------------------------
# readXML — mocked URL fetch
# ---------------------------------------------------------------------------


class TestReadXML:
    def test_reads_data_from_url(self):
        xml_bytes = b"<root><item>42</item></root>"
        mock_response = MagicMock()
        mock_response.read.return_value = xml_bytes

        with patch("bioservices.xmltools.urlopen", return_value=mock_response):
            x = readXML("http://example.com/fake.xml")

        assert x.data == xml_bytes

    def test_parsed_content_accessible_via_getitem(self):
        xml_bytes = b"<root><item>42</item></root>"
        mock_response = MagicMock()
        mock_response.read.return_value = xml_bytes

        with patch("bioservices.xmltools.urlopen", return_value=mock_response):
            x = readXML("http://example.com/fake.xml")

        assert len(x["item"]) == 1

    def test_inherits_easyxml_getchildren(self):
        xml_bytes = b"<root><a/><b/></root>"
        mock_response = MagicMock()
        mock_response.read.return_value = xml_bytes

        with patch("bioservices.xmltools.urlopen", return_value=mock_response):
            x = readXML("http://example.com/fake.xml")

        assert len(x.getchildren()) == 2


# ---------------------------------------------------------------------------
# XMLObjectify
# ---------------------------------------------------------------------------


class TestXMLObjectify:
    def test_init_from_easyxml_instance(self):
        x = easyXML(_VALID_XML)
        obj = XMLObjectify(x)
        assert obj.root is not None

    def test_init_from_raw_bytes(self):
        obj = XMLObjectify(_VALID_XML)
        assert obj.root is not None

    def test_str_lists_child_tags(self):
        x = easyXML(_VALID_XML)
        obj = XMLObjectify(x)
        s = str(obj)
        assert "child" in s

    def test_obj_attribute_preserved(self):
        x = easyXML(_VALID_XML)
        obj = XMLObjectify(x)
        assert obj.obj is x
