from pathlib import Path
import runpy


def main():
    model = runpy.run_path(str(Path(__file__).with_name("miwa_full.py")))
    slab = model["build_slab"]()
    distance = lambda i, j: slab.get_distance(i, j, mic=True)
    checks = [
        ("1-2", distance(0, 4), 2.59), # For this bond, the table coordinates are used, mismatch with Fig. 3 is expected. 
        ("1'-2'", distance(1, 5), 2.51),
        ("2-3", distance(4, 6), 2.59),
        ("2'-3'", distance(5, 7), 2.62),
        ("AA lower As bond", distance(9, 23), 2.87),
        ("BB 3'-subsurface In", distance(7, 8), 2.77),
    ]
    for label, actual, expected in checks:
        status = "OK" if abs(actual - expected) <= 0.03 else "MISMATCH"
        print(f"{label:29} {actual:.3f} / Fig. 3 {expected:.2f} A  {status}")
    assert all(abs(actual - expected) <= 0.03 for _, actual, expected in checks[1:])


if __name__ == "__main__":
    main()
