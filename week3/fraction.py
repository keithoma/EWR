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
        if denominator == 0:
            raise ZeroDivisionError

        self.numerator = abs(numerator)
        self.denominator = abs(denominator)

        # set the sign, True if positive (or zero) and False if negative
        self.sign = False
        if numerator * denominator >= 0:
            self.sign = True

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

def main():
    """
        Here be dragons.
    """
    test_fraction = Fraction(-15, -3)
    print(test_fraction.numerator)
    print(test_fraction.denominator)
    print(test_fraction.sign)

if __name__ == "__main__":
    main()
