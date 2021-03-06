from pymol import cmd
from mindist import mindist
from mutate import mutate
from fasta import fasta
from axes import axes
from split_chains import split_chains
from merge_chains import merge_chains
from princ_align import princ_align
from carve import carve

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

def test_split_chains():
    split_chains('4tsy')
    
def test_merge_chains():
    merge_chains('4tsy')

def test_princ_align():
    princ_align('4tsy')
    
def test_carve():
    carve('4tsy', view_key='F1')
    
