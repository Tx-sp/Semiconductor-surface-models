# Reconstructed Semiconductor Surfaces

Bachelor's thesis project constructing atomic models of silicon surface reconstructions from published structural information using the Atomic Simulation Environment (ASE).

## Models

| Surface | Reconstructions | Structural source | Documentation |
| --- | --- | --- | --- |
| Si(100) | p(2x1) symmetric, p(2x1) asymmetric, p(2x2), c(4x2) | Ramstad et al. (1995), theoretical displacements | [Si100](Si100/README.md) |
| Si(111) | (2x1) modified Pandey, enhanced-vibration fit | Xu et al. (2004), experimental LEED refinement | [Si111](Si111/README.md) |

Each surface folder contains generators, a separate geometry-validation script, and an `output/` directory for generated structures. The linked READMEs describe source tables, coordinate conventions, assumptions, and validation.

## Getting started

Run commands from the repository root with Python and the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Generate an Si(100) model and compare its geometry with the paper:

```powershell
python "Si100/p(2x1)s_fivelayers.py"
python Si100/validate_si100.py "Si100/output/p(2x1)s_fivelayers.extxyz"
```

Si(100) generators open the ASE viewer by default. Set `SHOW_GUI = False` in the generator to disable it.

Generate and validate Si(111) without opening the viewer:

```powershell
python "Si111/(2x1)mp_enhanced_vibrations.py" --no-gui
python Si111/validate_si111.py
```

## Outputs and scope

Generators export the fundamental cell as `.extxyz` and `.traj` files in their surface folder's `output/` directory. Both formats preserve cell and periodic boundary information. `DISPLAY_REPEAT` controls only visualization; repeated display cells are not exported.

The structure generators create static geometry models reconstructed from published data. Bottom surfaces are unpassivated. Si(100) bulk variants add ideal layers; Si(111) contains only the 16 tabulated atoms. See each model README for cell and vacuum conventions.

## MACE relaxation

[MACE](MACE/README.md) contains a simple relaxation script for each of the four five-layer Si(100) models and the Si(111) slab. The scripts use ASE and MACE-MPA-0 on CUDA to relax atomic positions with fixed cells. Each model's `output/` folder contains the relaxed CIF, ASE trajectory, and optimization log.

## References

- A. Ramstad, G. Brocks, and P. J. Kelly, "Theoretical study of the Si(100) surface reconstruction," *Physical Review B* **51**, 14504-14523 (1995). [DOI: 10.1103/PhysRevB.51.14504](https://doi.org/10.1103/PhysRevB.51.14504)
- G. Xu et al., "Atomic structure of the cleaved Si(111)-(2x1) surface refined by dynamical LEED," *Physical Review B* **70**, 045307 (2004). [DOI: 10.1103/PhysRevB.70.045307](https://doi.org/10.1103/PhysRevB.70.045307)
