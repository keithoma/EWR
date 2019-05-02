#! /usr/bin/env python3
"""
    20190416

    This module was written for the EWR course at Humboldt University.
    Given an integer between one and twelve it deduces the number of
    days for the given month.

    Module was constructed by:
    Christian Parpart (185676)
    Kei Thoma (574 613)
"""

def ask_month():
    """
        This function asks the user for an integer between one and twelve.

        Returns:
            (string): The integer is converted into a string, because it's more convenient for the
                      dictionary later on.
    """
    while True:
        try:
            month = int(input('With month number? (1 to 12): '))
            if month >= 1 and month <= 12:
                return month
            raise ValueError
        except ValueError:
            print('Invalid input. Please try again.')

def ask_leap():
    """
        This function asks the user if the year to inspect is a leap year or not and returns a
        boolean accordingly.

        Returns:
            (boolean): True for a leap year and False if not.
    """
    while True:
        leap = input('Is leap? [y|n] ').lower() # this returns only the first letter
        if leap == 'y':
            return True
        elif leap == 'n':
            return False
        print("Invalid input. Please try again.")

def main():
    """
        Our main function.
    """

    print("Hello, I give number days month.\n")

    month = ask_month()
    is_leap = ask_leap()

    if month == 2 and is_leap:
        month = 0 # offset zero points to leap-month's special day count

    day_month = [29, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    print('random number or days: ' + str(day_month[month]))

if __name__ == "__main__":
    main()
