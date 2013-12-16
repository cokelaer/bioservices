from bioservices import *
from easydev import Logging
try:
    import pandas as pd
except:
    pass




class Mapper(Logging):
    """Accepted code:

        uniprot

    """
    kegg_dblinks  = ["Ensembl", "HGNC", "HPRD", "NCBI-GI", "OMIM", "NCBI-GeneID", "UniProt", "Vega"]
    hgnc_dblink =  ['EC','Ensembl', 'EntrezGene', 'GDB', 'GENATLAS',
            'GeneCards', 'GeneTests', 'GoPubmed', 'H-InvDB', 'HCDM', 'HCOP',
            'HGNC', 'HORDE', 'IMGT_GENE_DB', 'INTERFIL', 'IUPHAR', 'KZNF',
            'MEROPS', 'Nucleotide', 'OMIM', 'PubMed', 'RefSeq', 'Rfam',
            'Treefam', 'UniProt', 'Vega', 'miRNA', 'snoRNABase']


    def __init__(self, verbosity="INFO"):
        super(Mapper, self).__init__(level=verbosity)
        self.logging.info("Initialising the services")
        self.logging.info("... uniprots")
        self._uniprot_service = UniProt()
        self.logging.info("... KEGG")
        self._kegg_service = KeggParser()
        self.logging.info("... HGNC")
        self._hgnc_service = HGNC()
        self.logging.info("... UniChem")
        self._unichem_service = UniChem()
        self.logging.debug




    def _uniprot2refseq(self, name):
        """

        There are 2 refseq alias: REFSEQ_NT_ID and P_REFSEQ_AC.

        Here, we use the first one to agree with wikipedia
        http://en.wikipedia.org/wiki/Protein_Kinase_B

        """
        return self._uniprot_service.mapping(fr="ACC", to="REFSEQ_NT_ID", query="P31749")

    def get_all_hgnc_into_df(self):
        """keys are unique Gene names"""
        print("Fetching the data from HGNC first. May take a few minutes")
        data = self._hgnc_service.mapping_all()
        # simplify to get a dictionary of dictionary
        data = {k1:{k2:v2['xkey'] for k2,v2 in data[k1].iteritems()} for k1 in data.keys()}
        dfdata = pd.DataFrame(data)
        dfdata = dfdata.transpose()
        # rename to tag with "HGNC"
        dfdata.columns = [this + "__HGNC_mapping" for this id dfdata.columns]
        self._df_hgnc = dfdata.copy()
        print("a dataframe was built using HGNC data set and saved in attributes  self._df_hgnc")
        return self._df_hgnc

    def get_all_kegg_into_df(self):
        print("Fetching mapping uniprot/kegg using KEGG service")
        mk2u = self._kegg_service.conv("hsa", "uniprot")
        mu2k = self._kegg_service.conv("uniprot", "hsa")


        keys, values = mk2u_kegg.keys, mk2u_kegg.values()

        import time
        t2 = time.time()
        keys, values = mk2u_kegg.keys, mk2u_kegg.values()
        N = len(mk2u_kegg.keys())

        # the common columns
        data = {
                "uniprot__KEGG_conv":mk2u_kegg.keys(), 
                "KEGG___KEGG_conv":mk2u_kegg.values()}

        # columns that will be filled via KEGG
        for this in self.kegg_dblinks:
            data.update({"%s_kegg" % this: [None] * N})

        df = pd.DataFrame(data,
                index=[x[3:] for x in mk2u_kegg.keys()])
        self._df_kegg = df.copy()

    def _update_uniprot_xref(self, df, 
            xref=["HGNC_ID", "ENSEMBLE_ID",  "P_ENTREZGENEID"]):
        """Update the dataframe using Uniprot to map indices onto cross
        reference databases


        """
        for ref in xref:
            print("Processing %s " % ref)
            res = self._uniprot_service.multi_mapping("ACC", ref,
                    list(df.index), timeout=10, ntrials=5)
            if "%s__uniprot_mapping" % ref not in df.columns:
                thisdf = pd.DataFrame({"%s__uniprot_mapping": res.values()},
                        index=res.keys())
                df = df.join(thisdf)
            else:
                for index in df.index:
                    if index in res.keys():
                        df.ix[index]["%s__uniprot_mapping" % ref] = res[index]



    def _update_dblinks_kegg(self, df, N=None):
        # Get more infor from KEGG using the dblinks only.
        keggids = df.KEGG_kegg
        if N == None:
            N = len(keggids)

        buffer_ = {}

        count = 0
        for index,keggid in zip(df.index, df.KEGG_kegg):
            count+=1
            print(count,index, keggid)
            #check if it does not exist already
            if keggid in buffer_.keys():
                res = buffer_[keggid]
                print("-------------------------used buffer")
            else:
                res = self._kegg_service.parse(self._kegg_service.get(keggid))['dblinks']
            for key in res.keys():
                if key in self.kegg_dblinks:
                    # fill df_i,j
                    df.ix[index][key+"_kegg"] = res[key]
                else:
                    raise NotImplementedError("Found an unknown key in KEGG dblink:%s" % key)
            if count > N:
                break
        return df



    def save(self, filename):
        pass

    def load(self, filename):
        pass


    def get_data_from_biodbnet(self, df_hgnc):
        """keys are unique Gene names
        
        
        
        input is made of the df based on HGNC data web services


        uniprot accession are duplicated sometimes. If som this is actually the
        iprimary accession entry and all secondary ones.


        e.g. ,
        
        ABHD11 >>>> Q8N723;Q8NFV2;Q8NFV3;Q6PJU0;Q8NFV4;H7BYM8;Q8N722;Q9HBS8 ABHDB_HUMAN Alpha/beta hydrolase domain-containing protein 11
        correspond actually to the primary one : Q8NFV4

        """
        b = biodbnet.BioDBNet()
        res2 = b.db2db("Gene Symbol", ["HGNC ID", "UniProt Accession", "UniProt Entry Name", "UniProt Protein Name", "KEGG Gene ID", "Ensembl Gene ID"], 
                res.keys()[0:2000])

        
        import pandas as pd
        import StringIO
        c = pd.read_csv(StringIO.StringIO(res2), delimiter="\t", index_col="Gene Symbol")
        return c
