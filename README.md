
# Assorted PyMOL scripts
Collection of pymol scripts written primarily for Giovanni Maglia's group members [(website](https://sites.google.com/a/rug.nl/maglia-lab-groningen/)[, university page)](https://www.rug.nl/research/chemical-biology/?lang=en)

## Usage:
Copy paste `run https://raw.githubusercontent.com/mjtadema/public_pymol_scripts/master/loader.py` into [your own pymolrc file](https://pymolwiki.org/index.php/Pymolrc). This will make PyMOL load the scripts automatically at startup.

### split_chains

DESCRIPTION
    Split object into chains.
    By default chains are also colored.

ARGUMENTS
    object: object to split (default: top object)
    color: color by chain (default: 1)

EXAMPLE
    split_chains obj01
    split_chains color=0

SEE ALSO
    merge_chains

### carve

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


### axes

DESCRIPTION
    Axes script (Based on https://pymolwiki.org/index.php/Axes)
    Show axes with nice cylinders and cones.
    By default it will move with the viewport and stay in the corner.
    Can be made to stay at 0,0,0 as well.

ARGUMENTS
    name: axes object name
    zero: keep axis object at zero (default: 0)

EXAMPLE
    axes
    axes new_axes
    axes center_axes, zero=1
    axes zero=1


### mindist

DESCRIPTION
    Calculate distances between all atoms
    in selection1 and selection2, then make a 
    distance object for the smallest distance.
    
    If you want to calculate the shortest distance for a very 
    large selection, consider installing anaconda (https://www.anaconda.com/).
    Anaconda provides numpy which is needed for faster calculations.
    
ARGUMENTS
    selection1  : selection string for atoms in the first selection
    selection2  : selection string for atoms in the selection selection
    n           : number of distances to calculate (default: 1)
    t           : threshold of number of atoms if using non-numpy calculation (default: 500)
    unique      : only one distance per residue (default: 0 (0=no, 1=yes))

EXAMPLE
    mindist chain A, chain D
    mindist chain A, chain D, n=10, unique=1

### mutate

DESCRIPTION
    Do mutations on an entire selection at once.
    Use default rotamers (by default the lowest strain).

ARGUMENTS
    selection   : selection string, all residues are mutated to the same resname
    resname     : name of the residue to mutate to, can be one or three letter code

EXAMPLE
    mutate resi 10, ARG
    mutate resi -1, A
    mutate resi 12 and chain A, G

### fasta

DESCRIPTION
    Print the fasta sequence of a selection

ARGUMENTS
    selection: selection string

EXAMPLE
    fasta chain A

### princ_align

DESCRIPTION
    Transform a selection such that its principle axes are aligned with the x, y, z axes

ARGUMENTS
    selection: a selection string

EXAMPLE
    princ_align obj01


### merge_chains

DESCRIPTION
    Merge chains back into a common object

ARGUMENTS
    name: base name of the original object

EXAMPLE
    split_chains obj
    merge_chains obj

SEE ALSO
    split_chains

