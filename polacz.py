import os
import psycopg2
from urllib.parse import urlparse

def polacz():
    url = urlparse(os.environ["DATABASE_URL"])
    return psycopg2.connect(database=url.path[1:], 
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
