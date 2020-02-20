'''Contains data structures for materials and lights'''
from Vector3 import Vector3

# alias so that color information is obviously color information, but as colors are essentially
# equivalent to vectors with 3 components, this is useful
Color = Vector3

# data structure class to hold information about lights in the scene
# diffuse and specular intensity are constants which relate to how strongly the light results in
# diffuse and specular lighting effects on objects
# each are vectors with 3 components, one for each color (R, G, B) with each component being a float between 0 and 1
class Light():
    def __init__(self, position, diffuse_intensity, specular_intensity):
        self.position = position
        self.diffuse_intensity = diffuse_intensity
        self.specular_intensity = specular_intensity

# data structure class to hold information about materials in the scene
# ambient, diffuse and specular constants are constants which relate to how much of each lighting effect appear on this material
# each are vectors with 3 components, one for each color (R, G, B) with each component being a float between 0 and 1
# shininess is a float which causes differences in specular highlights on this material
# higher shininess means smaller, brighter specular highlights
# lower shininess means larger, duller specular highlights
# the reflectivity constant relates to how much light is reflected by this material. Materials with high
# reflectivity constants usually have lower diffuse constants. The higher the reflectivity constant the more clear reflections are
# refracts and refractive_index are values relating to the refractive properties of the material. By default the material does not refract

class Material():
    def __init__(self, ambient_c, diffuse_c, specular_c, shininess, reflectivity_c, refracts=False, refractive_index=1):
        self.ambient_constant = ambient_c
        self.diffuse_constant = diffuse_c
        self.specular_constant = specular_c
        self.shininess = shininess
        self.reflectivity_constant = reflectivity_c
        self.refracts = refracts
        self.refractive_index = refractive_index