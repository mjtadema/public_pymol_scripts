
# Assorted PyMOL scripts
Collection of pymol scripts written primarily for Giovanni Maglia's group members [(website](https://sites.google.com/a/rug.nl/maglia-lab-groningen/)[, university page)](https://www.rug.nl/research/chemical-biology/?lang=en)

## Usage:
Copy paste `run https://raw.githubusercontent.com/mjtadema/public_pymol_scripts/master/loader.py` into [your own pymolrc file](https://pymolwiki.org/index.php/Pymolrc). This will make PyMOL load the scripts automatically at startup.

### mindist

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

### mutate

Do mutations on several chains at once.

Usage: mutate selection, resname

selection   : selection string, all residues are mutated to the same resname
resname     : name of the residue to mutate to, can be one or three letter code

