'''Sphere class. Includes basic definition of a sphere, as well as sphere intersection test'''

from utils import solve_quadratic

class Sphere():
    def __init__(self, position, radius, material):
        self.position = position
        self.material = material
        self.radius = radius
        self.diameter = radius*2

    
    def intersect(self, ray_direction, ray_origin):
        '''Contruct and solve a quadratic equation to find the intersection of the given ray and this sphere'''
        a = ray_direction.length**2

        to_sphere = ray_origin - self.position
        b = (ray_direction*to_sphere).product*2

        c = (to_sphere.length**2) - (self.radius**2)

        t = solve_quadratic(a, b, c)
        
        return t