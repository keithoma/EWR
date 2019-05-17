#! /usr/bin/env python3

import struct

class GreatestCommonDivisor:
    def __init__(self, _filename, _dim):
        self.dim_ = _dim
        self.filename_ = _filename
        self.num_width_ = 4
        try: 
            print("Try reading cache first")
            fh = open(_filename, 'rb') 
            fh.close()
        except: 
            self.write_cache()

    @staticmethod
    def compute(a, b):
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
                n = outfile.write(struct.pack("i", GreatestCommonDivisor.compute(a, b)))
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

gcd = GreatestCommonDivisor("gcd.bin", 1000)

def gcd_o1(a, b):
    c = gcd.gcd(a, b)
    print("gcd_precomputed({}, {}) = {}".format(a, b, c))

gcd_o1(10, 5)
gcd_o1(81, 72)
gcd_o1(1200, 700)
