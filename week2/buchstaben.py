#! /usr/bin/env python3
"""
    20190416

    This module was written for the EWR course at Humboldt University. Given a string, it returns the
    number of vowels in the string.

    Module was constructed by:
    Christian Parpart (185676)
    Kei Thoma (574 613)
"""

def count_vowels(sentence):
    """
        This function counts the number of vowels.
        Args:
            sentence (string): the string to inspect
        Returns:
            (int): the number of vowels in sentence
    """
    VOWEL_LIST = 'aeiou'

    return sum(letter in VOWEL_LIST for letter in sentence.lower())

def main():
    """
        The main function of or module. It's self-explanatory, really.
    """
    print("Hello, I count vowels.\n")
    sentence = input("GIVE. STRING. NOW.\n")
    print("Some number: " + str(count_vowels(sentence)))

if __name__ == "__main__":
    main()
