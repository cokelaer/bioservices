from bioservices import ArrayExpress



class test_AE(ArrayExpress):
    def __init__(self):
        super(test_AE, self).__init__()

    def test_retrieveFiles(self):
        res = self.retrieveFiles(keywords="cancer+breast", species="Home+Sapiens")
    
