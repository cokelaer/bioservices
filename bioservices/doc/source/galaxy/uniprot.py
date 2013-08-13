# -*- python -*-
#
#  This file is part of BioServices software
#
#  Copyright (c) 2013 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://pypi.python.org/pypi/bioservices
#
##############################################################################
import sys

def __main__():
    ids = sys.argv[1]
    filename = sys.argv[2]
    # TODO: check the validity and format ? 
    try:
        from  bioservices import UniProt
        u = UniProt(verbose=False)
        u.debugLevel = "ERROR"
    except ImportError:
        print("Could not import bioservoces ? Check that it is installed. Try 'pip install bioservices'")

    try:
        fasta = u.searchUniProtId(ids, "fasta")
    except:
        print("An error occured while fetching the FASTA file from uniprot")

    try:
        fh = open(filename, "w")
        fh.write(fasta)
        fh.close()
    except:
        print("could not save the FASTA file")


if __name__ == '__main__':
    __main__()
