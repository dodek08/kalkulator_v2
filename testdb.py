
# -*- coding: UTF-8 -*-

import os
import psycopg2
from urllib.parse import urlparse
import pprint
from random import randint
import generuj
import insert
import polacz


#Owarcie połączenia z BD.
conn = polacz.polacz()
#Uzyskanie kursora.
kursor = conn.cursor()
#uzupelnianie kandydatow.

for i in range(1,5):
 	for j in range(1,7):
		for k in range(1,3):
 			insert.kandydat(kursor,j,generuj.imie(),generuj.nazwisko(),i)

#Zautoamatyzowane głosowanie
t = [i for i in range(110,158)]

for idkandydat in t:
	for j in range(13,25):
		#Execute jako argument bierze zapytanie i krotkę wartości którą je uzupełnia.
		kursor.execute("""UPDATE kandydat_w_obwodzie set (liczba_glosow) = (%s)
		WHERE idkandydat = (%s) and idobwod_wyborczy = (%s)""", (randint(0,300),idkandydat,j))
		#Commit umieszcza zmiany w BD.
		conn.commit()

#Sprawdzenie obsługi UTF-8
s = "ęóąśłżźćń"
print(s)
#Zamknięcie połączenia.
conn.close()