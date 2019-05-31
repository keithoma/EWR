"""
This module is equipped with capabilities to take the user's input which is then passed to the functions
implemented in tools4.py. The main purpose of ab4.py is to test the equation
'1/x - 1/(x + 1) = 1/(x * (x + 1))' controlling for x and the mantissa length.

forged by:
    Christian Parpart
    Kei Thoma (574 613)

This file is part of the "The Lost World between Zero and Machine Epsilon" project.
(c) 2019 Christian Parpart <christian@parpart.family>
(c) 2019 Kei Thoma <thomakmj@gmail.com>
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at: http://opensource.org/licenses/MIT
"""


import numpy as np


import tools4


class _EndOfInput(Exception):
    """
    Auxiliary (exception) class for easy out of 'get_uint(prompt_text)'
    """
    pass


def get_uint(prompt_text):
    """
    Auxiliary function. She forces the user to enter a positive integer.

    Arguments:
        prompt_text (string): the string displayed to the user

    Returns:
        num (int): non-zero positive integer input by the user

    Raises:
        _EndOfInput: this is raised when the user wants to exit the application; used to exit the
        application in 'main()'
    """
    while True:
        try:
            line = input("{}: ".format(prompt_text))
            if line in ["", "exit", "quit", "ende", "Thanos did nothing wrong"]:
                raise _EndOfInput
            num = int(line)
            if num > 0:
                return num
            print("Entered value is negative or zero. Try again.")
        except ValueError as err:
            print("Not a number. {}".format(err.args))


def get_x_and_mantissa_length():
    """
    Auxiliary function which returns valid user input using 'get_uint(prompt_text)'

    Arguments:
        nothing

    Returns:
        (int, int): a a pair of two ints input by the user
    """
    user_x = get_uint("Please enter an integer for x")
    significand = get_uint("Please enter an integer for the mantissa length")
    return (user_x, significand)


def precision_calculation(_x, _significand):
    """
    She calculates both errors for a given x and mantissa length ('_significand'). Also draws the plot with
    the mantissa length as the variable.

    Arguments:
        _x (int): an unsigned int for which the equation is evaluated

        _significand (int): an unsigned int for the mantissa length; this is used to calculate the absolute
        and the relative error, but is not used to draw the plot since there the mantissa length is the
        variable

    Returns:
        nothing
    """
    equation = tools4.Equation(_significand)
    print("y = {}".format(equation.left_side(_x)))
    print("z = {}".format(equation.right_side(_x)))
    print()
    print("absolute error: {}".format(equation.absolute_error(_x)))
    print("relative error: {}".format(equation.relative_error(_x)))
    print()
    equation.draw_absolute_error(_x)
    equation.draw_relative_error(_x)

def main():
    """
    The main function. She takes user's input for x and the length of the mantissa to calculate the absolute
    and the relative error. A corresponding graph is also drawn. See the docstring of this module for more
    information.
    """
    print(globals()['__doc__'])

    # explore machine epsilon
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
        print("              {0}".format(tools4.explore_machine_epsilon(each)))
        print("it should be: {0}".format(np.finfo(each).eps))
        print("alternativly: {0}\n".format(alternative))

    try:
        precision_calculation(*get_x_and_mantissa_length())
    except _EndOfInput:
        default_x = 31415
        default_mlen = 80
        print()
        print("There was no input. Continue with example data.")
        print("Set the following variables: x={}, Mantissenlänge={}".format(default_x, default_mlen))
        print()
        precision_calculation(default_x, default_mlen)
        return

    while True:
        try:
            precision_calculation(*get_x_and_mantissa_length())
        except _EndOfInput:
            print("End of Input")
            return

if __name__ == '__main__':
    main()
