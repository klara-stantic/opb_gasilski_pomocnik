# Struktura spletne aplikacije
from bottle import *
import psycopg2
from auth import *

# Database dostop
conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)


@get('/')
def osnovna_stran():
    cur.
    return template('osnovna_stran.html')
       
    

# Priklop na bazo
baza = psycopg2.connect(conn_string)

# Poženemo strežnik
run(host='localhost', port=8080, reloader=True) 

## vaja git hahahaha