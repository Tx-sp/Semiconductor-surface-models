# Reconstructed Semiconductor Surfaces

Bachelor's thesis project on constructing atomic models of semiconductor
surface reconstructions from published structural information using ASE.

## Current work

Si(100) reconstructions:
- p(2×1) symmetric
- p(2×1) asymmetric
- p(2×2)
- c(4×2)

Each reconstruction has two variants:
- Five reconstructed atomic layers.
- Five reconstructed layers with ideal silicon layers underneath.

The bulk variants contain twelve layers by default.

## Source

A. Ramstad, G. Brocks, and P. J. Kelly,
"Theoretical study of the Si(100) surface reconstruction,"
Physical Review B 51, 14504–14523 (1995).

https://doi.org/10.1103/PhysRevB.51.14504

Coordinates are constructed from Tables III and IV.
Selected geometrical measurements are compared with Figure 18.

## Running the scripts

Install the dependencies:

    python -m pip install -r requirements.txt

Run a script from the main project folder:

    python "Si100/p(2x1)s_fivelayers.py"

Generated structures are saved in Si100/output.
Each generator writes `.extxyz` and `.traj` files and optionally opens the ASE
viewer. Set `SHOW_GUI = False` in the generator to run without the viewer.
`TOTAL_LAYERS` must be at least five, the number of reconstructed layers provided.

After running the desired generators, run the separate geometry comparisons:

    python Si100/validate_si100.py

By default, validation reads all eight generated `.extxyz` files and clearly
reports any missing files. To check selected files, including `.traj` files:

    python Si100/validate_si100.py "Si100/output/p(2x1)s_fivelayers.traj"

Run this script to see the model bond lengths and dimer buckling values and
their differences from the original paper.

## Current limitations

These are preliminary geometry models.
No energy minimisation or stability calculations have been performed.
Added bulk layers occupy ideal lattice positions.
The bottom surface is unpassivated.
