BioPython
=========

:URL: http://biopython.org/DIST/docs/tutorial/Tutorial.html#chapter:Bio.AlignIO

BioPython provides many tools for IO, algorithms and access to Web services. 
BioServices provides access to many web services. This example shows how (i) to use
BioServices to retrieve FASTA files and (ii) BioPython to play with the
sequences.


.. note:: We assume you have installed BioPython (pip install biopython)

First, let us retrieve two FASTA sequences and save them in 2 files::

    from bioservices import UniProt
    u = UniProt()
    akt1 = u.retrieve("P31749", "fasta")
    akt2 = u.retrieve("P31751", "fasta")

    fh = open("akt1.fasta", "w")
    fh.write(akt1)
    fh.close()

    fh = open("akt2.fasta", "w")
    fh.write(akt2)
    fh.close()

Now, on the BioPython side, we read the 2 sequences and introspect them::

    >>> from Bio import AlignIO
    >>> record1 = SeqIO.read("akt1.fasta", "fasta")
    >>> record2 = SeqIO.read("akt2.fasta", "fasta")
    >>> record1 += "-"   # this is to have 2 sequences on same length as requested by the following function

    >>> alignment = AlignIO.MultipleSeqAlignment([])
    >>> alignment.append(record1)
    >>> alignment.append(record2)

    >>> for record in alignment:
    >>>     print(description)
    sp|P31749|AKT1_HUMAN RAC-alpha serine/threonine-protein kinase OS=Homo sapiens GN=AKT1 PE=1 SV=2
    sp|P31751|AKT2_HUMAN RAC-beta serine/threonine-protein kinase OS=Homo sapiens GN=AKT2 PE=1 SV=2

You are ready to play with BioPython multiple alignment tools. Please consult
BioPython documentation for more examples.


