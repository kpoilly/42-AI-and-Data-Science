from S1E7 import Baratheon, Lannister


class King(Baratheon, Lannister):
    """
A class representing the Baratheon Family,
inheriting from the Character class.
    """
    def __init__(self, first_name, is_alive=True):
        """
Stark class (inheriting from Character class) constructor.

args:
    first_name (str)
    is_alive (bool, true by default)
        """
        super().__init__(first_name, is_alive)
        self.family_name = "Baratheon"

    def __repr__(self):
        return (f"Vector({self.family_name, self.eyes, self.hairs})")

    def __str__(self):
        status = "is alive" if self.is_alive else "is dead"
        return (f"{self.first_name} Baratheon, {status}.")

    def set_eyes(self, color):
        self.eyes = color

    def set_hairs(self, color):
        self.hairs = color

    def get_eyes(self):
        return self.eyes

    def get_hairs(self):
        return self.hairs
