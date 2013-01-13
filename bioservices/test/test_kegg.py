from bioservices import Kegg
from nose import with_setup

class test_Kegg(Kegg):


    def __init__(self):
        super(test_Kegg, self).__init__()

    def test_info(self):
        self.info()
