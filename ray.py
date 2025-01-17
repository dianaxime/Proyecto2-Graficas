from utils import writebmp, norm, V3, sub, dot, reflect, length, mul, sum, refract
from sphere import Sphere
from math import pi, tan
from materials import blue1, blue2, blue3, blue4, blue5, blue6, blue7, beige, brown, white, glass, mirror, green
import random
from light import *
from color import *
from cube import Cube
from envmap import Envmap
from pyramid import Pyramid
from ambientLight import AmbientLight
from plane import Plane


'''
    Diana Ximena de León Figueroa
    Carne 18607
    Proyecto # 2
    Graficas por Computadora
    30 de septiembre de 2020
'''

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
BACKGROUND = Color(80, 150, 240)
MAX_RECURSION_DEPTH = 3


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.currentColor = BACKGROUND
        self.envMap = None
        self.ambientLight = None
        self.clear()

    def clear(self):
        self.pixels = [
            [self.currentColor for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename='out.bmp'):
        writebmp(filename, self.width, self.height, self.pixels)

    def point(self, x, y, selectColor=None):
        try:
            self.pixels[y][x] = selectColor or self.currentColor
        except:
            pass

    def sceneIntersect(self, origin, direction):
        zbuffer = float('inf')
        
        material = None
        intersect = None
        
        for obj in self.scene:
            hit = obj.rayIntersect(origin, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect

    def castRay(self, origin, direction, recursion = 0):
        material, intersect = self.sceneIntersect(origin, direction)
        
        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envMap:
                return self.envMap.getColor(direction)
            return self.currentColor
            # Si el rayo no golpeo nada o si llego al limite de recursion
        
        lightDir = norm(sub(self.light.position, intersect.point))
        lightDistance = length(sub(self.light.position, intersect.point))

        if self.ambientLight:
            ambientColor = self.ambientLight.color * self.ambientLight.strength
        else:
            ambientColor = self.currentColor
        
        offsetNormal = mul(intersect.normal, 1.1)
        shadowOrigin = sub(intersect.point, offsetNormal) if dot(lightDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
        shadowMaterial, shadowIntersect = self.sceneIntersect(shadowOrigin, lightDir)
        shadowIntensity = 0

        if shadowMaterial and length(sub(shadowIntersect.point, shadowOrigin)) < lightDistance:
            shadowIntensity = 0.9

        intensity = self.light.intensity * max(0, dot(lightDir, intersect.normal)) * (1 - shadowIntensity)

        reflection = reflect(lightDir, intersect.normal)
        specularIntensity = self.light.intensity * (
            max(0, -dot(reflection, direction)) ** material.spec
        )

        if material.albedo[2] > 0:
            reflectDir = reflect(direction, intersect.normal)
            reflectOrigin = sub(intersect.point, offsetNormal) if dot(reflectDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
            reflectedColor = self.castRay(reflectOrigin, reflectDir, recursion + 1)
        else:
            reflectedColor = self.currentColor

        if material.albedo[3] > 0:
            refractDir = refract(direction, intersect.normal, material.refractionIndex)
            refractOrigin = sub(intersect.point, offsetNormal) if dot(refractDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
            refractedColor = self.castRay(refractOrigin, refractDir, recursion + 1)
        else:
            refractedColor = self.currentColor

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = Color(255, 255, 255) * specularIntensity * material.albedo[1]
        reflected = reflectedColor * material.albedo[2]
        refracted = refractedColor * material.albedo[3]
        
        return ambientColor + diffuse + specular + reflected + refracted


    def render(self):
        fov = int(pi / 2) # field of view
        for y in range(self.height):
            for x in range(self.width):
                #if random.randint(0,2) != 0:
                #    continue
                i = (2 * (x + 0.5) / self.width - 1) * self.width / self.height * tan(fov / 2)
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.pixels[y][x] = self.castRay(V3(0, 0, 0), direction)

    def gradientBackground(self):
        for x in range(self.width):
            for y in range(self.height):
                r = int((x / self.width) * 255) if x / self.width < 1 else 1
                g = int((y / self.height) * 255) if y / self.height < 1 else 1
                b = 0
                self.pixels[y][x] = Color(r, g, b)
    


r = Raytracer(400, 400)
#r.envMap = Envmap('fondo.bmp')
r.light = Light(
    position = V3(0, 20, 20),
    intensity = 1.5
)
r.ambientLight = AmbientLight(strength = 0.1)
r.scene = [
    Pyramid([V3(-1, 0, -10), V3(-3, 2, -10), V3(-5, 0, -10), V3(-1, 0, -10)], blue3),
    Pyramid([V3(1, 0, -10), V3(3, 2, -10), V3(5, 0, -10), V3(1, 0, -10)], blue3),
    Pyramid([V3(-2, 0, -10), V3(-4, 2, -10), V3(-6, 0, -10), V3(-2, 0, -10)], blue2),
    Pyramid([V3(2, 0, -10), V3(4, 2, -10), V3(6, 0, -10), V3(2, 0, -10)], blue2),
    Pyramid([V3(0, 0, -10), V3(-2, 2, -10), V3(-4, 0, -10), V3(0, 0, -10)], blue4),
    Pyramid([V3(0, 0, -10), V3(2, 2, -10), V3(4, 0, -10), V3(0, 0, -10)], blue4),
    Pyramid([V3(2, 0, -10), V3(0, 3, -10), V3(-2, 0, -10), V3(2, 0, -10)], blue1),
    Cube(V3(0, -2, -2), 2, beige),
    Pyramid([V3(-1, 0, -10), V3(3, 0, -10), V3(-1, 0, -5), V3(-1, -1, -10)], brown),
    Cube(V3(0.75, -0.75, -2.5), 0.5, blue5),
    Sphere(V3(0.75, -0.40, -2.5), 0.20, white),
    Sphere(V3(0.75, -0.16, -2.5), 0.05, white),
    Plane(V3(2, -10, -15), V3(0,1,0), mirror),
    
    
    Sphere(V3(5, 0.1, -10), 0.10, green),
    Sphere(V3(5.2, 0.2, -10), 0.10, green),
    Sphere(V3(4, -0.40, -10), 0.10, green),
    Sphere(V3(3.7, -0.40, -10), 0.10, green),
    Sphere(V3(4.2, -0.80, -10), 0.10, green),
    Sphere(V3(4.5, -0.80, -10), 0.10, green),
    Sphere(V3(4.4, 0, -10), 0.10, green),
    Sphere(V3(3.5, -0.50, -10), 0.10, green),
    Sphere(V3(4.5, -0.20, -10), 0.10, green),
    Sphere(V3(4.8, 0, -10), 0.10, green),
    Sphere(V3(3.5, -2, -10), 0.10, green),
    Sphere(V3(4.5, -1, -10), 0.10, green),
    Sphere(V3(4, -1.5, -10), 0.10, green),
    Sphere(V3(4.5, -1.4, -10), 0.10, green),
    Sphere(V3(4.2, -1.4, -10), 0.10, green),
    Sphere(V3(4.7, -1.8, -10), 0.10, green),
    Sphere(V3(5, -1.8, -10), 0.10, green),
    Sphere(V3(5, -1, -10), 0.10, green),
    Sphere(V3(4, -1.5, -10), 0.10, green),
    Sphere(V3(5, -1.2, -10), 0.10, green),
    Sphere(V3(5.3, -1, -10), 0.10, green),
    Sphere(V3(4, -3, -10), 0.10, green),
    Sphere(V3(5, -2, -10), 0.10, green),
    Sphere(V3(4.5, -2.5, -10), 0.10, green),
    Sphere(V3(4.7, -3, -10), 0.10, green),
    Sphere(V3(5, -3.5, -10), 0.10, green),
    Sphere(V3(5, -4, -10), 0.10, green),
    Sphere(V3(4, -4.5, -10), 0.10, green),
    Sphere(V3(5, -5, -10), 0.10, green),
    Sphere(V3(5.3, -4, -10), 0.10, green),
    Sphere(V3(4.5, -4.5, -10), 0.10, green),
    Sphere(V3(5, -3.5, -10), 0.10, green),
    Sphere(V3(4.5, -3, -10), 0.10, green),


    Sphere(V3(-3.7, -0.40, -10), 0.10, green),
    Sphere(V3(-4.2, -0.80, -10), 0.10, green),
    Sphere(V3(-4.5, -0.80, -10), 0.10, green),
    Sphere(V3(-4.4, 0, -10), 0.10, green),
    Sphere(V3(-3.5, -0.50, -10), 0.10, green),
    Sphere(V3(-4.5, -0.20, -10), 0.10, green),
    Sphere(V3(-4.8, 0, -10), 0.10, green),
    Sphere(V3(-3.5, -2, -10), 0.10, green),
    Sphere(V3(-4.5, -1, -10), 0.10, green),
    Sphere(V3(-4, -1.5, -10), 0.10, green),
]
r.render()

r.write()