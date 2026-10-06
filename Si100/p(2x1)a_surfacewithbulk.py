from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

# Ramstad et al. (1995), Table III. DOI: 10.1103/PhysRevB.51.14504
A0 = 5.431
TOTAL_LAYERS = 12
DISPLAY_REPEAT = (3, 3, 1)
SHOW_GUI = True

if TOTAL_LAYERS < 5:
    raise ValueError("TOTAL_LAYERS must be at least 5 for the reconstructed layers")

# Columns: k, l, m, dx, dz. All displacements are in angstroms.
table = np.array([
    [0, 0, 0, 1.162, -0.921],
    [2, 0, 0, -0.534, -0.213],
    [0, 1, -1, 0.066, -0.141],
    [2, 1, -1, -0.099, -0.112],
    [1, 1, -2, 0.031, -0.240],
    [3, 1, -2, -0.025, -0.003],
    [1, 0, -3, -0.013, -0.155],
    [3, 0, -3, -0.005, 0.002],
    [0, 0, -4, -0.042, -0.044],
    [2, 0, -4, 0.022, -0.040]
])

scale = A0 / 4 * np.array([np.sqrt(2), np.sqrt(2), 1])
positions = table[:, :3] * scale
positions[:, 0] += table[:, 3]
positions[:, 2] += table[:, 4]

# Continue the four-layer diamond stacking below the reconstructed layers.
stacking = [(0, 0), (0, 1), (1, 1), (1, 0)]
for n in range(5, TOTAL_LAYERS):
    k, l = stacking[n % 4]
    lower = np.array([[k, l, -n], [k + 2, l, -n]]) * scale
    positions = np.vstack([positions, lower])

slab = Atoms(
    symbols=["Si"] * len(positions),
    positions=positions,
    cell=[A0 * np.sqrt(2), A0 / np.sqrt(2), 0],
    pbc=[True, True, False],
    tags=np.repeat(np.arange(1, TOTAL_LAYERS + 1), 2)
)
slab.info["source_doi"] = "10.1103/PhysRevB.51.14504"
slab.info["reconstruction"] = "p(2x1)a"
slab.info["model"] = "Five reconstructed layers; any deeper layers ideal; bare bottom"

output = Path(__file__).resolve().parent / "output"
output.mkdir(exist_ok=True)
name = Path(__file__).stem
write(output / f"{name}.extxyz", slab)
write(output / f"{name}.traj", slab)

# Display x horizontally and z vertically, as in Figure 18.
if SHOW_GUI:
    view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)
