#!/usr/bin/env python3
"""
Very simple script to just print the fasta sequence of a selection

Usage: fasta selection

selection: selection string
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201214

from pymol import cmd

def fasta(selection="all"):
    print(cmd.get_fastastr(selection))

fasta.__doc__ = __doc__
cmd.extend('fasta', fasta)

cmd.auto_arg[0]['fasta'] = [cmd.selection_sc, 'selection', '']

