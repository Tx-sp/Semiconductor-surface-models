# Si(100) reconstructions

[Back to project overview](../README.md)

## Source

A. Ramstad, G. Brocks, and P. J. Kelly, "Theoretical study of the Si(100) surface reconstruction," *Physical Review B* **51**, 14504-14523 (1995). [DOI: 10.1103/PhysRevB.51.14504](https://doi.org/10.1103/PhysRevB.51.14504)

The structures come from theoretical geometry optimization within the local-density approximation, using norm-conserving pseudopotentials and a plane-wave basis. Tables III and IV report displacements from ideal atomic positions; Figure 18 gives reference bond lengths and dimer buckling angles. These scripts reconstruct the reported geometries without running the paper's electronic-structure calculations.

## Models and coordinates

| Filename prefix | Reconstruction | Source table | Atoms in five-layer cell | Atoms in default twelve-layer cell |
| --- | --- | --- | ---: | ---: |
| `p(2x1)s` | Symmetric dimers | III | 10 | 24 |
| `p(2x1)a` | Asymmetric dimers | III | 10 | 24 |
| `p(2x2)` | Alternating buckled dimers | IV | 20 | 48 |
| `c(4x2)` | Alternating buckled dimers | IV | 20 | 48 |

Each reconstruction has two generators: `_fivelayers.py` contains five reconstructed atomic layers, and `_surfacewithbulk.py` adds ideal silicon layers underneath, giving twelve layers by default. `TOTAL_LAYERS` controls the layer count and must be at least five.

Ideal Cartesian positions are constructed as `(k * sqrt(2), l * sqrt(2), m) * A0 / 4`, with `A0 = 5.431` angstroms. The tabulated displacements are then added in angstroms. Table III provides x and z displacements with zero y displacement; Table IV provides x, y, and z displacements. Displacement values are not multiplied by `A0`.

The z-axis is normal to the surface, and deeper layers have decreasing z. All models use periodic boundaries `(True, True, False)`.

- p(2x1): in-plane vectors `(A0 * sqrt(2), 0, 0)` and `(0, A0 / sqrt(2), 0)`.
- p(2x2): in-plane vectors `(A0 * sqrt(2), 0, 0)` and `(0, A0 * sqrt(2), 0)`.
- c(4x2): skewed primitive cell with vectors `(A0 * sqrt(2), A0 / sqrt(2), 0)` and `(0, A0 * sqrt(2), 0)`.

The current scripts leave the third cell vector zero and do not add vacuum.

## Running

Install dependencies as described in the [project README](../README.md). Run commands from the repository root:

```powershell
python "Si100/p(2x1)s_fivelayers.py"
python "Si100/p(2x1)s_surfacewithbulk.py"
```

Replace the filename prefix to generate another reconstruction. `SHOW_GUI = True` opens the ASE viewer by default; set it to `False` in the relevant generator to run without the viewer. `DISPLAY_REPEAT = (3, 3, 1)` controls visualization, with x horizontal and z vertical.

## Outputs

Each generator writes `output/<script_name>.extxyz` and `output/<script_name>.traj`, relative to this folder. Both contain the fundamental cell, not the repeated visualization, and preserve cell and periodic boundary information. Metadata records the source DOI, reconstruction, and model description; atom tags identify layers.

## Geometry validation

After generating all eight models, compare them with Figure 18:

```powershell
python Si100/validate_si100.py
```

By default, the validator reads all eight `.extxyz` files and reports missing files. To compare selected exports, including `.traj` files:

```powershell
python Si100/validate_si100.py "Si100/output/p(2x1)s_fivelayers.traj"
```

The script uses minimum-image distances and zero-based Python indices. It prints selected bond lengths, dimer buckling angles, and differences from the paper. Figure 18's buckling angles for p(2x2) and c(4x2) are averages over two dimers; the validator also reports their mean. Reference angles are 0.0, 18.3, 19.1, and 18.8 degrees for p(2x1)s, p(2x1)a, p(2x2), and c(4x2), respectively.

This validator reports geometry differences; it does not apply a numerical pass/fail tolerance to those differences. The paper estimates convergence of its calculated bond lengths to 0.01 angstrom and bond angles to 1 degree.
