
# -*- coding: UTF-8 -*-

import os
import psycopg2
from urllib.parse import urlparse
import pprint
import random
import generuj
import insert
import polacz
#urlparse.uses_netloc.append("postgres")

conn = polacz.polacz()

kursor = conn.cursor()



#cursor.execute("SELECT * FROM okreg_wyborczy")
# cursor.execute(INSTALL)        
for i in range(1,5):
	for j in range(1,7):
		for k in range(1,3):
			insert.kandydat(kursor,j,generuj.imie(),generuj.nazwisko(),i)
conn.commit()
# records = cursor.fetchall()
 
# 	# print out the records using pretty print
# 	# note that the NAMES of the columns are not shown, instead just indexes.
# 	# for most people this isn't very useful so we'll show you how to return
# 	# columns as a dictionary (hash) in the next example.
print(stare_id[0])

s = "ęóąśłżźćń"
print(s)

conn.close()