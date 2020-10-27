# C2Renderer
A simple ray tracing renderer written in python.   


![Refraction Image](https://github.com/bhuvan21/C2Renderer/blob/master/refrac.png?raw=true)


  
Includes the following features:
- Light sources
- Sphere geometry
- STL geometry
- Diffuse, specular and ambient light (Phong's Illumination Model)
- Shadows
- Reflective materials
- Refractive materials
- Anti-aliasing
- Parallel processing

## How does it work?
The basic premise is as follows. Rays are cast out from the camera position through the image plane. A ray is cast for each pixel (or more than one when anti-aliasing). Each ray is tested against every object in the scene. When an intersection is found, the base pixel color is calculated using the Phong Illumination model. If the material is refractive or reflective, the base pixel color is adjusted by recursively casting further rays, simulating the reflection/refraction of light.
There are of course some complexities involved in all of this, but that is the main gist.

## How can I use it?
Simply clone the repository, and adjust the bottom most part of "main.py".
The comments in the file should make it clear how to use the renderer.
