class calculator:
    """
A class representing a calculator able to do calculations
of 2 vectors.

Methods:
    dotproduct
    add_vec
    sous_vec
    """
    @staticmethod
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        """
    Method of the calculator class.

    Arguments:
        2 lists of floats.
    Return:
        Prints the dot product of the 2 lists
        """
        dp = 0
        for elem in range(len(V1)):
            dp += V1[elem] * V2[elem]
        print(f"Dot product is: {dp}")

    @staticmethod
    def add_vec(V1: list[float], V2: list[float]) -> None:
        """
    Method of the calculator class.

    Arguments:
        2 lists of floats.
    Return:
        Prints the addition of the 2 lists
        """
        V3 = [0.0] * len(V1)
        for elem in range(len(V1)):
            V3[elem] = float(V1[elem]) + float(V2[elem])
        print(f"Add Vector is : {V3}")

    @staticmethod
    def sous_vec(V1: list[float], V2: list[float]) -> None:
        """
    Method of the calculator class.

    Arguments:
        2 lists of floats.
    Return:
        Prints the soustraction of the 2 lists
        """
        V3 = [0.0] * len(V1)
        for elem in range(len(V1)):
            V3[elem] = float(V1[elem]) - float(V2[elem])
        print(f"Add Vector is : {V3}")
