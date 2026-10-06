from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

# Ramstad et al. (1995), Table IV. DOI: 10.1103/PhysRevB.51.14504
A0 = 5.431
TOTAL_LAYERS = 12
DISPLAY_REPEAT = (3, 3, 1)
SHOW_GUI = True

if TOTAL_LAYERS < 5:
    raise ValueError("TOTAL_LAYERS must be at least 5 for the reconstructed layers")

# Columns: k, l, m, dx, dy, dz. All displacements are in angstroms.
table = np.array([
    [0, 0, 0, 0.992, 0.000, -0.832],
    [2, 0, 0, -0.688, 0.000, -0.094],
    [0, 2, 0, 0.675, 0.000, -0.076],
    [2, 2, 0, -1.010, 0.000, -0.829],
    [0, 1, -1, 0.105, 0.119, -0.101],
    [2, 1, -1, -0.118, -0.112, -0.109],
    [0, 3, -1, 0.105, -0.118, -0.101],
    [2, 3, -1, -0.118, 0.113, -0.109],
    [1, 1, -2, -0.011, 0.001, -0.237],
    [3, 1, -2, -0.003, 0.002, 0.050],
    [1, 3, -2, -0.011, 0.000, -0.237],
    [3, 3, -2, -0.003, -0.002, 0.050],
    [1, 0, -3, 0.024, 0.000, -0.160],
    [3, 0, -3, 0.037, 0.000, 0.037],
    [1, 2, -3, -0.031, 0.000, -0.164],
    [3, 2, -3, -0.048, 0.000, 0.034],
    [0, 0, -4, -0.012, 0.000, -0.039],
    [2, 0, -4, 0.066, 0.000, -0.030],
    [0, 2, -4, -0.074, 0.000, -0.031],
    [2, 2, -4, 0.007, 0.000, -0.041]
])

scale = A0 / 4 * np.array([np.sqrt(2), np.sqrt(2), 1])
positions = table[:, :3] * scale
positions += table[:, 3:6]

# Continue the four-layer diamond stacking below the reconstructed layers.
stacking = [(0, 0), (0, 1), (1, 1), (1, 0)]
for n in range(5, TOTAL_LAYERS):
    k, l = stacking[n % 4]
    lower = np.array([[k, l, -n], [k + 2, l, -n],
                      [k, l + 2, -n], [k + 2, l + 2, -n]]) * scale
    positions = np.vstack([positions, lower])

slab = Atoms(
    symbols=["Si"] * len(positions),
    positions=positions,
    cell=[A0 * np.sqrt(2), A0 * np.sqrt(2), 0],
    pbc=[True, True, False],
    tags=np.repeat(np.arange(1, TOTAL_LAYERS + 1), 4)
)
slab.info["source_doi"] = "10.1103/PhysRevB.51.14504"
slab.info["reconstruction"] = "p(2x2)"
slab.info["model"] = "Five reconstructed layers; any deeper layers ideal; bare bottom"

output = Path(__file__).resolve().parent / "output"
output.mkdir(exist_ok=True)
name = Path(__file__).stem
write(output / f"{name}.extxyz", slab)
write(output / f"{name}.traj", slab)

# Display x horizontally and z vertically, as in Figure 18.
if SHOW_GUI:
    view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)
