import argparse
from pathlib import Path

import numpy as np
from ase.io import read


REFERENCES = {
    "p(2x1)s": {
        "bonds": [(0, 1, 2.23), (0, 2, 2.27), (1, 3, 2.27),
                  (2, 4, 2.34), (2, 5, 2.33)],
        "dimers": [(0, 1)],
        "buckling": 0.0,
    },
    "p(2x1)a": {
        "bonds": [(0, 1, 2.26), (0, 2, 2.29), (1, 3, 2.34),
                  (2, 4, 2.38), (2, 5, 2.35)],
        "dimers": [(0, 1)],
        "buckling": 18.3,
    },
    "p(2x2)": {
        "bonds": [(0, 1, 2.28), (2, 3, 2.28), (0, 4, 2.31), (1, 5, 2.34)],
        "dimers": [(0, 1), (2, 3)],
        "buckling": 19.1,
    },
    "c(4x2)": {
        "bonds": [(0, 1, 2.29), (2, 3, 2.29), (0, 4, 2.31), (1, 5, 2.35)],
        "dimers": [(0, 1), (2, 3)],
        "buckling": 18.8,
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Compare generated Si100 structures with Ramstad et al. (1995)."
    )
    parser.add_argument(
        "files", nargs="*", type=Path,
        help="Structure files (.extxyz or .traj); defaults to all eight generated .extxyz files.",
    )
    args = parser.parse_args()
    output = Path(__file__).resolve().parent / "output"
    files = args.files or [
        output / f"{reconstruction}_{variant}.extxyz"
        for reconstruction in REFERENCES
        for variant in ("fivelayers", "surfacewithbulk")
    ]

    print("Ramstad, Brocks and Kelly (1995), Figure 18; DOI: 10.1103/PhysRevB.51.14504")
    print("p(2x2) and c(4x2) paper buckling values refer to the mean of two dimers.")
    print("The symmetric p(2x1)s reference is zero buckling by symmetry. Atom indices are zero-based.")

    failed = False
    for path in files:
        print(f"\n{path}")
        if not path.is_file():
            print(f"MISSING: {path}; run the corresponding generator first.")
            failed = True
            continue
        try:
            slab = read(path)
            reconstruction = slab.info.get("reconstruction")
            if reconstruction not in REFERENCES:
                raise ValueError(f"Unsupported or missing reconstruction metadata: {reconstruction!r}")
            references = REFERENCES[reconstruction]
            print(f"Reconstruction: {reconstruction}")
            print("Bond (angstrom)    Model    Paper    Difference")
            for i, j, reference in references["bonds"]:
                distance = slab.get_distance(i, j, mic=True)
                print(f"{i}-{j:<13} {distance:8.5f}  {reference:5.2f}  {distance - reference:+.5f}")

            bucklings = []
            for i, j in references["dimers"]:
                dimer = slab.get_distance(i, j, mic=True, vector=True)
                buckling = np.degrees(np.arctan2(abs(dimer[2]), np.linalg.norm(dimer[:2])))
                bucklings.append(buckling)
                print(f"Dimer {i}-{j} buckling: {buckling:.5f} degrees")
            mean = np.mean(bucklings)
            reference = references["buckling"]
            print("Buckling (degrees)   Model    Paper    Difference")
            print(f"Mean              {mean:8.5f}  {reference:5.1f}  {mean - reference:+.5f}")
        except (OSError, ValueError, IndexError) as error:
            print(f"ERROR: {path}: {error}")
            failed = True

    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
