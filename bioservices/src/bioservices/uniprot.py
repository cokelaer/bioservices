"""Interface to some part of the UniProt web service

.. topic:: What is UniProt ?

    :URL: http://www.uniprot.org
    :Citation:

    .. highlights::

    "The Universal Protein Resource (UniProt) is a comprehensive resource for protein
    sequence and annotation data. The UniProt databases are the UniProt
    Knowledgebase (UniProtKB), the UniProt Reference Clusters (UniRef), and the
    UniProt Archive (UniParc). The UniProt Metagenomic and Environmental Sequences
    (UniMES) database is a repository specifically developed for metagenomic and
    environmental data."


    -- From Uniprot web site (help/about) , Dec 2012


.. mappiung betwenn uniprot and bench of other DBs.
.. ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/


"""
# Import SOAPpy WSDL package.
#from SOAPpy import WSDL
from services import Service
import urllib2



# this is not Uniprot but WSDBfetch


class UniProt(Service):
    """Interface to the `UniProt <http://www.uniprot.org>`_ service

    .. warning:: this class does not cover all UniProt services but a subset
        (identifier mapping service for now).

    Use the identifier mapping interface::

        >>> u = Uniprot(verbose=False)
        >>> u.mapping(fr="ACC", to="KEGG_ID", query='P43403')
        ['FromACC', 'ToKEGG_ID', 'P43403', 'hsa:7535']


    """
    def __init__(self, name="UniProt",
            url='http://www.uniprot.org/',
            verbose=True, debug=False):
        super(UniProt, self).__init__(name=name, url=url, verbose=verbose)

    def mapping(self, fr="ID", to="KEGG_ID", format="tab", query="P13368"):
        """This is an interface to the UniProt mapping service


        ::

            res = u.mapping(fro="ACC", to="KEGG_ID", query='P43403')
            ['From:ACC', 'To:KEGG_ID', 'P43403', 'hsa:7535']


        There is a web page that gives the list of correct `database identifiers
        <http://www.uniprot.org/faq/28>`_

        :URL: http://www.uniprot.org/mapping/

        """
        import urllib
        url = self.url + '/mapping/'
        params = {'from':fr, 'to':to, 'format':format, 'query':query}
        data = urllib.urlencode(params)
        if self.verbose: print data
        request = urllib2.Request(url, data)
        # 2 following lines are optional
        #contact = ""
        #request.add_header('User-Agent', 'Python contact')
        response = urllib2.urlopen(request)
        result = response.read(200000)

        # let us improvve the output a little bit using a list  instead of a
        # string
        try:
            result = result.split()
            result[0]+=':'+fr
            result[1]+=':'+to
        except:
            pass

        return result
