import math


def dist(a_lon, a_lat, b_lon, b_lat):
    dx = abs(a_lon - b_lon) * 111 * 1000 * math.cos(math.radians((a_lat + b_lat) / 2))
    dy = abs(a_lat - b_lat) * 111 * 1000

    return math.sqrt(dx * dx + dy * dy)
