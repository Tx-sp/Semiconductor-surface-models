# Si(100)

Source: A. Ramstad, G. Brocks, and P. J. Kelly, Phys. Rev. B 51, 14504 (1995). https://doi.org/10.1103/PhysRevB.51.14504

| Script | Reconstruction | Data | Atoms (7 layers) |
| --- | --- | --- | ---: |
| `p2x1s.py` | p(2x1), symmetric dimers | Table III | 14 |
| `p2x1a.py` | p(2x1), asymmetric dimers | Table III | 14 |
| `p2x2.py` | p(2x2), alternating buckled dimers | Table IV | 28 |
| `c4x2.py` | c(4x2), alternating buckled dimers | Table IV | 28 |

Each atom is put on its ideal site `(k*sqrt(2), l*sqrt(2), m) * A0/4` and the tabulated displacement (in Å) is added. The tables cover the top five layers; any layers below these are ideal bulk. The p(2x1) and p(2x2) cells are rectangular, and the c(4x2) model uses the skewed primitive cell. Atom tags give the layer number, counted from the top.

Settings: `TOTAL_LAYERS = 7` (at least 5) and `A0 = 5.431` Å, the experimental Si lattice constant.

```
python Si100/p2x1s.py
python Si100/validate_si100.py
```

Each generator saves `Si100/output/<script name>.extxyz` and `.traj`. The validator reads all four models (or the files given as arguments) and prints the bond lengths and mean dimer buckling angle next to Fig. 18 of the paper.
