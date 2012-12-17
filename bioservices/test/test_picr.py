from bioservices import picr



class TestPICR(object):

    def __init__(self):
        self.picr = picr.PICR()
        self.sequence="MDSTNVRSGMKSRKKKPKTTVIDDDDDCMTCSACQSKLVKISDITKVSLDYINTMRGNTLACAACGSSLKLLNDFAS"


    def test_getUPIForSequence(self):
        res = self.picr.getUPIForSequence(self.sequence, ["IPI", "ENSEMBL", "SWISSPROT"])
        assert len(res)>0


