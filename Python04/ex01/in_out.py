def square(x: int | float) -> int | float:
    """
Square function
Returns the square of a given number.
    """
    return x * x


def pow(x: int | float) -> int | float:
    """
Power function
Returns the exponentiation of a given number by itself.
    """
    return x ** x


def outer(x: int | float, function) -> object:
    """
Outer function
Takes as argument a number and a function,
and returns an object that when called returns the result of the arguments
calculation.
    """
    def inner() -> float:
        nonlocal x
        res = function(x)
        x = res
        return res
    return inner
