from color import *

'''
  Diana Ximena de León Figueroa
  Carne 18607
  RT2 - Phong model
  Graficas por Computadora
  10 de septiembre de 2020
'''


class Material(object):
  def __init__(self, diffuse, albedo, spec, refractionIndex = 0):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec
    self.refractionIndex = refractionIndex


WHITE = Color(250, 245, 250)

BLUE1 = Color(80, 115, 180)
BLUE2 = Color(90, 115, 165)
BLUE3 = Color(80, 100, 160)
BLUE4 = Color(60, 90, 140)
BLUE5 = Color(15, 70, 140)
BLUE6 = Color(10, 60, 120)
BEIGE = Color(195, 170, 160)
BROWN = Color(110, 100, 90)


blue1 = Material(diffuse = BLUE1, albedo = (1, 1, 0, 0), spec = 50, refractionIndex = 0)
blue2 = Material(diffuse = BLUE2, albedo = (1, 1, 0, 0), spec = 50, refractionIndex = 0)
blue3 = Material(diffuse = BLUE3, albedo = (1, 1, 0, 0), spec = 50, refractionIndex = 0)
blue4 = Material(diffuse = BLUE4, albedo = (1, 1, 0, 0), spec = 50, refractionIndex = 0)
blue5 = Material(diffuse = BLUE5, albedo = (1, 1, 0, 0.9), spec = 50, refractionIndex = 0)
blue6 = Material(diffuse = BLUE6, albedo = (1, 0, 0, 0), spec = 50, refractionIndex = 0)
blue7 = Material(diffuse = BLUE5, albedo = (0.25, 1, 1, 0), spec = 65, refractionIndex = 0)
beige = Material(diffuse = BEIGE, albedo = (1, 0, 0, 0), spec = 65, refractionIndex = 0)
brown = Material(diffuse = BROWN, albedo = (1, 0, 0, 0), spec = 65, refractionIndex = 0)
