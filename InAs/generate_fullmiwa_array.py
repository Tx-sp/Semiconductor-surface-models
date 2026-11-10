from pathlib import Path

import numpy as np

A0 = 5.96
IN_PARTNER_OFFSET = 2.76
LOWER_AS_ROWS = ((-2.12, -3.03), (2.12, -3.04))
LOWER_AS_COLUMNS = 4
LOWER_AS_CORRUGATION = 0.20

# Original Table 1 coordinates
# Bond 1-2 (0--4) is 2.497 A here, but 2.59 A in Fig. 3.
# The figure label may be incorrect, so the table coordinates are used as the reference for validation.
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

    # Reflection across y = 6.26 ----
    for row in range(9):
        point = table[row].copy()
        point[1] = 2 * REFLECTION_Y - point[1]
        positions.append(point)
        elements.append(symbols[row])
        tags.append(row + 1)

    # Add 2.76 angstroms to the In partner's x coordinate ------

    partner = table[8].copy()
    partner[0] += IN_PARTNER_OFFSET
    positions.append(partner.copy())

    # Reflect the In partner ---

    partner[1] = 2 * REFLECTION_Y - partner[1]
    positions.append(partner)
    elements.extend(["In", "In"])
    tags.extend([9, 9])

    # Add eight inferred lower As atoms ---

    for x, height in LOWER_AS_ROWS:
        for column in range(LOWER_AS_COLUMNS):
            y = REFLECTION_Y if column == 1 else (column + 0.5) * spacing
            z = height if column == 1 else height - LOWER_AS_CORRUGATION
            positions.append([x, y, z])
            elements.append("As")
            tags.append(12 + 4 * (x > 0) + column)

    # Save to file for reading by zeta(4x2)_Miwa_fig3.py
    
    np.savez(Path(__file__).with_name("miwa_array.npz"),
             positions=np.array(positions), symbols=np.array(elements),
             tags=np.array(tags), cell=np.array([2 * spacing, 4 * spacing, 0]))


if __name__ == "__main__":
    main()
