#! /usr/bin/env python3
"""
    A small calculator for adding two fractions together.

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



import fraction



def interpret(user_input):
    """
        This function constructs a fraction object according to the string passed.

        Args:
            user_input (string): the string entered to the console by the user

        Returns:
            (Fraction): the Fraction object constructed by the user's input

        Raise:
            ValueError: if the input has multiple separators; or if a non-integer is input by the user
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

        solution = interpret(input("The first fraction: ")) + interpret(input("The second fraction: "))
        print("The additive solution is: {0} \n\n".format(solution))

        if input("Exit [y|n]? ").lower()[0] == "y":
            break



if __name__ == "__main__":
    main()
