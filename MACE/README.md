# MACE relaxation

Each model folder has its own `relax.py` and `output/` folder:

- `Si100_p2x1s`
- `Si100_p2x1a`
- `Si100_p2x2`
- `Si100_c4x2`
- `Si111_2x1`

Edit `FMAX`, `STEPS`, or `OPTIMIZER` directly in the chosen script. Run it once, for example from the repository root:

```powershell
.venv312/Scripts/python.exe MACE/Si100_p2x1a/relax.py
```

To hide the known checkpoint-loading and TorchScript warnings from MACE's dependencies:

```powershell
.venv312/Scripts/python.exe -W 'ignore:Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD:UserWarning' -W 'ignore:`torch.jit:FutureWarning' MACE/Si100_p2x1a/relax.py
```

This only hides those warnings; it does not change the calculation. Normal startup messages still appear. Check the final `Converged:` line.

Each script reads its original slab, uses CUDA MACE-MPA-0 in float64, and runs FIRE. Change `OPTIMIZER = FIRE` to `OPTIMIZER = BFGS` to use BFGS instead. All atoms are free; cells stay fixed. (For now)..  Si(100) uses five layers with 10 Å vacuum per side; Si(111) keeps its existing vacuum.

The script saves `relaxed.cif`, `relaxed.traj`, and `optimization.log` inside its own `output/`. Rerunning replaces those files. To open the result in ASE:

```powershell
.venv312/Scripts/python.exe -m ase gui MACE/Si100_p2x1a/output/relaxed.traj
```

With `.venv312` activated, display a larger surface:

```powershell
python -m ase gui MACE/Si100_p2x1a/output/relaxed.traj -r 3,3,1 -b
```

Use `.venv312` for Python 3.12 compatibility. Select `.venv312/Scripts/python.exe` as the Python interpreter.
