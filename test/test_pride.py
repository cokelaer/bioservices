from bioservices import PRIDE







def test_pride_project():
    p = PRIDE()
    res = p.get_project_accession("PRD000001")
    assert res['numPeptides'] == 6758

    projects = p.get_project_list(show=100)
    
    
    counter = p.get_project_count(show=100)
    assert counter > 1000

                                    
