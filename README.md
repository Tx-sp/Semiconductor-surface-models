# Reconstructed Semiconductor Surfaces

Bachelor's thesis project constructing atomic models of silicon and InAs surface reconstructions from published structural information using the Atomic Simulation Environment (ASE).

## Models

| Surface | Reconstructions | Structural source | Documentation |
| --- | --- | --- | --- |
| Si(100) | p(2x1) symmetric, p(2x1) asymmetric, p(2x2), c(4x2) | Ramstad et al. (1995), theoretical displacements | [Si100](Si100/README.md) |
| Si(111) | (2x1) modified Pandey, enhanced-vibration fit | Xu et al. (2004), experimental LEED refinement | [Si111](Si111/README.md) |
| InAs(001) | c(8x2) | Kumpf et al. (2001), Table I | [InAs](InAs/README.md) |
| InAs(001) | zeta(4x2), original and 30-atom Figure 3 completion | Miwa et al. (2003), Table 1 and Figure 3 | [InAs](InAs/README.md) |

Each surface folder contains modelling scripts and an `output/` directory. Si folders also include geometry-validation scripts. See the linked READMEs for details.

## Getting started

Run commands from the repository root with Python and the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Generate an Si(100) model and compare its geometry with the paper:

```powershell
python "Si100/p(2x1)s.py"
python Si100/validate_si100.py "Si100/output/p(2x1)s.extxyz"
```

Si(100) generators open the ASE viewer by default. Set `SHOW_GUI = False` in the generator to disable it.

Generate and validate Si(111) without opening the viewer:

```powershell
python "Si111/(2x1)mp_enhanced_vibrations.py" --no-gui
python Si111/validate_si111.py
```

Generate the Miwa Figure 3 array, then export and view the InAs model:

```powershell
python InAs/generate_fullmiwa_array.py
python "InAs/miwa_full.py"
```

The generator uses mirroring, In partners and eight inferred lower As atoms; the modelling script reads `miwa_array.npz`. 

## Outputs and scope

Generators export the fundamental cell as `.extxyz` and `.traj` files in their surface folder's `output/` directory. InAs models also export `.cif` files.

The structure generators create static geometry models reconstructed from published data. Bottom surfaces are unpassivated. Si(100) bulk variants add ideal layers; Si(111) contains only the 16 tabulated atoms. The Miwa Figure 3 model contains 30 atoms. See each model README for cell and vacuum conventions.

## MACE relaxation

[MACE](MACE/README.md) contains a simple relaxation script for each of the four five-layer Si(100) models and the Si(111) slab. Each script runs MACE-MH-0 and MACE-MH-1 with the `omat_pbe` head, CUDA, float64 and FIRE (BFGS available). All atoms are free; cells stay fixed. Results are saved as CIF, ASE trajectory and optimization log in `output/mh-0/` and `output/mh-1/`. MACE runs require a CUDA-enabled PyTorch and MACE installation in addition to the geometry dependencies.

## References

- A. Ramstad, G. Brocks, and P. J. Kelly, "Theoretical study of the Si(100) surface reconstruction," *Physical Review B* **51**, 14504-14523 (1995). [DOI: 10.1103/PhysRevB.51.14504](https://doi.org/10.1103/PhysRevB.51.14504)
- G. Xu et al., "Atomic structure of the cleaved Si(111)-(2x1) surface refined by dynamical LEED," *Physical Review B* **70**, 045307 (2004). [DOI: 10.1103/PhysRevB.70.045307](https://doi.org/10.1103/PhysRevB.70.045307)
- C. Kumpf et al., *Physical Review B* **64**, 075307 (2001). [DOI: 10.1103/PhysRevB.64.075307](https://doi.org/10.1103/PhysRevB.64.075307)
- R. H. Miwa et al., *Surface Science* **542**, 101-111 (2003). [DOI: 10.1016/S0039-6028(03)00955-5](https://doi.org/10.1016/S0039-6028(03)00955-5)
