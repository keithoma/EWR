"""
20190416

This module was written for the EWR course at Humboldt University. Given a string, it returns the
number of vowels in the string.

Module was constructed by:
Christian Parpart (XXXXX)
Kei Thoma (574 613)
"""



VOWEL_LIST = ['a', 'e', 'i', 'o', 'u']



def count_vowels(sentence):
    """ This function counts the number of vowels.
    Args:
        sentence (string): the string to inspect
    Returns:
        (int): the number of vowels in sentence
    """
    return sum(letter in VOWEL_LIST for letter in sentence)



def main():
    """ The main function of or module. It's self-explanatory, really.
    """
    print("Hello, I count vowels.\n")
    sentence = input("GIVE. STRING. NOW.\n")
    print("Some number: " + str(count_vowels(sentence)))



if __name__ == "__main__":
    main()
