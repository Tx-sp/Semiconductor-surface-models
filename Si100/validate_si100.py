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
    parser = argparse.ArgumentParser(description="Compare Si100 geometry with Ramstad et al., Figure 18.")
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()
    output = Path(__file__).resolve().parent / "output"
    files = args.files or [output / f"{name}.extxyz" for name in REFERENCES]
    for path in files:
        slab = read(path)
        references = REFERENCES[path.stem]
        print(f"\n{path.name}")
        print("Bond (0-based)    Model    Figure 18    Difference (angstrom)")
        for i, j, reference in references["bonds"]:
            distance = slab.get_distance(i, j, mic=True)
            print(f"{i}-{j:<12} {distance:8.3f} {reference:12.3f} {distance - reference:+13.3f}")
        bucklings = []
        for i, j in references["dimers"]:
            dimer = slab.get_distance(i, j, mic=True, vector=True)
            bucklings.append(np.degrees(np.arctan2(abs(dimer[2]), np.linalg.norm(dimer[:2]))))
        mean = np.mean(bucklings)
        reference = references["buckling"]
        print("Buckling (deg)    Model    Figure 18    Difference")
        print(f"Mean           {mean:8.3f} {reference:12.3f} {mean - reference:+13.3f}")


if __name__ == "__main__":
    main()
