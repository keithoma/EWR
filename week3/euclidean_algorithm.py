#! /usr/bin/env python3
"""
    In this module, we first implemented the well known Euclidean algorithm which finds the greatest common
    divisor given two integers. From there, we use the result of the aforementioned algorithm to calculate
    the least common multiple.

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



def euclidean_algorithm(first_number, second_number):
    """
        She finds the greatest common divisor with the help of a recursively implemented Euclidean
        algorithm.

        Args:
            first_number (int): the first number
            second_number (int): the second number

        Returns:
            (int): the greatest common divisor of 'first_number' and 'second_number'
    """
    # first of all, break the cycle if we already have a zero
    if second_number == 0:
        return first_number

    # this is the actual part of the algorithm
    # input the 'second_number' as the new first argument and modify the second argument
    return euclidean_algorithm(second_number, first_number % second_number)



def least_common_multiple(first_number, second_number):
    """
        She calculates the least common multiple using the Euclidean algorithm and the well-known formula,
        lcm(a, b) = abs(ab) / gcd(a, b).

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
    print("\n\n")
    print("lcm(12, 3) = {0} (should be 12)".format(least_common_multiple(12, 3)))



if __name__ == "__main__":
    main()
