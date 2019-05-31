"""
In this module, we implemented the class Equation which represents '1/x - 1/(x + 1) = 1/(x * (x + 1))'.
Each instance of this class is initalized with a fixed mantissa length to evaluate both side of this
equation in order to observe the effect of decimal rounding in the floating point arithmetic.

Furtheremore, we provided a function which approximates machine epsilon for a given floating type such as
np.float16.

forged by:
    Christian Parpart
    Kei Thoma (574 613)

This file is part of the "The Lost World between Zero and Machine Epsilon" project.
(c) 2019 Christian Parpart <christian@parpart.family>
(c) 2019 Kei Thoma <thomakmj@gmail.com>
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at: http://opensource.org/licenses/MIT
"""

import decimal
import numpy as np
import matplotlib.pyplot as plt


# for ease of use
D = decimal.Decimal


# ----------------------------------------------------------------------------------------------------------
# EXERCISE 3
# ----------------------------------------------------------------------------------------------------------


class Equation:
    """
    This is more of an auxiliary class to store the given equation '1/x - 1/(x + 1) = 1/(x * (x + 1))', and
    the two formulas which returns the absolute and the relative error. He can also draw graphs for both of
    the errors.

    Attributes:
        precision_ (int): the precision set for the whole Equation object; every term inside of an Equation
        object adheres to this precision; note that this attribute should be private and must not be changed
        unless 'change_precision(self, _precision)' is called

        equation_context_ (Context): this is the Context object from the decimal library with its 'prec'
        attribute to 'precision_' (see above); again this attribute should be private

    Methods:
        change_precision(self, _precision): changes the precision for the Equation object

        left_side(self, _x): the left side of the equation, '1/x - 1/(x + 1)'

        right_side(self, _x): the right side of the equation, '1/(x * (x + 1))'

        absolute_error(self, _x): the absolute difference of 'left_side(self, _x)' and 'right_side(self,
        _x)'

        relative_error(self, _x): the relative difference of 'left_side(self, _x)' and 'right_side(self,
        _x)'

        draw_absolute_error(self, _x): draws an two dimensional graph of 'absolute_error(self, _x)' for a
        fixed x using matplotlib

        draw_relative_error(self, _x): draws an two dimensional graph of 'relative_error(self, _x)' for a
        fixed x using matplotlib
    """
    def __init__(self, _precision=28):
        """
        She constructs an equation object with respect to the desired precision.

        Arguments:
            _precision (int): the precision for the decimal.Decimal object; must not be zero or negative; is
            directly stored under 'precision_'; the default value is 28, the same as the default value in
            the decimal library

        Returns:
            nothing

        Raises:
            ValueError: if zero or negative values are passed as '_precision'
        """
        if _precision < 1:
            raise ValueError("Class Equation: The precision must not be 0 or negative.")

        # set precision for the equation object locally
        self.precision_ = _precision
        self.equation_context_ = decimal.Context(_precision)


    def change_precision(self, _precision):
        """
        Since merely changing the 'precision_' attribute from the outside won't do anything, this methods
        allows the user to change the precision for a given object by correctly changing the 'prec'
        attribute of the Context object

        Arguments:
            _precision (int): the precision for the decimal.Decimal object; must not be zero or negative; is
            directly stored under 'precision_'

        Returns:
            nothing

        Raises:
            ValueError: if zero or negative values are passed as '_precision'
        """
        if _precision < 1:
            raise ValueError("Class Equation: The precision must not be 0 or negative.")

        self.precision_ = _precision
        self.equation_context_.prec = _precision


    def left_side(self, _x):
        """
        She represents the left side of the equation '1/x - 1/(x + 1)'.

        Arguments:
            _x (int): the value for x; 0 and -1 are not allowed and this function will naturally raise a
            ZeroDivisionError

        Returns:
            (Decimal): the solution for the left side of the equation
        """
        with decimal.localcontext(self.equation_context_):
            return (D('1') / D(str(_x))) - D('1') / (D(str(_x)) + D('1'))


    def right_side(self, _x):
        """
        She represents the left side of the equation '1/x - 1/(x + 1)'.

        Arguments:
            _x (int): the value for x; 0 and -1 are not allowed and this function will naturally raise a
            ZeroDivisionError

        Returns:
            (Decimal): the solution for the right side of the equation
        """
        with decimal.localcontext(self.equation_context_):
            return D('1') / (D(str(_x)) * (D(str(_x)) + D('1')))


    def absolute_error(self, _x):
        """
        This methods computes the absolute difference between 'left_side(self, _x)' and 'right_side(self,
        _x)'.

        Arguments:
            _x (int): the value for x for the equation

        Returns:
            (Decimal): the absolute difference between both side of the equation
        """
        with decimal.localcontext(self.equation_context_):
            return abs(self.left_side(_x) - self.right_side(_x))


    def relative_error(self, _x):
        """
        This methods computes the relative difference between 'left_side(self, _x)' and
        'right_side(self, _x)'.

        Arguments:
            _x (int): the value for x for the equation

        Returns:
            (Decimal): the relative difference between both side of the equation
        """
        with decimal.localcontext(self.equation_context_):
            return abs((self.left_side(_x) - self.right_side(_x)) / self.right_side(_x))



    def draw_absolute_error(self, _x):
        """
        She draws a two dimensional graph of the absolute error of the equation for a fixed x depending on
        the mantissa length.

        Arguments:
            _x (int): the fixed x for which the graph is drawn

        Returns:
            nothing
        """
        # values for the x-axis (mantissa length)
        x_axis = np.arange(1, 28, 1)

        # values for the y-axis (absolute error)
        y_axis = []
        for significand in x_axis:
            self.change_precision(int(significand))
            y_axis.append(self.absolute_error(_x))

        # draw
        fig = plt.figure()
        axe = fig.add_subplot(1, 1, 1)

        axe.set_title("absolute error for x = " + str(_x))
        axe.set_xlabel("mantissa length")
        axe.set_ylabel("absolute error")

        plt.plot(x_axis, y_axis)
        plt.show()


    def draw_relative_error(self, _x):
        """
        She draws a two dimensional graph of the relative error of the equation for a fixed x depending on
        the mantissa length.

        Arguments:
            _x (int): the fixed x for which the graph is drawn

        Returns:
            nothing
        """
        # values for the x-axis (mantissa length)
        x_axis = np.arange(1, 28, 1)

        # values for the y-axis (relative error)
        y_axis = []
        for significand in x_axis:
            self.change_precision(int(significand))
            y_axis.append(self.relative_error(_x))

        # draw
        fig = plt.figure()
        axe = fig.add_subplot(1, 1, 1)

        axe.set_title("relative error for x = " + str(_x))
        axe.set_xlabel("mantissa length")
        axe.set_ylabel("relative error")

        plt.plot(x_axis, y_axis)
        plt.show()


# ----------------------------------------------------------------------------------------------------------
# EXERCISE 2
# ----------------------------------------------------------------------------------------------------------


def explore_machine_epsilon(float_type):
    """
    This little algorithm tries to find the machine precision of the given float type, such as np.float16,
    iterativly.

    Arguments:
        float_type (class): the class for the float type we want to inspect e.g. np.float32;

    Returns:
        epsilon (float_type): the machine precision; its data type corresponds to the data type passed
        as the argument
    """
    epsilon = float_type(1.0)

    while float_type(1.0 + epsilon * 0.5) != 1.0:
        epsilon = float_type(epsilon * 0.5)

    return epsilon

def main():
    """
    She is our main-function. Use the switch, 'test_switch', to test various capabilities of this module.
    (See the docstring for more information.)
    """
    # set here what to test
    test_switch = {'epsilon': False, 'equation': False, 'draw': True}

    print(globals()['__doc__'])

    # test here the machine precision of different data types
    if test_switch['epsilon']:
        float_type_list = (np.float16, np.float32, np.float64)

        print("In the following we print out for each given floating type the name of the type, the" +
              "precision found by the algorithm (see explore_machine_epsilon(float_type), the actual" +
              "precision given by numpy native function 'finfo()' and finally the precision given by the" +
              "formula eps = 7 / 3 - 4 / 3 - 1')")
        print("\n\n")

        for each in float_type_list:
            # the following is an alternative way to calculate the machine precision; for the validity of
            # this formula see the documentation
            alternative = each(abs(each(7 / 3) - each(4 / 3) - each(1.0)))

            # padding in the second line added for readability
            # "__name__" returns the name of the class; such as "np.float16"
            print("The machine epsilon for {0} is:".format(each.__name__))
            print("              {0}".format(explore_machine_epsilon(each)))
            print("it should be: {0}".format(np.finfo(each).eps))
            print("alternativly: {0}\n".format(alternative))

        print("\n\n")

    # test here the Equation class
    if test_switch['equation']:
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

        print("\n\n")

    # here, we draw the graphs for the absolute and the relative errors
    if test_switch['draw']:
        draw_graph_x = 5
        print("We will draw the graph for x = {0}".format(draw_graph_x))
        obj3 = Equation()
        obj3.draw_absolute_error(draw_graph_x)
        obj3.draw_relative_error(draw_graph_x)
        print("\n\n")


if __name__ == "__main__":
    main()
