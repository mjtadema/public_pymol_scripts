"""
Loader script to dynamically load pymol scripts in pymol
"""
import requests
from pymol import cmd
from pathlib import Path
from datetime import datetime
import json
from hashlib import sha1 as sha

author = "Matthijs J. Tadema, MSc (2020)"
version = 20201214


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
    # This can be much much longer, changed to 24
    if delta_hours(response_file) >= 24:
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
exclude = ["readme.py", "test_all.py"]
exclude_load = ["loader.py"]
modules = {}
for obj in objects:
    name = obj['name']
    if name in exclude: continue
    if name.endswith(".py"):
        # Add also file hash
        modules[obj['name']] = (obj['download_url'], obj['sha'])

# Update cached modules
for module, (url, hash_remote) in modules.items():
    module_path = Path(cachedir / module)
    try:
        assert module_path.exists()
        # Change this to test for changes (/w file hashes)
        with open(module_path, 'rb') as file_to_hash:
            b_file = file_to_hash.read()
            # Apparently git uses this weird way of hashing files which includes
            # "blob {length of file}\0" (\0 being NULL)
            b_blob = b'blob ' + bytearray(str(len(b_file)), 'utf-8') + b'\0'
            hash_local = sha(b_blob + b_file).hexdigest()
        print(f"Reading {module} hash")
        print(f"Remote hash {hash_remote}")
        print(f"Local hash {hash_local}")
        assert hash_local == hash_remote
        print(f"{module} is up to date")
    except AssertionError:
        print(f"Caching {module}")
        with open(module_path, 'wb') as fout:
            reponse = requests.get(url)
            fout.write(reponse.content)
    
# Cache first, load later..
for module in modules.keys():
    if module in exclude_load: continue
    # Finally load the module and inform the user
    module_path = Path(cachedir/module)
    cmd.run(str(module_path.absolute()))
    print(f"Loaded {module}")
    
