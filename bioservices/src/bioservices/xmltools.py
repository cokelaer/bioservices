"""This module will include common tools to manipulate XML files"""
import xml.etree.ElementTree as ET




class easyXML(object):

    def __init__(self, data):
        self.data = data[:]
        self.root = ET.fromstring(data)

    def getchildren(self):
        return self.root.getchildren()


class easyXML_RheaSearch(easyXML):
    """

    Here is an XML  strucutre returned by rhea.search method

    resultset
       rheaReaction
          rheaid
            id
            idprefix
            rheaUri

    ex.root.getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0].text

    """
    def __init__(self, data):
        super(easyXML_Rhea, self).__init__(data)

    def get_reactions_elements(self):
        reactions = self.getchildren()[0].getchildren()
        return reactions

    def get_reactions_ids(self):
        reactions = self.get_reactions_elements()

        ids = []
        for reaction in reactions:
            elements = reaction.getchildren()[0].getchildren()
            for element in elements:
                if element.tag == 'id':
                    ids.append(element.text)
        return ids






    def get_reactions_idprefix(self):
        reactions = self.get_reactions_elements()

        ids = []
        for reaction in reactions:
            elements = reaction.getchildren()[0].getchildren()
            for element in elements:
                if element.tag == 'idprefix':
                    ids.append(element.text)
        return ids

    def get_reactions_rheaUri(self):
        reactions = self.get_reactions_elements()

        rhea_elements = []
        for reaction in reactions:
            elements = reaction.getchildren()[0].getchildren()
            for element in elements:
                if element.tag == 'rheaUri':
                    rhea_elements.append(element)

        rheaUri = []
        for rhea_element in rhea_elements:
            elements = rhea_element.getchildren()
            for element in elements:
                if element.tag == 'uri':
                    rheaUri.append(element.text)
        return rheaUri
