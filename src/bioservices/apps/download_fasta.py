from bioservices.ena import ENA
from bioservices.eutils import EUtils


def download_fasta(accession, output_filename=None, method="EUtils", service=None):
    """Utility to download a FASTQ file from ENA or EUtils

    :param accession: a valid accession number with possible version (see
        example)
    :param output_filename: if none, use accession + fa extension (replaces dot
        with underscore)
    :param method: either EUtils or ENA
    :param service: an existing instance of ENA or EUtils. This is useful to
        call this functions many times. The creation of the service is indeed
        time consuming. If used, then **method** is ignored.

    ::

        download_fasta("FN433596.1")

    """
    if service:
        method = service.services.name

    if output_filename is None:
        output_filename = accession.replace(".", "_") + ".fa"

    if method == "EUtils":
        _download_fasta_ncbi(accession, output_filename, service)
    elif method == "ENA":
        _download_fasta_ena(accession, output_filename, service)
    else:
        raise ValueError("method or service must be either ENA or EUtils")


def _download_fasta_ena(accession, output_filename, service=None):
    if service is None:
        service = ENA()
    data = service.get_data(accession, "fasta")
    # data = data.decode()
    return _data_to_file(data, output_filename)


def _download_fasta_ncbi(accession, output_filename, service=None):
    if service is None:
        service = EUtils()
    data = service.EFetch("nucleotide", accession, rettype="fasta")
    data = data.decode()
    return _data_to_file(data, output_filename)


def _data_to_file(data, output_filename):
    # Split header and Fasta
    header, others = data.split("\n", 1)

    # Source of failure:
    # - some entries may be deleted
    if "suppressed" in header:
        raise ValueError("According to the header this accession has been suppressed")
    if ">" not in header:
        raise ValueError("No > character found in the header")

    # Save to local file
    with open(output_filename, "w") as fout:
        fout.write(header + "\n" + others)
