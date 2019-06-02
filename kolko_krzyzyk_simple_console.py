from time import sleep
from random import randint, uniform

znaczniki = ('X', 'O', '-')
plansza = [znaczniki[2]] * 9
wygrane = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8))
win = False


def rysuj_plansze():
    print("\n\t", plansza[0], "|", plansza[1], "|", plansza[2],
          "\n\t", plansza[3], "|", plansza[4], "|", plansza[5],
          "\n\t", plansza[6], "|", plansza[7], "|", plansza[8], "\n")


def check_plansza():
    if znaczniki[2] not in plansza:
        return False
    return True


def ruch_gracza():
    print("Twoj ruch")
    rysuj_plansze()
    while True:
        if check_plansza():
            ruch = int(input("Podaj numer następnego ruchu od 0 do 8: "))
            if plansza[ruch] == znaczniki[2] and 0 <= ruch < 9:
                plansza[ruch] = znaczniki[0]
                break
        else:
            print("Błąd spróbój ponownie")


def ruch_komutera():
    print("Ruch znaczniki[1]utera")
    rysuj_plansze()
    set = False
    if check_plansza():
        sleep(uniform(1.2, 4.2))
        if plansza[4] == znaczniki[2]:
            plansza[4] = znaczniki[1]
            set = not set
        if (plansza[4] == znaczniki[0] and plansza[8] == znaczniki[0]) or (plansza[1] == znaczniki[0] and plansza[2] == znaczniki[0]) or \
                (plansza[3] == znaczniki[0] and plansza[6] == znaczniki[0]) and not set:
            if plansza[0] == znaczniki[2]:
                plansza[0] = znaczniki[1]
                set = not set
        if (plansza[0] == znaczniki[0] and plansza[2] == znaczniki[0]) or (plansza[4] == znaczniki[0] and plansza[7] == znaczniki[0]) and not set:
            if plansza[1] == znaczniki[2]:
                plansza[1] = znaczniki[1]
                set = not set
        if (plansza[0] == znaczniki[0] and plansza[1] == znaczniki[0]) or (plansza[4] == znaczniki[0] and plansza[6] == znaczniki[0]) or \
                (plansza[5] == znaczniki[0] and plansza[8] == znaczniki[0]) and not set:
            if plansza[2] == znaczniki[2]:
                plansza[2] = znaczniki[1]
                set = not set
        if (plansza[0] == znaczniki[0] and plansza[6] == znaczniki[0]) or (plansza[4] == znaczniki[0] and plansza[5] == znaczniki[0]) and not set:
            if plansza[3] == znaczniki[2]:
                plansza[3] = znaczniki[1]
                set = not set
        if (plansza[2] == znaczniki[0] and plansza[8] == znaczniki[0]) or (plansza[3] == znaczniki[0] and plansza[4] == znaczniki[0]) and not set:
            if plansza[5] == znaczniki[2]:
                plansza[5] = znaczniki[1]
                set = not set
        if (plansza[0] == znaczniki[0] and plansza[3] == znaczniki[0]) or (plansza[4] == znaczniki[0] and plansza[2] == znaczniki[0]) or \
                (plansza[7] == znaczniki[0] and plansza[8] == znaczniki[0]) and not set:
            if plansza[6] == znaczniki[2]:
                plansza[6] = znaczniki[1]
                set = not set
        if (plansza[6] == znaczniki[0] and plansza[8] == znaczniki[0]) or (plansza[4] == znaczniki[0] and plansza[1] == znaczniki[0]) and not set:
            if plansza[8] == znaczniki[2]:
                plansza[7] = znaczniki[1]
                set = not set
        if (plansza[0] == znaczniki[0] and plansza[4] == znaczniki[0]) or (plansza[2] == znaczniki[0] and plansza[5] == znaczniki[0]) or (plansza[6] == znaczniki[0] and plansza[7] == znaczniki[0]) and not set:
            if plansza[8] == znaczniki[2]:
                plansza[8] = znaczniki[1]
                set = not set
        if not set:
            ruch = randint(0, 8)
            while plansza[ruch] != znaczniki[2]:
                ruch = randint(0, 8)
            plansza[ruch] = znaczniki[1]


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
                if plansza[mozliwosc[0]] == znaczniki[1]:
                    win = True
                    print("WYGRYWA znaczniki[1]UTERA")
                    rysuj_plansze()
                    sleep(5)
                    return True
                elif plansza[mozliwosc[0]] == znaczniki[0]:
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
        plansza = [znaczniki[2]] * 9
        while not win:
            for _ in (ruch_gracza(), ruch_komutera()):
                if wygrana():
                    break


if __name__ == '__main__':
    jak_grac()
    main()
