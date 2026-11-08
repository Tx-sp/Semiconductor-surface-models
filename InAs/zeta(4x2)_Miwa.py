from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

A0 = 5.96
VACUUM = 10.0
DISPLAY_REPEAT = (1, 1, 1)
SHOW_GUI = True

symbols = ["As", "As", "In", "In", "In", "In", "As", "As", "In", "In", "In"]
table = np.array([
    [0.00, 0.00, 0.00],
    [4.21, 0.04, 0.05],
    [-2.12, -0.01, -1.51],
    [2.12, -0.01, -1.51],
    [-0.00, 2.49, 0.19],
    [4.21, 2.53, 0.38],
    [-2.05, 3.97, 0.76],
    [2.051, 3.97, 0.76],
    [2.84, 3.99, -1.89],
    [-1.33, 6.26, -0.27],
    [1.33, 6.26, -0.28]
])


def build_slab():
    spacing = A0 / np.sqrt(2)
    positions = list(table.copy())
    elements = list(symbols)
    tags = list(range(1, len(table) + 1))
    for row in range(9):
        point = table[row].copy()
        point[1] = 2 * table[9, 1] - point[1]
        positions.append(point)
        elements.append(symbols[row])
        tags.append(row + 1)

    partner = table[8].copy()
    partner[0] += 2.76
    positions.append(partner.copy())
    partner[1] = 2 * table[9, 1] - partner[1]
    positions.append(partner)
    elements.extend(["In", "In"])
    tags.extend([9, 9])

    slab = Atoms(elements, positions=positions,
                 cell=[2 * spacing, 4 * spacing, 0],
                 pbc=[True, True, False], tags=tags)
    slab.wrap()
    slab.center(vacuum=VACUUM, axis=2)
    slab.info["source_doi"] = "10.1016/S0039-6028(03)00955-5"
    slab.info["source_table"] = "Table 1, all 11 printed Cartesian coordinates in angstroms"
    slab.info["reconstruction"] = "InAs(001)-zeta(4x2), Figures 1(d) and 3"
    slab.info["model"] = "Reconstruction only; Figure 3 inferred counterparts; no bulk layers"
    slab.info["lattice_constant_angstrom"] = A0
    slab.info["vacuum_per_side_angstrom"] = VACUUM
    return slab


def main():
    slab = build_slab()
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    name = Path(__file__).stem
    for extension in ("extxyz", "traj", "cif"):
        write(output / f"{name}.{extension}", slab)
    if SHOW_GUI:
        view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)


if __name__ == "__main__":
    main()
