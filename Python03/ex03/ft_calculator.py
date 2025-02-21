class calculator:
    """
A class representing a calculator able to do calculations
of vector with a scalar.
Methods:
    +, *, -, /
    """
    def __init__(self, vector):
        self.vector = vector

    def __add__(self, object) -> None:
        for elem in range(len(self.vector)):
            self.vector[elem] += object
        print(self.vector)

    def __mul__(self, object) -> None:
        for elem in range(len(self.vector)):
            self.vector[elem] *= object
        print(self.vector)

    def __sub__(self, object) -> None:
        for elem in range(len(self.vector)):
            self.vector[elem] -= object
        print(self.vector)

    def __truediv__(self, object) -> None:
        for elem in range(len(self.vector)):
            self.vector[elem] /= object
        print(self.vector)
