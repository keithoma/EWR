"""
    forged by:
    Christian Parpart
    Kei Thoma (574 613)
"""

import numpy as np

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
    epsilon = float_type(1.0)

    while float_type(1.0 + epsilon * 0.5) != 1.0:
        epsilon = float_type(epsilon * 0.5)

    return epsilon

def main():
    """
        The main function for testing purposes.
    """
    list_to_test = [np.float16, np.float32, np.float64]

    for each in float_type_list:
        # padding in the second line added for readability 
        # "__name__" returns the name of the class; such as "np.float16"
        print("The machine epsilon for {0} is:".format(each.__name__))
        print("              {0}".format(explore_machine_epsilon(each)))
        print("it should be: {0}\n".format(np.finfo(each).eps))


if __name__ == "__main__":
    main()
