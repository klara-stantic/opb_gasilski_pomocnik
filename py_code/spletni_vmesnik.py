# Struktura spletne aplikacije
from bottle import *
from auth import *

import os

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # Znebimo se problemov s šumniki

#PRIVZETE NASTAVITVE 
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Database dostop
conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)


@get('/')
def osnovna_stran():
    return template('osnovna_stran.html')
       
@get('/intervencije/')
def intervencije():
    return template('osnovna_stran.html')

@get('/tekmovanja/')
def tekmovanja():
    return template('osnovna_stran.html')

@get('/oprema/')
def oprema():
    return template('osnovna_stran.html')

@get('/drustvo/')
def drustvo():
    return template('osnovna_stran.html')

@get('/oprema/osebna_oprema/')
def osebna_oprema():
    return template('osnovna_stran.html')

@get('/oprema/skupna_oprema/')
def skupna_oprema():
    return template('osnovna_stran.html')


# Priklop na bazo
baza = psycopg2.connect(conn_string)

# Poženemo strežnik
run(host='localhost', port=8080, reloader=True) 

## vaja git hahahaha