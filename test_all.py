from pymol import cmd
from mindist import mindist
from mutate import mutate
from fasta import fasta
from axes import axes

cmd.fetch('4tsy')

def test_mindist_np():
    import numpy as np
    mindist("chain A", "chain D", n=10)

def test_mindist_warn():
    try:
        mindist("chain A", "chain D", n=10, _legacy=1)
        raise RuntimeError
    except ResourceWarning:
        return 

def test_mindist():
    mindist("chain A and resi 10:12", "chain D and resi 10:12", n=10, unique=1)

def test_mutate():
    mutate("resi 12", "R")

def test_fasta():
    fasta('(all)')

def test_axes():
    axes()
    axes(zero=1)
