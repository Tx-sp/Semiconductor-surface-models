from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

TOTAL_LAYERS = 10           # total layers; extra ones are ideal bulk added below the 8 tabulated ones (min 8)
DISPLAY_REPEAT = (3, 3, 1)  # only for the viewer, the saved file is one cell
SHOW_GUI = True             # set False to only save the files

# Table II of Xu et al. (2004), MP structure with enhanced vibrations: atoms 1-16, x, y, z in Å
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

# Ideal bulk positions of atoms 9-16 from Table II, used to add the extra layers
ideal = np.array([
    [5.542, 1.920, -3.135],
    [2.217, 0.000, -3.135],
    [4.434, 0.000, -3.919],
    [1.108, 1.920, -3.919],
    [4.434, 0.000, -6.270],
    [1.108, 1.920, -6.270],
    [3.325, 1.920, -7.054],
    [0.000, 0.000, -7.054],
])


def build_slab():
    if TOTAL_LAYERS < 8:
        raise ValueError("TOTAL_LAYERS must be at least 8")
    positions = table.copy()
    t = ideal[4] - ideal[0]
    layers = list(ideal.reshape(4, 2, 3))
    for layer in range(8, TOTAL_LAYERS):
        lower = layers[layer - 6] + t
        lower[:, :2] %= [6.65, 3.84]
        layers.append(lower)
        positions = np.vstack([positions, lower])
    slab = Atoms(
        symbols=["Si"] * len(positions),
        positions=positions,
        cell=[6.65, 3.84, 0],
        pbc=[True, True, False],
        tags=np.repeat(np.arange(1, TOTAL_LAYERS + 1), 2)
    )
    slab.info["source_doi"] = "10.1103/PhysRevB.70.045307"
    slab.info["source_table"] = "Table II, rightmost column group"
    slab.info["source_columns"] = "MP structure with enhanced vibrations"
    slab.info["coordinate_units"] = "angstrom"
    slab.info["structure_origin"] = "Experimental LEED refinement using automated tensor LEED"
    slab.info["reconstruction"] = "Si(111)-(2x1), modified Pandey"
    slab.info["model"] = f"16 tabulated atoms (8 layers) + {TOTAL_LAYERS - 8} ideal layers below; bare bottom"
    slab.info["total_layers"] = TOTAL_LAYERS
    slab.info["atom_order"] = "Paper atoms 1-16 correspond to Python indices 0-15"
    slab.info["surface_normal"] = "+z outward"
    slab.info["vacuum_per_side_angstrom"] = 10.0
    slab.center(vacuum=10.0, axis=2)
    slab.info["z_translation_angstrom"] = float(slab.positions[0, 2] - table[0, 2])
    return slab


def main():
    slab = build_slab()

    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    name = Path(__file__).stem
    for extension in ("extxyz", "traj"):
        path = output / f"{name}.{extension}"
        write(path, slab)
        print(path)

    if SHOW_GUI:
        view(slab.repeat(DISPLAY_REPEAT), rotations="-90x", show_bonds=True)


if __name__ == "__main__":
    main()
