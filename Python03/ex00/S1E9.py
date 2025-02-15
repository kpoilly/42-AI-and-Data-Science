from abc import ABC, abstractmethod


class Character(ABC):
    """
    An abstract class used to represent a character

Attributes
----------
firt_name: The name of the character.
is_alive: Boolean to tell if the character is alive.

Methods
-------
die():
    sets the is_alive attribute to False
    """
    @abstractmethod
    def __init__(self, first_name, is_alive=True):
        """
Character class constructor.

args:
    first_name (str)
    is_alive (bool, true by default)
        """
        self.first_name = first_name
        self.is_alive = is_alive

    def die(self):
        """
Sets the is_alive attribute to false.
        """
        self.is_alive = False


class Stark(Character):
    """
A class inheriting from the Character class
    """
    def __init__(self, first_name, is_alive=True):
        """
Stark class (inheriting from Character class) constructor.

args:
    first_name (str)
    is_alive (bool, true by default)
        """
        Character.__init__(self, first_name, is_alive)
