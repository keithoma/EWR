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



import struct



class GreatestCommonDivisor:
    """
        This class is implementing the Euclidean algorithm with ensuring that smaller greatest common
        divisors have complexity O(1), by precomputing all greatest common divisors between 1 and n (with n
        being chosen at the constructor).
        
        The precomputed greatest common divisors are stored in a local file for faster instanciation
        later.
    """
    def __init__(self, _filename, _dim):
        """
        Constructing the greatest common divisor object by either optionally precomputing all greatest common
        divisor between 1 and _dim, and writes them to disk (_filename) for future acess.

        Args:
            _filename (string): the file name
            _dim (int): the largest number to precomputed
        """
        self.dim_ = _dim
        self.filename_ = _filename
        self.num_width_ = 4
        try:
            open(_filename, 'rb').close()
        except:
            self.write_cache()

    @staticmethod
    def compute(a, b):
        """
            Returns the result of the Euclidean algorithm of a and b by actually computing.
        """
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def write_cache_to(filename, dim):
        """
            Class method to populate a cache for O(1) access.
        """
        print("Writing cache of GCD values between {} and {} ...".format(1, dim))
        outfile = open(filename, "wb", True)
        for a in range(1, dim + 1):
            for b in range(1, dim + 1):
                outfile.write(struct.pack("i", GreatestCommonDivisor.compute(a, b)))
        outfile.close()

    def write_cache(self):
        """
            Member method to populate a cache for O(1) access.
        """
        GreatestCommonDivisor.write_cache_to(self.filename_, self.dim_)

    def gcd(self, a, b):
        """
            Computes GCD of `a` and `b` either in O(1) complexity if in range of precomputation,
            or manually computed.
        """
        if a > 0 and a <= self.dim_ and b > 0 and b <= self.dim_:
            infile = open(self.filename_, "rb", True)
            infile.seek((a - 1) * (self.dim_ * self.num_width_) + (b - 1) * self.num_width_)
            data = infile.read(self.num_width_)
            infile.close()
            return struct.unpack("i", data)[0]
        else:
            return GreatestCommonDivisor.compute(a, b)



def euclidean_algorithm(first_number, second_number):
    """
        She returns the result of the Euclidean algorithm by using the GreatestCommonDivisor class.
        This implemention is using local cache for the first 1024 values for each parameter, which is
        located in the current working directory with the filename 'gcd.bin', which is created on demand on
        the first method invocation.

        Args:
            first_number (int): the first number
            second_number (int): the second number

        Returns:
            (int): the greatest common divisor of 'first_number' and 'second_number'
    """
    return GreatestCommonDivisor("gcd.bin", 2 ** 10).gcd(first_number, second_number)



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
