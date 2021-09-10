#
#  This file is part of BioServices
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import functools
import glob
import os
from pathlib import Path
import pkg_resources
import shutil
import subprocess
import sys
import tempfile

import click

import colorlog

logger = colorlog.getLogger(__name__)

__all__ = ["main"]


# This can be used by all commands as a simple decorator
def common_logger(func):
    @click.option(
        "--logger",
        default="INFO",
        type=click.Choice(["INFO", "DEBUG", "WARNING", "CRITICAL", "ERROR"]),
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


from bioservices import version
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version)
def main(**kwargs):
    """This is the main entry point for a set of BioServices application

    """
    pass


@main.command()
@click.option("--accession", type=click.STRING)
@click.option("--output", type=click.STRING, default=None)
@click.option("--method", type=click.Choice(["ENA", "EUtils"]),
    default="EUtils")
def download_accession(**kwargs):
    """

    Input file can be gzipped or not. The --output-file

        bioservices download-accession FN433596.1
    """
    from bioservices.apps.download_fasta import download_fasta
    download_fasta(kwargs['accession'], output_filename=kwargs['output'],
        method=kwargs['method'])

