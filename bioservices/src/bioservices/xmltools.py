"""This module will include common tools to manipulate XML files"""
import xml.etree.ElementTree as ET
import BeautifulSoup


class easyXML(object):
    """class to ease the introspection of XML document.


        >>> import nciblast
        >>> n = nciblast.NCIBlast()
        >>> res = n.parameters() # res is an instance of easyXML
	# You can retreive XML from this instance of easyXML and print the content
        # in a more human-readable way.
        >>> print res
        >>> res.soup.findAll('id') # a Beautifulsoup instance is available
        >>> res.root # and the root using xml.etree.ElementTree

    """
    def __init__(self, data):
        """Constructor

        :param data: a document in XML format

        """
        self.data = data[:]
        self.root = ET.fromstring(data)
        self._soup = None
        self.prettify = self.soup.prettify
        self.findAll = self.soup.findAll

    def getchildren(self):
        """returns all children of the root XML document"""
        return self.root.getchildren()

    def _get_soup(self):
        if self._soup == None:
            self._soup = BeautifulSoup.BeautifulSoup(self.data)
        return self._soup
    soup = property(_get_soup)

    def __str__(self):
        txt = self.soup.prettify()
        return txt


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
