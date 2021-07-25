from bioservices import seqret
import pytest



fasta = """MDAPRQVVNFGPGPAKLPHSVLLEIQKELLDYKGVGISVLEMSHRSSDFAKIINNTENLVRELLAVPDNYKVIFLQGGGCGQFSAVPLNLIGLKAGRCADYVVTGAWSAKAAEEAKKFGTINIVHPKLGSYTKIPDPSTWNLNPDASYVYYCANETVHGVEFDFIPDVKGAVLVCDMSSNFLSKPVDVSKFGVIFAGAQKNVGSAGVTVVIVRDDLLGFALRECPSVLEYKVQAGNSSLYNTPPCFSIYVMGLVLEWIKNNGGAAAMEKLSSIKSQTIYEIIDNSQGFYVCPVEPQNRSKMNIPFRIGNAKGDDALEKRFLDKALELNMLSLKGHRSVGGIRASLYNAVTIEDVQKLAAFMKKFLEMHQL"""

pytest.mark.xfail
def test_readseq():

    s = seqret.Seqret()
    jobid = s.run(**{"email":"cokelaer@test.co.uk", "title":"test", "sequence":fasta,
        "inputformat":"raw", "outputformat":"fasta", "stype":"protein"})

    import time
    count = 0
    while s.get_status(jobid) != "FINISHED" and count<20:
        count += 1
        time.sleep(1)
        print(count)
    newfasta = s.get_result(s._jobid)
