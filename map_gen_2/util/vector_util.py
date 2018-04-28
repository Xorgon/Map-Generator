import math


def angle(a, b):
    cos_theta = dot_prod(a, b) / (length(a) * length(b))
    if cos_theta > 1:
        cos_theta = 1
    if cos_theta < -1:
        cos_theta = -1
    return math.acos(cos_theta)


def dot_prod(a, b):
    return a[0] * b[0] + a[1] * b[1]


def get_unit_perp(a):
    m_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    if m_a > 0:
        return [a[1] / m_a, -a[0] / m_a]


def length(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def dist(p1, p2):
    return length([p2[0] - p1[0], p2[1] - p1[1]])


def full_angle(a, b):
    if dot_prod(a, b) < 0:
        return math.pi - angle(a, b)
    else:
        return angle(a, b)


def split_line(p1, p2, rand, mag_fact=0.25):
    mid_p = [0, 0]
    mid_p[0] = (p1[0] + p2[0]) / 2
    mid_p[1] = (p1[1] + p2[1]) / 2

    mid_vect = [mid_p[0] - p1[0], mid_p[1] - p1[1]]
    perp_vect = get_unit_perp(mid_vect)

    split_p = [0, 0]
    rand_fact = rand.random() - 0.5
    distance = dist(p1, p2)

    split_p[0] = mid_p[0] + rand_fact * mag_fact * distance * perp_vect[0]
    split_p[1] = mid_p[1] + rand_fact * mag_fact * distance * perp_vect[1]
    return split_p


def subtract(a, b):
    """ Subtracts b from a. """
    return [a[0] - b[0], a[1] - b[1]]
