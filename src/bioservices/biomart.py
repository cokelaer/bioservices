#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id$
"""This module provides a class :class:`~BioModels` that allows an easy access
to all the BioModel service.


.. topic:: What is BioMart ?

    :URL: http://www.biomart.org/
    :REST: http://www.biomart.org/martservice.html

    .. highlights::

        The BioMart project provides free software and data services to the
        international scientific community in order to foster scientific collaboration
        and facilitate the scientific discovery process. The project adheres to the open
        source philosophy that promotes collaboration and code reuse.

        -- from BioMart March 2013

.. note:: SOAP and REST are available. We use REST for the wrapping.
"""
from bioservices import REST, BioServicesError

__all__ = ["BioMart"]


class BioMart(REST):
    r"""Interface to the `BioMart <http://www.biomart.org>`_ service

    BioMart is made of different views. Each view correspond to a specific **MART**.
    For instance the UniProt service has a `BioMart view <http://www.ebi.ac.uk/uniprot/biomart/martview/>`_.

    The registry can help to find the different services available through
    BioMart.

        >>> from bioservices import *
        >>> s = BioMart()
        >>> ret = s.registry() # to get information about existing services

    The registry is a list of dictionaries. Some aliases are available to get
    all the names or databases::

        >>> s.names      # alias to list of valid service names from registry
        >>> "unimart" in s.names
        True

    Once you selected a view, you will want to select a database associated with
    this view and then a dataset. The datasets can be retrieved as follows::

        >>> s.datasets("prod-intermart_1")  # retrieve datasets available for this mart

    The main issue is how to figure out the database name (here **prod-intermart_1**) ?
    Indeed, from the web site, what you see is the **displayName** and you must
    introspect the registry to get this information. In **BioServices**, we provide
    the :meth:`~bioservices.biomart.BioMart.lookfor` method to help you. For instance, to
    retrieve the database name of **interpro**, type::

        >>> s = BioMart(verbose=False)
        >>> s.lookfor("interpro")
        Candidate:
             database: intermart_1
            MART name: prod-intermart_1
          displayName: INTERPRO (EBI UK)
                hosts: www.ebi.ac.uk

    The display name (INTERPRO) correspond to the MART name
    prod-intermart_1. Let us you it to retrieve the datasets::

        >>> s.datasets("prod-intermart_1")
        ['protein', 'entry', 'uniparc']

    Now that we have the dataset names, we can select one and build a
    query. Queries are XML that contains the dataset name, some
    attributes and filters. The dataset name is one of the element
    returned by the datasets method. Let us suppose that we want to query
    **protein**, we need to add this dataset to the query::

        >>> s.add_dataset_to_xml("protein")

    Then, you can add attributes (one of the keys of the dictionary
    returned by attributes("protein")::

        >>> s.add_attribute_to_xml("protein_accession")

    Optional filters can be used::

        >>> s.add_filter_to_xml("protein_length_greater_than", 1000)

    Finally, you can retrieve the XML query::

        >>> xml_query = s.get_xml()

    and send the request to biomart::

        >>> res = s.query(xml_query)
        >>> len(res)
        12801
        # print the first 10 accession numbers
        >>> res = res.split("\n")
        >>> for x in res[0:10]: print(x)
        ['P18656',
         'Q81998',
         'O09585',
         'O77624',
         'Q9R3A1',
         'E7QZH5',
         'O46454',
         'Q9T3F4',
         'Q9TCA3',
         'P72759']


    REACTOME example::

        s.lookfor("reactome")
        s.datasets("REACTOME")
        ['interaction', 'complex', 'reaction', 'pathway']

        s.new_query()
        s.add_dataset_to_xml("pathway")
        s.add_filter_to_xml("species_selection", "Homo sapiens")
        s.add_attribute_to_xml("pathway_db_id")
        s.add_attribute_to_xml("_displayname")
        xmlq = s.biomartQuery.get_xml()
        res = s.query(xmlq)


    .. note:: the biomart sevice is slow (in my experience, 2013-2014) so please be patient...

    """
    _xml_example = """<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE Query>
                    <Query virtualSchemaName="default" formatter="CSV" header="0" uniqueRows="0" count="" datasetConfigVersion="0.6">
                    <Dataset name="mmusculus_gene_ensembl" interface="default">
                    <Filter name="ensembl_gene_id" value="ENSMUSG00000086981"/>
                    <Attribute name="ensembl_gene_id"/>
                    <Attribute name="ensembl_transcript_id"/>
                    <Attribute name="transcript_start"/>
                    <Attribute name="transcript_end"/>
                    <Attribute name="exon_chrom_start"/>
                    <Attribute name="exon_chrom_end"/>
                    </Dataset>
                    </Query>"""


    def __init__(self, verbose=False, host=None, cache=False):
        """.. rubric:: Constructor


        By default, the URL used for the biomart service is::

            http://www.biomart.org/biomart/martservice

        Sometimes, the server is down, in which case you may want to use another
        one (e.g., www.ensembl.org). To do so, use the **host** parameter.

        :param str host: a valid host (e.g. "www.ensembl.org")


        """
        if host is None:
            host = "www.biomart.org"
        url = "http://%s/biomart/martservice" % host

        super(BioMart, self).__init__("BioMart", url=url, verbose=verbose,
            cache=cache)
        self._names = None
        self._databases = None
        self._display_names = None
        self._valid_attributes = None
        self._hosts = None

        self._init()   # can be commented if we do not want to check the validity of attributes

    def _init(self):
        temp = self.debugLevel
        self.debugLevel = "ERROR"
        _ = self.lookfor("uniprot", verbose=False)
        _ = self.valid_attributes
        self.debugLevel = temp
        self._biomartQuery = BioMartQuery()

    def registry(self):
        """to retrieve registry information

         the XML contains list of children called MartURLLocation made
         of attributes. We parse the xml to return a list of dictionary.
         each dictionary correspond to one MART.

        aliases to some keys are provided: names, databases, displayNames

        """
        ret = self.http_get("?type=registry", frmt="xml")
        ret = self.easyXML(ret)
        # the XML contains list of children called MartURLLocation made
        # of attributes. We parse the xml to return a list of dictionary.
        # each dictionary correspond to one MART.
        ret = [x.attrib for x in ret.getchildren()]
        return ret

    def datasets(self, mart, raw=False):
        """to retrieve datasets available for a mart:

        :param str mart: e.g. ensembl. see :attr:`names` for a list of valid MART names
            the mart is the database. see lookfor method or databases attributes

        >>> s = BioMart(verbose=False)
        >>> s.datasets("prod-intermart_1")
        ['protein', 'entry', 'uniparc']


        """
        if mart not in self.names:
            raise BioServicesError("Provided mart name (%s) is not valid. see 'names' attribute" % mart)
        ret = self.http_get("?type=datasets&mart=%s" %mart, frmt="txt")

        if raw is False:
            try:
                ret2 = [x.split("\t") for x in ret.split("\n") if len(x.strip())]
                ret = [x[1] for x in ret2]
            except:
                ret = ["?"]

        return ret

    def attributes(self, dataset):
        """to retrieve attributes available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        #assert dataset in self.names
        if dataset not in [x for k in self.valid_attributes.keys() for x in self.valid_attributes[k]]:
            raise ValueError("provided dataset (%s) is not found. see valid_attributes" % dataset)
        ret = self.http_get("?type=attributes&dataset=%s" %dataset, frmt='txt')

        ret = [x for x in ret.split("\n") if len(x)]
        results = {}
        for line in ret:
            key = line.split("\t")[0]
            results[key] = line.split("\t")[1:]
        return results

    def filters(self, dataset):
        r"""to retrieve filters available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        ::

            >>> s.filters("uniprot").split("\n")[1].split("\t")
            >>> s.filters("pathway")["species_selection"]
            [Arabidopsis thaliana,Bos taurus,Caenorhabditis elegans,Canis familiaris,Danio
            rerio,Dictyostelium discoideum,Drosophila melanogaster,Escherichia coli,Gallus
            gallus,Homo sapiens,Mus musculus,Mycobacterium tuberculosis,Oryza
            sativa,Plasmodium falciparum,Rattus norvegicus,Saccharomyces
            cerevisiae,Schizosaccharomyces pombe,Staphylococcus aureus N315,Sus
            scrofa,Taeniopygia guttata ,Xenopus tropicalis]

        """
        if dataset not in [x for k in self.valid_attributes.keys() for x in self.valid_attributes[k]]:
            raise ValueError("provided dataset (%s) is not found. see valid_attributes" % dataset)
        ret = self.http_get("?type=filters&dataset=%s" %dataset, frmt=None)
        ret = [x for x in ret.split("\n") if len(x)]
        results = {}
        for line in ret:
            key = line.split("\t")[0]
            results[key] = line.split("\t")[1:]
        return results

    def configuration(self, dataset):
        """to retrieve configuration available for a dataset:

        :param str dataset: e.g. oanatinus_gene_ensembl

        """
        ret = self.http_get("?type=configuration&dataset=%s" %dataset, frmt="xml")
        ret = self.easyXML(ret)
        return ret

    def version(self, mart):
        """Returns version of a **mart**

        :param str mart: e.g. ensembl

        """
        ret = self.http_get("?type=version&mart=%s" % mart, frmt="xml")
        ret = self.easyXML(ret)
        return ret.root.strip()

    def new_query(self):
        self._biomartQuery.reset()

    def query(self, xmlq):
        """Send a query to biomart

        The query must be formatted in a XML format which looks like (
        example from https://gist.github.com/keithshep/7776579)::

            <?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE Query>
                    <Query virtualSchemaName="default" formatter="CSV" header="0" uniqueRows="0" count="" datasetConfigVersion="0.6">
                    <Dataset name="mmusculus_gene_ensembl" interface="default">
                    <Filter name="ensembl_gene_id" value="ENSMUSG00000086981"/>
                    <Attribute name="ensembl_gene_id"/>
                    <Attribute name="ensembl_transcript_id"/>
                    <Attribute name="transcript_start"/>
                    <Attribute name="transcript_end"/>
                    <Attribute name="exon_chrom_start"/>
                    <Attribute name="exon_chrom_end"/>
                    </Dataset>
                    </Query>
    
        .. warning:: the input XML must be valid. THere is no validation made
            in thiss method.
        """
        ret = self.http_post(None, frmt=None, 
                data={'query':xmlq.strip()}, headers={})
        return ret

    def add_attribute_to_xml(self, name, dataset=None):
        attr = self.create_attribute(name, dataset)
        self._biomartQuery.add_attribute(attr)

    def add_filter_to_xml(self, name, value, dataset=None):
        filt = self.create_filter(name, value, dataset)
        self._biomartQuery.add_filter(filt)

    def add_dataset_to_xml(self, dataset):
        self.attributes(dataset)
        #    raise BioServicesError("invalid dataset names provided. Check names attribute")
        self._biomartQuery.add_dataset(dataset)

    def get_xml(self):
        return self._biomartQuery.get_xml()

    def create_filter(self, name, value, dataset=None):
        if dataset:
            valid_filters = self.filters(dataset).keys()
            if name not in valid_filters:
                raise BioServicesError("Invalid filter name. ")

        _filter = """        <Filter name = "%s" value = "%s"/>""" % (name, value)
        return _filter

    def create_attribute(self, name, dataset=None):
        #s.attributes(dataset)
        # valid dataset
        if dataset:
            valid_attributes = self.attributes(dataset).keys()
            if name not in valid_attributes:
                raise BioServicesError("Invalid attribute name. ")
        attrib = """        <Attribute name = "%s" />""" % name
        return attrib

    def _get_names(self):
        if self._names is None:
            ret = self.registry()
            names = [x["name"] for x in ret]
            self._names = names[:]
        return self._names
    names = property(_get_names, doc="list of valid datasets")

    def _get_displayNames(self):
        if self._display_names is None:
            ret = self.registry()
            names = [x["displayName"] for x in ret]
            self._display_names = names[:]
        return self._display_names
    displayNames = property(_get_displayNames, doc="list of valid datasets")

    def _get_databases(self):
        if self._databases is None:
            ret = self.registry()
            names = sorted([x.get("database", "?") for x in ret])
            self._databases = names[:]
        return self._databases
    databases = property(_get_databases, doc="list of valid datasets")

    def _get_hosts(self):
        if self._hosts is None:
            ret = self.registry()
            names = [x.get("host", "?") for x in ret]
            self._hosts = names[:]
        return self._hosts
    hosts = property(_get_hosts, doc="list of valid hosts")


    def _get_valid_attributes(self,):
        res = {}
        if self._valid_attributes is None:
            # we could use a loop and call self.datasets(name, raw=False) but it
            # can be a bit longish, so we use the asynchronous call using
            # requests
            saveme = self.settings.params['general.async_threshold']
            # TODO: not python3 compatible for now. Waiting for gevent package
            # to be available.
            self.settings.params['general.async_threshold'][0] = 10000 # 

            queries = ["?type=datasets&mart=%s" % name for name in
                    self.names]
            results = self.http_get(queries, frmt="txt")

            self.settings.params['general.async_threshold'] = saveme
            #requests.start()
            #requests.wait()
            #results = requests.get_results()

            for i, name in enumerate(self.names):
                try:
                    res[name] = [x.split("\t")[1] for x in results[i].split("\n") if len(x.strip())>1]
                except:
                    res[name] = "?"
            self._valid_attributes = res.copy()
        return self._valid_attributes
    valid_attributes = property(_get_valid_attributes, doc="list of valid datasets")

    def lookfor(self, pattern, verbose=True):
        for a,x,y,z in zip(self.hosts, self.databases, self.names, self.displayNames):
            found = False
            if pattern.lower() in x.lower():
                found = True
            if pattern.lower() in y.lower():
                found = True
            if pattern.lower() in z.lower():
                found = True
            if found is True and verbose is True:
                print("Candidate:")
                print("     database: %s " %x)
                print("    MART name: %s " %y)
                print("  displayName: %s " %z)
                print("        hosts: %s " %a)


class BioMartQuery(object):
    def __init__(self, version="1.0", virtualScheme="default"):

        params = {
            "version": version,
            "virtualSchemaName": virtualScheme,
            "formatter": "TSV",
            "header":0,
            "uniqueRows":0,
            "configVersion":"0.6"

        }

        self.header = """<?xml version="%(version)s" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "%(virtualSchemaName)s" formatter = "%(formatter)s"
header = "%(header)s" uniqueRows = "%(uniqueRows)s" count = ""
datasetConfigVersion = "%(configVersion)s" >\n""" % params


        self.footer = "    </Dataset>\n</Query>"
        self.reset()

    def add_filter(self, filter):
        self.filters.append(filter)

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def add_dataset(self, dataset):
        self.dataset = """    <Dataset name = "%s" interface = "default" >""" % dataset

    def reset(self):
        self.attributes = []
        self.filters = []
        self.dataset = None

    def get_xml(self):
        if self.dataset is None:
            raise BioServicesError("data set must be set. Use add_dataset method")
        xml = self.header
        xml += self.dataset + "\n\n"
        for line in self.filters:
            xml += line +"\n"
        for line in self.attributes:
            xml += line + "\n"
        xml += self.footer
        return xml


