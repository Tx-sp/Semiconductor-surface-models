from pathlib import Path

import numpy as np

A0 = 5.96                                         # theoretical InAs lattice constant in Å used by Miwa et al.
IN_PARTNER_OFFSET = 2.76                          # x shift in Å from In atom 9 to its inferred partner
LOWER_AS_ROWS = ((-2.12, -3.03), (2.12, -3.04))   # x and z in Å of the two inferred lower As rows
LOWER_AS_COLUMNS = 4                              # lower As atoms per row
LOWER_AS_CORRUGATION = 0.20                       # drop in Å of the lower As atoms not at y = 6.26

# Table 1 of Miwa et al. (2003): Cartesian x, y, z in Å
symbols = ["As", "As", "In", "In", "In", "In", "As", "As", "In", "In", "In"]
table = np.array([
    [0.00, 0.00, 0.00],
    [4.21, 0.04, 0.05],
    [-2.12, -0.01, -1.51],
    [2.12, -0.01, -1.51],
    [-0.00, 2.49, 0.19],
    [4.21, 2.53, 0.38],
    [-2.05, 3.97, 0.76],
    [2.051, 3.97, 0.76],
    [2.84, 3.99, -1.89],
    [-1.33, 6.26, -0.27],
    [1.33, 6.26, -0.28]
])
REFLECTION_Y = table[9, 1]


def main():
    spacing = A0 / np.sqrt(2)
    positions = list(table.copy())
    elements = list(symbols)
    tags = list(range(1, len(table) + 1))

    # Mirror atoms 1-9 across y = 6.26
    for row in range(9):
        point = table[row].copy()
        point[1] = 2 * REFLECTION_Y - point[1]
        positions.append(point)
        elements.append(symbols[row])
        tags.append(row + 1)

    # Inferred In partner of atom 9
    partner = table[8].copy()
    partner[0] += IN_PARTNER_OFFSET
    positions.append(partner.copy())

    # Mirror the partner
    partner[1] = 2 * REFLECTION_Y - partner[1]
    positions.append(partner)
    elements.extend(["In", "In"])
    tags.extend([9, 9])

    # Eight inferred lower As atoms
    for x, height in LOWER_AS_ROWS:
        for column in range(LOWER_AS_COLUMNS):
            y = REFLECTION_Y if column == 1 else (column + 0.5) * spacing
            z = height if column == 1 else height - LOWER_AS_CORRUGATION
            positions.append([x, y, z])
            elements.append("As")
            tags.append(12 + 4 * (x > 0) + column)

    # Read by miwa_zeta4x2.py
    np.savez(Path(__file__).with_name("miwa_array.npz"),
             positions=np.array(positions), symbols=np.array(elements),
             tags=np.array(tags), cell=np.array([2 * spacing, 4 * spacing, 0]))


if __name__ == "__main__":
    main()
