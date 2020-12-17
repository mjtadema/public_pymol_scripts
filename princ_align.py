"""
Align a selection such that its principle axes are aligned with the x, y, z axes

"""
author = "Matthijs J. Tadema, MSc (2020)"
version = 20201217
# inspired by https://github.com/pierrepo/principal_axes
from pymol import cmd
try:
    import numpy as np
except:
    pass


def get_principal_axes(coords):
    """Calculate princ axes for the selection,
    return: ordered eigenvectors"""
    # Should figure out what's going on here...
    inertia = np.dot(coords.T, coords)
    eig_val, eig_vec = np.linalg.eig(inertia)
    # Order by largest eigenvalue
    order = np.argsort(eig_val)
    eig_val = eig_val[order]
    eig_vec = eig_vec[:, order].T
    return eig_vec


def vec_angle(v1, v2):
    # These should both be 1 actually...
    l1 = np.linalg.norm(v1)
    l2 = np.linalg.norm(v2)
    # Return degrees...
    rad = np.arccos(np.dot(v1, v2) / (l1*l2))
    return np.rad2deg(rad)


def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    Shamelessly stolen from https://stackoverflow.com/a/59204638
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix


def princ_align(selection='(all)'):

    model = cmd.get_model(f"{selection} and name CA")
    coords = [at.coord for at in model.atom]
    try:
        center = np.mean(coords, axis=0)
    except NameError:
        print("This command will not work without numpy.\nConsider installing numpy (or anaconda, provides numpy).")
        return
    coords -= center

    eig_vec = get_principal_axes(coords)
    # Now i have to calculate angles...
    # largest should be aligned with Z-axis
    Ox = np.array([1, 0, 0])
    Oy = np.array([0, 1, 0])
    Oz = np.array([0, 0, 1])

    # Transform everything such that it is centered around
    # selection's center, and rotated
    # Such that the principal axes of the selection
    # align with those of the frame of reference
    rot_mat = rotation_matrix_from_vectors(eig_vec[0], Oz)
    
    TTT = [
            *rot_mat[0], -center[0],
            *rot_mat[1], -center[1],
            *rot_mat[2], -center[2],
            0, 0, 0, 1
    ]
    
    cmd.transform_selection('(all)', TTT, transpose=1)
    
    # Finally center all
    cmd.center()
    return eig_vec # Just in case i need them later

cmd.extend('princ_align', princ_align)
cmd.auto_arg[0][princ_align] = [cmd.selection_sc, 'selection', '']
