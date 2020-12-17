"""
Loader script to dynamically load pymol scripts in pymol
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201214
import requests
from pymol import cmd
import sys
from pathlib import Path
from datetime import datetime
import json


class ResponseOutOfDate(Exception): pass
class RateLimit(Exception): pass


def delta_hours(somepath: Path):
    "return the hours delta to now"
    previous_response_time = datetime.fromtimestamp(somepath.stat().st_mtime)
    delta = datetime.now() - previous_response_time
    return delta.seconds / 3600


cachedir = Path.home()/"mjtadema_pymol_cache"
cachedir.mkdir(exist_ok=True)
response_file = cachedir/"pymol_loader.json"

try:
    # Check for a cached repo response
    if not response_file.exists():
        raise FileNotFoundError

    # Check if file is out of date
    if delta_hours(response_file) >= 1:
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
exclude =  ["loader.py", "readme.py", "test_all.py"]
modules = {}
for obj in objects:
    name = obj['name']
    if name in exclude: continue
    if name.endswith(".py"):
        modules[obj['name']] = obj['download_url']

# Update cached modules
for module, url in modules.items():
    try:
        module_path = Path(cachedir/module)
        assert module_path.exists()
        assert delta_hours(module_path) <= 0.5
    except AssertionError:
        print(f"Caching {module}")
        with open(module_path, 'wb') as fout:
            reponse = requests.get(url)
            fout.write(reponse.content)
    
# Cache first, load later..
for module in modules.keys():
    # Finally load the module and inform the user
    cmd.run(str(module_path.absolute()))
    print(f"Loaded {module}")
    
