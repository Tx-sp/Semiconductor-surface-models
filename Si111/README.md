# Si(111)-(2x1), modified Pandey structure

[Back to project overview](../README.md)

## Source

G. Xu et al., "Atomic structure of the cleaved Si(111)-(2x1) surface refined by dynamical LEED," *Physical Review B* **70**, 045307 (2004). [DOI: 10.1103/PhysRevB.70.045307](https://doi.org/10.1103/PhysRevB.70.045307)

The structure comes from experimental low-energy electron diffraction (LEED) data refined using automated tensor LEED. The generator uses Table II's rightmost column group, "MP structure with enhanced vibrations." Table III provides reference surface bond lengths.

## Model and coordinates

The model contains 16 tabulated atoms in 8 layers of 2 atoms, plus ideal layers below. `TOTAL_LAYERS` controls the depth (default 10, minimum 8). The x and z values of the tabulated atoms are reported Cartesian coordinates in angstroms, while y remains equal to the ideal bulk y coordinate. All 16 rows were checked against Table II. Atom order and three-decimal input precision are preserved: paper atoms 1-16 correspond to Python indices 0-15.

Tabulated coordinates are used directly as positions without multiplying by a lattice constant. Added layers use Table II's ideal bulk-terminated rows 13-16 as seeds. Each new layer is the ideal layer two layers above translated by `ideal[4] - ideal[0] = (-1.108, -1.920, -3.135)` angstroms, one bilayer translation. Added x and y coordinates are wrapped into the cell; no displacements are applied. In-plane vectors remain `(6.65, 0, 0)` and `(0, 3.84, 0)` angstroms. Positive z points outward, and periodic boundaries are `(True, True, False)`.

Tags identify layers from top to bottom: tag 1 belongs to rows 1-2, tag 2 to rows 3-4, and so on. With the default 10 layers, tags 9 and 10 identify the four added ideal atoms.

ASE centering adds 10 angstroms of vacuum on each side along z. With the default 20 atoms, this translates every z coordinate by +20.189 angstroms, preserves relative positions, and gives a cell height of 33.641 angstroms. The shift and height depend on `TOTAL_LAYERS`.

## Running

Install dependencies as described in the [project README](../README.md). Run commands from the repository root:

```powershell
python "Si111/(2x1)mp_enhanced_vibrations.py" --no-gui
```

Omit `--no-gui` to open the ASE viewer. `SHOW_GUI = True` and `DISPLAY_REPEAT = (3, 3, 1)` are configurable in the generator. The viewer displays x horizontally and z vertically.

## Outputs

The generator writes `output/(2x1)mp_enhanced_vibrations.extxyz` and `output/(2x1)mp_enhanced_vibrations.traj`, relative to this folder. Both contain the fundamental cell with `2 * TOTAL_LAYERS` atoms, not the repeated visualization, and preserve cell, periodic boundaries, layer tags, and source metadata.

Metadata records the paper DOI, Table II column choice, coordinate units, experimental LEED-refinement origin, atom ordering, surface normal, vacuum thickness, z translation, and total layer count.

## Geometry validation

```powershell
python Si111/validate_si111.py
```

The script reads both exports and prints the three Table III bond lengths: model, paper, and difference in angstroms. Specific export paths can be passed as positional arguments. It is a comparison table only; it does not check metadata, layer tags, bulk coordination, or pass/fail tolerances.

The height difference between paper atoms 1 and 2 is 0.498 angstrom. Distances use minimum-image periodic boundaries after converting paper atom numbers to zero-based Python indices:

| Paper atoms | Python indices | Calculated distance (angstrom) | Table III (angstrom) |
| --- | --- | ---: | ---: |
| 1-2 | 0-1 | 2.270557 | 2.271 |
| 1-4 | 0-3 | 2.312728 | 2.313 |
| 2-3 | 1-2 | 2.346094 | 2.347 |

The differences are below 0.005 angstrom for both generated exports, consistent with rounding of the published coordinates and in-plane cell dimensions.

## Scope and limitations

This is one static reconstructed geometry. "Enhanced vibrations" identifies the paper's refinement; no atomic vibrations are applied. The generator adds ideal bulk layers but no split atoms, hydrogen, constraints, calculator, or geometry optimization. The bottom surface remains unpassivated.

`MACE/Si111_2x1/relax.py` fixes the bottom two tagged layers during relaxation. At the default depth, these are the four added ideal atoms; all 16 tabulated atoms remain free. At `TOTAL_LAYERS = 8` or `9`, the bottom-two-layer rule also fixes some tabulated atoms.
