import os
import psycopg2
from urllib.parse import urlparse

#Funkcja używana do uzyskania połączenia z bazą danych. Link zawierający login i hasło jest ustawiony jako zmienna systemowa.
#Zwraca obiekt połączenia z biblioteki psycopg2, interfejsu SQL Pythona: http://initd.org/psycopg/docs/.
#Zostałą obudowana też dlatego, że wywoływanie całości w każdej funkcji sprawiłoby, że kod byłby zupełnie nieczytelny.

def polacz():
    url = urlparse(os.environ["DATABASE_URL"])
    return psycopg2.connect(database=url.path[1:], 
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
