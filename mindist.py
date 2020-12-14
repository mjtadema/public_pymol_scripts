#!/usr/bin/env python3
"""
Calculate distances between all atoms
in selection1 and selection2, then make a 
distance object for the smallest distance.

If you want to calculate the shortest distance for a very 
large selection, consider installing anaconda (https://www.anaconda.com/).
Anaconda provides numpy which is needed for faster calculations.


Usage: mindist selection1, selection2, [n=1, [t=500, [unique=False]]]

selection1  : selection string for atoms in the first selection
selection2  : selection string for atoms in the selection selection
n           : number of distances to calculate (default: 1)
t           : threshold of number of atoms if using non-numpy calculation (default: 500)
unique      : only one distance per residue (default: 0 (0=no, 1=yes))
"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201213

from pymol import cmd
import warnings
warnings.simplefilter('error', ResourceWarning)
try:
    import numpy as np
except:
    warnings.warn("Using mindist without numpy; limit your selections to few atoms.")


def gen_index(selection) -> int:
    "convert the selection to a list of unique indices"
    model = cmd.get_model(selection)
    for at in model.atom:
        yield int(at.index)

def gen_pairs(selection1, selection2, *, t=500) -> tuple:
    "Exhaustively generate index pairs for all atoms in selection"
    set_selection1 = set(list(gen_index(selection1)))
    set_selection2 = set(list(gen_index(selection2)))
    # Check if not selecting too many atoms
    l1 = len(set_selection1)
    l2 = len(set_selection2)
    l = sum([l1, l2])
    if l > t:
        msg = f"Using slow (non numpy) implementation with too many atoms ({l}> {t}). Consider selecting fewer atoms or installing numpy/conda."
        warnings.warn(msg, ResourceWarning)
    # ensure that all pairs are unique
    diff_selection2 = set_selection1.difference(set_selection2)
    for i in set_selection1:
        for j in set_selection2:
            yield (i, j)


def get_distances(selection1, selection2, **kwargs) -> float:
    "Calculate distances for all atoms in selection"
    for at1, at2 in gen_pairs(selection1, selection2, **kwargs):
        d = float(cmd.get_distance(f"index {at1}", f"index {at2}"))
        yield (at1, at2), d


def get_mindist(selection1, selection2, **kwargs):
    """
    Terribly slow implementation.
    Warn if selecting too many atoms
    t: int, threshold value
    """
    all_distances = {pair: d for pair, d in get_distances(selection1, selection2, **kwargs)}    
    sortkey = lambda x: all_distances[x]
    min_pairs = sorted(all_distances.keys(), key=sortkey)
    for min_pair in min_pairs:
        yield min_pair

def get_mindist_np(selection1, selection2):
    """
    Calculate distances using numpy
    """
    # Generate two arrays for coordinates
    index_1 = []
    coord_1 = []
    for at in cmd.get_model(selection1).atom:
        x, y, z = [float(n) for n in at.coord]
        coord_1.append((x, y, z))
        index_1.append(int(at.index))
    index_2 = []
    coord_2 = []
    for at in cmd.get_model(selection2).atom:
        x, y, z = [float(n) for n in at.coord]
        coord_2.append((x, y, z))
        idx = int(at.index)
        if idx not in index_1:
            index_2.append(int(at.index))
            # Else just skip, don't want duplicates

    # Calculate distance matrix
    coord_1 = np.array(coord_1)
    coord_2 = np.array(coord_2)
    matrix = np.subtract(coord_1[:,None], coord_2[None,:])
    dm = np.linalg.norm(matrix, axis=2)
    # Min index of the matrix
    sort_index = np.argsort(dm, axis=None)

    for idx in sort_index:
        # Min indices unraveled
        idx1, idx2 = np.unravel_index(idx, np.shape(dm))
        # Back to atom indices
        min_pair = (index_1[idx1], index_2[idx2])
        yield min_pair


def idx_to_resi(idx: int) -> int:
    "Get the residue number corresponding to the atom index"
    model = cmd.get_model(f"index {idx}")
    resi = model.atom[0].resi
    resi = int(resi)
    return resi
ir = idx_to_resi # abbrev
    

def mindist(selection1, selection2, n=1, t=500, unique=0, _legacy=0):
    try:
        if int(_legacy) != 0:
            raise ImportError("Used for testing without numpy")
        gen_mindist = get_mindist_np(selection1, selection2)
    except (NameError, ImportError, NotImplementedError):
        gen_mindist = get_mindist(selection1, selection2, t=500)
    resi_pairs = [] # keep track of residue pairs in case we want to skip
    count = 0
    while count < int(n):
        try:
            min_pair = next(gen_mindist)
        except StopIteration:
            # it could be that < n pairs were selected
            break
        a, b = min_pair
        resi_pair = {ir(a), ir(b)}
        if unique == 1 and resi_pair in resi_pairs:
            # skip if we want only unique residues
            # distances are sorted anyway so we'll get the shortes distance
            continue
        else:
            resi_pairs.append(resi_pair)
        cmd.distance(f"mindist_{a}_{b}", f"index {a}", f"index {b}")
        count += 1

mindist.__doc__ = __doc__
cmd.extend('mindist', mindist)
    
cmd.auto_arg[0]['mindist'] = [cmd.selection_sc, 'selection 1', ', ']
cmd.auto_arg[1]['mindist'] = [cmd.selection_sc, 'selection 2', ', ']
cmd.auto_arg[2]['mindist'] = ['', '#distances', '']
cmd.auto_arg[3]['mindist'] = ['', 'threshold', '']
# For some reason pymol doesn't want to add a 5th one...
#cmd.auto_arg[4]['mindist'] = ['', 'unique res', '']
