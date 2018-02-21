
# -*- coding: UTF-8 -*-

import os
import psycopg2
from urllib.parse import urlparse
import pprint
import random
import generuj

def okreg_wyborczy(kursor, idokreg_wyborczy):
	kursor.execute("""DELETE FROM 
	 WHERE idokreg_wyborczy=(%s);""",(idokreg_wyborczy,))

def komitet(kursor, id):
	kursor.execute("""DELETE FROM komitet 
		WHERE idkomitetu = (%s);""",(id,))

def czlonek_komisji(kursor,id):
	kursor.execute("""DELETE FROM czlonek_komisji 
		WHERE idczlonek_komisji = (%s);""",(id,))

def obwod_wyborczy(kursor, id):
	kursor.execute("""DELETE FROM obwod_wyborczy 
		WHERE idobwod_wyborczy = (%s);""",())

def wyborca(kursor, pesel, idobwod):
	kursor.execute("""DELETE FROM wyborca
		WHERE idobwod_wyborczy = (%s) AND pesel = (%s);""",(idobwod, pesel))

def kandydat(kursor, id):
	kursor.execute("""DELETE FROM kandydat 
		WHERE idkandydat = (%s);""",(id,))

# def sklad_komisji(kursor, idczlonek_komisji,  idobwod_wyborczy ,  idprzewodniczacego ):
# 	kursor.execute("""DELETE FROM sklad_komisji (idczlonek_komisji, idprzewodniczacego)  (%s, %s, %s) 
# 		WHERE idobwod_wyborczy = (%s);""",(idczlonek_komisji, idprzewodniczacego, idobwod_wyborczy))

# def kandydat_w_okregu (kursor, idKandydat, idokreg_wyborczy, liczba_glosow):
	# kursor.execute("""DELETE FROM obwod_wyborczy (idKandydat, idokreg_wyborczy, liczba_glosow)  ( %s, %s, %s) WHERE id""",(idKandydat, idokreg_wyborczy, liczba_glosow))

# def kandydat_w_obwodzie (kursor, idKandydat, idobwod_wyborczy):
# 	kursor.execute("""DELETE FROM kandydat_w_obwodzie
# 		WHERE idkandydat = (%s) and idobwod_wyborczy = (%s); """,( idKandydat, idobwod_wyborczy,))
