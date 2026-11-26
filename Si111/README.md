# Si(111)-(2x1)

Source: G. Xu et al., Phys. Rev. B 70, 045307 (2004). https://doi.org/10.1103/PhysRevB.70.045307

The coordinates are the modified Pandey chain from Table II, column group "MP structure with enhanced vibrations", which is an experimental LEED refinement. The reference bond lengths are from Table III.

The 16 tabulated atoms (8 layers of 2) are Cartesian coordinates in Å and are used directly, in a 6.65 x 3.84 Å cell. Layers below these are ideal bulk: each new layer is the ideal layer two layers above, shifted by one bilayer. Paper atoms 1-16 are Python indices 0-15, and atom tags give the layer number from the top.

Settings: `TOTAL_LAYERS = 10` (at least 8). There is no lattice constant setting, since the table gives the coordinates in Å.

```
python Si111/si111_2x1.py
python Si111/validate_si111.py
```

The generator saves `Si111/output/si111_2x1.extxyz` and `.traj`. The validator prints the three Table III bond lengths next to the model values.
