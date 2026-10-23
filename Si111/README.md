# Si(111)-(2x1), modified Pandey structure

[Back to project overview](../README.md)

## Source

G. Xu et al., "Atomic structure of the cleaved Si(111)-(2x1) surface refined by dynamical LEED," *Physical Review B* **70**, 045307 (2004). [DOI: 10.1103/PhysRevB.70.045307](https://doi.org/10.1103/PhysRevB.70.045307)

The structure comes from experimental low-energy electron diffraction (LEED) data refined using automated tensor LEED. The generator uses Table II's rightmost column group, "MP structure with enhanced vibrations." Table III provides reference surface bond lengths.

## Model and coordinates

One 16-atom modified Pandey model is constructed. The x and z values are reported Cartesian coordinates in angstroms, while y remains equal to the ideal bulk y coordinate. All 16 rows were checked against Table II. Atom order and three-decimal input precision are preserved: paper atoms 1-16 correspond to Python indices 0-15.

Coordinates are used directly as positions, without adding ideal positions or multiplying by a lattice constant. In-plane vectors are `(6.65, 0, 0)` and `(0, 3.84, 0)` angstroms. Positive z points outward, and periodic boundaries are `(True, True, False)`.

ASE centering adds 10 angstroms of vacuum on each side along z. This translates every z coordinate by +17.058 angstroms, preserves relative positions, and gives a cell height of 30.510 angstroms.

## Running

Install dependencies as described in the [project README](../README.md). Run commands from the repository root:

```powershell
python "Si111/(2x1)mp_enhanced_vibrations.py" --no-gui
```

Omit `--no-gui` to open the ASE viewer. `SHOW_GUI = True` and `DISPLAY_REPEAT = (3, 3, 1)` are configurable in the generator. The viewer displays x horizontally and z vertically.

## Outputs

The generator writes `output/(2x1)mp_enhanced_vibrations.extxyz` and `output/(2x1)mp_enhanced_vibrations.traj`, relative to this folder. Both contain the fundamental 16-atom cell, not the repeated visualization, and preserve cell, periodic boundaries, and source metadata.

Metadata records the paper DOI, Table II column choice, coordinate units, experimental LEED-refinement origin, atom ordering, surface normal, vacuum thickness, and z translation.

## Geometry validation

```powershell
python Si111/validate_si111.py
```

By default, the validator reads both exports and checks atom count, silicon composition, cell, periodic boundaries, atom order, positions, vacuum, and source metadata. It also checks the absence of constraints, a calculator, and momenta. Specific export paths can be passed as positional arguments.

The height difference between paper atoms 1 and 2 is 0.498 angstrom. Distances use minimum-image periodic boundaries after converting paper atom numbers to zero-based Python indices:

| Paper atoms | Python indices | Calculated distance (angstrom) | Table III (angstrom) |
| --- | --- | ---: | ---: |
| 1-2 | 0-1 | 2.270557 | 2.271 |
| 1-4 | 0-3 | 2.312728 | 2.313 |
| 2-3 | 1-2 | 2.346094 | 2.347 |

Both exports pass the 0.005 angstrom bond-length tolerance, which allows for rounding of the published coordinates and in-plane cell dimensions.

## Scope and limitations

This is one static reconstructed geometry. "Enhanced vibrations" identifies the paper's refinement; no atomic vibrations are applied. The model contains no split atoms, additional bulk layers, hydrogen, constraints, calculator, or geometry optimization. The bottom surface remains unpassivated.
