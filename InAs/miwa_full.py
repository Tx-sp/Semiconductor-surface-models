from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

A0 = 5.96
VACUUM = 10.0
TOTAL_LAYERS = 7
DISPLAY_REPEAT = (2, 1, 1)
EXPORT_REPEAT = (2, 1, 1)
SHOW_GUI = True


def build_slab():
    array_path = Path(__file__).with_name("miwa_array.npz")
    with np.load(array_path, allow_pickle=False) as data:
        slab = Atoms(data["symbols"].tolist(), positions=data["positions"],
                     cell=data["cell"], pbc=[True, True, False], tags=data["tags"])
    slab.wrap()

    # Bulk layers here
    extra_bulk_layers = TOTAL_LAYERS - 3
    spacing = A0 / np.sqrt(2)
    as_indices = np.flatnonzero(slab.numbers == 33)
    lowest = as_indices[np.argsort(slab.positions[as_indices, 2])[:8]]
    reference = slab.positions[lowest]
    sites = np.rint((reference[:, :2] - reference[0, :2]) / spacing)
    origin = (reference[:, :2] - sites * spacing).mean(axis=0)
    reference_xy = origin + sites * spacing
    reference_z = reference[:, 2].mean()
    offsets = np.array([(0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)])
    last_tag = slab.get_tags().max()

    for layer in range(1, extra_bulk_layers + 1):
        xy = (reference_xy + spacing * offsets[layer % 4]) % slab.cell.lengths()[:2]
        z = np.full(8, reference_z - layer * A0 / 4)
        symbol = "In" if layer % 2 else "As"
        slab.extend(Atoms([symbol] * 8, positions=np.column_stack((xy, z)),
                          tags=[last_tag + layer] * 8))

    slab.center(vacuum=VACUUM, axis=2)
    slab.info["source_doi"] = "10.1016/S0039-6028(03)00955-5"
    slab.info["source_table"] = "Table 1, all 11 printed Cartesian coordinates in angstroms"
    slab.info["reconstruction"] = "InAs(001)-zeta(4x2), Figures 1(d) and 3"
    slab.info["model"] = "Figure 3 reconstruction with eight inferred lower As sites and ideal zinc-blende bulk planes"
    slab.info["total_layers"] = TOTAL_LAYERS
    slab.info["extra_bulk_layers"] = extra_bulk_layers
    slab.info["lattice_constant_angstrom"] = A0
    slab.info["vacuum_per_side_angstrom"] = VACUUM
    return slab


def main():
    slab = build_slab()
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    name = Path(__file__).stem
    export_slab = slab.repeat(EXPORT_REPEAT)
    for extension in ("extxyz", "traj", "cif"):
        write(output / f"{name}.{extension}", export_slab)
    if SHOW_GUI:
        view(slab.repeat(DISPLAY_REPEAT), rotations="-90z", show_bonds=True)


if __name__ == "__main__":
    main()
