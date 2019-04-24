"""
Aufgabe 2.1 -- Buchstaben

Author: Robert Bedard
"""

def wie_viele_vokale(wort):
    """
        zaehlt die vokale
    """
    vokale = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    anzahl = 0
    for buchstabe in wort:
        if buchstabe in vokale:
            anzahl = anzahl + 1
        list(wort).pop(0)
    return anzahl

print(wie_viele_vokale("Hallo, dieser Satz hat viele Vokale!"))
