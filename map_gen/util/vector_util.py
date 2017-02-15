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
        return [a[1]/m_a, -a[0]/m_a]


def length(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def full_angle(a, b):
    if dot_prod(a, b) < 0:
        return math.pi - angle(a, b)
    else:
        return angle(a, b)
