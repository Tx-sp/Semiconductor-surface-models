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
PAIR = (0, 1)
ANGLE = (1, 0, 4)

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
ideal = table[:, :3] * scale
positions = ideal.copy()
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

# Check the built coordinates against Table IV before any translation.
print("\nTable IV comparison (A):")
print("ID Layer    (k,l,m)       dx model/table       dy model/table       dz model/table")
for i, row in enumerate(table):
    delta = slab.positions[i] - ideal[i]
    klm = tuple(map(int, row[:3]))
    print(f"{i:2} {slab.get_tags()[i]:5} {str(klm):>12}"
          f"    {delta[0]:7.3f}/{row[3]:7.3f}"
          f"    {delta[1]:7.3f}/{row[4]:7.3f}"
          f"    {delta[2]:7.3f}/{row[5]:7.3f}")

print("\nFigure 18 comparison (A):")
print("Atoms   Model    Paper")
for i, j, reference in [(0, 1, 2.29), (2, 3, 2.29), (0, 4, 2.31), (1, 5, 2.35)]:
    distance = slab.get_distance(i, j, mic=True)
    print(f"{i}-{j}     {distance:.5f}   {reference:.2f}")

bucklings = []
for i, j in [(0, 1), (2, 3)]:
    dimer = slab.get_distance(i, j, mic=True, vector=True)
    buckling = np.degrees(np.arctan2(abs(dimer[2]), np.linalg.norm(dimer[:2])))
    bucklings.append(buckling)
    print(f"Dimer {i}-{j} buckling: {buckling:.2f} degrees")
print(f"Mean buckling: {np.mean(bucklings):.2f} degrees (paper: 18.8)")

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
