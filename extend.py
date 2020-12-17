"""
Extend a protein structure with a peptide sequence
"""

from pymol import cmd
from tempfile import TemporaryDirectory
import os

cwd = os.getcwd()

with TemporaryDirectory() as tmpdir:
    os.chdir(tmpdir)
    cmd.save('_tmp.pse')
    try:
        pass
    except as e:
        print("Reverting to previous state...")
    finally:
        os.chdir(cwd)
