#!/usr/bin/env python3
"""
Generate the README.md file based on a base file
+ docstrings from the separate tools.
"""
from pathlib import Path
import sys
import importlib

scriptdir = Path(sys.argv[0]).parent.absolute()

with open(scriptdir/"pymolrc") as rch:
    pymolrc = rch.readline().strip()

README_base = f"""
# Assorted PyMOL scripts
Collection of pymol scripts written primarily for Giovanni Maglia's group members [(website](https://sites.google.com/a/rug.nl/maglia-lab-groningen/)[, university page)](https://www.rug.nl/research/chemical-biology/?lang=en)

## Usage:
Copy paste `{pymolrc}` into [your own pymolrc file](https://pymolwiki.org/index.php/Pymolrc). This will make PyMOL load the scripts automatically at startup.
"""

exclude = ['loader.py', 'readme.py', 'test_all.py']

modules = []
for f in scriptdir.iterdir():
    if f.name in exclude: continue
    if f.suffix == ".py":
        modules.append(f.stem)

print(f"{len(modules)} modules")

sys.path.append(str(scriptdir.absolute()))
with open(scriptdir/"README.md", 'w') as fout:
    fout.write(README_base)
    fout.write("\n")
    for module in modules:
        print(f"loading module {module}")
        loaded_module = importlib.import_module(module)
        fout.write(f"### {module}\n")
        fout.write(loaded_module.__doc__)
        fout.write("\n")
    
    
