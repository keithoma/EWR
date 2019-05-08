#! /usr/bin/env python3
"""
    constructed by:
    Christian Parpart (18 56 76)
    Kei Thoma (574613)
"""



import fraction



def interpret(user_input):
    """
        Args:
            input (string): the string entered to the console by the user

        Returns:
            (Fraction): the Fraction object constructed by the user's input

        Raise:
            ValueError: if the input has multiple separators
    """
    user_input = user_input.split("/")

    if len(user_input) > 2:
        raise ValueError("I can't read that.")

    return fraction.Fraction(int(user_input[0]), int(user_input[1]))



def main():
    """
        Our looping calculator.
    """
    while True:
        print("I can add two fractions!")

        solution = interpret(input("The first fraction: ")) +
                   interpret(input("The second fraction: "))
        print("The solution is: {0} \n\n".format(solution))

        if input("Exit?").lower()[0] == "y":
            break



if __name__ == "__main__":
    main()
