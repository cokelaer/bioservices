from bioservices import PDB


pdb = PDB(verbose=False)


def test_similarity():
    seq = "VLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTAVAHVDDMPNAL"
    results = pdb.get_similarity_sequence(seq)


def test_split_query():
    pdb.search(query ={
                "type": "terminal",
                "service": "sequence",
                "parameters": {
                  "evalue_cutoff": 1,
                  "identity_cutoff": 0.9,
                  "target": "pdb_protein_sequence",
                  "value": "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHQYREQIKRVKDSDDVPMVLVGNKCDLPARTVETRQAQDLARSYGIPYIETSAKTRQGVEDAFYTLVREIRQHKLRKLNPPDESGPGCMNCKCVIS"
                }},
            request_options =  { "scoring_strategy": "sequence"},
            return_type= "polymer_entity"
    )



def test_get_current_ids():
    assert len(pdb.get_current_ids()) > 100


def test_pdb():
    res  = pdb.search({
  "query": {
    "type": "group",
    "logical_operator": "and",
    "nodes": [
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "exact_match",
          "value": "C2",
          "attribute": "rcsb_struct_symmetry.symbol"
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "exact_match",
          "value": "Global Symmetry",
          "attribute": "rcsb_struct_symmetry.kind"
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "value": "\"heat-shock transcription factor\""
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "greater_or_equal",
          "value": 1,
          "attribute": "rcsb_entry_info.polymer_entity_count_DNA"
        }
      }
    ]
  },
  "return_type": "assembly"
})
