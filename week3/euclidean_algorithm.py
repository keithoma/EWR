"""
    constructed by:
    Christian Parpart (XXX XXX)
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
    else:
        return euclidean_algorithm(second_number, first_number % second_number)



def least_common_multiple(first_number, second_number):
    """
        some text
    """

    # we will break up the calculation in few steps due to limited space
    gcd = euclidean_algorithm(first_number, second_number)
    numerator = abs(first_number * second_number)
    return int(gcd / numerator)


def main():
    pass



if __name__ == "__main__":
    main()
