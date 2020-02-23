from bioservices import EVA



def test_get_allinfo():
    e = EVA()
    e.fetch_allinfo("PRJEB4019")
