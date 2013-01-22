"""This module provides a class :class:`Chembl` 

.. topic:: What is ChEMBL 

    :URL:  https://www.ebi.ac.uk/chembldb/index.php/

    .. highlights::

        "Using the ChEMBL web service API users can retrieve data from the ChEMBL
        database in a programmatic fashion. The following list defines the currently
        supported functionality and defines the expected inputs and outputs of each
        method."

       -- From ChEMBL web page Dec 2012




"""
from services import RESTService
import urllib2, json, re, os, webbrowser


class Chembl(RESTService):
    """Interface to `<http://www.ebi.ac.uk/chembldb/index.php>`_ 

    """
    _url = "http://www.ebi.ac.uk/chemblws/"
    def __init__(self, verbose=True):
        super(Chembl, self).__init__(url=Chembl._url, 
            name="Chembl", verbose=verbose)


    # wrapper for functions
    def __f1(func):
        def f2(self,k):
            def f3(k):
                url = func()
                k = url%k
                target_data = urllib2.urlopen(k).read()
                target_data = json.loads(target_data)
                return target_data
            if isinstance(k,str):
                return f3(k)
            elif isinstance(k,list) or isinstance(k,tuple):
                return map(f3,k)
        f2.__doc__ = func.__doc__
        return f2

    
    def api_status(self):
        """ Check API status

        :return: Response is the string 'UP' if services are running
        """
        "http://www.ebi.ac.uk/chemblws/status/"
        #target_data = urllib2.urlopen(url).read()
        res = self.request("status/", format="txt")
        return res


    def get_compound_by_ChemblId(url='http://www.ebi.ac.uk/chemblws/compounds/%s.json'):
        """
        Description: Get compound by ChEMBLID
        Input: Compound ChEMBLID
        Output: Compound Record
        Example URL (XML Output):
            http://www.ebi.ac.uk/chemblws/compounds/CHEMBL1
        Example URL (JSON Output):
            http://www.ebi.ac.uk/chemblws/compounds/CHEMBL1.json
        OUT:
           A dictionary is returned. The dictionary has a unique key 'compound'.
           The value of that key is another dictionary keyed by
                smiles
                chemblId
                medChemFriendly
                molecularWeight
                molecularFormula
                acdLogp
                stdInChiKey
                knownDrug
                passesRuleOfThree
                rotatableBonds
                alogp
                numRo5Violations
                acdLogd

        """
        return url    
    get_compound_by_ChemblId = __f1(get_compound_by_ChemblId)
        

    def get_individual_compund_by_InChiKey(url = 'http://www.ebi.ac.uk/chemblws/compounds/stdinchikey/%s.json'):
        """
        Description: Get individual compound by standard InChi Key
        Input: Standard InChi Key
        Output: Compound Record
        Example URL (XML Output):
            http://www.ebi.ac.uk/chemblws/compounds/stdinchikey/QFFGVLORLPOAEC-SNVBAGLBSA-N
        Example URL (JSON Output):
            http://www.ebi.ac.uk/chemblws/compounds/stdinchikey/QFFGVLORLPOAEC-SNVBAGLBSA-N.json
        """
        return url
    get_individual_compund_by_InChiKey = __f1(get_individual_compund_by_InChiKey)


    def get_compounds_by_SMILES(url='http://www.ebi.ac.uk/chemblws/compounds/smiles/%s.json'):
        """
        Description: Get list of compounds by Canonical SMILES
        Input: SMILES string
        Output: List of Compound Records
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/smiles/COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/smiles/COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56.json
        """
        return url
    get_compounds_by_SMILES = __f1(get_compounds_by_SMILES)


    def get_compounds_by_SMILES_and_http_post(url='http://www.ebi.ac.uk/chemblws/compounds/smiles'):
        """
        Description: Get list of compounds by Canonical SMILES by HTTP POST
        Input: SMILES string
        Output: List of Compound Records
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/smiles
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/smiles.json
        POST parameter: smiles (Required)
        Example parameter value: COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56
        """
        pass


    def get_compounds_containing_SMILES(url='http://www.ebi.ac.uk/chemblws/compounds/substructure/%s.json'):
        """
        Description: Get list of compounds containing the substructure represented by the given Canonical SMILES
        Input: SMILES string
        Output: List of Compound Records
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/substructure/COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/substructure/COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56.json
        """
        return url
    get_compounds_containing_SMILES = __f1(get_compounds_containing_SMILES)


    def get_compunds_containing_SMILES_by_HTTP_POST(url='http://www.ebi.ac.uk/chemblws/compounds/substructure'):
        """
        Description: Get list of compounds containing the substructure represented by the given Canonical SMILES by HTTP POST
        Input: SMILES string
        Output: List of Compound Records
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/substructure
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/substructure.json
        POST parameter: smiles (Required)
        Example parameter value: N#CCc2ccc1ccccc1c2
        """
        pass


    def get_compounds_similar_to_SMILES(url='http://www.ebi.ac.uk/chemblws/compounds/similarity/%s.json'):
        """
        Description: Get list of compounds similar to the one represented by the given Canonical SMILES, at a similarity cutoff percentage score (minimum value=70%, maximum value=100%).
        Input: SMILES string
        Output: List of Compound Records
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/similarity/COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56/70
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/similarity/COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56/70.json
        """
        return url
    get_compounds_similar_to_SMILES = __f1(get_compounds_similar_to_SMILES)

        
    def get_compounds_similar_to_SMILES_by_http_post():
        """
        Description: Get list of compounds similar to the one represented by the given Canonical SMILES, at a similarity cutoff percentage score (minimum value=70%, maximum value=100%) by HTTP POST
        Input: SMILES string
        Output: List of Compound Records
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/similarity
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/similarity.json
        POST parameter: smiles (Required)
        Example parameter value: O=C(C=CC#Cc2cccc(NS(=O)(=O)c1ccc(N(=O)=O)cc1)c2)NO
        POST parameter: simscore (Required)
        Example parameter value: 75
        """
        pass


    def get_image_of_compound_by_ChEMBLID(self, k, dimensions=None, file_out=None):
        """
        Description: Get the image of a given compound.
        Input: Compound ChEMBLID
        Output: Byte array image data
        Example URL: http://www.ebi.ac.uk/chemblws/compounds/CHEMBL192/image
        Example URL with dimensions parameter: http://www.ebi.ac.uk/chemblws/compounds/CHEMBL192/image?dimensions=200
        """
        def __f_save(target_data,file_out):
            FILE = open(file_out,'w')
            FILE.write(target_data)
            FILE.close()
            print "saved to %s"%file_out
            
        if isinstance(k,str):
            url='http://www.ebi.ac.uk/chemblws/compounds/%s/image'%k
            if dimensions is not None:
                url += '?dimensions=%s'%dimensions
            target_data = urllib2.urlopen(url).read()
            print url
            if file_out is None:
                file_out = os.getcwd()
                file_out += '/%s.png'%k
            __f_save(target_data,file_out)
            webbrowser.open(file_out)
            
        elif isinstance(k,tuple) or isinstance(k,list):
            for item in k:
                url='http://www.ebi.ac.uk/chemblws/compounds/%s/image'%item
                if dimensions is not None:
                    url += '?dimensions=%s'%dimensions
                target_data = urllib2.urlopen(url).read()
                if file_out is None:
                    file_out = os.getcwd()
                    file_out += '/%s.png'%item
                __f_save(target_data,file_out)


    def get_compound_activities(url='http://www.ebi.ac.uk/chemblws/compounds/%s/bioactivities.json'):
        """
        Description: Get individual compound bioactivities
        Input: Compound ChEMBLID
        Output: List of all bioactivity records in ChEMBLdb for a given compound ChEMBLID
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/compounds/CHEMBL2/bioactivities
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/compounds/CHEMBL2/bioactivities.json
        """
        return url
    get_compound_activities = __f1(get_compound_activities)


    def get_target_by_chemblId(url='http://www.ebi.ac.uk/chemblws/targets/%s.json'):
        """
        Description: Get target by ChEMBLID
        Input: Target ChEMBLID
        Output: Target Record
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/targets/CHEMBL2477
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/targets/CHEMBL2477.json
        """
        return url
    get_target_by_chemblId = __f1(get_target_by_chemblId)


    def get_target_by_uniprotId(url='http://www.ebi.ac.uk/chemblws/targets/uniprot/%s.json'):
        """
        Description: Get individual target by UniProt Accession Id
        Input: UniProt Accession Id
        Output: Target Record
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/targets/uniprot/Q13936
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/targets/uniprot/Q13936.json
        """
        return url        
    get_target_by_uniprotId = __f1(get_target_by_uniprotId)

    

    def get_target_by_refSeqId(url='http://www.ebi.ac.uk/chemblws/targets/refseq/%s.json'):
        """
        Description: Get individual target by RefSeq Accession Id
        Input: RefSeq Accession Id
        Output: Target Record
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/targets/refseq/NP_001128722
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/targets/refseq/NP_001128722.json
        """
        return url


    def get_target_bioactivities(url='http://www.ebi.ac.uk/chemblws/targets/%s/bioactivities.json'):
        """        
        Description: Get individual target bioactivities
        Input: Target ChEMBLID
        Output: List of all bioactivity records in ChEMBLdb for a given target ChEMBLID
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/targets/CHEMBL240/bioactivities
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/targets/CHEMBL240/bioactivities.json
        """
        return url
    get_target_bioactivities = __f1(get_target_bioactivities)



    def get_all_targets(url='http://www.ebi.ac.uk/chemblws/targets.json'):
        """
        Description: Get all targets
        Input: N/A
        Output: List of all target records in ChEMBLdb
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/targets
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/targets.json
        """
        target_data = urllib2.urlopen(url).read()
        target_data = json.loads(target_data)
        return target_data



    def get_assay_by_chemblId(url='http://www.ebi.ac.uk/chemblws/assays/%s.json'):
        """
        Description: Get assay by ChEMBLID
        Input: Assay ChEMBLID
        Output: Assay Record
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/assays/CHEMBL1217643
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/assays/CHEMBL1217643.json
        """
        return url
    get_assay_by_chemblId = __f1(get_assay_by_chemblId)
    

    def get_assay_bioactivities(url='http://www.ebi.ac.uk/chemblws/assays/%s/bioactivities.json'):
        """
        Description: Get individual assay bioactivities
        Input: Assay ChEMBLID
        Output: List of all bioactivity records in ChEMBLdb for a given assay ChEMBLID
        Example URL (XML Output): http://www.ebi.ac.uk/chemblws/assays/CHEMBL1217643/bioactivities
        Example URL (JSON Output): http://www.ebi.ac.uk/chemblws/assays/CHEMBL1217643/bioactivities.json 
        """
        return url
    get_assay_bioactivities = __f1(get_assay_bioactivities)
