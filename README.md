# Reconstructed Semiconductor Surfaces

Atomic models of reconstructed Si and InAs surfaces, built from published structural data with the Atomic Simulation Environment (ASE). The models were made for my bachelor's thesis at Aalto University (2026) and are meant as starting geometries for DFT and machine-learning calculations.

## Models

| Surface | Reconstruction | Source | Folder |
| --- | --- | --- | --- |
| Si(100) | p(2x1)s, p(2x1)a, p(2x2), c(4x2) | Ramstad et al. (1995) | [Si100](Si100/README.md) |
| Si(111) | (2x1) modified Pandey chain | Xu et al. (2004) | [Si111](Si111/README.md) |
| InAs(001) | c(8x2) | Kumpf et al. (2001) | [InAs](InAs/README.md) |
| InAs(001) | zeta(4x2) | Miwa et al. (2003) | [InAs](InAs/README.md) |

Each folder has the generator scripts and an `output/` folder with the saved structures (`.extxyz`, `.traj`, and `.cif` for InAs). Every model is one surface cell with 10 Å vacuum on each side and a bare bottom.

## Install

```
python -m pip install -r requirements.txt
```

This is enough for building and checking the models. MACE is only needed for the relaxations, see [MACE](MACE/README.md).

## Build a model

```
python Si100/p2x1s.py
python Si111/si111_2x1.py
python InAs/kumpf_c8x2.py
python InAs/miwa_array.py
python InAs/miwa_zeta4x2.py
```

The settings are at the top of each script. `TOTAL_LAYERS` changes how many layers the slab has; the extra layers are ideal bulk added at the bottom. The ASE viewer opens after saving; set `SHOW_GUI = False` to only save the files.

## Check a model against the source

```
python Si100/validate_si100.py
python Si111/validate_si111.py
python InAs/validate_miwa.py
```

These print the bond lengths (and buckling angles for Si(100)) of the model next to the values in the paper.

## MACE relaxation

The `MACE/` folder has one `relax.py` per model. Each one relaxes the saved model with MACE-MH-0 and MACE-MH-1 and saves the result in its `output/` folder. See [MACE](MACE/README.md).

## References

- A. Ramstad, G. Brocks, and P. J. Kelly, Phys. Rev. B 51, 14504 (1995). https://doi.org/10.1103/PhysRevB.51.14504
- G. Xu et al., Phys. Rev. B 70, 045307 (2004). https://doi.org/10.1103/PhysRevB.70.045307
- C. Kumpf et al., Phys. Rev. B 64, 075307 (2001). https://doi.org/10.1103/PhysRevB.64.075307
- R. H. Miwa et al., Surf. Sci. 542, 101 (2003). https://doi.org/10.1016/S0039-6028(03)00955-5

## License

MIT, see [LICENSE](LICENSE).
