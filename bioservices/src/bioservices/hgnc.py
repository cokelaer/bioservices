# -*- python -*-
#
#  This file is part of BioServices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://pythonhosted.org/bioservices/
#
##############################################################################
from bioservices import *
from urllib2 import HTTPError


class HGNC(RESTService):
    """

    :references: http://www.avatar.se/HGNC/doc/tutorial.html

    """
    def __init__(self):
        url = "http://www.avatar.se/HGNC/wr/gene/"
        super(RESTService,self).__init__("HGNC", url=url)

    def get_xml(self, gene):
        """
            res = s.fetchXML("ZAP70")
            res.findAll("alias")
            for x in res.findAll("alias"):
                print(x.text)
        """
        try:
            res = self.request("%s.xml" % gene)
        except HTTPError:
            print("!!BioServices HTTPError caught in HGNC. Probably an invalid gene name")
            res = ""
        except Exception:
            
        return res

    def get_aliases(self, gene):
        """Get aliases of a given gene"""
        res = self.request("%s.xml" % gene)
        aliases = [x.text for x in res.findAll("alias")]
        return aliases

    def get_name(self, gene):
        res = self.request("%s.xml" % gene)
        name = [x.text for x in res.findAll("name")][0]

    def get_chromosome(self, gene):
        pass

"""

    <chromosome xlink:href="/HGNC/wr/chromosome/2q" xlink:title="2q">
     2q11-q13
    </chromosome>

    <previous_symbols>
     <previous_symbol>
      SRK
     </previous_symbol>
    </previous_symbols>

    <withdrawn_symbols>
     <withdrawn_symbol hgnc_id="11294">
      SRK
     </withdrawn_symbol>
    </withdrawn_symbols>

    <previous_names>
     <previous_name>
      zeta-chain (TCR) associated protein kinase (70 kD)
     </previous_name>
    </previous_names>

    <xrefs>
     <xref mapped="false" xdb="EntrezGene" xkey="7535">
      <link format="html" mimetype="text/html"
xlink:href="http://view.ncbi.nlm.nih.gov/gene/7535" xlink:title="EntrezGene"/>
      <link format="html" mimetype="text/html"
xlink:href="http://www.ncbi.nlm.nih.gov/mapview/map_search.cgi?direct=on&amp;neighb=off&amp;taxid=9606&amp;query=(7535[id]+AND+gene[obj_type])"
xlink:title="EntrezMapViewer"/>
     </xref>
     <xref mapped="true" xdb="GDB" xkey="433738">
      <link format="html" mimetype="text/html"
xlink:href="http://www.gdb.org/gdb-bin/genera/accno?accessionNum=GDB:433738"
xlink:title="GDB"/>
     </xref>
     <xref mapped="true" xdb="GENATLAS" xkey="ZAP70">
      <link format="html" mimetype="text/html"
xlink:href="http://www.dsi.univ-paris5.fr/genatlas/gensearch.php?type=0&amp;SYMBOL=ZAP70"
xlink:title="GENATLAS"/>
     </xref>
     <xref mapped="true" name="ZAP70" xdb="GeneCards" xkey="12858">
      <link format="html" mimetype="text/html"
xlink:href="http://www.genecards.org/cgi-bin/carddisp.pl?id=12858&amp;id_type=hgnc"
xlink:title="GeneCards"/>
     </xref>
     <xref mapped="true" xdb="GeneTests" xkey="ZAP70">
      <link format="html" mimetype="text/html"
xlink:href="http://www.genetests.org/query?gene=ZAP70" xlink:title="GeneTests"/>
     </xref>
     <xref mapped="true" xdb="GoPubmed" xkey="ZAP70">
      <link format="html" mimetype="text/html"
xlink:href="http://www.gopubmed.org/search?t=hgnc&amp;q=ZAP70"
xlink:title="GoPubmed"/>
     </xref>
     <xref mapped="true" xdb="H-InvDB" xkey="ZAP70">
     </xref>
     <xref mapped="true" xdb="HCOP" xkey="ZAP70">
      <link format="html" mimetype="text/html"
xlink:href="http://www.genenames.org/cgi-bin/hcop.pl?species_pair=Human+and+Any+species&amp;column=symbol&amp;query=ZAP70&amp;Search=Search"
xlink:title="HCOP"/>
     </xref>
     <xref mapped="false" name="ZAP70" xdb="HGNC" xkey="12858">
      <link format="html" mimetype="text/html"
xlink:href="http://www.genenames.org/data/hgnc_data.php?hgnc_id=HGNC:12858"
xlink:title="HGNC"/>
      <link format="html" mimetype="text/html"
xlink:href="http://www.avatar.se/HGNC/wr/gene/12858" xlink:title="HGNC/wr"/>
      <link format="xml" mimetype="text/xml"
xlink:href="http://www.avatar.se/HGNC/wr/gene/12858.xml" xlink:title="HGNC/wr"/>
     </xref>
     <xref mapped="false" xdb="Nucleotide" xkey="L05148">
      <link format="html" mimetype="text/html"
xlink:href="http://www.ebi.ac.uk/cgi-bin/dbfetch?db=embl&amp;id=L05148&amp;format=embl&amp;style=html"
xlink:title="EMBL"/>
      <link format="xml" mimetype="text/xml"
xlink:href="http://www.ebi.ac.uk/cgi-bin/dbfetch?db=embl&amp;id=L05148&amp;format=emblxml&amp;style=raw"
xlink:title="EMBL"/>
      <link format="fasta" mimetype="text/plain"
xlink:href="http://www.ebi.ac.uk/cgi-bin/dbfetch?db=embl&amp;id=L05148&amp;format=fasta&amp;style=raw"
xlink:title="EMBL"/>
      <link format="html" mimetype="text/html"
xlink:href="http://www.ncbi.nlm.nih.gov/entrez/viewer.fcgi?db=nucleotide&amp;id=L05148"
xlink:title="GenBank"/>
      <link format="xml" mimetype="text/xml"
xlink:href="http://www.ncbi.nlm.nih.gov/entrez/viewer.fcgi?db=nucleotide&amp;uids=L05148&amp;dopt=tinyseq&amp;sendto=t"
xlink:title="GenBank"/>
      <link format="insdseq" mimetype="application/xml"
xlink:href="http://www.ncbi.nlm.nih.gov/entrez/viewer.fcgi?db=nucleotide&amp;uids=L05148&amp;dopt=gpc&amp;sendto=t"
xlink:title="GenBank"/>
      <link format="html" mimetype="text/html"
xlink:href="http://genome.ucsc.edu/cgi-bin/hgTracks?Submit=Submit&amp;position=L05148"
xlink:title="UCSCBrowser"/>
      <link format="html" mimetype="text/html"
xlink:href="http://genome.cse.ucsc.edu/cgi-bin/hgGene?org=Human&amp;hgg_gene=L05148&amp;hgg_chrom=none&amp;hgg_type=knownGene"
xlink:title="UCSCIndex"/>
     </xref>
     <xref mapped="false" xdb="PubMed" xkey="1423621">
      <link format="html" mimetype="text/html"
xlink:href="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&amp;db=PubMed&amp;dopt=Abstract&amp;list_uids=1423621"
xlink:title="PubMed"/>
      <link format="xml" mimetype="text/xml"
xlink:href="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?retmode=xml&amp;db=PubMed&amp;id=1423621"
xlink:title="PubMed"/>
     </xref>
     <xref mapped="true" xdb="RefSeq" xkey="NM_001079">
      <link format="html" mimetype="text/html"
xlink:href="http://www.ncbi.nlm.nih.gov/entrez/viewer.fcgi?val=NM_001079"
xlink:title="RefSeq"/>
     </xref>
     <xref mapped="true" xdb="Treefam" xkey="12858">
      <link format="html" mimetype="text/html"
xlink:href="http://www.treefam.org/cgi-bin/TFinfo.pl?xref=12858&amp;dbid=hgnc&amp;spec=9606"
xlink:title="Treefam"/>
     </xref>
     <xref mapped="true" xdb="UniProt" xkey="P43403">
      <link format="html" mimetype="text/html"
xlink:href="http://www.uniprot.org/uniprot/P43403" xlink:title="UniProt"/>
      <link format="xml" mimetype="text/xml"
xlink:href="http://www.uniprot.org/uniprot/P43403.xml" xlink:title="UniProt"/>
      <link format="fasta" mimetype="text/plain"
xlink:href="http://www.uniprot.org/uniprot/P43403.fasta" xlink:title="UniProt"/>
      <link format="txt" mimetype="application/octet-stream"
xlink:href="http://www.uniprot.org/uniprot/P43403.txt" xlink:title="UniProt"/>
      <link format="gff" mimetype="application/octet-stream"
xlink:href="http://www.uniprot.org/uniprot/P43403.gff" xlink:title="UniProt"/>
      <link format="rdf" mimetype="application/rdf+xml"
xlink:href="http://www.uniprot.org/uniprot/P43403.rdf" xlink:title="UniProt"/>
     </xref>
     <xref mapped="true" xdb="Vega" xkey="ZAP70">
      <link format="html" mimetype="text/html"
xlink:href="http://vega.sanger.ac.uk/Homo_sapiens/geneview?gene=ZAP70"
xlink:title="Vega"/>
     </xref>
    </xrefs>
   </gene>
  </hgnc-wr>
"""










    def getOutdatedSymbols(self, gene):
        pass
