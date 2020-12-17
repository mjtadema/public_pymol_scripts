"""
Clip a selection through one of its principal axes

"""
# Beware these are crude early versions, only possible to align with z axis for now
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201217
from pymol import cmd
from princ_align import princ_align


def cut(selection, cut_range):
    cut_range = cut_range.split(":")
    try:
        cut_range = [int(n) for n in cut_range]
    except ValueError as e:
        msg = f"Malformed range {cut_range}"
        e.message = msg
        raise e

    # First align to principal axes
    princ_align(selection)
    
    if len(cut_range) == 1:
        # symmetrically cut with thickness 
        pass
    elif len(cut_range) == 2:
        # cut from start to end
        pass
    else:
        # panic
        raise ValueError("range can be at most 2 integers")
