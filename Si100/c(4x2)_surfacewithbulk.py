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
    [0, 0, 0, 0.989, 0.000, -0.789],
    [2, 0, 0, -0.685, 0.000, -0.055],
    [0, 2, 0, 0.675, 0.000, -0.045],
    [2, 2, 0, -1.001, 0.000, -0.788],
    [0, 1, -1, 0.108, 0.120, -0.079],
    [2, 1, -1, -0.120, -0.117, -0.086],
    [0, 3, -1, 0.108, -0.119, -0.079],
    [2, 3, -1, -0.120, 0.117, -0.086],
    [1, 1, -2, -0.009, 0.001, -0.223],
    [3, 1, -2, -0.003, 0.020, 0.066],
    [1, 3, -2, -0.009, 0.000, -0.223],
    [3, 3, -2, -0.003, -0.020, 0.066],
    [1, 0, -3, 0.006, 0.000, -0.153],
    [3, 0, -3, -0.005, 0.000, 0.069],
    [1, 2, -3, -0.011, 0.000, -0.155],
    [3, 2, -3, -0.006, 0.000, 0.028],
    [0, 0, -4, -0.041, 0.000, -0.023],
    [2, 0, -4, 0.039, 0.000, -0.040],
    [0, 2, -4, -0.045, 0.000, -0.038],
    [2, 2, -4, 0.037, 0.000, -0.023]
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

# Primitive c(4x2) cell: crossing x also shifts y by half its period.
slab = Atoms(
    symbols=["Si"] * len(positions),
    positions=positions,
    cell=[[A0 * np.sqrt(2), A0 / np.sqrt(2), 0],
          [0, A0 * np.sqrt(2), 0], [0, 0, 0]],
    pbc=[True, True, False],
    tags=np.repeat(np.arange(1, TOTAL_LAYERS + 1), 4)
)
slab.info["source_doi"] = "10.1103/PhysRevB.51.14504"
slab.info["reconstruction"] = "c(4x2)"
slab.info["model"] = "Five reconstructed layers; any deeper layers ideal; bare bottom"

output = Path(__file__).resolve().parent / "output"
output.mkdir(exist_ok=True)
name = Path(__file__).stem
write(output / f"{name}.extxyz", slab)
write(output / f"{name}.traj", slab)

# Display x horizontally and z vertically, as in Figure 18.
if SHOW_GUI:
    view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)
