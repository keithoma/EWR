"""
    forged by:
    Christian Parpart
    Kei Thoma (574 613)
"""


# ----------------------------------------------------------------------------------------------------------
# FRAGEN AN CHRIS
# ----------------------------------------------------------------------------------------------------------

# in class Equation, würde es nicht besser sein wenn die Funktionen static oder class methods wären?
# in main() teste ich verschiedene Sachen aus und habe gerade ein if-Switch, der bestimmt von Pylint bemäckert wird
# wie macht man solche Sachen am besten?


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
        WRITE THIS.
    """
    def __init__(self, _precision = 9, _default_x = None):

        # set precision for the equation object locally
        self.precision_ = _precision
        self.equation_context_ = decimal.Context(_precision)

        self.default_x = _default_x


    def change_precision(self, _precision):
        self.precision_ = _precision
        self.equation_context_.prec = _precision


    def left_side(self, _x = None):
        _x = self.default_x if _x is None else _x
        with decimal.localcontext(self.equation_context_):
            return (D('1') / D(str(_x))) - D('1') / (D(str(_x)) + D('1'))


    def right_side(self, _x = None):
        _x = self.default_x if _x is None else _x
        with decimal.localcontext(self.equation_context_):
            return D('1') / (D(str(_x)) * (D(str(_x)) + D('1')))


    def absolute_error(self, _x = None):
        _x = self.default_x if _x is None else _x
        with decimal.localcontext(self.equation_context_):
            return abs(self.left_side(_x) - self.right_side(_x))


    def relative_error(self, _x = None):
        _x = self.default_x if _x is None else _x
        with decimal.localcontext(self.equation_context_):
            return abs((self.left_side(_x) - self.right_side(_x)) / self.right_side(_x))



    def draw_absolute_error(self, _x = None):
        """Zeichnet einen Graph für den absoluten Fehler für eine gegebenen
        Variable in Abhängigkeit von der Mantissenlänge.
        Args:
            vari (float): die Variable wofür die Abweichung der zwei Gleichungen
                          berechnet werden soll
        To-Do:
        * Der Graph muss noch für die relative Abhängigkeit gezeichnet werden.
        * Der Graph brauch noch Labels wahrscheinlich.
        """
        _x = self.default_x if _x is None else _x

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


    def draw_relative_error(self, _x = None):
        """Zeichnet einen Graph für den relativen Fehler für eine gegebenen
        Variable in Abhängigkeit von der Mantissenlänge.
        Args:
            vari (float): die Variable wofür die Abweichung der zwei Gleichungen
                          berechnet werden soll
        To-Do:
        * Der Graph muss noch für die relative Abhängigkeit gezeichnet werden.
        * Der Graph brauch noch Labels wahrscheinlich.
        """
        _x = self.default_x if _x is None else _x
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


    if False:
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


    if True:
        obj = Equation(1)
        obj.draw_absolute_error(5)
        obj.draw_relative_error(5)




if __name__ == "__main__":
    main()
