import math

class Points(object):
    def __init__(self, x, y, z):
        # Initialize point coordinates
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, no):
        # Define vector subtraction (returns a new vector)
        return Points(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no):
        # Compute dot product between two vectors
        return ((self.x * no.x) + (self.y * no.y) + (self.z * no.z))

    def cross(self, no):
        # Compute cross product between two vectors
        return Points(
            (self.y * no.z - self.z * no.y),
            (self.z * no.x - self.x * no.z),
            (self.x * no.y - self.y * no.x)
        )

    def absolute(self):
        # Compute magnitude (length) of a vector
        return pow((self.x ** 2 + self.y ** 2 + self.z ** 2), 0.5)


def main():
    points = [[0, 4, 5],
              [1, 7, 6],
              [0, 5, 9],
              [1, 7, 2]
            ]

    # Create Points objects for each coordinate set
    a, b, c, d = Points(*points[0]), Points(*points[1]), Points(*points[2]), Points(*points[3])

    # Calculate normal vectors to the planes:
    # X = AB × BC, Y = BC × CD
    x = (b - a).cross(c - b)
    y = (c - b).cross(d - c)

    # Compute the torsional angle between the planes
    angle = math.acos(x.dot(y) / (x.absolute() * y.absolute()))

    # Convert to degrees and print with 2 decimal places
    print("%.2f" % math.degrees(angle))

if __name__ == '__main__':
    main()