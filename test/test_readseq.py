from bioservices import readseq
from nose.plugins.attrib import attr



fasta = """MDAPRQVVNFGPGPAKLPHSVLLEIQKELLDYKGVGISVLEMSHRSSDFAKIINNTENLVRELLAVPDNYKVIFLQGGGCGQFSAVPLNLIGLKAGRCADYVVTGAWSAKAAEEAKKFGTINIVHPKLGSYTKIPDPSTWNLNPDASYVYYCANETVHGVEFDFIPDVKGAVLVCDMSSNFLSKPVDVSKFGVIFAGAQKNVGSAGVTVVIVRDDLLGFALRECPSVLEYKVQAGNSSLYNTPPCFSIYVMGLVLEWIKNNGGAAAMEKLSSIKSQTIYEIIDNSQGFYVCPVEPQNRSKMNIPFRIGNAKGDDALEKRFLDKALELNMLSLKGHRSVGGIRASLYNAVTIEDVQKLAAFMKKFLEMHQL"""


@attr('fixme') # does not work on travis
def test_readseq():

    # 8 is 
    # 2 is GenBank
    s = readseq.Readseq()
    jobid = s.run("cokelaer@test.co.uk", "test", sequence=fasta, inputformat=8, 
            outputformat=2)
    # should fail
    genbank = s.get_result(s._jobid)

    import time
    count = 0
    while s.get_status(s._jobid) != "FINISHED" and count<20:
        count += 1
        time.sleep(1)
        print(count)

    genbank = s.get_result(s._jobid)


    # now let us do the inverse
    jobid = s.run("cokelaer@ebi.co.uk", "test", sequence=genbank, inputformat=2, 
            outputformat=8)
    #FIXME do not know yet how to check
