"""
DESCRIPTION
    Clip a selection through the ZY-plane of its principal axes

ARGUMENTS
    selection: selection string
    cut_range: slab thickness
    view_key: optionally store the resulting view as an F key

EXAMPLE
    carve
    carve obj1
    carve obj1, 20
    carve obj1, view_key=F1 

"""
# Beware these are crude early versions, only possible to align with z axis for now
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201217
from pymol import cmd
from pathlib import Path
# Bit of a janky solution but have to inject the cache directory here...
import sys
cachedir = Path.home()/"mjtadema_pymol_cache"
sys.path.append(cachedir.name)
from princ_align import princ_align


@cmd.extend
def carve(selection='(all)', cut_range="5", view_key=None):
    cut_range = cut_range.split(":")
    try:
        cut_range = [int(n) for n in cut_range]
    except ValueError as e:
        msg = f"Malformed range {cut_range}"
        e.message = msg
        raise e

    # First align to principal axes
    princ_align(selection)
    cachedir = Path.home()/"mjtadema_pymol_cache"
    if len(cut_range) == 1:
        # symmetrically cut with thickness t
        t = cut_range[0]
        cut_select = f"{selection} and (y > {-t} and y < {t})"
        cmd.orient(cut_select)
        cmd.clip('slab', t*2, cut_select)
        if view_key is not None:
            cmd.view(view_key, 'store')
    elif len(cut_range) == 2:
        # cut from start to end
        raise NotImplementedError("Didn't get to asymmetric cuts yet")
        pass
    else:
        # panic
        raise ValueError("range can be at most 2 integers")

carve.__doc__ = __doc__
cmd.auto_arg[0]['carve'] = [cmd.selection_sc, 'selection', ', ']
cmd.auto_arg[1]['carve'] = ['', 'slab thickness', '']
f_keys_sc = lambda: cmd.Shortcut([f"F{n}" for n in range(12)])
cmd.auto_arg[2]['carve'] = [f_keys_sc, 'F1 key to store', '']
