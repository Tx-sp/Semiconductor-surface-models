# InAs(001)-c(8x2)

[Kumpf et al., PRB 64, 075307 (2001)](https://doi.org/10.1103/PhysRevB.64.075307), Table I, InAs column only: all 36 occupied rows, including the unnumbered deeper rows (five bilayers). Printed three-decimal coordinates are retained.

LEED basis: a = a0[1,-1,0]/2, b = a0[1,1,0]/2, c = a0[0,0,1]. The in-plane origin is the In3 site/mirror intersection in Fig. 5; z = 0 is the ideal In-terminated surface height (Fig. 3). In surface-aligned Cartesian axes, multiply Table I coordinates by `(a0/sqrt(2), a0/sqrt(2), a0)`. Apply c2mm operations `(±x, ±y, z)` and centering `(4,1,0)`, then wrap x modulo 8 and y modulo 2. Only repeated images of the same row are removed (12-decimal keys); distinct sites remain separate. Supercell in-plane fractions would be `(x/8,y/2)`, not `(x,y)`. 

The paper supplies no numerical a0. We use **6.0583 Å**, the experimental InAs value in [Table 1 of the Ioffe-hosted band-parameter study](https://journals.ioffe.ru/articles/viewPDF/5724). ASE adds 10 Å vacuum per side along +z; PBC is `(True, True, False)`. No extra bulk layers, passivation, or relaxation are included.

Run `python "InAs/c(8x2)_tableI.py"` from the repository root. Set `SHOW_GUI = False` for export only. `DISPLAY_REPEAT = (3,3,1)` affects only the viewer, with x horizontal and z vertical. Fundamental-cell exports are `output/c(8x2)_tableI.extxyz`, `.traj`, and `.cif`; use extxyz/traj to preserve the slab PBC flags, which CIF does not encode.


## InAs(001)-zeta(4x2), Miwa

[Miwa et al., Surface Science 542, 101-111 (2003)](https://doi.org/10.1016/S0039-6028(03)00955-5), Figures 1(d), 3 and Table 1. `miwa_from_table.py` retains all 11 printed Cartesian coordinates in angstroms (including 2.051). Using a0 = 5.96 Angstrom, the short x direction (parallel to [110], vertical in Figure 3) and long y direction (parallel to [1,-1,0], horizontal in Figure 3) have periods 2a0/sqrt(2) and 4a0/sqrt(2). 

Figure 3's left/right counterparts are inferred by reflection about y = 6.26; the missing subsurface dimer partners inferred at x = 2.84 + 2.76 = 5.60. Deeper As and In coordinates are not fully supplied and are omitted.

Run `python "InAs/miwa_from_table.py"` from the repository root. `VACUUM = 10.0`, `SHOW_GUI = True` and `DISPLAY_REPEAT = (1, 1, 1)` follow the example script; set `SHOW_GUI = False` for export only. Fundamental-cell `.extxyz`, `.traj` and `.cif` files go to `InAs/output/miwa_from_table.*`, with in-plane PBC (use extxyz/traj to retain the nonperiodic z flag).

## Miwa Figure 3 completion

`generate_fullmiwa_array.py` generates the 30-atom NumPy array `miwa_array.npz` from Table 1 using mirroring, In partners and eight inferred lower As atoms to complete Figure 3. `miwa_full.py` reads this array and uses the same ASE modelling workflow as the original Miwa script.

There are some inconsistency regarding the 1-2 bond (Atoms 0--4) from Fig. 3 and the coordinate table, so tabulated coordinates are retained. This will be addressed later.

`miwa_full.py` adds ideal bulk planes with `EXTRA_BULK_LAYERS` (default 6; use 0 for the original 30 atoms). `EXPORT_REPEAT` controls saved structures and `DISPLAY_REPEAT` controls the viewer.
