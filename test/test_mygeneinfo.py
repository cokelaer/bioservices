from bioservices.mygeneinfo import MyGeneInfo

mgi = MyGeneInfo()


def test_get_all_genes():
    res =  mgi.get_genes("301345,22637")
    assert len(res) == 2
    assert res[0]['_id'] == '301345'


    mgi.get_genes(("301345,22637"))
    # first one is rat, second is mouse. This will return a 'notfound'
    # entry and the second entry as expected.
    res = mgi.get_genes("301345,22637", species="mouse") 
    assert '_id' not in res[0]
    assert res[1]['_id'] == '22637'
    assert res[1]['taxid'] == 10090


def test_get_one_gene():
    res =  mgi.get_one_gene("301345")
    assert res['_id'] == '301345'
    assert res['taxid'] == 10116


def test_get_one_query():
    res = mgi.get_one_query("zap70", size=10, dotfield=True, sort="taxid")
def test_get_queries():
    res = mgi.get_queries("zap70,zap70", dotfield=True)


def test_get_metadata():   
    res = mgi.get_metadata()
    res = mgi.get_taxonomy()
    assert 'human' in res
