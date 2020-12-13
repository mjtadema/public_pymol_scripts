#!/usr/bin/env python3
"""
Do mutations on several chains at once.

Usage: mutate selection, resname

selection   : selection string, all residues are mutated to the same resname
resname     : name of the residue to mutate to, can be one or three letter code
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201213

from pymol import cmd

def get_resi(selection):
    model = cmd.get_model(selection)
    return {at.resi for at in model.atom}

def get_chains(selection):
    model = cmd.get_model(selection)
    return {at.chain for at in model.atom}

def is_one_residue(selection):
    "Check if selection is a single residue"
    objects = {*cmd.get_object_list(selection)}
    chains = get_chains(selection)
    resi = get_resi(selection)
    return len(chains) == 1 and len(resi) == 1 and len(objects) == 1

def mutate_one(selection, aa):
    """
    Selection must be one residue
    """
    assert is_one_residue(selection)
    cmd.select(selection)
    cmd.get_wizard().do_select('''sele''')
    cmd.get_wizard().set_mode(aa)
    cmd.get_wizard().apply()
    print(f"Mutated {selection} to {aa}")
        
def iter_residues(selection):
    "return selection string for a single residue"
    objects = cmd.get_object_list(selection)
    for obj in objects:
        for chain in get_chains(f"{selection} and {obj}"):
            for resi in get_resi(f"{selection} and {obj}"):
                yield f"resi {resi} and chain {chain} and {obj}"

aminos = { 
    'A': "ALA",    'C': "CYS",
    'D': "ASP",    'E': "GLU",
    'F': "PHE",    'G': "GLY",
    'H': "HIS",    'I': "ILE",
    'K': "LYS",    'L': "LEU",
    'M': "MET",    'N': "ASN",
    'P': "PRO",
    'Q': "GLN",    'R': "ARG",
    'S': "SER",    'T': "THR",
    'V': "VAL",
    'W': "TRP",    'Y': "TYR"
    }
extra = ["ARGN", "ASPH", "GLUH", "HID", "HIE", 
         "HIP", "LYSN"]

def fix_aa(aa):
    aa = aa.upper()
    if len(aa) == 1:
        # Deal with a letter coding
        aa = aminos[aa].upper()
    elif len(aa) not in (1,3):
        raise ValueError(
        f"""Amino acid encoding must be 
        one or three letter, was {aa}""")
    return aa

def mutate(selection, aa):
    aa = fix_aa(aa)
    cmd.set("retain_order", 0)
    cmd.wizard("mutagenesis")
    cmd.refresh_wizard()
    for single_res in iter_residues(selection):
        mutate_one(single_res, aa)
    cmd.set_wizard()
    cmd.sort()

mutate.__doc__ = __doc__
cmd.extend('mutate', mutate)

cmd.auto_arg[0]['mutate'] = [cmd.selection_sc, 'selection', '']
amino_sc = lambda: cmd.Shortcut(list(aminos.keys())+list(aminos.values())+extra)
cmd.auto_arg[1]['mutate'] = [amino_sc, 'amino acid', '']
