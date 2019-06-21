#! /usr/bin/env python3
# vim:ai:et

"""
    Dieses Programm analysiert eine Liste von Zahlen und gibt deren größte,
    kleinste Zahl aus, sowie die Anzahl der einzigartigen Zahlen.
"""

def get_numbers(count):
    """
    Verlangt vom Benutzer {count} Zahlen und hört nicht eher auf bis er diese hat,
    und gibt sie dann zurück.
    """
    zahlen = []
    while len(zahlen) < count:
        try:
            num_missing = count - len(zahlen)
            prompt = "Ich benoetige noch {}/{} Zahlen. Gib mir eine Zahl: "
            number = int(input(prompt.format(num_missing, count)))
            zahlen.append(number)
        except ValueError as error:
            print("Fehler in der Eingabe. {}".format(error.args))
    return zahlen

def maxmin(zahlen):
    """
    Programm zum Vergleich verschiedener Zahlen
    Input: zahlen (list of ints)
        -- Liste mit mindestens 5 ganzen Zahlen
    Returns: Triple of ints
        -- Triple: groesste Zahl, kleinste Zahl, Anz. versch. Zahlen)
    """

    biggest = max(zahlen)
    smallest = min(zahlen)
    uniques = set(zahlen)

    return (biggest, smallest, uniques)

def main():
    """
    Hauptprogramm: Interaktion mit dem Nutzer (Eingabe von
                   Daten, Ausgabe des Programmes), Aufruf von maxmin()
    kein Input (lediglich den von stdin)
    kein return ()
    """

    # Gebe die Programmbeschreibung aus.
    # -- ich benutze hier globals() um explizit auf den global scope aufmerksam zu machen.
    print(globals()['__doc__'])

    zahlen = get_numbers(5)
    biggest, smallest, uniques = maxmin(zahlen)

    print()
    print("Deine Eingabe: {}".format(zahlen))
    print("Die groesste Zahl lautet: {}".format(biggest))
    print("Die kleinste Zahl lautet: {}".format(smallest))
    print("Anzahl unterschiedlicher Zahlen: {} (und zwar: {})".format(len(uniques), uniques))

if __name__ == '__main__':
    main()
