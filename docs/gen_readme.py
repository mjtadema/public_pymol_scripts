#!/usr/bin/env python3
"""
Generate the README.md file based on a base file
+ docstrings from the separate tools.
"""
from pathlib import Path
import sys
import importlib

scriptdir = Path(sys.argv[0]).parent.absolute()
maindir = Path(scriptdir/"..")
sys.path.append(str(maindir.absolute()))

modules = []
for f in maindir.iterdir():
    if f.suffix == ".py":
        modules.append(f.stem)

print(f"{len(modules)} modules")

with open(maindir/"README.md", 'w') as fout:
    with open(scriptdir/"README-base.md") as fin:
        fout.writelines(fin)
        fout.write("\n")
    for module in modules:
        print(f"loading module {module}")
        loaded_module = importlib.import_module(module)
        fout.write(f"### {module}\n")
        fout.write(loaded_module.__doc__)
        fout.write("\n")
    
    
