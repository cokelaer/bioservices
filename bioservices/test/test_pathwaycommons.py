from bioservices import pathwaycommons



def test_search_queries():
    pc2 = pathwaycommons.PathwayCommons(verbose=False)
    pc2.search("Q06609")
    pc2.search("brca2", type="proteinreference", organism="homo sapiens",
            datasource="pid")
    pc2.search("name:'col5a1'", type="proteinreference", organism=9606)
    pc2.search("a*", page=3)


    #http://www.pathwaycommons.org/pc2/get?uri=http://identifiers.org/uniprot/Q06609
def test_get():
    pc2 = pathwaycommons.PathwayCommons(verbose=False)
    pc2.get("col5a1")
    pc2.get("http://identifiers.org/uniprot/Q06609")


def test_idmapping():
    pc2 = pathwaycommons.PathwayCommons(verbose=False)
    pc2.idmapping("BRCA2")
    pc2.idmapping(["TP53", "BRCA2"])

def test_top_pathways():
    pc2 = pathwaycommons.PathwayCommons(verbose=False)
    res = pc2.top_pathways()


def test_graph(): 
    pc2 = pathwaycommons.PathwayCommons(verbose=False)
    res = pc2.graph(source="http://identifiers.org/uniprot/P20908",
            kind="neighborhood", frmt="EXTENDED_BINARY_SIF")

    #res = pc2.graph(source="P20908", kind="neighborhood")


    #res = pc2.graph(source="COL5A1", kind="neighborhood")
    #res = pc2.graph(kind="neighborhood", source="COL5A1")


def test_traverse():
     pc2 = pathwaycommons.PathwayCommons(verbose=False)
     res = pc2.traverse(
        uri=['http://identifiers.org/uniprot/P38398', 'http://identifiers.org/uniprot/Q06609'], 
        path="ProteinReference/organism")
     #res = pc2.traverse(
     #       uri="http://identifiers.org/uniprot/Q06609",
     #       path="ProteinReference/entityReferenceOf:Protein/name")
     #res = pc2.traverse(
     #        "http://identifiers.org/uniprot/P38398",
     #        path="ProteinReference/entityReferenceOf:Protein")
     #res =pc2.traverse(uri=["http://identifiers.org/uniprot/P38398",
     #       "http://identifiers.org/taxonomy/9606"],
     #       path="Named/name")


test_traverse()

