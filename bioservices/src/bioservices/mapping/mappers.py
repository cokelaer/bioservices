import time
from bioservices import Kegg, UniProt, KeggParser, UniChem, BioDBNet, HGNC
from easydev import Logging
try:
    import pandas as pd
except:
    pass

import  os


class Mapper(Logging):
    """Accepted code:

        uniprot


    m = Mapper()
    # HGNC
    df_hgnc = m.get_all_hgnc_into_df()
    df_hgnc.to_pickle("mapper_hgnc.dat")

    # KEGG
    df_kegg1 = m.get_all_kegg_into_df1()
    df_kegg2 = m.get_all_kegg_into_df2()

    uniq_keggid = 

    """
    kegg_dblinks  = ["IMGT", "Ensembl", "HGNC", "HPRD", "NCBI-GI", "OMIM", "NCBI-GeneID", "UniProt", "Vega"]
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
        self._kegg_service = KeggParser(verbose=False)

        self.logging.info("... HGNC")
        self._hgnc_service = HGNC()

        self.logging.info("... UniChem")
        self._unichem_service = UniChem()

        self.logging.info("...BioDBNet")
        self._biodbnet = BioDBNet()

    def _uniprot2refseq(self, name):
        """

        There are 2 refseq alias: REFSEQ_NT_ID and P_REFSEQ_AC.

        Here, we use the first one to agree with wikipedia
        http://en.wikipedia.org/wiki/Protein_Kinase_B

        """
        return self._uniprot_service.mapping(fr="ACC", to="REFSEQ_NT_ID", query="P31749")

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


class MapperBase(object):
    def __init__(self):
        pass

    def build_dataframe(self):
        raise NotImplementedError

    def to_csv(self, filename):
        self.df.to_csv(filename)

    def read_csv(self, filename):
        self.df = pd.read_csv(filename)


class HGNCMapper(object):
    hgnc_dblink =  ['EC','Ensembl', 'EntrezGene', 'GDB', 'GENATLAS',
            'GeneCards', 'GeneTests', 'GoPubmed', 'H-InvDB', 'HCDM', 'HCOP',
            'HGNC', 'HORDE', 'IMGT_GENE_DB', 'INTERFIL', 'IUPHAR', 'KZNF',
            'MEROPS', 'Nucleotide', 'OMIM', 'PubMed', 'RefSeq', 'Rfam',
            'Treefam', 'UniProt', 'Vega', 'miRNA', 'snoRNABase']
    def __init__(self, filename=None):
        self._hgnc_service = HGNC()
        if filename == None:
            self.alldata = self.load_all_hgnc()
            self.df = self.build_dataframe()
        else:
            self.read_csv(filename)

    def load_all_hgnc(self):
        """keys are unique Gene names"""
        print("Fetching the data from HGNC first. May take a few minutes"),
        alldata = self._hgnc_service.mapping_all()
        print("done")
        return alldata

    def build_dataframe(self):
        # simplify to get a dictionary of dictionary
        data = {k1:{k2:v2['xkey'] for k2,v2 in self.alldata[k1].iteritems()} for k1 in self.alldata.keys()}
        dfdata = pd.DataFrame(data)
        dfdata = dfdata.transpose()
        # rename to tag with "HGNC"
        dfdata.columns = [this + "__HGNC_mapping" for this in dfdata.columns]
        print("a dataframe was built using HGNC data set and saved in attributes  self._df_hgnc")
        return dfdata



class KEGGMapper(object):
    """

    """
    kegg_dblinks  = ["IMGT", "Ensembl", "HGNC", "HPRD", "NCBI-GI", "OMIM", "NCBI-GeneID", "UniProt", "Vega"]
    def __init__(self, verbose=True):
        self._kegg_service = KeggParser(verbose=verbose)

        print("Loading all gene identifiers for HSA")
        names = self._kegg_service.list("hsa")
        names = names.strip().split("\n")
        names = [x.split("\t")[0] for x in names]
        self._names = names[:]

        print("Fetching all data")
        self.alldata = {}
        self.load_all_kegg_entries()

        print("Building the dataframe")
        try:
            self.df = self.build_dataframe()
        except:
            print("error in build_dataframe")

    def _get_names(self):
        return self._names
    names = property(_get_names)

    def _get_entries(self):
        return sorted(self.alldata.keys())
    entries = property(_get_entries)

    def build_dataframe(self):

        names = ['class', 'definition', 'disease', 'drug_target',
                'module', 'motif', 'name', 'orthology', 'pathway', 'position', 'structure']

        N = len(self.entries)
        # build an empty dataframe with relevant names
        data = {}
        # for the dblinks
        for this in self.kegg_dblinks:
            data.update({"%s_kegg" % this: [None] * N})

        # and other interesting entries
        for name in names:
            #e.g. name == position
            data[name] = [self.alldata[entry][name] if name in self.alldata[entry].keys() else None for entry in self.entries]

        df = pd.DataFrame(data, index=self.entries)

        # scan again to fill the df with dblinks
        for index, entry in enumerate(self.entries):
            res = self.alldata[entry]['dblinks']
            for key in res.keys():
                if key in self.kegg_dblinks:
                    # fill df_i,j
                    df.ix[entry][key+"_kegg"] = res[key]
                else:
                    raise NotImplementedError("Found an unknown key in KEGG dblink:%s" % key)
        return df

    def load_all_kegg_entries(self, filename="kegg_gene.dat"):
        if os.path.isfile(filename):
            import pickle
            results = pickle.load(open(filename, "r"))
            return results
        # TODO:
        # donwload from a URL  
        print("could not find kegg data. fetching data from website if possible")
        # Fetches the KEGG results using multicore to send several requests at the same time
        found = self.alldata.keys()
        names = [x for x in self.names if x not in found]
        print("Fetching %s enties" % len(names))


        mc = test_func(names)
        self.mcresults = mc.results.copy()
        # here are the entries to be used as keys
        try:
            entries = ["hsa:"+x['entry'].split()[0] for x in self.mcresults if x]

            for entry, result in zip(entries, self.mcresults):
                self.alldata[entry] = result
        except:
            print("something wrng happened while scaning mcresults")

        #import pickle
        #pickle.dump(results, open("kegg_gene.dat","w"))
        

from bioservices import KeggParser
kegg = KeggParser(verbose=False)

def test_func(names):
    from easydev import MultiProcessing
    t = MultiProcessing(verbose=False, maxcpu=8)
    for name in names:
        t.add_job(keggfunc, name)
    t.run()
    return t

def keggfunc(name):
    global kegg
    try:
        id_ = kegg.get(name)
        res = kegg.parse(id_)
        return res
    except:
        return None






