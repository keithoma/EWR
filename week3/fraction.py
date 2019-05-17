#! /usr/bin/env python3
"""
    This module defines the fraction class and implements some useful magic methods.

    Forged by:
        Christian Parpart (185 676)
        Kei Thoma (574 613)

    This file is part of the "Complexity One Horizon" project.
    (c) 2019 Christian Parpart <christian@parpart.family>
    (c) 2019 Kei Thoma <thomakmj@gmail.com>

    Licensed under the MIT License (the "License"); you may not use this file except in compliance with the
    License. You may obtain a copy of the License at: http://opensource.org/licenses/MIT

    “Life is really simple, but we insist on making it complicated.”
    ― Confucius
"""



import euclidean_algorithm



class Fraction:
    """
        This class represents a fraction object.

        Attributes:
            numerator_ (int): the numerator of the fraction object
            denominator_ (int): the denominator of the fraction object
            sign_ (boolean): False for positive (or zero) and True if negative

        Methods:
            reduce_fraction_(self): reduces the given fraction object properly
            sgn_(self): helper function to apply the boolean sign

            get_numerator(self): simply returns numerator_
            get_denominator(self): simply returns denominator_
            get_sign(self): simply returns sign_

            __pos__(self): overloads unary plus operator
            __neg__(self): overloads unary negative operator
            __abs__(self): overloads the absolute function

            __add__(self, other): overloads binary infix plus operator
            __sub__(self, other): overloads binary infix minus operator
            __mul__(self, other): overloads binary infix multiplication operator

            __repr__(): returns a neatly formatted string containing all necessary information to print the
                        fraction
    """
    def __init__(self, numerator, denominator=1):
        """
            The constructor of our Fraction class. She takes two arguments for the numerator and
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
        self.numerator_ = abs(numerator)
        self.denominator_ = abs(denominator)

        # set the sign, False if positive (or zero) and True if negative
        self.sign_ = numerator * denominator < 0

        # finally, reduce the fraction
        self.reduce_fraction_()



    def reduce_fraction_(self):
        """
            This (private) method reduces the fraction using the euclidean algorithm implemented in
            'euclidean_algorithm.py'.
        """
        gcd = euclidean_algorithm.euclidean_algorithm(self.numerator_, self.denominator_)
        if gcd > 1:
            self.numerator_ = int(self.numerator_ / gcd)
            self.denominator_ = int(self.denominator_ / gcd)



    def sgn_(self):
        """
            This (private) method simply applies the sign which should be a boolean by returning 1 or -1
            appropriately.

            Returns:
                (int): 1 for True and -1 for False
        """
        return -1 if self.sign_ else 1



    def get_numerator(self):
        """
            She simply returns numerator_ of the instance.

            Returns:
                self.numerator_ (int): the numerator of the instance
        """
        return self.numerator_



    def get_denominator(self):
        """
           She simply returns denominator_ of the instance.

            Returns:
                self.denominator_ (int): the numerator of the instance
        """
        return self.denominator_



    def get_sign(self):
        """
            She simply returns sign_ of the instance.

            Returns:
                self.sign_ (boolean): the sign of the instance
        """
        return self.sign_



    def __pos__(self):
        """
            She overloads the unary plus operator; not very exciting.

            Returns:
                (Fraction): a new fraction object
        """
        return Fraction(self.numerator_, self.denominator_)



    def __neg__(self):
        """
            She overloads the unary minus operator.

            Returns:
                (Fraction): a new fraction object with inversed sign

        """
        return Fraction(-self.numerator_, self.denominator_)



    def __abs__(self):
        """
            She overloads the absolute value function.

            Returns:
                (Fraction): a new fraction object with False as his sign
        """
        return -self if self.sign_ else self



    def __add__(self, other):
        """
            This magic method overloads the binary infix plus and returns the sum of two fractions as a new
            instance.

            Args:
                self (Fraction): the fraction on the right side; first summand
                other (Fraction): the fraction on the left side; second summand

            Returns:
                (Fraction): the sum of self and other as a new instance of the Fraction class
        """
        # we don't need to optimize here, because we will reduce the fraction at the constructor
        sum_numerator = (self.sgn_() * self.numerator_ * other.denominator_ +
                         self.sgn_() * other.numerator_ * self.denominator_)
        sum_denominator = self.denominator_ * other.denominator_

        return Fraction(sum_numerator, sum_denominator)



    def __sub__(self, other):
        """
            She overloads the binary infix minus.

            Args:
                self (Fraction): the fraction on the right side; the subtrahend
                other (Fraction): the fraction on the left side; the minuend

            Returns:
                (Fraction): the difference of self and other as a new instance of the Fraction class
        """
        return self + (-other)



    def __mul__(self, other):
        """
            She overloads the binary infix multiplication.

            Args:
                self (Fraction): the fraction on the right side; the first factor
	            other (Fraction): the fraction on the left side; the second factor

            Returns:
                (Fraction): the product of self and other as new instance of the Fraction class
        """
        return Fraction(self.numerator_ * other.numerator_, self.denominator_ * other.denominator_)


    def __str__(self):
        """
            This magic methode returns a neatly formated string of the Fraction object which in turn is
            printed out via the usual print() function.

            Returns:
                (string): for example the format of the fraction is '-1/2'
        """
        return "{0}/{1}".format(self.sgn_() * self.numerator_,
                                self.denominator_)



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


if __name__ == "__main__":
    main()
