def get_poly_from_polys(poly_1, poly_2):
    poly = []
    idx_1 = 0

    while poly_2.count(poly_1[idx_1]) > 0:
        idx_1 += 1

    init_idx_1 = idx_1
    poly_1_complete = False
    poly_2_complete = False
    while not poly_1_complete:
        if poly_1[idx_1] == -1:
            idx_1 += 1
            continue
        poly.append(poly_1[idx_1])
        if poly_2.count(poly_1[idx_1]) > 0 and not poly_2_complete:
            # Try normal direction first.
            direction = 1
            idx_2 = poly_2.index(poly_1[idx_1]) + direction
            if idx_2 == len(poly_2) and direction == 1:
                idx_2 = 0
            if poly_1.count(poly_2[idx_2]) > 0:
                direction = -1
                idx_2 = poly_2.index(poly_1[idx_1]) + direction
            if poly_1.count(poly_2[idx_2]) > 0:
                direction = -1
                idx_2 = poly_2.index(poly_1[idx_1]) + direction

            if idx_2 == -1 and direction == -1:
                idx_2 = len(poly_2) - 1
            initial = True
            while not poly_2_complete:
                poly.append(poly_2[idx_2])
                if poly_1.count(poly_2[idx_2]) > 0 and not initial:
                    poly_2_complete = True
                    idx_1 = poly_1.index(poly_2[idx_2]) + 1
                else:
                    idx_2 += direction
                    initial = False
                    if idx_2 == len(poly_2) and direction == 1:
                        idx_2 = 0
                    if idx_2 == -1 and direction == -1:
                        idx_2 = len(poly_2) - 1

        else:
            idx_1 += 1

        if idx_1 == len(poly_1) and init_idx_1 == 0:
            poly_1_complete = True
        elif idx_1 == len(poly_1):
            idx_1 = 0
        elif idx_1 == init_idx_1:
            poly_1_complete = True

    return poly
