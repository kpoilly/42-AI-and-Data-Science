from S1E9 import Character


class Baratheon(Character):
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
        Character.__init__(self, first_name, is_alive)
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hairs = "dark"

    def __repr__(self):
        return (f"Vector({self.family_name, self.eyes, self.hairs})")

    def __str__(self):
        status = "is alive" if self.is_alive else "is dead"
        return (f"{self.first_name} Baratheon, {status}.")


class Lannister(Character):
    """
A class representing the Lannister Family,
inheriting from the Character class.
    """
    def __init__(self, first_name, is_alive=True):
        """
Stark class (inheriting from Character class) constructor.

args:
    first_name (str)
    is_alive (bool, true by default)
        """
        Character.__init__(self, first_name, is_alive)
        self.family_name = "Lannister"
        self.eyes = "blue"
        self.hairs = "light"

    def __repr__(self):
        return (f"Vector({self.family_name, self.eyes, self.hairs})")

    def __str__(self):
        status = "is alive" if self.is_alive else "is dead"
        return (f"{self.first_name} Lannister, {status}.")

    @classmethod
    def create_lannister(cls, first_name, is_alive=True):
        return cls(first_name, is_alive)
