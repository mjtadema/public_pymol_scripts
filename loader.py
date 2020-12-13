"""
Loader script to dynamically load pymol scripts in pymol
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201213
import requests
from pymol import cmd
import sys
from pathlib import Path

# Query the git repo for all files in root of branch master 
response = requests.get(r'https://api.github.com/repos/mjtadema/public_pymol_scripts/contents?ref=master')
if response.status_code is not 200:
    raise Exception(response.text)
objects = response.json()

# Search for pymol modules
scriptname = Path(sys.argv[0]).name
modules = {}
for obj in objects:
    name = obj['name']
    # But skip this file
    if name == scriptname: continue
    if name.endswith(".py"):
        modules[obj['name']] = obj['download_url']

# Load all the modules and inform the user
for module, url in modules.items():
    cmd.run(url)
    print(f"Loaded {module}")
