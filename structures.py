'''Contains data structures for materials and lights'''
from Vector3 import Vector3

Color = Vector3

class Light():
    def __init__(self, position, diffuse_intensity, specular_intensity):
        self.position = position
        self.diffuse_intensity = diffuse_intensity
        self.specular_intensity = specular_intensity

class Material():
    def __init__(self, ambient_c, diffuse_c, specular_c, shininess):
        self.ambient_constant = ambient_c
        self.diffuse_constant = diffuse_c
        self.specular_constant = specular_c
        self.shininess = shininess