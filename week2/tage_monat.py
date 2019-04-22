#! /usr/bin/env python3
"""
    20190416

    This module was written for the EWR course at Humboldt University. Given an integer between one and
    twelve it deduces the number of days for the given month.

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
            month = int(input('INTEGER. YOU. WRITE.\n')[0])
            if month < 1 or month > 12:
                print('please do it again, im no patient man\n')
            else:
                break
        except ValueError:
            print('really? be better\n')
    return month - 1    # the zero index points to January

def ask_leap():
    """
        This function asks the user if the year to inspect is a leap year or not and returns a
        boolean accordingly.

        Returns:
            (boolean): True for a leap year and False if not.
    """
    while True:
        leap = input('Is leap?')[0].lower() # this returns only the first letter

        if leap == '' or leap not in ['y', 'n']:
            print("you suck. next time I'll raise error\n")
        else:
            break

    if leap == 'y':
        return True
    elif leap == 'n':
        return False

def main():
    """
        Our main function.
    """

    print("Hello, I give number days month. Input only integer, else I die.\n")

    month = ask_month()
    leap = ask_leap()

    if month == 2 and leap is True:
        month = 13 # 13th month has 29 days

    day_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 29]

    print('random number or days: ' + str(day_month[month]))
    print('me no hablo engles ... bye <3\n\n\n')

if __name__ == "__main__":
    main()
