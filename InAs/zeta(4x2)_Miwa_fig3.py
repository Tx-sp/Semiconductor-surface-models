from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import write
from ase.visualize import view

A0 = 5.96
VACUUM = 10.0
DISPLAY_REPEAT = (4, 2, 1)
EXPORT_REPEAT = (4, 2, 1)
SHOW_GUI = True


def build_slab():
    array_path = Path(__file__).with_name("miwa_array.npz")
    if not array_path.is_file():
        raise SystemExit("Run generate_fullmiwa_array.py first to create miwa_array.npz.")
    with np.load(array_path, allow_pickle=False) as data:
        slab = Atoms(data["symbols"].tolist(), positions=data["positions"],
                     cell=data["cell"], pbc=[True, True, False], tags=data["tags"])
    slab.wrap()
    slab.center(vacuum=VACUUM, axis=2)
    slab.info["source_doi"] = "10.1016/S0039-6028(03)00955-5"
    slab.info["source_table"] = "Table 1, all 11 printed Cartesian coordinates in angstroms"
    slab.info["reconstruction"] = "InAs(001)-zeta(4x2), Figures 1(d) and 3"
    slab.info["model"] = "Figure 3 reconstruction including eight inferred lower As sites; no deeper bulk"
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
