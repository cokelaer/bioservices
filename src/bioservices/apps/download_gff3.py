from bioservices.ena import ENA
from bioservices.eutils import EUtils


def download_gff3(accession, output_filename=None, method="EUtils", service=None):
    """Utility to download a GFF3 file from ENA or EUtils

    :param accession: a valid accession number with possible version (see
        example)
    :param output_filename: if none, use accession + fa extension (replaces dot
        with underscore)
    :param method: either EUtils or ENA
    :param service: an existing instance of ENA or EUtils. This is useful to
        call this functions many times. The creation of the service is indeed
        time consuming. If used, then **method** is ignored.

    ::

        download_gff3("FN433596.1")

    """
    if service:
        method = service.services.name

    if output_filename is None:
        output_filename = accession.replace(".", "_") + ".gff3"

    if method == "EUtils":
        _download_gff3_ncbi(accession, output_filename, service)
    elif method == "ENA":
        _download_gff3_ena(accession, output_filename, service)
    else:
        raise ValueError("method or service must be either ENA or EUtils")


def _download_gff3_ena(accession, output_filename, service=None):
    raise NotImplementedError

def _download_gff3_ncbi(accession, output_filename, service=None):
    if service is None:
        service = EUtils()
    data = service.EFetch("nucleotide", accession, rettype="gff3")
    data = data.decode()
    # Save to local file
    with open(output_filename, "w") as fout:
        fout.write(data)


