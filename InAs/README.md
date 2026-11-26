# InAs(001)

## c(8x2), Kumpf et al.

Source: C. Kumpf et al., Phys. Rev. B 64, 075307 (2001). https://doi.org/10.1103/PhysRevB.64.075307

The coordinates are the InAs column of Table I, all 36 rows including the unnumbered deeper rows. They are LEED fractions in the basis a = a0[1-10]/2, b = a0[110]/2, c = a0[001]. Each row is copied with the c2mm symmetry (±x, ±y) and the (4, 1) centering, wrapped into the 8 x 2 cell and scaled by (a0/sqrt(2), a0/sqrt(2), a0).

Settings: `A0 = 6.0583` Å is the experimental InAs value (Vurgaftman et al., 2001), since the paper gives none. `TOTAL_LAYERS` (1 to 9, default 7) chooses how many of the tabulated layers are kept; no ideal layers are added.

```
python InAs/kumpf_c8x2.py
```

This saves `InAs/output/kumpf_c8x2.extxyz`, `.traj` and `.cif`. CIF does not store the non-periodic z direction, so use `.extxyz` or `.traj` for calculations.

## zeta(4x2), Miwa et al.

Source: R. H. Miwa et al., Surf. Sci. 542, 101 (2003). https://doi.org/10.1016/S0039-6028(03)00955-5

The 11 atoms of Table 1 are Cartesian coordinates in Å. `miwa_array.py` completes the reconstruction of Fig. 3: atoms 1-9 are mirrored across y = 6.26 Å, the missing In partner is placed 2.76 Å from atom 9 (and mirrored), and eight lower As atoms are inferred. The 30 atoms are saved in `InAs/miwa_array.npz`. `miwa_zeta4x2.py` reads this array, puts it in a 2a0/sqrt(2) x 4a0/sqrt(2) cell and adds ideal zinc-blende layers below.

Settings: `A0 = 5.96` Å, the theoretical lattice constant used in the paper. `TOTAL_LAYERS = 7` gives 62 atoms; 3 keeps only the 30 reconstruction atoms.

The 1-2 bond from the table coordinates is 2.50 Å, while Fig. 3 gives 2.59 Å. The table coordinates are kept and the validator reports this bond without testing it.

```
python InAs/miwa_array.py
python InAs/miwa_zeta4x2.py
python InAs/validate_miwa.py
```

The model is saved as `InAs/output/miwa_zeta4x2.extxyz`, `.traj` and `.cif`. The validator compares six bonds with Fig. 3 and accepts differences up to 0.03 Å.
