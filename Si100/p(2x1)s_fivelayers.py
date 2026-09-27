from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

# Ramstad et al. (1995), Table III. DOI: 10.1103/PhysRevB.51.14504
A0 = 5.431
TOTAL_LAYERS = 5
DISPLAY_REPEAT = (3, 3, 1)
SHOW_GUI = True
PAIR = (0, 1)
ANGLE = (1, 0, 2)

# Columns: k, l, m, dx, dz. All displacements are in angstroms.
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
ideal = table[:, :3] * scale
positions = ideal.copy()
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
slab.info["reconstruction"] = "p(2x1)s"
slab.info["model"] = "Five reconstructed layers; any deeper layers ideal; bare bottom"

# Check the built coordinates against Table III before any translation.
print("\nTable III comparison (A):")
print("ID Layer    (k,l,m)       dx model/table       dz model/table")
for i, row in enumerate(table):
    delta = slab.positions[i] - ideal[i]
    klm = tuple(map(int, row[:3]))
    print(f"{i:2} {slab.get_tags()[i]:5} {str(klm):>12}"
          f"    {delta[0]:7.3f}/{row[3]:7.3f}"
          f"    {delta[2]:7.3f}/{row[4]:7.3f}")

print("\nFigure 18 comparison (A):")
print("Atoms   Model    Paper")
for i, j, reference in [(0, 1, 2.23), (0, 2, 2.27), (1, 3, 2.27),
                         (2, 4, 2.34), (2, 5, 2.33)]:
    distance = slab.get_distance(i, j, mic=True)
    print(f"{i}-{j}     {distance:.5f}   {reference:.2f}")

dimer = slab.get_distance(0, 1, mic=True, vector=True)
buckling = np.degrees(np.arctan2(abs(dimer[2]), np.linalg.norm(dimer[:2])))
print(f"\nDimer buckling: {buckling:.2f} degrees (paper: 0)")

# Change PAIR or ANGLE above; the middle atom is the angle's vertex.
print(f"Distance {PAIR}: {slab.get_distance(*PAIR, mic=True):.5f} A")
print(f"Angle {ANGLE}: {slab.get_angle(*ANGLE, mic=True):.2f} degrees")

output = Path(__file__).resolve().parent / "output"
output.mkdir(exist_ok=True)
name = Path(__file__).stem
write(output / f"{name}.extxyz", slab)
write(output / f"{name}.traj", slab)

# Display x horizontally and z vertically, as in Figure 18.
if SHOW_GUI:
    view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)
