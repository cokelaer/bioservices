from bioservices.xmltools import easyXML



xmldata = """
<xml>
  <parameter>
    <value>1</value>
  </parameter>
</xml>
"""


def test_easyXML():
    res = easyXML(xmldata)
    res['parameter']
