import argparse
from pathlib import Path

from ase.io import read

REFERENCES = [(1, 2, 2.271), (1, 4, 2.313), (2, 3, 2.347)]


def main():
    parser = argparse.ArgumentParser(description="Compare Si111 bonds with Xu et al., Table III.")
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()
    output = Path(__file__).resolve().parent / "output"
    files = args.files or [output / f"(2x1)mp_enhanced_vibrations.{ext}" for ext in ("extxyz", "traj")]
    for path in files:
        slab = read(path)
        print(f"\n{path.name}")
        print("Paper atoms    Model    Table III    Difference (angstrom)")
        for i, j, reference in REFERENCES:
            distance = slab.get_distance(i - 1, j - 1, mic=True)
            print(f"{i}-{j:<10} {distance:8.3f} {reference:12.3f} {distance - reference:+13.3f}")


if __name__ == "__main__":
    main()
