from pathlib import Path

from ase.io import read, write
from ase.optimize import BFGS, FIRE
from mace.calculators import mace_mp

FMAX = 0.005
STEPS = 2000
OPTIMIZER = FIRE


def main():
    folder = Path(__file__).resolve().parent
    repository = folder.parent.parent
    output = folder / "output"
    output.mkdir(exist_ok=True)

    slab = read(repository / "Si100/output/p(2x1)s_fivelayers.traj")
    slab.center(vacuum=10.0, axis=2)
    slab.calc = mace_mp(
        model="medium-mpa-0",
        device="cuda",
        default_dtype="float64",
        dispersion=False,
    )

    with (output / "optimization.log").open("w") as log:
        optimizer = OPTIMIZER(slab, logfile=log)
        converged = optimizer.run(fmax=FMAX, steps=STEPS)

    write(output / "relaxed.cif", slab, wrap=False)
    write(output / "relaxed.traj", slab)
    force = (slab.get_forces() ** 2).sum(axis=1).max() ** 0.5
    print(f"Converged: {converged}, steps: {optimizer.nsteps}")
    print(f"Energy: {slab.get_potential_energy():.8f} eV, max force: {force:.6f} eV/angstrom")
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
