"""
DESCRIPTION
    Merge chains back into a common object

ARGUMENTS
    name: base name of the original object

EXAMPLE
    split_chains obj
    merge_chains obj

SEE ALSO
    split_chains
"""

author = "Matthijs J. Tadema, MSc (2020)"
version = 20201214

from pymol import cmd

def merge_chains(obj):
    cmd.create('_tmp', f"{obj}_*")
    cmd.delete(f"{obj}_*")
    cmd.set_name('_tmp', obj) 
    cmd.center(obj)

cmd.extend('merge_chains', merge_chains)

