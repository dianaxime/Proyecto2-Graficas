from utils import sum, V3, sub, norm, cross, dot, mul, length, barycentric
from intersect import Intersect

class Pyramid(object):
    def __init__(self, arrPoints, material):
        self.arrPoints = arrPoints
        self.material = material

    def side(self, v0, v1, v2, origin, direction):
        v0v1 = sub(v1, v0)
        v0v2 = sub(v2, v0)

        N = cross(v0v1, v0v2)
        
        raydirection = dot(N, direction)

        if abs(raydirection) < 0.0001:
            return None
        
        d = dot(N, v0)
        
        t = (dot(N, origin) + d) / raydirection
        
        if t < 0:
            return None

        P = sum(origin, mul(direction, t))
        U, V, W = barycentric(v0, v1, v2, P)
        
        if U < 0 or V < 0 or W < 0:
            return None
        else: 
            return Intersect(distance = d,
                         point = P,
                         normal = norm(N))
        

    def rayIntersect(self, origin, direction):
        v0, v1, v2, v3 = self.arrPoints
        sides = [
            self.side(v0, v3, v2, origin, direction),
            self.side(v0, v1, v2, origin, direction),
            self.side(v1, v3, v2, origin, direction),
            self.side(v0, v1, v3, origin, direction)
        ]

        t = float('inf')
        intersect = None

        for side in sides:
            if side is not None:
                if side.distance < t:
                    t = side.distance
                    intersect = side

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal)
