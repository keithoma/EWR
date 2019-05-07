#! /usr/bin/env python3
"""
    constructed by:
    Christian Parpart (18 56 76)
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



    def _apply_sign(self, boolean_sign):
        """
            This (private) method simply applies the sign which should be a boolean by returning
            1 or -1 appropriately. She is should only used in the two functions below.

            Args:
                boolean_sign (boolean): a boolean which should be this class' attribute 'sign'
            
            Returns:
                (int): 1 for True and -1 for False
        """
        return -1 if boolean_sign else 1



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
        new_numerator_self = self._apply_sign(self.sign) * self.numerator * sum_denominator / self.denominator
        new_numerator_other = self._apply_sign(other.sign) * other.numerator * sum_denominator / other.denominator
        sum_numerator = int(new_numerator_self + new_numerator_other)

        return Fraction(sum_numerator, sum_denominator)



    def __repr__(self):
        """
            This magic methode returns a neatly formated string of the Fraction object which in
            turn is printed out via the usual print() function.

            Returns:
                (string): for example the format of the fraction is '-1/2'
        """
        return "{0}/{1}".format(self._apply_sign(self.sign) * self.numerator,
                                self.denominator)

def main():
    """
        Here be dragons.
    """
    test_fraction = Fraction(3, -5)
    another_fraction = Fraction(4, -7)
    sum_fraction = test_fraction + another_fraction

    print("{0} + {1} = {2}".format(test_fraction, another_fraction, sum_fraction))



if __name__ == "__main__":
    main()
