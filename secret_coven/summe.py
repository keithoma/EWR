"""
    20190424

    In this module, various methodes to calculate the natural sum to a given integer, that is
    counting up the total sum from 0 to this integer, is presented.

    This was written for the EWR course at Humboldt-University of Berlin.

    Authors:
"""



def partial_sum_formula(goal_number):
    """
        Args:
            goal_number (int): the integer to which we are going to count, note that the input integer
                               is included in the sum
        Returns:
            (int): the solution of the sum
    """

    return int((goal_number * (goal_number + 1)) / 2)    # we need to convert to int, because we
                                                         # don't want to print a decimal number



def summation_with_for(goal_number):
    """
        Args:
            goal_number (int): the integer to which we are going to count, note that the input integer
                               is included in the sum
        Returns:
            (int): the solution of the sum
    """

    total = 0   # we will return this number later

    for intermediate in range(0, goal_number + 1):
        # ^ because of the quirk of range() in python, we have to add a 1 to include the last
        #   number
        total = total + intermediate

    return total



def summation_with_while(goal_number):
    """
        Args:
            goal_number (int): the integer to which we are going to count, note that the input integer
                               is included in the sum
        Returns:
            (int): the solution of the sum
    """

    total = 0           # we will return this number
    intermediate = 0    # and use this number to iterate

    while intermediate < goal_number:
        intermediate = intermediate + 1
        total = total + intermediate

    return total



def take_integer():
    """
        Args:
            none
        Returns:
            (int): the integer the user has input
    """
    while True:
        # ^ force this loop until the user inputs a viable integer

        input_integer = int(input("Please input an integer!\n"))
        # ^ because a string is given by the user, we have to convert it to an int

        # if the integer is viable, we will break the loop here
        if input_integer > 0:
            break

    # after the loop is broken, we will return the integer input by the user
    return input_integer



def main():
    """
        This is the main function of this module. It will ask the user to input an integer and then
        calculates the natural sum.
    """

    # start the module and take the integer from the user
    print("This module will calculate the total sum of all numbers between 0 and the given " +
          "integer\n")
    input_integer = take_integer()

    # print some empty lines to make it more pretty
    print()
    print()

    # print the solutions of the sum obtained by our three functions which hopefully should be the
    # same
    print("Calculated with the partial sum formula: " + str(partial_sum_formula(input_integer)))
    print("Calculated with a for loop: " + str(summation_with_for(input_integer)))
    print("Calculated with a while loop: " + str(summation_with_while(input_integer)))

    # again let's print some empty lines to make it more pretty
    print()
    print()

if __name__ == "__main__":
    main()
