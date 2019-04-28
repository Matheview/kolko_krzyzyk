# -*- coding: utf-8 -*-

import pygame
import pygame.locals
from random import randrange, randint
from time import sleep

kol_czarny = (0, 0, 0)
kol_szary = (220, 220, 220)
kol_szary_akt = (200, 200, 200)
kol_czerwony = (255, 40, 40)
kol_zielony = (40, 255, 40)
kol_niebieski = (40, 40, 255)
wybor = ["łatwy", "średni", "trudny"]
choose = {False: 'gracz', True: 'komputer'}


class Plansza(object):

    def __init__(self, width):
        self.plansza = pygame.display.set_mode((width, width), 0, 32)
        self.wielkosc = self.plansza.get_width()
        self.poziom = [False, '', False]
        pygame.display.set_caption('Kółko i krzyżyk')
        pygame.font.init()
        self.fps_clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.match_font('Arial'), int(width/5))
        self.znaczniki = [None] * 9
        self.clicked = 0
        self.gracz = 'X'
        self.komp = 'O'
        self.runda = [0, 2]

    def rysuj(self, *args):
        if self.poziom[1] == '':
            self.plansza.fill(kol_czarny)
            self.wybor_poz_trudnosci()
            self.poziom[2] = False
            pygame.display.update()
        else:
            self.poziom[2] = True
            self.plansza.fill(kol_szary)
            self.rysuj_siatke()
            self.rysuj_znaczniki()
            self.wyswietl_wynik()
            for arg in args:
                arg.draw_on(self.plansza)
            pygame.display.update()

    def przycisk(self, tekst, x, y, width, height):
        myszka = pygame.mouse.get_pos()
        klik = pygame.mouse.get_pressed()
        kolor = kol_szary
        if x + width > myszka[0] > x and y + height > myszka[1] > y:
            kolor = kol_szary_akt
            if bool(klik[0])and self.clicked == 0:
                if tekst in wybor:
                    self.poziom[1] = tekst
                    self.rysuj()
                elif tekst in choose[self.poziom[0]]:
                    self.poziom[0] = not self.poziom[0]
                self.clicked = 1
            if not bool(klik[0]):
                self.clicked = 0
        pygame.draw.rect(self.plansza, kolor, (x, y, width, height))
        self.renderuj_tekst(tekst, x, y, width, height, kol_czarny, 7)

    def renderuj_tekst(self, tekst, x, y, width, height, kolor, font_size_par):
        font = pygame.font.Font(pygame.font.match_font('Arial'), int(width / font_size_par))
        tekst = font.render(tekst, True, kolor)
        pole_przycisk = tekst.get_rect()
        pole_przycisk.center = ((x + (width / 2)), (y + (height / 2)))
        self.plansza.blit(tekst, pole_przycisk)

    def wybor_poz_trudnosci(self):
        self.plansza.fill(kol_czarny)
        self.renderuj_tekst("Wybierz poziom trudności", self.wielkosc / 4, self.wielkosc / 60, self.wielkosc/2,
                            self.wielkosc / 7, kol_szary, 6)
        for num, text in enumerate(wybor):
            self.przycisk(text, self.wielkosc / 4, (self.wielkosc / 6) * (num+1), self.wielkosc/2, self.wielkosc / 7)
        self.renderuj_tekst("Grę rozpoczyna", self.wielkosc / 4, (self.wielkosc / 6) *4, self.wielkosc / 2,
                            self.wielkosc / 7, kol_szary, 6)
        self.przycisk(choose[self.poziom[0]], self.wielkosc / 4, (self.wielkosc / 5) * 4, self.wielkosc / 2,
                      self.wielkosc / 6)
        pygame.display.update()

    def rysuj_siatke(self):
        cl = (0, 0, 0)
        width = self.plansza.get_width()
        for i in range(1, 3):
            pol_linii = width / 3*i
            pygame.draw.line(self.plansza, cl, (0, pol_linii), (width, pol_linii), 3)
            pygame.draw.line(self.plansza, cl, (pol_linii, 0), (pol_linii, width), 3)

    def rysuj_znaczniki(self):
        plansza_side = self.plansza.get_width() / 3
        for x in range(3):
            for y in range(3):
                znacznik = self.znaczniki[x + y *3]
                if znacznik:
                    srodek_x = x * plansza_side + plansza_side / 2
                    srodek_y = y * plansza_side + plansza_side / 2
                    self.rysuj_tekst(znacznik, (srodek_x, srodek_y))

    def rysuj_tekst(self, tekst, srodek, kolor=(10, 10, 10)):
        plansza_tekst = self.font.render(tekst, True, kolor)
        kwadrat = plansza_tekst.get_rect()
        kwadrat.center = srodek
        self.plansza.blit(plansza_tekst, kwadrat)

    def ruch_gracza(self, x, y):
        komorka = self.plansza.get_width() / 3
        x /= komorka
        y /= komorka
        if not self.znaczniki[int(x) + int(y) * 3]:
            self.znaczniki[int(x) + int(y) * 3] = zaznaczenie_gracza(True)
            return True
        return False

    def wyswietl_wynik(self):
        if wygrana(self.znaczniki, True):
            if self.poziom[1] == 'średni':
                self.runda[1] += 1
            wynik = 'Wygrana'
            color = kol_zielony
        elif wygrana(self.znaczniki, False):
            wynik = 'Przegrana'
            color = kol_czerwony
        elif None not in self.znaczniki:
            wynik = 'Remis'
            color = kol_niebieski
        else:
            return
        self.poziom = [False, '', False]
        komunikat_center_pos = self.plansza.get_width() / 2
        s = pygame.Surface((self.wielkosc, self.wielkosc), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.plansza.blit(s, (0, 0))
        self.rysuj_tekst(wynik, (komunikat_center_pos, komunikat_center_pos), color)
        self.znaczniki = [None] * 9
        self.runda[0] = 0
        pygame.display.update()
        pygame.time.wait(2000)


class GameInit(object):

    def __init__(self, width, ruch_komp=False):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.plansza = Plansza(width)
        self.komputer = Komputer(self.plansza)
        self.ruch_komp = ruch_komp

    def run(self):
        while not self.handle_events():
            self.plansza.rysuj()
            if not self.plansza.poziom[2]:
                self.ruch_komp = self.plansza.poziom[0]
            if self.ruch_komp and self.plansza.poziom[2]:
                self.komputer.wykonaj_ruch()
                self.ruch_komp = False
            self.fps_clock.tick(15)

    def handle_events(self):
        event = pygame.event.poll()
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and self.plansza.poziom[2]:
            if not self.ruch_komp:
                x, y = pygame.mouse.get_pos()
                if self.plansza.ruch_gracza(x, y):
                    self.ruch_komp = True


class Komputer(object):

    def __init__(self, plansza):
        self.plansza = plansza
        self.p_gracz = self.plansza.gracz
        self.p_komp = self.plansza.komp

    def wykonaj_ruch(self):
        if not None in self.plansza.znaczniki:
            return
        ruch = 4
        if self.plansza.poziom[1] == 'łatwy':
            ruch = randint(0, 8)
        elif self.plansza.poziom[1] == 'średni':
            ruch = randrange(0, 9, 2)
        for znacznik in self.plansza.znaczniki:
            if znacznik is not None:
                ruch = self.kolejny_ruch(self.plansza.znaczniki)
                break
        pygame.time.wait(500)
        self.plansza.znaczniki[ruch] = zaznaczenie_gracza(False)

    def kolejny_ruch(self, znaczniki):
        if self.plansza.poziom[1] == 'łatwy':
            ruchy = self.oblicz_ruch_latwy(znaczniki, False)
            wyniki, ruch = max(ruchy, key=lambda m: m[0])
            return ruch
        elif self.plansza.poziom[1] == 'średni':
            self.plansza.runda[0] += 1
            return self.oblicz_ruch_sredni(znaczniki)
        elif self.plansza.poziom[1] == 'trudny':
            return self.oblicz_ruch_trudny(znaczniki)

    def oblicz_ruch_latwy(self, znaczniki, gracz):
        mozliwe_ruchy = (i for i, m in enumerate(znaczniki) if m is None)
        for ruch in mozliwe_ruchy:
            from copy import copy
            mozliwosci = copy(znaczniki)
            mozliwosci[ruch] = zaznaczenie_gracza(gracz)
            if wygrana(mozliwosci, gracz):
                wynik = -1 if gracz else 1
                yield wynik, ruch
                continue

            kolejne_ruchy = list(self.oblicz_ruch_latwy(mozliwosci, not gracz))
            if not kolejne_ruchy:
                yield 0, ruch
                continue

            wyniki, ruchy = zip(*kolejne_ruchy)
            yield sum(wyniki), ruch

    def oblicz_ruch_sredni(self, znaczniki):
        if self.plansza.runda[1] >= self.plansza.runda[0]:
            return self.oblicz_ruch_trudny(znaczniki)
        else:
            ruchy = self.oblicz_ruch_latwy(znaczniki, False)
            wyniki, ruch = max(ruchy, key=lambda m: m[0])
            return ruch

    def oblicz_ruch_trudny(self, zn):
        for ruch in (self.finish(zn), self.obrona(zn), self.atak(zn)):
            if ruch is not None:
                return ruch

    def obrona(self, zn):
        if ((zn[1] == self.p_gracz and zn[2] == self.p_gracz) or (zn[4] == self.p_gracz and zn[8] == self.p_gracz)
                or (zn[3] == self.p_gracz and zn[6] == self.p_gracz)) and zn[0] is None:
            return 0
        if ((zn[0] == self.p_gracz and zn[2] == self.p_gracz) or (zn[4] == self.p_gracz and zn[7] == self.p_gracz)) \
                and zn[1] is None:
            return 1
        if ((zn[0] == self.p_gracz and zn[1] == self.p_gracz) or (zn[4] == self.p_gracz and zn[6] == self.p_gracz)
                or (zn[5] == self.p_gracz and zn[8] == self.p_gracz)) and zn[2] is None:
            return 2
        if ((zn[0] == self.p_gracz and zn[6] == self.p_gracz) or (zn[4] == self.p_gracz and zn[5] == self.p_gracz)) \
                and zn[3] is None:
            return 3
        if ((zn[3] == self.p_gracz and zn[4] == self.p_gracz) or (zn[2] == self.p_gracz and zn[8] == self.p_gracz)) \
                and zn[5] is None:
            return 5
        if ((zn[0] == self.p_gracz and zn[3] == self.p_gracz) or (zn[2] == self.p_gracz and zn[4] == self.p_gracz)
                or (zn[7] == self.p_gracz and zn[8] == self.p_gracz) or (zn[3] == self.p_gracz and zn[7] == self.p_gracz)) \
                and zn[6] is None:
            return 6
        if ((zn[1] == self.p_gracz and zn[4] == self.p_gracz) or (zn[6] == self.p_gracz and zn[8] == self.p_gracz)) \
                and zn[7] is None:
            return 7
        if ((zn[2] == self.p_gracz and zn[5] == self.p_gracz) or (zn[6] == self.p_gracz and zn[7] == self.p_gracz)
                or (zn[5] == self.p_gracz and zn[7] == self.p_gracz)) and zn[8] is None:
            return 8

    def atak(self, zn):
        if zn[4] is None:
            return 4
        if zn[4] is not None and zn[0] is None and zn[2] is None:
            return 0
        if zn[4] == self.p_komp and zn[1] is None and zn[7] is None:
            return 1
        if zn[4] == self.p_komp and zn[2] is None:
            return 2
        if zn[4] == self.p_komp and zn[5] is None:
            return 5
        if zn[4] == self.p_komp and zn[6] is None:
            return 6
        if zn[4] == self.p_gracz and zn[7] is None:
            return 7
        else:
            ruch = randint(0, 9)
            while zn[ruch] is not None:
                ruch = randint(0, 9)
            return ruch

    def finish(self, znaczniki):
        if ((znaczniki[1] == self.p_komp and znaczniki[2] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[8] == self.p_komp)
                or (znaczniki[3] == self.p_komp and znaczniki[6] == self.p_komp)) and znaczniki[0] is None:
            return 0
        if ((znaczniki[0] == self.p_komp and znaczniki[2] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[7] == self.p_komp)) and znaczniki[1] is None:
            return 1
        if ((znaczniki[0] == self.p_komp and znaczniki[1] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[6] == self.p_komp)
                or (znaczniki[5] == self.p_komp and znaczniki[8] == self.p_komp)) and znaczniki[2] is None:
            return 2
        if ((znaczniki[0] == self.p_komp and znaczniki[6] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[2] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[5] == self.p_komp)) and znaczniki[3] is None:
            return 3
        if ((znaczniki[0] == self.p_komp and znaczniki[6] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[2] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[5] == self.p_komp)) and znaczniki[3] is None:
            return 4
        if ((znaczniki[2] == self.p_komp and znaczniki[8] == self.p_komp)
                or (znaczniki[3] == self.p_komp and znaczniki[4] == self.p_komp)) and znaczniki[5] is None:
            return 5
        if ((znaczniki[0] == self.p_komp and znaczniki[3] == self.p_komp)
                or (znaczniki[4] == self.p_komp and znaczniki[2] == self.p_komp)
                or (znaczniki[7] == self.p_komp and znaczniki[8] == self.p_komp)) and znaczniki[6] is None:
            return 6
        if ((znaczniki[4] == self.p_komp and znaczniki[1] == self.p_komp)
                or (znaczniki[6] == self.p_komp and znaczniki[8] == self.p_komp)) and znaczniki[7] is None:
            return 7
        if ((znaczniki[2] == self.p_komp and znaczniki[5] == self.p_komp)
                or (znaczniki[6] == self.p_komp and znaczniki[7] == self.p_komp)
                or (znaczniki[0] == self.p_komp and znaczniki[4] == self.p_komp)) and znaczniki[8] is None:
            return 8
        return None


def zaznaczenie_gracza(gracz):
    return "X" if gracz else "O"


def wygrana(znaczniki, gracz):
    win = [zaznaczenie_gracza(gracz)] * 3
    seq = range(3)

    def znacznik(x, y):
        return znaczniki[x + y * 3]

    for x in seq:
        row = [znacznik(x, y) for y in seq]
        if row == win:
            return True
    for y in seq:
        col = [znacznik(x, y) for x in seq]
        if col == win:
            return True

    przekatna1 = [znacznik(i, i) for i in seq]
    przekatna2 = [znacznik(i, abs(i-2)) for i in seq]
    if przekatna1 == win or przekatna2 == win:
        return True


if __name__ == "__main__":
    game = GameInit(500)
    game.run()
