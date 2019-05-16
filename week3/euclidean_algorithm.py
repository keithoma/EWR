#! /usr/bin/env python3
"""
    In this module, we first implement the well known euclidean algorithm where the greatest common divisor
    of two integers is calculated. From there, we use the euclidean algorithm to also define a function to
    find the least common multiple.

    constructed by:
        Christian Parpart (18 56 76)
        Kei Thoma (574 613)
"""



def euclidean_algorithm(first_number, second_number):
    """
        This function finds the greatest common divisor with the help of recursive euclidean
        algorithm.

        Args:
            first_number (int): the first number
            second_number (int): the second number

        Returns:
            (int): the greatest common divisor of 'first_number' and 'second_number'
    """
    # first of all, break the cycle if we already have a zero
    # notice also that without this, we'd get a zero-division error
    if second_number == 0:
        return first_number

    # this is the actual part of the algorithm
    # input the 'second_number' as the new first argument and modify the second argument
    return euclidean_algorithm(second_number, first_number % second_number)



def least_common_multiple(first_number, second_number):
    """
        This one calculates the least common multiple via the greatest common divisor through the
        well known formula, lcm(a, b) = abs(ab) / gcd(a, b).

        Args:
            first_number (int): in the formula this is 'a'
            second_number (int): in the forumula this is 'b'

        Returns:
            (int): the least common divisor
    """
    # we will break up the calculation in few steps due to limited space
    gcd = euclidean_algorithm(first_number, second_number)
    numerator = abs(first_number * second_number)
    return int(numerator / gcd)



def main():
    """
        The main-function for testing purposes.
    """
    print("We will do some tests:")
    print("gcd(195, 1287) = " + str(euclidean_algorithm(195, 1287)) + " (should be 39)")
    print("gcd(13, 17) = " + str(euclidean_algorithm(13, 17)) + " (should be 1)")
    print("gcd(24, 24) = " + str(euclidean_algorithm(24, 24)) + " (should be 24)")
    print("gcd(0, 1) = " + str(euclidean_algorithm(0, 1)) + " (should be 1)")
    print("gcd(0, 2) = " + str(euclidean_algorithm(0, 2)) + " (should be 2)")
    print("gcd(12, 0) = " + str(euclidean_algorithm(12, 0)) + " (should be 12)")
    print("gcd(-195, 1287) = " + str(euclidean_algorithm(12, 0)) + " (should be 12)")
    print("gcd(-195, -1287) = " + str(euclidean_algorithm(12, 0)) + " (should be 12)")



if __name__ == "__main__":
    main()
