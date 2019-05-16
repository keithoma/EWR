#! /usr/bin/env python3
"""
    constructed by:
        Christian Parpart (18 56 76)
        Kei Thoma (574 613)
"""

import euclidean_algorithm

def precalc():
    """
    """
    precalc_file = open("euclidean_algorithm_precalculation.txt", "w")
    for number_a in range(2, 2 ** 12):     # 2 ** 12 = 4096
        print(number_a)
        for number_b in range(2, 2 ** 12): # we don't need 0 and 1 because it's trivial
            precalc_file.write(str(euclidean_algorithm.euclidean_algorithm(number_a, number_b)) + "\n")
    precalc_file.close()


def precalc_ggt(first_number, second_number):
    """
    """
    with open("euclidean_algorithm_precalculation.txt", "r") as precalc_file:
        for i, line in enumerate(precalc_file):
            if i == first_number + (2 ** 12) * second_number:
               return line
            elif i > first_number + (2 ** 12) * second_number:
                break

def main():
    """
    """
    # precalc()
    print(precalc_ggt(195, 1287))

if __name__ == "__main__":
    main()
