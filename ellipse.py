from utils import sub, dot, length, sum, mul, norm
from intersect import *

class Ellipse(object):
  def __init__(self, center, a, b,  material):
    self.center = center
    self.a = a
    self.b = b
    self.material = material

  def rayIntersect(self, origin, direction):
    L = sub(self.center, origin)
    tca = dot(L, direction)
    l = length(L)
    # distancia al cuadrado
    dc = (l ** 2) / (self.a ** 2)  - (tca ** 2) / (self.b ** 2)

    if dc > 1:
        return None

    #thc = (self.b ** 2) ** 0.5
    #t0 = tca - thc
    #t1 = tca + thc
    t0 = self.a + self.b
    t1 = self.b - self.a
    if t0 < 0:
        t0 = t1
    if t0 < 0:
        return None

    hit = sum(origin, mul(direction, t0))
    normal = norm(sub(hit, self.center))

    return Intersect(
        distance=t0,
        point=hit,
        normal=normal
    )
