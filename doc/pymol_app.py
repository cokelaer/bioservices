import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import os
if os.path.isfile("bioservices_pdb.png"):
    os.remove("bioservices_pdb.png")

# BioServices 1: obtain the PDB ID from a given uniprot ID (P43403 i.e. ZAP70)
from bioservices import *
print("Retrieving PDB ID")
u = UniProt(verbose=False)
res = u.mapping(fr="UniProtKB_AC-ID", to="PDB", query="P43403")
pdb_id = res['results']['P43403'][0]   # e.g, "1FBV"

# BioServices 2: Download the PDB file from the PDB Web Service
print("Fetching PDB file")
p = pdbe.PDBe()
res = p.get_files(pdb_id)

# General: save the fetched file in a temporary file
import tempfile
fh = tempfile.NamedTemporaryFile()
fh.write(res)
sname = fh.name

# THIS IS NOT BIOSERVICES ANYMORE but PYMOL 
import pymol
pymol.finish_launching()
pymol.cmd.load(sname)
pymol.cmd.png("bioservices_pdb.png", width="15cm", height="15cm", dpi=140)
#pymol.cmd.png("my_image.png")
# Get out!
pymol.cmd.quit()
