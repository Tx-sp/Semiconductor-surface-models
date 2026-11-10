# MACE relaxation

Each model folder has its own `relax.py` and `output/` folder:

- `Si100_p2x1s`
- `Si100_p2x1a`
- `Si100_p2x2`
- `Si100_c4x2`
- `Si111_2x1`

Edit `MODELS`, `HEAD`, `FMAX`, `STEPS`, or `OPTIMIZER` directly in the chosen script. Run it once, for example from the repository root:

```powershell
.venv/Scripts/python.exe MACE/Si100_p2x1a/relax.py
```

To hide the known checkpoint-loading and TorchScript warnings from MACE's dependencies:

```powershell
.venv/Scripts/python.exe -W 'ignore:Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD:UserWarning' -W 'ignore:`torch.jit:FutureWarning' MACE/Si100_p2x1a/relax.py
```

This only hides those warnings; it does not change the calculation. Normal startup messages still appear. Check the final `Converged:` line.

Each script reads its original slab, runs both MACE-MH-0 and MACE-MH-1 independently with the `omat_pbe` head, CUDA, float64, and FIRE. Set `MODELS = ("mh-1",)` to run only MH-1. The [MACE foundation releases](https://github.com/ACEsuit/mace-foundations/releases/tag/mace_mh_1) describe this head as suitable across materials and surfaces; accuracy for these specific Si slabs still needs reference validation. Change `OPTIMIZER = FIRE` to `OPTIMIZER = BFGS` to use BFGS instead. All atoms are free; cells stay fixed. (For now)..  Si(100) uses five layers with 10 Å vacuum per side; Si(111) keeps its existing vacuum.

The script saves `relaxed.cif`, `relaxed.traj`, and `optimization.log` inside its own `output/mh-0/` and `output/mh-1/` folders. Rerunning replaces the selected models' files. These replace the previous MPA-0 outputs. The trajectory metadata records the model, head, optimizer, convergence, step count, and force target. To open the result in ASE:

```powershell
.venv/Scripts/python.exe -m ase gui MACE/Si100_p2x1a/output/mh-1/relaxed.traj
```

To display a larger surface:

```powershell
python -m ase gui MACE/Si100_p2x1a/output/mh-1/relaxed.traj -r 3,3,1 -b
```
