
# -*- coding: UTF-8 -*-

import os
import psycopg2
from urllib.parse import urlparse
import pprint
import random
import generuj
import insert
import update
import delete
import random
import tkinter
from tkinter import ttk
from tkinter import messagebox


url = urlparse("postgres://mzinsdkb:r-InJgOMNfiZDttqphIrEpVJv5fwa49y@horton.elephantsql.com:5432/mzinsdkb")

conn = psycopg2.connect(database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
)

cursor = conn.cursor()
# komisarz = generuj.imie()+" "+generuj.nazwisko()
# insert.okreg_wyborczy(cursor,"Legnica",komisarz)
# insert.komitet(cursor,"PSL")
# insert.obwod_wyborczy(cursor, 3, "Reymonta 29")
# cursor.execute("""SELECT * FROM obwod_wyborczy;""")
cursor.execute("SELECT * FROM okreg_wyborczy;")
# cursor.execute("SELECT * FROM komitet;")
# insert.czlonek_komisji(cursor, generuj.imie(), generuj.nazwisko(),"PSL")
# cursor.execute("""SELECT * FROM czlonek_komisji;""")
# insert.wyborca(cursor, generuj.pesel(), 5, generuj.imie(), generuj.nazwisko())
# cursor.execute("""SELECT * FROM wyborca;""")
# insert.kandydat(cursor, 3, generuj.imie(), generuj.nazwisko())
# cursor.execute("""SELECT * FROM kandydat;""")
# records = cursor.fetchall()
# print(records)
# insert.sklad_komisji(cursor,5,5,6)
# cursor.execute("""SELECT * FROM sklad_komisji;""")
# insert.kandydat_w_obwodzie (cursor, 2, 5, 300)
# cursor.execute("""SELECT * FROM kandydat_w_obwodzie;""")
# update.glosy_w_okregu(cursor,3,2)
# cursor.execute("""SELECT * FROM kandydat_w_okregu;""")
# records = cursor.fetchall()
# print(records)
# update.okreg_wyborczy(cursor,3,"Wałbrzych",komisarz)
# cursor.execute("SELECT * FROM okreg_wyborczy;")
# conn.commit()
records = cursor.fetchall()
print(records)
conn.close()


