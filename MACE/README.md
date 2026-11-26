# MACE relaxation

Each folder has a `relax.py` that relaxes one saved model:

- `Si100_p2x1s`, `Si100_p2x1a`, `Si100_p2x2`, `Si100_c4x2`
- `Si111_2x1`
- `InAs_Kumpf_c8x2`, `InAs_Miwa_4x2`

Install PyTorch with CUDA for your GPU from pytorch.org first, then `python -m pip install -r requirements-mace.txt`.

The script reads the `.traj` file of the model, so run the generator first if you change the model. It relaxes the slab with MACE-MH-0 and MACE-MH-1 on CUDA in float64. The atoms in the two deepest layers are fixed and the cell is fixed. The settings are at the top of each script:

- `MODELS`: which MACE models to run, `("mh-0", "mh-1")`
- `HEAD`: MACE head, `"omat_pbe"`
- `FMAX`: force target, 0.005 eV/Å
- `STEPS`: maximum optimizer steps, 2000
- `OPTIMIZER`: ASE optimizer, `FIRE`; `BFGS` also needs `from ase.optimize import BFGS`

```
python MACE/Si100_p2x1a/relax.py
python -m ase gui MACE/Si100_p2x1a/output/mh-1/relaxed.traj
```

Each run writes `relaxed.cif`, `relaxed.traj` and `optimization.log` to `output/mh-0/` and `output/mh-1/`, and replaces the earlier files. The trajectory info stores the model, head, optimizer, convergence, number of steps and force target.
