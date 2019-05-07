#! /usr/bin/env python3
"""
    constructed by:
    Christian Parpart (XXX XXX)
    Kei Thoma (574613)
"""

import euclidean_algorithm

class Fraction:
    """
        OMG FILL ME NOW, BABY ONE MORE TIME. :-*
    """
    def __init__(self, numerator, denominator=1):
        """
            The constructor of our fraction object. She takes two arguments for the numerator and denominator; the sign is deduced from the arguments.

            Args:
                numerator (int): a whole number which becomes our (unsigned) numerator
                denominator (int): a whole number which becomes our (unsigned) denominator

            Raise:
                ZeroDivisionError: if 0 is taken as the denominator
        """
        # we don't want 0 as our denominator
        if denominator == 0:
            raise ZeroDivisionError

        # since we will have an attribute representing the sign, we only need absolute values for the numerator and the denominator
        self.numerator = abs(numerator)
        self.denominator = abs(denominator)

        # set the sign, False if positive (or zero) and True if negative
        self.sign = numerator * denominator < 0

        # finally, reduce the fraction
        self.reduce_fraction()

    def reduce_fraction(self):
        """
            This method reduces the fraction using the euclidean algorithm implemented in
            'euclidean_algorithm.py'.
        """
        gcd = euclidean_algorithm.euclidean_algorithm(self.numerator, self.denominator)
        if gcd > 1:
            self.numerator = int(self.numerator / gcd)
            self.denominator = int(self.denominator / gcd)



    def __add__(self, other):
        """
        """
        def convert_sign(boolean_sign):
            """
            """
            if boolean_sign is False:
                return 1
            else:
                return -1

        # we find the denominator with the "least_common_multiple()" function
        sum_denominator = euclidean_algorithm.least_common_multiple(self.denominator, other.denominator)

        # here, we find the numerator of our new fraction; the calculation is broken up in few pieces
        new_numerator_self = convert_sign(self.sign) * self.numerator * sum_denominator / self.denominator
        new_numerator_other = convert_sign(other.sign) * other.numerator * sum_denominator / other.denominator
        sum_numerator = int(new_numerator_self + new_numerator_other)

        return Fraction(sum_numerator, sum_denominator)

def main():
    """
        Here be dragons.
    """
    test_fraction = Fraction(1, 3)
    another_fraction = Fraction(1, 2)
    sum_fraction = test_fraction + another_fraction
    print(sum_fraction.numerator)
    print(sum_fraction.denominator)
    print(sum_fraction.sign)



if __name__ == "__main__":
    main()
