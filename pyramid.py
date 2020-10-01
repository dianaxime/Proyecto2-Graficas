from plane import Plane
from utils import sum, V3, sub, norm, cross, dot, mul, length
from intersect import Intersect

class Pyramid(object):
    def __init__(self, arrVec, material):
        self.arrVec = arrVec
        self.material = material
        print("aqui")

    def rayIntersect(self, origin, direction):
        v0, v1, v2 = self.arrVec
        v0v1 = sub(v1, v0)
        v0v2 = sub(v2, v0)

        N = cross(v0v1, v0v2)
        # area2 = length(N)

        raydirection = dot(N, direction)

        if abs(raydirection) < 0.0001:
            return None
        
        d = dot(N, v0)
        
        t = dot(N, origin) + d
        
        if t < 0:
            return None

        P = sum(origin, mul(direction, t))

        edge0 = sub(v1, v0)
        vp0 = sub(P, v0)

        C = cross(edge0, vp0)

        nc = dot(N, C)
        print("C", nc)
        if nc < 0:
            return None

        edge1 = sub(v2, v1)
        vp1 = sub(P, v1)

        C = cross(edge1, vp1)

        if dot(N, C) < 0:
            return None

        edge2 = sub(v0, v2)
        vp2 = sub(P, v2)

        C = cross(edge2, vp2)

        if dot(N, C) < 0:
            return None

        print("hola")

        return Intersect(distance = (t / raydirection),
                         point = P,
                         normal = norm(N))

    
