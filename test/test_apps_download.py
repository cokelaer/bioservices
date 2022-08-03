from bioservices.apps import download_fasta as df
import pytest



@pytest.mark.flaky
def test_download():

    from easydev import TempFile
    with TempFile() as f1:
        df.download_fasta("FN433596.1", output_filename=f1.name, method="ENA")

    with TempFile() as f2:
        df.download_fasta("FN433596.1", output_filename=f2.name, method="EUtils")

    with TempFile() as f3:
        from bioservices import ENA
        ena = ENA()
        df.download_fasta("FN433596.1", output_filename=f2.name, method="EUtils",
            service=ena)

    try:
        df.download_fasta("FN433596.1", method="dummy")
        assert False
    except:
        assert True
