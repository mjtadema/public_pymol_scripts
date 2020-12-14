#!/usr/bin/env python3
"""
DESCRIPTION
    Print the fasta sequence of a selection

ARGUMENTS
    selection: selection string

EXAMPLE
    fasta chain A
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = "20201214_1"

from pymol import cmd

def fasta(selection="all"):
    print(cmd.get_fastastr(selection))

fasta.__doc__ = __doc__
cmd.extend('fasta', fasta)

cmd.auto_arg[0]['fasta'] = [cmd.selection_sc, 'selection', '']

