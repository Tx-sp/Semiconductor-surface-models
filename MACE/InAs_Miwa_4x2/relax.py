from pathlib import Path

from ase.constraints import FixAtoms
from ase.io import read, write
from ase.optimize import FIRE
from mace.calculators import mace_mp

MODELS = ("mh-0", "mh-1")   # which MACE models to run
HEAD = "omat_pbe"           # MACE head used for all runs
FMAX = 0.005                # stop when the largest force is below this (eV/Å)
STEPS = 2000                # max optimizer steps
OPTIMIZER = FIRE            # ASE optimizer class


def main(model):
    folder = Path(__file__).resolve().parent
    repository = folder.parent.parent
    output = folder / "output" / model
    output.mkdir(parents=True, exist_ok=True)

    slab = read(repository / "InAs/output/miwa_zeta4x2.traj")
    # Fix the two deepest layers
    slab.set_constraint(FixAtoms(mask=slab.get_tags() > slab.get_tags().max() - 2))
    slab.calc = mace_mp(
        model=model,
        head=HEAD,
        device="cuda",
        default_dtype="float64",
        dispersion=False,
    )

    with (output / "optimization.log").open("w") as log:
        optimizer = OPTIMIZER(slab, logfile=log,
                              trajectory=str(output / "optimization.traj"))
        converged = optimizer.run(fmax=FMAX, steps=STEPS)

    slab.info.update(mace_model=model, mace_head=HEAD,
                     optimizer=OPTIMIZER.__name__, converged=bool(converged),
                     optimization_steps=optimizer.nsteps, fmax_target=FMAX)
    force = (slab.get_forces() ** 2).sum(axis=1).max() ** 0.5
    write(output / "relaxed.cif", slab, wrap=False)
    write(output / "relaxed.traj", slab)
    print(f"Model: {model}, head: {HEAD}")
    print(f"Converged: {converged}, steps: {optimizer.nsteps}")
    print(f"Energy: {slab.get_potential_energy():.8f} eV, max force: {force:.6f} eV/angstrom")
    print(f"Output: {output}")


if __name__ == "__main__":
    for model in MODELS:
        main(model)
