from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

# Model config
A0 = 5.431
TOTAL_LAYERS = 7

# Display config
DISPLAY_REPEAT = (3, 3, 1)
SHOW_GUI = True

# Table III: k, l, m, dx, dz (angstroms)
table = np.array([
    [0, 0,  0,  0.805, -0.524],
    [2, 0,  0, -0.805, -0.524],
    [0, 1, -1,  0.075, -0.141],
    [2, 1, -1, -0.075, -0.141],
    [1, 1, -2,  0.000, -0.216],
    [3, 1, -2,  0.000,  0.005],
    [1, 0, -3,  0.000, -0.139],
    [3, 0, -3,  0.000,  0.002],
    [0, 0, -4, -0.022, -0.040],
    [2, 0, -4,  0.022, -0.040]
])

scale = A0 / 4 * np.array([np.sqrt(2), np.sqrt(2), 1])
positions = table[:, :3] * scale
positions[:, 0] += table[:, 3]
positions[:, 2] += table[:, 4]

# Bulk layers
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
slab.info["reconstruction"] = "p(2x1)s"
slab.info["model"] = "Five reconstructed layers; any deeper layers ideal; bare bottom"

output = Path(__file__).resolve().parent / "output"
output.mkdir(exist_ok=True)
name = Path(__file__).stem
write(output / f"{name}.extxyz", slab)
write(output / f"{name}.traj", slab)

# Display
if SHOW_GUI:
    view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)
