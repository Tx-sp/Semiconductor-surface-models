from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

A0 = 6.0583
VACUUM = 10.0
TOTAL_LAYERS = 7
DISPLAY_REPEAT = (2, 2, 1)
EXPORT_REPEAT = (2, 2, 1)
SHOW_GUI = True

symbols = [
    "In", "In", "In", "In", "In", "As", "As", "As",
    "In", "In", "As", "As", "As",
    "In", "In", "In", "In", "In",
    "As", "As", "As", "As", "In", "In", "As", "As", "As",
    "In", "In", "In", "In", "In", "As", "As", "As", "As"
]
table = np.array([
    [2.000, 0.500, 0.004],
    [0.000, 1.000, -0.251],
    [0.000, 0.000, -0.101],
    [0.902, 0.000, -0.166],
    [0.923, 1.000, -0.108],
    [0.563, 0.482, -0.089],
    [1.529, 0.000, -0.238],
    [1.474, 1.000, -0.251],
    [0.519, 0.334, -0.511],
    [1.498, 0.489, -0.502],
    [0.000, 0.500, -0.733],
    [1.001, 0.500, -0.757],
    [2.000, 0.500, -0.751],
    [0.000, 0.000, -0.970],
    [1.002, 0.000, -1.011],
    [1.995, 1.000, -1.000],
    [1.012, 1.000, -0.991],
    [0.000, 1.000, -0.992],
    [0.515, 0.000, -1.248],
    [1.503, 0.000, -1.234],
    [1.505, 1.000, -1.270],
    [0.474, 1.000, -1.245],
    [0.495, 0.516, -1.493],
    [1.503, 0.465, -1.502],
    [2.000, 0.500, -1.754],
    [0.997, 0.482, -1.747],
    [0.000, 0.500, -1.750],
    [2.000, 0.000, -2.004],
    [0.994, 1.000, -2.004],
    [1.000, 0.000, -1.991],
    [0.000, 1.000, -1.998],
    [0.000, 0.000, -1.998],
    [1.500, 1.000, -2.250],
    [1.500, 0.000, -2.250],
    [0.500, 1.000, -2.250],
    [0.500, 0.000, -2.250]
])


def build_slab():
    if type(TOTAL_LAYERS) is not int or not 1 <= TOTAL_LAYERS <= 9:
        raise ValueError("TOTAL_LAYERS must be an integer from 1 to 9.")
    layer_last_tags = (8, 10, 13, 18, 22, 24, 27, 32, 36)
    scale = A0 * np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 1])
    positions, elements, tags = [], [], []
    for row, (symbol, xyz) in enumerate(zip(symbols, table), start=1):
        seen = set()
        for shift in ([0, 0, 0], [4, 1, 0]):
            for signs in ([1, 1, 1], [-1, 1, 1], [1, -1, 1], [-1, -1, 1]):
                point = xyz * signs + shift
                point[:2] %= [8, 2]
                key = tuple(np.round(point, 12))
                if key not in seen:
                    seen.add(key)
                    positions.append(point * scale)
                    elements.append(symbol)
                    tags.append(row)

    slab = Atoms(elements, positions=positions,
                 cell=[8 * scale[0], 2 * scale[1], 0],
                 pbc=[True, True, False], tags=tags)
    slab = slab[slab.get_tags() <= layer_last_tags[TOTAL_LAYERS - 1]]
    slab.center(vacuum=VACUUM, axis=2)
    slab.info["source_doi"] = "10.1103/PhysRevB.64.075307"
    slab.info["source_table"] = "Table I, InAs column, including all unnumbered rows"
    slab.info["reconstruction"] = "InAs(001)-c(8x2), conventional centered rectangular cell"
    slab.info["model"] = "Table II integer occupancy: In1/In2/In3 full; In2d absent; bare bottom"
    slab.info["lattice_constant_angstrom"] = A0
    slab.info["vacuum_per_side_angstrom"] = VACUUM
    return slab


def main():
    slab = build_slab()
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    name = "c(8x2)_tableI"
    export_slab = slab.repeat(EXPORT_REPEAT)
    for extension in ("extxyz", "traj", "cif"):
        write(output / f"{name}.{extension}", export_slab)
    if SHOW_GUI:
        view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)


if __name__ == "__main__":
    main()
