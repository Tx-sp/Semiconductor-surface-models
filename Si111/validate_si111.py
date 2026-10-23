import argparse
from importlib import import_module
from pathlib import Path

import numpy as np
from ase.io import read

table = import_module("(2x1)mp_enhanced_vibrations").table

REFERENCES = [(1, 2, 2.271), (1, 4, 2.313), (2, 3, 2.347)]
TOLERANCE = 0.005


def validate(slab):
    if len(slab) != 16 or slab.get_chemical_symbols() != ["Si"] * 16:
        raise ValueError("Expected exactly 16 silicon atoms")
    np.testing.assert_array_equal(slab.pbc, [True, True, False])
    np.testing.assert_allclose(slab.cell.array, np.diag([6.65, 3.84, 30.510]), atol=1e-8, rtol=0)
    np.testing.assert_allclose(slab.positions[:, :2], table[:, :2], atol=1e-8, rtol=0)
    np.testing.assert_allclose(
        slab.positions[:, 2] - table[:, 2], 17.058, atol=1e-8, rtol=0
    )
    np.testing.assert_allclose(
        [slab.positions[:, 2].min(), slab.cell[2, 2] - slab.positions[:, 2].max()],
        [10.0, 10.0], atol=1e-8, rtol=0
    )
    if slab.constraints or slab.calc is not None or slab.has("momenta"):
        raise ValueError("Expected static geometry without constraints, calculator, or momenta")
    expected_metadata = {
        "source_doi": "10.1103/PhysRevB.70.045307",
        "source_table": "Table II, rightmost column group",
        "source_columns": "MP structure with enhanced vibrations",
        "coordinate_units": "angstrom",
        "structure_origin": "Experimental LEED refinement using automated tensor LEED",
    }
    for key, value in expected_metadata.items():
        if slab.info.get(key) != value:
            raise ValueError(f"Incorrect or missing metadata: {key}")
    height = slab.positions[1 - 1, 2] - slab.positions[2 - 1, 2]
    np.testing.assert_allclose(height, 0.498, atol=1e-8, rtol=0)
    print("16 Si atoms; cell 6.65 x 3.84 x 30.510 angstrom; PBC (True, True, False)")
    print("Atom order and relative positions preserved; 10 angstrom vacuum on each side")
    print(f"Paper atoms 1-2 height difference: {height:.6f} angstrom")
    print("Paper pair  Python indices  Model       Table III   Difference (angstrom)")
    for atom_a, atom_b, reference in REFERENCES:
        i, j = atom_a - 1, atom_b - 1
        distance = slab.get_distance(i, j, mic=True)
        print(f"{atom_a}-{atom_b:<9} {i}-{j:<13} {distance:.6f}    {reference:.3f}       {distance - reference:+.6f}")
        if abs(distance - reference) > TOLERANCE:
            raise ValueError(f"Paper pair {atom_a}-{atom_b} exceeds {TOLERANCE} angstrom tolerance")


def main():
    parser = argparse.ArgumentParser(description="Validate Si111 exports against Xu et al., Tables II and III.")
    parser.add_argument("files", nargs="*", type=Path, help="Defaults to both fundamental-cell exports.")
    args = parser.parse_args()
    output = Path(__file__).resolve().parent / "output"
    files = args.files or [output / f"(2x1)mp_enhanced_vibrations.{ext}" for ext in ("extxyz", "traj")]
    failed = False
    for path in files:
        print(f"\n{path}")
        try:
            validate(read(path))
            print("PASS")
        except (OSError, ValueError, AssertionError) as error:
            print(f"FAIL: {error}")
            failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
