"""
    forged by:
    Christian Parpart
    Kei Thoma (574 613)
"""

import collections
import decimal
import numpy as np

# for ease of use
D = decimal.Decimal

# ----------------------------------------------------------------------------------------------------------
# EXERCISE 3
# ----------------------------------------------------------------------------------------------------------

class Equation:
    """
        WRITE THIS.
    """
    def __init__(self, precision):
        self.precision_ = precision
        self.equation_context_ = decimal.Context(precision)

    def change_precision(self, precision):
        self.precision_ = precision
        self.equation_context_.prec = precision

    # @staticmethod
    def left_side(self, x):
        with decimal.localcontext(self.equation_context_):
            return (D('1') / D(str(x))) - D('1') / (D(str(x)) + D('1'))

    # @staticmethod
    def right_side(self, x):
        with decimal.localcontext(self.equation_context_):
            return D('1') / (D(str(x)) * (D(str(x)) + D('1')))

    def absolute_error(self, x):
        with decimal.localcontext(self.equation_context_):
            return abs(self.left_side(x) - self.right_side(x))
    
    def relative_error(self, x):
        with decimal.localcontext(self.equation_context_):
            return abs((self.left_side(x) - self.right_side(x)) / self.right_side(x))

# ----------------------------------------------------------------------------------------------------------
# EXERCISE 2
# ----------------------------------------------------------------------------------------------------------

def explore_machine_epsilon(float_type):
    """
        This little algorithm tries to find the machine precision of the given float type such as
        np.float16 iterativly.

        Arguments:
            float_type (class): the class for the float type we want to inspect; e.g. np.float32

        Returns:
            epsilon (float_type): the machine precision; its data type corresponds to the data type passed
                                  as the argument
    """
    # remember that one can pass functions as arguments in Python
    epsilon = float_type(1.0)

    while float_type(1.0 + epsilon * 0.5) != 1.0:
        epsilon = float_type(epsilon * 0.5)

    return epsilon

def main():
    """
        WRITE THIS.
    """

    if False:
        float_type_list = (np.float16, np.float32, np.float64)  

        print("In the following we print out for each given floating type the name of the type, the precision" +
              "found by the algorithm (see explore_machine_epsilon(float_type), the actual precision given by" +
              "numpy native function 'finfo()' and finally the precision given by the formula " +
              "'eps = 7 / 3 - 4 / 3 - 1')")
        print("\n\n")

        for each in float_type_list:
            # the following is an alternative way to calculate the machine precision; for the validity of this
            # formula see the documentation
            alternative = each(abs(each(7 / 3) - each(4 / 3) - each(1.0)))  

            # padding in the second line added for readability
            # "__name__" returns the name of the class; such as "np.float16"
            print("The machine epsilon for {0} is:".format(each.__name__))
            print("              {0}".format(explore_machine_epsilon(each)))
            print("it should be: {0}".format(np.finfo(each).eps))
            print("alternativly: {0}\n".format(alternative))

    if True:
        print("Now we will test the class Equation.")
        print("\n\n")

        obj1 = Equation(2)
        obj2 = Equation(8)

        for number in range(1, 21):
            print("x = {0}\n".format(number))
            print("precision: {0}".format(obj1.precision_))
            print("left side:  {0}".format(obj1.left_side(number)))
            print("right side: {0}".format(obj1.right_side(number)))
            print("abs error:  {0}".format(obj1.absolute_error(number)))
            print("rel error:  {0}".format(obj1.relative_error(number)))
            print()
            print("precision: {0}".format(obj2.precision_))
            print("left side:  {0}".format(obj2.left_side(number)))
            print("right side: {0}".format(obj2.right_side(number)))
            print("abs error:  {0}".format(obj2.absolute_error(number)))
            print("rel error:  {0}".format(obj2.relative_error(number)))
            print("\n--------------------\n")

if __name__ == "__main__":
    main()
