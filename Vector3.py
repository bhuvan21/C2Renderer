'''Contains the Vector3 Class, a helper class for working with vectors with 3 components'''
from math import sqrt

# the Vector3 class can be initialised with 3 separate values, or an array of 3 values
class Vector3():
    def __init__(self, a=0, b=0, c=0, full=[0, 0, 0]):

        if full == [0, 0, 0]:
            self.values = [a, b, c]
        else:
            self.values = full

        # the syntax for dot product with this class is (a*b).product, simply because the syntax read aloud is 'dot product'
        self.product = self.values[0]+self.values[1]+self.values[2]
        
        self.length = sqrt((self.values[0]**2) + (self.values[1]**2) + (self.values[2]**2))

    # returns a normalized version of the vector
    def normalized(self):
        scale_factor = 1.0/self.length
        return scale_factor*self
    
    # returns the cross product of this vector with another
    def cross(self, other):
        cx = (self.values[1]*other.values[2]) - (self.values[2]*other.values[1])
        cy = (self.values[2]*other.values[0]) - (self.values[0]*other.values[2])
        cz = (self.values[0]*other.values[1]) - (self.values[1]*other.values[0])
        return Vector3(cx, cy, cz)

    # implementing basic addition and subtraction of instances of the Vector3 class
    def __add__(self, other):
        
        r = []
        for i in range(3):
            r.append(self.values[i]+other.values[i])
        return Vector3(full=r)
    
    def __sub__(self, other):
        r = []
        for i in range(3):
            r.append(self.values[i]-other.values[i])
        return Vector3(full=r)

    # implements indexing of the Vector3 class
    def __getitem__(self, key):
        return self.values[key]

    # makes Vector3 classes iterable
    def __iter__(self):
        return iter(self.values)

    def __mul__(self, other):
        # this is technically not a proper operation, but in conjunction with '.product' it has the desired effect
        if type(other) == Vector3:
            r = []
            for i in range(3):
                r.append(self.values[i]*other.values[i])
            return Vector3(full=r)
        else:
            # vector3 multiplication by a scalar
            return Vector3(full=[other*y for y in self.values])

    # same as __mul__ but reversed in order
    def __rmul__(self, other):
        if type(other) == Vector3:
            r = []
            for i in range(3):
                r.append(self.values[i]*other.values[i])
            return Vector3(full=r)
        else:

            return Vector3(full=[other*y for y in self.values])
    
    # raising Vector3 instances to a power is now defined (this way)
    def __pow__(self, other):
        return Vector3(full=[other**y for y in self.values])
    
    def __repr__(self):
        return str(self.values)