
# -*- coding: UTF-8 -*-

import os
import psycopg2
from urllib.parse import urlparse
import pprint
import random
import generuj

def okreg_wyborczy(kursor, nazwa, komisarz):
	kursor.execute("""INSERT into okreg_wyborczy (Nazwa, Komisarz) values ( %s, %s)""",(nazwa, komisarz))

def komitet(kursor, nazwa):
	kursor.execute("""INSERT into komitet (nazwa_komitetu) values ( %s)""",(nazwa,))

def czlonek_komisji(kursor, imie, nazwisko, afiliacja):
	kursor.execute("""INSERT into czlonek_komisji (imie, nazwisko, afiliacja) 
		values ( %s, %s, %s) RETURNING idczlonek_komisji;""",(imie, nazwisko, afiliacja))
	idczlonek_komisji=kursor.fetchone()
	return idczlonek_komisji

def obwod_wyborczy_komisja(kursor, idokreg, lokalizacja, imie, nazwisko, afiliacja):
	kursor.execute("""INSERT into obwod_wyborczy (idokreg_wyborczy, lokalizacja) 
		values ( %s, %s) RETURNING idobwod_wyborczy;""",(idokreg,lokalizacja))
	idobwod_wyborczy = kursor.fetchone()
	kursor.execute("""INSERT into czlonek_komisji (imie, nazwisko, afiliacja) 
		values ( %s, %s, %s) RETURNING idczlonek_komisji;""",(imie, nazwisko, afiliacja))
	idczlonek_komisji = kursor.fetchone()
	kursor.execute("""INSERT into komisja (idobwod_wyborczy, idczlonek_komisji) 
		values (%s, %s);""",(idobwod_wyborczy,idczlonek_komisji))


def wyborca(kursor, pesel, idobwod, imie, nazwisko):
	kursor.execute("""INSERT into wyborca (pesel, idobwod_wyborczy, imie, nazwisko) values ( %s, %s, %s, %s)""",(pesel, idobwod, imie, nazwisko))

def kandydat(kursor, idkomitet, imie, nazwisko, numer):
	kursor.execute("""INSERT into kandydat (imie, nazwisko) values (%s, %s) RETURNING idkandydat;""",(imie, nazwisko))
	idkandydat=kursor.fetchone()
	kursor.execute("""INSERT into lista (idkandydat, idkomitet) values (%s, %s)""",(idkandydat,idkomitet))
	kursor.execute("""INSERT INTO kandydat_w_okregu (idokreg_wyborczy,idkandydat) values (%s,%s)""", (numer,idkandydat))
	kursor.execute("""SELECT idobwod_wyborczy FROM obwod_wyborczy WHERE idokreg_wyborczy = (%s) ORDER BY idobwod_wyborczy;""",(numer,))
	obwody = kursor.fetchall()
	idobwodow = [ido[0] for ido in obwody]
	for id in idobwodow:
		kursor.execute("""INSERT INTO kandydat_w_obwodzie (idobwod_wyborczy,idkandydat) values (%s, %s)""",(id,idkandydat))


def komisja(kursor,  idczlonek_komisji,  idobwod_wyborczy):
	kursor.execute("""INSERT into sklad_komisji (idczlonek_komisji,  idobwod_wyborczy) values ( %s, %s)""",(idczlonek_komisji,  idobwod_wyborczy))

# def kandydat_w_okregu (kursor, idKandydat, idokreg_wyborczy, liczba_glosow):
	# kursor.execute("""INSERT into obwod_wyborczy (idKandydat, idokreg_wyborczy, liczba_glosow) values ( %s, %s, %s)""",(idKandydat, idokreg_wyborczy, liczba_glosow))

def kandydat_w_obwodzie (kursor, idKandydat, idobwod_wyborczy, liczba_glosow):
	kursor.execute("""UPDATE kandydat_w_obwodzie set (liczba_glosow) = (%s)
		WHERE idkandydat = (%s) and idobwod_wyborczy = (%s) """,(liczba_glosow, idKandydat, idobwod_wyborczy))

def glosy_w_okregu(kursor, idokreg):
	kursor.execute("""SELECT * FROM policz_glosy_w_okregu(%s);""",(idokreg,))



# INSERT INTO kandydat_w_okregu (idKandydat, idokreg_wyborczy, liczba_glosow)
 #        VALUES (select idKandydat from kandydat_w_obwodzie where idobwod_wyborczy in 
 #          {select idobwod_wyborczy from obwod_wyborczy where idokreg_wyborczy=idokreg}, idokreg, 
 #          {select sum(liczba_glosow) from kandydat_w_obwodzie where idkandydat in 
 #          {select idKandydat from kandydat_w_obwodzie where idobwod_wyborczy in 
 #          {select idobwod_wyborczy from obwod_wyborczy where idokreg_wyborczy=idokreg}}});

