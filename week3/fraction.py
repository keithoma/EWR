#! /usr/bin/env python3
"""
    This module defines the fraction class and implements some useful magic methods.

    constructed by:
        Christian Parpart (18 56 76)
        Kei Thoma (574 613)
"""



import euclidean_algorithm



class Fraction:
    """
        This class represents a fraction object.

        Attributes:
            numerator (int): the numerator of the fraction object
            denominator (int): the denominator of the fraction object
            sign (boolean): False for positive (or zero) and True if negative

        Methods:
            reduce_fraction_(): reduces the given fraction object properly
            sgn_(): helper function to apply the boolean sign
            __add__(): adds two fraction object correctly
            __repr__(): prints a fraction object neatly into the console
    """
    def __init__(self, numerator, denominator=1):
        """
            The constructor of our fraction object. She takes two arguments for the numerator and
            denominator; the sign is deduced from the arguments.

            Args:
                numerator (int): a whole number which becomes our (unsigned) numerator
                denominator (int): a whole number which becomes our (unsigned) denominator

            Raise:
                ZeroDivisionError: if 0 is taken as the denominator
        """
        # we don't want 0 as our denominator
        if denominator == 0:
            raise ZeroDivisionError

        # since we will have an attribute representing the sign,
        # we only need absolute values for the numerator and the denominator
        self.numerator = abs(numerator)
        self.denominator = abs(denominator)

        # set the sign, False if positive (or zero) and True if negative
        self.sign = numerator * denominator < 0

        # finally, reduce the fraction
        self.reduce_fraction_()



    def reduce_fraction_(self):
        """
            This (private) method reduces the fraction using the euclidean algorithm implemented in
            'euclidean_algorithm.py'.
        """
        gcd = euclidean_algorithm.euclidean_algorithm(self.numerator, self.denominator)
        if gcd > 1:
            self.numerator = int(self.numerator / gcd)
            self.denominator = int(self.denominator / gcd)



    def sgn_(self):
        """
            This (private) method simply applies the sign which should be a boolean by returning 1 or -1
            appropriately.

            Returns:
                (int): 1 for True and -1 for False
        """
        return -1 if self.sign else 1



    def inverse_fraction_(self):
        """
            A little (private) function who returns the multiplicative inverse of a fraction e.g. given 2/3
            she would return 3/2.

            Returns:
                (Fraction): the multiplicative inverse of self
        """
        return Fraction(self.sgn_() * self.denominator, self.numerator)



    def __pos__(self):
        """
            She overloads the unitary '+' operator; not very exciting.

            Returns:
                (Fraction): unchanged self
        """
        return self



    def __neg__(self):
        return Fraction(-self.sgn_() * self.numerator, self.denominator)



    def __abs__(self):
        # there must be a way to make this code cleaner
        if self.sign is False:
            return self
        return -self



    def __add__(self, other):
        """
            This magic methodes adds two objects of this Fraction class.

            Args:
                other (Fraction): the second fraction to be added to the object of this class

            Returns:
                (Fraction): the sum of the two fraction as a new Fraction object
        """
        # we find the denominator with the "least_common_multiple()" function
        sum_denominator = euclidean_algorithm.least_common_multiple(self.denominator, other.denominator)

        # here, we find the numerator of our new fraction; the calculation is broken up in few pieces
        new_numerator_self = self.sgn_() * self.numerator * sum_denominator / self.denominator
        new_numerator_other = other.sgn_() * other.numerator * sum_denominator / other.denominator
        sum_numerator = int(new_numerator_self + new_numerator_other)

        return Fraction(sum_numerator, sum_denominator)



    def __sub__(self, other):
        return self + (-other)



    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)



    def __truediv__(self, other):
        return self * other.inverse_fraction_()



    def __str__(self):
        """
            This magic methode returns a neatly formated string of the Fraction object which in turn is
            printed out via the usual print() function.

            Returns:
                (string): for example the format of the fraction is '-1/2'
        """
        return "{0}/{1}".format(self.sgn_() * self.numerator,
                                self.denominator)



def main():
    """
        The main-function for testing purposes.
    """
    test_fraction = Fraction(3, -5)
    another_fraction = Fraction(4, -7)
    sum_fraction = test_fraction + another_fraction

    print("{0} + {1} = {2}".format(test_fraction, another_fraction, sum_fraction))
    print("+{0} = {1}".format(test_fraction, +test_fraction))
    print("-{0} = {1}".format(test_fraction, -test_fraction))
    print("abs({0}) = {1}".format(test_fraction, abs(test_fraction)))
    print("{0} - {1} = {2}".format(test_fraction, another_fraction, test_fraction - another_fraction))
    print("{0} * {1} = {2}".format(test_fraction, another_fraction, test_fraction * another_fraction))
    print("{0} / {1} = {2}".format(test_fraction, another_fraction, test_fraction / another_fraction))



if __name__ == "__main__":
    main()
