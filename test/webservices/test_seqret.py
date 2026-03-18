import pytest

from bioservices import seqret

fasta = """MDAPRQVVNFGPGPAKLPHSVLLEIQKELLDYKGVGISVLEMSHRSSDFAKIINNTENLVRELLAVPDNYKVIFLQGGGCGQFSAVPLNLIGLKAGRCADYVVTGAWSAKAAEEAKKFGTINIVHPKLGSYTKIPDPSTWNLNPDASYVYYCANETVHGVEFDFIPDVKGAVLVCDMSSNFLSKPVDVSKFGVIFAGAQKNVGSAGVTVVIVRDDLLGFALRECPSVLEYKVQAGNSSLYNTPPCFSIYVMGLVLEWIKNNGGAAAMEKLSSIKSQTIYEIIDNSQGFYVCPVEPQNRSKMNIPFRIGNAKGDDALEKRFLDKALELNMLSLKGHRSVGGIRASLYNAVTIEDVQKLAAFMKKFLEMHQL"""


@pytest.mark.timeout(120)
@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_readseq():

    s = seqret.Seqret()
    jobid = s.run(
        **{
            "email": "cokelaer@test.co.uk",
            "title": "test",
            "sequence": fasta,
            "inputformat": "raw",
            "outputformat": "fasta",
            "stype": "protein",
        }
    )

    import time

    count = 0
    while s.get_status(jobid) != "FINISHED" and count < 20:
        count += 1
        time.sleep(1)
        print(count)
    s.get_result(s._jobid)
