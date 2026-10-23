import argparse
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

DISPLAY_REPEAT = (3, 3, 1)
SHOW_GUI = True

table = np.array([
    [4.338, 1.920,  3.452],
    [5.443, 0.000,  2.954],
    [1.019, 0.000,  2.213],
    [2.430, 1.920,  2.145],
    [0.072, 0.000, -0.017],
    [3.269, 1.920, -0.073],
    [5.466, 1.920, -0.670],
    [2.256, 0.000, -0.997],
    [5.610, 1.920, -3.049],
    [2.213, 0.000, -3.258],
    [4.477, 0.000, -3.911],
    [1.100, 1.920, -3.971],
    [4.478, 0.000, -6.287],
    [1.127, 1.920, -6.324],
    [3.299, 1.920, -6.998],
    [0.014, 0.000, -7.058]
])


def build_slab():
    slab = Atoms(
        symbols=["Si"] * len(table),
        positions=table,
        cell=[6.65, 3.84, 0],
        pbc=[True, True, False]
    )
    slab.info["source_doi"] = "10.1103/PhysRevB.70.045307"
    slab.info["source_table"] = "Table II, rightmost column group"
    slab.info["source_columns"] = "MP structure with enhanced vibrations"
    slab.info["coordinate_units"] = "angstrom"
    slab.info["structure_origin"] = "Experimental LEED refinement using automated tensor LEED"
    slab.info["reconstruction"] = "Si(111)-(2x1), modified Pandey"
    slab.info["model"] = "Static 16-atom geometry from the enhanced-vibration fit"
    slab.info["atom_order"] = "Paper atoms 1-16 correspond to Python indices 0-15"
    slab.info["surface_normal"] = "+z outward"
    slab.info["vacuum_per_side_angstrom"] = 10.0
    slab.center(vacuum=10.0, axis=2)
    slab.info["z_translation_angstrom"] = float(slab.positions[0, 2] - table[0, 2])
    return slab


def main():
    parser = argparse.ArgumentParser(description="Build Xu et al.'s Si(111)-(2x1) MP structure.")
    parser.add_argument("--no-gui", action="store_true", help="Export without opening the ASE viewer.")
    args = parser.parse_args()
    slab = build_slab()

    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    name = Path(__file__).stem
    for extension in ("extxyz", "traj"):
        path = output / f"{name}.{extension}"
        write(path, slab)
        print(path)

    if SHOW_GUI and not args.no_gui:
        view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)


if __name__ == "__main__":
    main()
