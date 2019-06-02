from time import sleep
from random import randint, uniform

gracz = 'X'
komp = 'O'
POLE = "-"
plansza = [POLE] * 9
wygrane = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8))
win = False


def rysuj_plansze():
    print("\n\t", plansza[0], "|", plansza[1], "|", plansza[2],
          "\n\t", plansza[3], "|", plansza[4], "|", plansza[5],
          "\n\t", plansza[6], "|", plansza[7], "|", plansza[8], "\n")


def check_plansza():
    if POLE not in plansza:
        return False
    return True


def ruch_gracza():
    print("Twoj ruch")
    rysuj_plansze()
    while True:
        if check_plansza():
            ruch = int(input("Podaj numer następnego ruchu od 0 do 8: "))
            if plansza[ruch] == POLE and 0 <= ruch < 9:
                plansza[ruch] = gracz
                break
        else:
            print("Błąd spróbój ponownie")


def ruch_komputera():
    print("Ruch komputera")
    rysuj_plansze()
    set = False
    if check_plansza():
        sleep(uniform(1.2, 4.2))
        if plansza[4] == POLE:
            plansza[4] = komp
            set = not set
        if (plansza[4] == gracz and plansza[8] == gracz) or (plansza[1] == gracz and plansza[2] == gracz) or \
                (plansza[3] == gracz and plansza[6] == gracz) and not set:
            if plansza[0] == POLE:
                plansza[0] = komp
                set = not set
        if (plansza[0] == gracz and plansza[2] == gracz) or (plansza[4] == gracz and plansza[7] == gracz) and not set:
            if plansza[1] == POLE:
                plansza[1] = komp
                set = not set
        if (plansza[0] == gracz and plansza[1] == gracz) or (plansza[4] == gracz and plansza[6] == gracz) or \
                (plansza[5] == gracz and plansza[8] == gracz) and not set:
            if plansza[2] == POLE:
                plansza[2] = komp
                set = not set
        if (plansza[0] == gracz and plansza[6] == gracz) or (plansza[4] == gracz and plansza[5] == gracz) and not set:
            if plansza[3] == POLE:
                plansza[3] = komp
                set = not set
        if (plansza[2] == gracz and plansza[8] == gracz) or (plansza[3] == gracz and plansza[4] == gracz) and not set:
            if plansza[5] == POLE:
                plansza[5] = komp
                set = not set
        if (plansza[0] == gracz and plansza[3] == gracz) or (plansza[4] == gracz and plansza[2] == gracz) or \
                (plansza[7] == gracz and plansza[8] == gracz) and not set:
            if plansza[6] == POLE:
                plansza[6] = komp
                set = not set
        if (plansza[6] == gracz and plansza[8] == gracz) or (plansza[4] == gracz and plansza[1] == gracz) and not set:
            if plansza[8] == POLE:
                plansza[7] = komp
                set = not set
        if (plansza[0] == gracz and plansza[4] == gracz) or (plansza[2] == gracz and plansza[5] == gracz) or (plansza[6] == gracz and plansza[7] == gracz) and not set:
            if plansza[8] == POLE:
                plansza[8] = komp
                set = not set
        if not set:
            ruch = randint(0, 8)
            while plansza[ruch] != POLE:
                ruch = randint(0, 8)
            plansza[ruch] = komp


def jak_grac():
    global win
    win = False
    print(
        """Wybieraj ruch wpisując cyfry na planszy poniżej:
        0 | 1 | 2
        3 | 4 | 5
        6 | 7 | 8
    """)


def wygrana():
    global win
    if not check_plansza():
        win = True
        print("REMIS")
        rysuj_plansze()
        sleep(5)
        return True
    else:
        for mozliwosc in wygrane:
            if plansza[mozliwosc[0]] == plansza[mozliwosc[1]] == plansza[mozliwosc[2]]:
                if plansza[mozliwosc[0]] == komp:
                    win = True
                    print("WYGRYWA KOMPUTERA")
                    rysuj_plansze()
                    sleep(5)
                    return True
                elif plansza[mozliwosc[0]] == gracz:
                    win = True
                    print("WYGRALES!!!")
                    rysuj_plansze()
                    sleep(5)
                    return True
    return False


def main():
    global win, plansza
    while True:
        win = False
        plansza = [POLE] * 9
        while not win:
            for _ in (ruch_gracza(), ruch_komputera()):
                if wygrana():
                    break


if __name__ == '__main__':
    jak_grac()
    main()
