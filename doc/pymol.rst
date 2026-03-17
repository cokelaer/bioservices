PYMOL
=========

:URL: http://www.pymol.org/

This example below uses the external software called PyMOL. It can be installed via conda::

    conda install -c schrodinger pymol-bundle


The following code uses BioServices to get the PDB Identifier of a protein
called ZAP70. To do so, we use :class:`bioservices.uniprot.UniProt` to get its accession number (P43403) and its
PDB identifer. Then, we use :class:`bioservices.pdb.PDB` to get the 3D structure in PDB
format.



.. literalinclude:: pymol_app.py
    :language: python
    :linenos:
    :emphasize-lines: 8,15,26

The script above uses PyMOL in a script manner to save the 3D graphical representation of the protein (here below) but you could also
use PyMOL in an interactive mode.

.. figure:: pymol.png
