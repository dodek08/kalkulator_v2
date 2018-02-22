
# -*- coding: UTF-8 -*-

import os
import psycopg2
from urllib.parse import urlparse
import pprint
import random
import generuj

"""
Plik zawiera obudowane funkcja update. Kilka z nich nie zostało wykorzystanych.
Bardziej rozbudowane obsługują formularze i w miejsce pustych - bo nieobowiązkowych pól wstawiają stare wartości.
Przy zmianie ID wykorzystują zamianę w trjkącie na wypadek istnienia rekordu o danym id.
Po wykorzystaniu każdej funkcji należy na obiekcie połączenia wywołać metodę .commit() oraz .close()
"""


def okreg_wyborczy(kursor, idokreg_wyborczy, nazwa, komisarz):
    kursor.execute("""UPDATE okreg_wyborczy set (Nazwa, Komisarz)= (%s, %s)
     WHERE idokreg_wyborczy=(%s);""",(nazwa, komisarz, idokreg_wyborczy))

def komitet(kursor, id, noweid, nazwa):
    kursor.execute("""SELECT * FROM komitet WHERE idkomitet = (%s)""", (  id ,))
    stary_komitet = kursor.fetchone()
    if not   nazwa :
          nazwa  = stary_komitet[1]
    kursor.execute("""UPDATE komitet set (nazwa_komitetu) = (%s) 
        WHERE idkomitet = (%s);""",(nazwa,id))
    if   noweid  is not None:
        kursor.execute("""UPDATE komitet set idkomitet = (%s) where idkomitet =(%s);""",(999,  noweid ))
        kursor.execute("""UPDATE komitet set idkomitet = (%s) where idkomitet =(%s);""",(  noweid ,  id ))
        kursor.execute("""UPDATE komitet set idkomitet = (%s) where idkomitet =(%s);""",(  id ,999)) 

def czlonek_komisji(kursor,id, imie, nazwisko, afiliacja=None):
    kursor.execute("""UPDATE czlonek_komisji set (imie, nazwisko, afiliacja)  (%s, %s, %s) 
        WHERE idczlonek_komisji = (%s);""",(imie, nazwisko, afiliacja, id))

def obwod_wyborczy_komisja(kursor,   id ,  noweid ,  noweidokregu ,  lokalizacja,  imie, nazwisko, afiliacja):
    kursor.execute("""SELECT * FROM obwod_wyborczy WHERE idobwod_wyborczy = (%s)""", (  id ,))
    stary_obwod = kursor.fetchone()
    kursor.execute("""SELECT idczlonek_komisji FROM komisja WHERE idobwod_wyborczy = (%s)""", (id,))
    idczlonek_komisji = kursor.fetchone()
    kursor.execute("""SELECT * FROM czlonek_komisji WHERE idczlonek_komisji = (%s)""", (idczlonek_komisji,))
    stary_czlonek_komisji = kursor.fetchone()
    if not imie:
        imie = stary_czlonek_komisji[1]
    if not nazwisko:
        nazwisko = stary_czlonek_komisji[2]
    if not afiliacja:
        afiliacja = stary_czlonek_komisji[3]
    if not lokalizacja:
          lokalizacja  = stary_obwod[2]
    if noweidokregu is None:
        noweidokregu = stary_obwod[1]
    kursor.execute("""UPDATE obwod_wyborczy set (idokreg_wyborczy, lokalizacja) = (%s, %s) 
        WHERE idobwod_wyborczy = (%s);""", (noweidokregu,lokalizacja, id))
    kursor.execute("""UPDATE czlonek_komisji set (imie, nazwisko, afiliacja) = (%s, %s, %s) 
        WHERE idczlonek_komisji = (%s)""",(imie, nazwisko, afiliacja, idczlonek_komisji))
    if   noweid  is not None:
        kursor.execute("""UPDATE obwod_wyborczy set idobwod_wyborczy = (%s) where idobwod_wyborczy =(%s);""",("-1",  noweid ))
        kursor.execute("""UPDATE obwod_wyborczy set idobwod_wyborczy = (%s) where idobwod_wyborczy =(%s);""",(  noweid ,  id ))
        kursor.execute("""UPDATE obwod_wyborczy set idobwod_wyborczy = (%s) where idobwod_wyborczy =(%s);""",(  id ,"-1")) 

def wyborca(kursor, pesel, idobwod, imie, nazwisko):
    kursor.execute("""UPDATE wyborca set ( idobwod_wyborczy, imie, nazwisko)  (%s, %s, %s) 
        WHERE pesel = (%s);""",(idobwod, imie, nazwisko, pesel))

def kandydat(kursor, idkomitet, id, noweid, imie, nazwisko):
    kursor.execute("""SELECT * FROM kandydat WHERE idkandydat = (%s)""", (id,))
    stary_kandydat = kursor.fetchone()
    if not imie:
        imie = stary_kandydat[1]
    if not nazwisko:
        nazwisko = stary_kandydat[2]
    kursor.execute("""UPDATE kandydat set (imie, nazwisko) = (%s, %s) 
    WHERE idkandydat = (%s);""",(imie, nazwisko, id))
    if idkomitet is not None:
    	kursor.execute("""DELETE FROM lista where idkandydat=(%s)""",(id,))
    	kursor.execute("""INSERT INTO lista (idkandydat,idkomitet) values (%s,%s);""",(id,idkomitet))
    if noweid is not None:
        kursor.execute("""UPDATE kandydat set idkandydat = (%s) where idkandydat =(%s);""",("-1",noweid))
        kursor.execute("""UPDATE kandydat set idkandydat = (%s) where idkandydat =(%s);""",(noweid,id))
        kursor.execute("""UPDATE kandydat set idkandydat = (%s) where idkandydat =(%s);""",(id,"-1"))


def sklad_komisji(kursor, idczlonek_komisji,  idobwod_wyborczy ,  idprzewodniczacego ):
    kursor.execute("""UPDATE sklad_komisji set (idczlonek_komisji, idprzewodniczacego)  (%s, %s, %s) 
        WHERE idobwod_wyborczy = (%s);""",(idczlonek_komisji, idprzewodniczacego, idobwod_wyborczy))

def kandydat_w_obwodzie (kursor, idKandydat, idobwod_wyborczy, liczba_glosow):
    kursor.execute("""UPDATE kandydat_w_obwodzie set (liczba_glosow)  (%s) 
        WHERE idkandydat = (%s) and idobwod_wyborczy = (%s); """,(liczba_glosow, idKandydat, idobwod_wyborczy,))

def glosy_w_okregu(kursor, idokreg, idkandydat):
    kursor.execute("""DELETE FROM kandydat_w_okregu WHERE idokreg_wyborczy = (%s) AND idkandydat = (%s); """,(idokreg, idkandydat))
    kursor.execute("""SELECT * FROM policz_glosy_w_okregu(%s);""",(idokreg,))