Run from the repository root. Install POV-Ray; the default Windows installation is detected automatically. 

```powershell
python -m pip install ase matplotlib pillow
```

All original models:
```powershell
python figures/render_figures.py --all --no-mace
```

Originals + MACE:
```powershell
python figures/render_figures.py --all --include-mace
```

MACE only:
```powershell
python figures/render_figures.py --mace-only
```

One group (`si100`, `si111`, `inas`):
```powershell
python figures/render_figures.py --group si100
python figures/render_figures.py --group inas --mace-only
```

PNG files: `figures/output/`.
