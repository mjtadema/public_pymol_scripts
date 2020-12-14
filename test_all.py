from pymol import cmd
from mindist import mindist
from mutate import mutate

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
