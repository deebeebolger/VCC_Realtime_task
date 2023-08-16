import math as m
import matplotlib as mpl

"""
Adapted from Ozdemir et al script at https://github.com/mkfzdmr/Deep-Learning-based-Emotion-Recognition.git

"""

def cart2sph(x, y, z):
    x2_y2 = x ** 2 + y ** 2
    r = m.sqrt(x2_y2 + z ** 2)  # r
    elev = m.atan2(z, m.sqrt(x2_y2))  # Elevation
    az = m.atan2(y, x)  # Azimuth
    return r, elev, az


def pol2cart(theta, rho):
    return rho * m.cos(theta), rho * m.sin(theta)

def azim_proj(pos):
    """
    Computes the Azimuthal Equidistant Projection of input point in 3D Cartesian Coordinates.
    Imagine a plane being placed against (tangent to) a globe. If
    a light source inside the globe projects the graticule onto
    the plane the result would be a planar, or azimuthal, map
    projection.

    :param pos: position in 3D Cartesian coordinates
    :return: projected coordinates using Azimuthal Equidistant Projection
    """
    [r, elev, az] = cart2sph(pos[0], pos[1], pos[2])
    return pol2cart(az, m.pi / 2 - elev)