"""
DESCRIPTION
    Split object into chains.
    By default chains are also colored.

ARGUMENTS
    object: object to split (default: top object)
    color: color by chain (default: 1)

EXAMPLE
    split_chains obj01
    split_chains color=0

SEE ALSO
    merge_chains
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201214

from pymol import cmd, util


def split_chains(obj=None, color=1):
    if obj is None:
        obj = cmd.get_object_list()[0]
    chains = cmd.get_chains(obj)
    for chain in chains:
        new_obj = obj+"_"+chain
        cmd.create(new_obj, f"{obj} and chain {chain}")
        cmd.color('atomic', new_obj)
    cmd.center(obj)
    cmd.delete(obj)
    if int(color) == 1:
        util.color_objs(f"elem c and {obj}_*")

split_chains.__doc__ = __doc__
cmd.extend('split_chains', split_chains)
cmd.auto_arg[0]['split_chains'] = [cmd.object_sc, 'object', '']


