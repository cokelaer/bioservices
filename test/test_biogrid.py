from bioservices import BioGRID

from nose.plugins.attrib import attr

# IF BIOMART WORKS, BIOGRIOD should work


# BioGRID design is not meant to be used really as a class. Need to be fixed.
#class test_biodbnet(object):
#    @classmethod
#    def setup_class(klass):
#        klass.s = BioGRID(verbose=False)


@attr('slow')
def test_biogrid():
    b = BioGRID(query=["map2k4","akt1"],taxId = "9606")
    b.biogrid.interactors
    b = BioGRID(query=["mtor","akt1"],taxId="9606",exP="two hybrid")
    b = BioGRID(query="mtor",taxId="9606")
    b.biogrid.interactors


