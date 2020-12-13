"""
Loader script to dynamically load pymol scripts in pymol
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201213
import requests
from pymol import cmd
import sys
from pathlib import Path
from datetime import datetime
import json

class ResponseOutOfDate(Exception): pass
class RateLimit(Exception): pass

cachedir = Path.home()
response_file = cachedir/"pymol_loader.json"
try:
    # Check for a cached repo response
    if not response_file.exists():
        raise FileNotFoundError
    previous_response_time = datetime.fromtimestamp(response_file.stat().st_mtime)
    delta = datetime.now() - previous_response_time
    delta_hours = delta.seconds / 3600
    # Check if file is out of date
    if delta_hours >= 2:
        raise ResponseOutOfDate
    print("Reading cached list")
    with response_file.open() as rfh:
        objects = json.load(rfh)
except (FileNotFoundError, ResponseOutOfDate):
    # Query the git repo for all files in root of branch master 
    print("Querying for new list")
    response = requests.get(r'https://api.github.com/repos/mjtadema/public_pymol_scripts/contents?ref=master')
    if response.status_code != 200:
        raise RateLimit("Hit rate limiter, try again later")
    # Cache the response to file to avoid rate limiter
    with open(response_file, 'w') as cache_out:
        cache_out.write(response.text) 
    objects = response.json()

# Search for pymol modules
exclude =  ["loader.py", "readme.py"]
modules = {}
for obj in objects:
    name = obj['name']
    if name in exclude: continue
    if name.endswith(".py"):
        modules[obj['name']] = obj['download_url']

# Load all the modules and inform the user
for module, url in modules.items():
    cmd.run(url)
    print(f"Loaded {module}")
